#!/usr/bin/env python3
"""Vérifie la sécurité HTTP d'un site : HTTPS, redirection, en-têtes de sécurité,
attributs des cookies, et (option) fichiers sensibles exposés.

Usage :
    python3 check_headers.py <url> [--probe-files] [--json]

N'utiliser que sur le site de l'utilisateur (local, préproduction ou production
avec son accord). --probe-files fait quelques requêtes GET normales vers des
chemins sensibles connus (/.env, /.git/HEAD…) pour vérifier qu'ils ne sont pas
servis : rien de plus.

Bibliothèque standard uniquement.
"""

import argparse
import json
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = "conformite-legale-check/1.0"
TIMEOUT = 15

EXPECTED = [
    ("strict-transport-security", "S4/S11", "haute", "HSTS absent : ajouter Strict-Transport-Security: max-age=31536000; includeSubDomains", "https_only"),
    ("content-security-policy", "S11", "moyenne", "CSP absente : ajouter une Content-Security-Policy (commencer en Report-Only)", None),
    ("x-content-type-options", "S11", "moyenne", "X-Content-Type-Options absent : ajouter nosniff", None),
    ("referrer-policy", "S11", "info", "Referrer-Policy absent : ajouter strict-origin-when-cross-origin", None),
    ("permissions-policy", "S11", "info", "Permissions-Policy absent : désactiver camera, microphone, geolocation si inutilisés", None),
]
SENSITIVE_PATHS = [
    "/.env", "/.env.local", "/.env.production", "/.git/HEAD", "/.git/config", "/.DS_Store",
    "/phpinfo.php", "/server-status", "/wp-config.php.bak", "/config.json", "/backup.zip",
    "/.vscode/settings.json", "/docker-compose.yml",
]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def fetch(url, follow=True):
    handlers = [] if follow else [NoRedirect()]
    opener = urllib.request.build_opener(*handlers, urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        resp = opener.open(req, timeout=TIMEOUT)
        return resp.status, resp.geturl(), resp.headers, resp.read(4096)
    except urllib.error.HTTPError as e:
        return e.code, url, e.headers, e.read(4096) if e.fp else b""


def check(url, probe_files):
    findings = []
    info = {"url": url}
    parsed = urllib.parse.urlparse(url)
    is_local = parsed.hostname in {"localhost", "127.0.0.1", "::1"} or (parsed.hostname or "").endswith(".localhost")

    try:
        status, final_url, headers, body = fetch(url)
    except Exception as e:
        return {"url": url, "erreur": f"Site injoignable : {e}", "constats": []}
    info.update({"statut": status, "url_finale": final_url})
    final = urllib.parse.urlparse(final_url)

    if final.scheme != "https" and not is_local:
        findings.append({"point": "S4", "gravite": "haute", "constat": "Le site n'est pas servi en HTTPS"})

    # Redirection HTTP -> HTTPS
    if parsed.scheme == "https" and not is_local:
        http_url = urllib.parse.urlunparse(("http",) + tuple(parsed[1:]))
        try:
            st, loc, h, _ = fetch(http_url, follow=False)
            location = h.get("Location", "") if h else ""
            if not (300 <= st < 400 and location.startswith("https://")):
                findings.append({"point": "S4", "gravite": "haute",
                                 "constat": f"http:// ne redirige pas vers https:// (statut {st})"})
        except Exception:
            pass

    lower = {k.lower(): v for k, v in headers.items()}
    info["en_tetes"] = {k: lower[k] for k in sorted(lower) if k in {e[0] for e in EXPECTED} or k in {"x-frame-options", "server", "x-powered-by"}}

    for name, point, sev, msg, cond in EXPECTED:
        if cond == "https_only" and (final.scheme != "https" or is_local):
            continue
        if name not in lower:
            findings.append({"point": point, "gravite": sev, "constat": msg})

    csp = lower.get("content-security-policy", "")
    if "frame-ancestors" not in csp and "x-frame-options" not in lower:
        findings.append({"point": "S11", "gravite": "moyenne",
                         "constat": "Protection contre l'intégration en iframe (clickjacking) absente : frame-ancestors 'self' ou X-Frame-Options"})
    if csp and ("'unsafe-inline'" in csp and "script-src" in csp and "nonce-" not in csp):
        findings.append({"point": "S11", "gravite": "info", "constat": "CSP autorise 'unsafe-inline' pour les scripts (protection XSS réduite)"})
    for leak in ("x-powered-by", "server"):
        v = lower.get(leak, "")
        if v and any(ch.isdigit() for ch in v):
            findings.append({"point": "S2", "gravite": "info", "constat": f"En-tête {leak} révèle la technologie et sa version : {v}"})

    # Cookies
    cookies = headers.get_all("Set-Cookie") or []
    info["cookies_http"] = []
    for c in cookies:
        name = c.split("=", 1)[0].strip()
        attrs = c.lower()
        flags = {"secure": "; secure" in attrs, "httponly": "; httponly" in attrs, "samesite": "samesite=" in attrs}
        info["cookies_http"].append({"nom": name, **flags})
        missing = [k for k, v in flags.items() if not v and not (k == "secure" and is_local)]
        if missing:
            sev = "haute" if any(t in name.lower() for t in ("sess", "auth", "token", "sid", "jwt")) else "moyenne"
            findings.append({"point": "S11", "gravite": sev,
                             "constat": f"Cookie « {name} » sans {', '.join(missing)}"})
        if not any(t in name.lower() for t in ("sess", "csrf", "xsrf", "auth", "token", "sid", "consent", "cookie", "lang", "locale", "cart", "panier", "__host", "__secure", "cf_", "__cf")):
            findings.append({"point": "10", "gravite": "moyenne",
                             "constat": f"Cookie « {name} » déposé par le serveur dès la première visite : vérifier qu'il est strictement nécessaire"})

    if probe_files:
        base = f"{final.scheme}://{final.netloc}"
        exposed = []
        for p in SENSITIVE_PATHS:
            try:
                st, _, h, body = fetch(base + p, follow=False)
            except Exception:
                continue
            ctype = (h.get("Content-Type", "") if h else "").lower()
            text = body[:400].decode("utf-8", "ignore")
            looks_html = "text/html" in ctype or "<html" in text.lower() or "<!doctype" in text.lower()
            if st == 200 and not looks_html and text.strip():
                exposed.append(p)
        info["chemins_testes"] = SENSITIVE_PATHS
        for p in exposed:
            findings.append({"point": "S2", "gravite": "haute", "constat": f"Fichier sensible accessible publiquement : {p}"})

    return {**info, "constats": findings}


def render(r):
    if "erreur" in r:
        return f"# Vérification HTTP — {r['url']}\n\n❌ {r['erreur']}"
    icon = {"haute": "🔴", "moyenne": "🟠", "info": "🔵"}
    out = [f"# Vérification HTTP — {r['url']}", "", f"Statut : {r['statut']} · URL finale : {r['url_finale']}", ""]
    out.append("## Constats")
    if not r["constats"]:
        out.append("✅ Aucun problème détecté sur les en-têtes et les cookies.")
    for f in sorted(r["constats"], key=lambda x: {"haute": 0, "moyenne": 1, "info": 2}[x["gravite"]]):
        out.append(f"- {icon[f['gravite']]} [{f['point']}] {f['constat']}")
    out.append("")
    out.append("## En-têtes présents")
    for k, v in r.get("en_tetes", {}).items():
        out.append(f"- `{k}: {v[:120]}`")
    if r.get("cookies_http"):
        out.append("")
        out.append("## Cookies posés par le serveur")
        for c in r["cookies_http"]:
            out.append(f"- {c['nom']} — Secure {'✅' if c['secure'] else '❌'} · HttpOnly {'✅' if c['httponly'] else '❌'} · SameSite {'✅' if c['samesite'] else '❌'}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--probe-files", action="store_true", help="Tester l'exposition de fichiers sensibles connus")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    url = a.url if "://" in a.url else "https://" + a.url
    r = check(url, a.probe_files)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else render(r))
    sys.exit(0)


if __name__ == "__main__":
    main()
