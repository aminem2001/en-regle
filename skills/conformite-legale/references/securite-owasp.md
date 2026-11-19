# Sécurité : OWASP Top 10 2025 + 5 compléments

Référence : OWASP Top 10:2025 (finalisé en janvier 2026), OWASP API Security Top 10, OWASP Top 10 for LLM Applications, recommandations ANSSI et CNIL.
Lien avec le droit : RGPD art. 32 (sécurité), art. 33-34 (violations). Une faille exploitable qui expose des données personnelles est un manquement sanctionnable, pas seulement un risque technique.

**Règles de conduite pour les tests** : ne teste que le projet de l'utilisateur, en local ou sur un environnement qu'il désigne. Aucun test d'intrusion actif sur un site en production sans son accord explicite, aucune attaque sur des services tiers. Les tests ci-dessous sont des lectures de code, des requêtes normales et des vérifications de configuration.

## Sommaire
S1 à S10 : OWASP Top 10 2025 · S11 à S15 : compléments

---

## S1. A01 Contrôle d'accès défaillant
- **Vérifier** : chaque route API et chaque action serveur vérifie l'authentification **et** l'autorisation sur l'objet demandé (l'utilisateur A ne peut pas lire la commande de B en changeant l'identifiant) ; routes d'administration protégées côté serveur, pas seulement masquées dans l'interface ; pas de contrôle uniquement côté client ; SSRF : pas de requête serveur vers une URL fournie par l'utilisateur sans liste d'autorisation.
- **Tester** : lire les gestionnaires de routes (`app/api`, `pages/api`, contrôleurs, server actions, règles Firebase/Supabase RLS) ; en local, appeler une ressource d'un autre utilisateur avec la session d'un premier.
- **Corriger** : middleware d'authentification + vérification de propriété (`where: { id, userId: session.user.id }`) ; politiques RLS activées (Supabase) ; refus par défaut.

## S2. A02 Mauvaise configuration
- **Vérifier** : mode debug désactivé en production ; pas de traces de pile renvoyées au client ; CORS limité aux origines nécessaires (pas `*` avec identifiants) ; fichiers sensibles non servis (`.env`, `.git/`, sauvegardes, `phpinfo`) ; listing de répertoires désactivé ; comptes et mots de passe par défaut changés ; buckets de stockage non publics par erreur.
- **Tester** : `scripts/check_headers.py <url> --probe-files` (vérifie `/.env`, `/.git/HEAD`, etc. sur le site **de l'utilisateur**) ; lecture de la configuration.
- **Corriger** : variables d'environnement par environnement, configuration CORS stricte, règles de l'hébergeur pour bloquer les fichiers cachés.

## S3. A03 Chaîne d'approvisionnement logicielle
- **Vérifier** : vulnérabilités connues des dépendances ; lockfile commité ; dépendances abandonnées ; scripts tiers chargés depuis un CDN sans `integrity` (SRI) ; actions CI épinglées.
- **Tester** : `npm audit --omit=dev` (ou `pnpm audit`, `yarn npm audit`), `pip-audit`, `composer audit`, `bundle audit`, `govulncheck` selon la stack.
- **Corriger** : mettre à jour les paquets vulnérables (corrections mineures d'abord, majeures avec tests), ajouter `integrity` + `crossorigin` aux scripts CDN, activer Dependabot ou Renovate.

## S4. A04 Défaillances cryptographiques
- **Vérifier** : HTTPS partout et redirection HTTP → HTTPS, HSTS ; mots de passe hachés avec **argon2id** ou **bcrypt** (jamais MD5, SHA-1 ou SHA-256 seul) ; données sensibles chiffrées au repos si nécessaire ; pas de crypto maison ; jetons aléatoires générés avec un générateur cryptographique.
- **Tester** : `check_headers.py` ; recherche de `md5(`, `sha1(`, `createHash('sha256')` appliqués à des mots de passe, `Math.random()` pour des jetons.
- **Corriger** : bibliothèque de hachage éprouvée, `crypto.randomBytes` / `secrets.token_urlsafe`, HSTS.

## S5. A05 Injections
- **Vérifier** : requêtes SQL paramétrées ou ORM (pas de concaténation) ; pas de `eval`, `exec`, `child_process` avec des entrées utilisateur ; XSS : pas de `dangerouslySetInnerHTML`, `v-html`, `innerHTML`, `{!! !!}`, `|safe` sur du contenu utilisateur non nettoyé ; injection NoSQL (`$where`, objets passés tels quels).
- **Tester** : `scripts/audit_static.py` signale les motifs dangereux ; lecture de chaque occurrence.
- **Corriger** : requêtes préparées, échappement par défaut du framework, DOMPurify pour le HTML utilisateur, validation des entrées (zod, joi, pydantic).

## S6. A06 Conception non sécurisée
- **Vérifier** : le prix, la remise, la quantité ou le rôle ne sont jamais acceptés depuis le client ; coupons à usage limité ; limites métier (montants, quantités) ; vérification côté serveur du statut de paiement via webhook signé, pas via la redirection de retour.
- **Tester** : lecture du tunnel de commande et des actions sensibles.
- **Corriger** : recalcul serveur à partir du catalogue, règles métier côté serveur.

## S7. A07 Authentification
- **Vérifier** : limitation des tentatives de connexion ; messages d'erreur qui ne révèlent pas si le compte existe ; réinitialisation de mot de passe par jeton à usage unique et expirant ; sessions invalidées à la déconnexion et au changement de mot de passe ; politique de mot de passe conforme à la recommandation CNIL (longueur ≥ 12 sans contrainte de complexité, ou 8 avec complexité et limitation) ; 2FA pour les comptes d'administration.
- **Corriger** : utiliser une solution éprouvée (Auth.js, Lucia, Supabase Auth, Clerk, Devise, Django auth…) plutôt qu'un système maison.

## S8. A08 Intégrité des logiciels et des données
- **Vérifier** : webhooks (Stripe, etc.) **vérifiés par signature** ; pas de désérialisation non sûre (`pickle`, `unserialize`, `yaml.load` sans SafeLoader) ; mises à jour et artefacts de build vérifiés.
- **Corriger** : `stripe.webhooks.constructEvent`, `yaml.safe_load`, JSON plutôt que formats sérialisés natifs.

## S9. A09 Journalisation et alertes
- **Vérifier** : connexions, échecs, changements de droits et erreurs serveur journalisés ; **aucun mot de passe, jeton ou donnée de carte dans les journaux** ; durée de conservation limitée (6 mois à 1 an, recommandation CNIL) ; alerte en cas d'anomalie.
- **Tester** : rechercher `console.log(req.body)`, `logger.info(user)`, journalisation de mots de passe.
- **Alertes qui s'emballent** : un e-mail envoyé à chaque erreur (`onRequestError` de Next.js, `process.on('uncaughtException')`, gestionnaire d'erreurs Express, Django, Rails…) peut partir des centaines de fois quand des robots fouillent le site. Vérifier que les **404 et redirections sont ignorées** (`NEXT_NOT_FOUND`, `NEXT_HTTP_ERROR_FALLBACK`, `NEXT_REDIRECT`, statut < 500), que la limite d'envoi est **partagée** (pas une variable en mémoire sur un hébergement serverless ou edge) et que l'alerte ne contient **aucune donnée personnelle**. Sinon : quota du service d'envoi épuisé, adresse bloquée, vraies demandes de clients perdues. `audit_static.py` signale ces cas.

## S10. A10 Mauvaise gestion des conditions exceptionnelles
- **Vérifier** : erreurs attrapées et renvoyées au client sous forme générique ; pas de « fail-open » (une erreur dans la vérification des droits ne doit pas laisser passer) ; promesses non gérées ; limites de taille sur les requêtes et les téléversements.
- **Corriger** : gestionnaire d'erreurs global, refus par défaut en cas d'erreur, limites de taille.

---

## S11. En-têtes HTTP et cookies
| En-tête | Valeur recommandée |
|---|---|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` |
| `Content-Security-Policy` | Politique adaptée au site ; au minimum `frame-ancestors 'self'`, `object-src 'none'`, `base-uri 'self'` ; idéalement scripts limités aux origines utilisées |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | désactiver ce qui n'est pas utilisé (`camera=(), microphone=(), geolocation=()`) |
| `X-Frame-Options` | `DENY` ou `SAMEORIGIN` (si pas de `frame-ancestors`) |

Cookies de session : `Secure`, `HttpOnly`, `SameSite=Lax` (ou `Strict`), durée limitée.
**Tester** : `scripts/check_headers.py <url>`. **Corriger** : selon l'hébergeur (voir `corrections.md` §Sécurité).

## S12. Secrets
- **Vérifier** : aucune clé, aucun mot de passe et aucun jeton dans le code, l'historique Git ou le bundle envoyé au navigateur (variables `NEXT_PUBLIC_`, `VITE_`, `PUBLIC_` réservées aux valeurs publiques) ; `.env` dans `.gitignore`.
- **Tester** : `audit_static.py` (motifs de clés connues) ; `git log -p | grep` ciblé si nécessaire ; gitleaks ou trufflehog s'ils sont installés.
- **Secret collé dans une conversation** (avec Claude, un support, un forum) : il doit être considéré comme exposé, même s'il n'est pas dans le code. Le révoquer et en créer un nouveau.
- **Corriger** : déplacer en variables d'environnement serveur, **révoquer et régénérer** toute clé qui a été commitée (la supprimer du code ne suffit pas), ajouter `.env*` au `.gitignore`.

## S13. Abus et limitation
- Rate limiting sur la connexion, l'inscription, la réinitialisation de mot de passe, les formulaires de contact et les routes coûteuses (IA, e-mails, SMS).
- Anti-spam : pot de miel, Turnstile, Friendly Captcha ou hCaptcha plutôt que reCAPTCHA (voir cookies).
- **Hébergement serverless ou edge** (Vercel, Netlify, Cloudflare Workers, AWS Lambda…) : un compteur en mémoire (`new Map()` + `Date.now()`) n'est pas partagé entre les instances, la limite est donc contournable. Utiliser un stockage partagé (Cloudflare KV ou Durable Objects, Upstash, Redis) ou la règle de limitation de l'hébergeur (Cloudflare Rate Limiting, Vercel Firewall). `audit_static.py` le signale quand il détecte les deux.

## S14. API (OWASP API Top 10)
- Autorisation au niveau de chaque objet (BOLA) et de chaque propriété (ne pas renvoyer `passwordHash`, `role`, données internes).
- Pagination et limites ; validation stricte des entrées ; pas d'assignation de masse (`User.update(req.body)`).
- Documentation et routes de test non exposées en production.

## S15. Fonctionnalités IA (OWASP LLM Top 10)
- Clé d'API du fournisseur **jamais côté client**.
- Injection de prompt : ne pas donner au modèle des droits ou des outils plus larges que ceux de l'utilisateur ; séparer instructions et contenus d'utilisateurs.
- Sorties : échapper ou filtrer avant affichage ; ne pas exécuter de code ou de SQL généré sans contrôle.
- Données : ne pas envoyer de données personnelles inutiles au fournisseur ; vérifier l'option de non-réutilisation pour l'entraînement ; mentionner dans la politique de confidentialité.
- Coût : quotas par utilisateur et plafond global.
- Transparence AI Act : mention « assistant IA » (voir `saas-plateformes.md` §6).
