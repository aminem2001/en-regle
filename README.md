<div align="center">

# ⚖️ En règle

### Ton site est-il vraiment en règle ?
**Claude le vérifie, le teste dans un vrai navigateur, puis le corrige.**

RGPD · Cookies CNIL · Mentions légales · CGV · Accessibilité RGAA · DSA · AI Act · Sécurité OWASP

![Claude Code](https://img.shields.io/badge/Claude_Code-skill-D97757)
![France · UE](https://img.shields.io/badge/droit-France_%C2%B7_UE-0055A4)
![45 points](https://img.shields.io/badge/grille-45_points-2EA44F)
![OWASP 2025](https://img.shields.io/badge/OWASP-Top_10_2025-000000)
![Licence MIT](https://img.shields.io/badge/licence-MIT-lightgrey)

</div>

---

## 🍪 Le piège classique

Tu as un joli bandeau cookies. Mais pendant qu'il s'affiche, **Google Analytics est déjà parti**. Ton bouton « Refuser » est un petit lien gris. Ta case newsletter est cochée par défaut. Ta page « mentions légales » a été copiée d'un autre site.

Ce sont exactement les manquements que la CNIL et la DGCCRF contrôlent et sanctionnent. Les cookies sont depuis plusieurs années une priorité de contrôle de la CNIL, avec des amendes record pour les grandes plateformes et une procédure simplifiée pour sanctionner rapidement les plus petits sites.

**En règle** est un skill Claude qui repère tout ça **avant** qu'un contrôle, un concurrent ou un client ne le fasse.

## ✨ Ce que ça fait, en une phrase

> « Je vais mettre mon site en ligne, vérifie que je suis en règle. »

Et Claude déroule tout le cycle, sur **ton** projet, dans **ta** stack :

```
 🔍 Analyse le code
 🧪 Teste le site dans un vrai navigateur
 📋 Te remet un rapport clair, point par point
 ✋ Attend ton feu vert        ← rien n'est modifié sans ton accord
 🔧 Corrige
 ✅ Reteste et prouve que c'est corrigé
```

Next.js, Nuxt, React, Vue, Svelte, Astro, Laravel, Django, Rails, WordPress, Shopify, HTML pur, appli iOS ou Android : il s'adapte.

## 🎬 Ce qu'il trouve (vrai test)

Sur un site de démonstration piégé, voici une partie de ce que les outils du skill ont relevé :

```text
🔴 Cookies Google Analytics (_ga, _ga_…) déposés AVANT tout consentement
🔴 Données envoyées à google-analytics.com avant consentement
🔴 « refuser » : simple lien de 37×13 px, contre un bouton de 188×49 px pour « Tout accepter »
🔴 Case « offres des partenaires » pré-cochée
🔴 Clé Stripe sk_live_… écrite dans le JavaScript public
🔴 Fichier .env téléchargeable par n'importe qui
🔴 Injection SQL dans la route de connexion · mots de passe hachés en MD5
🔴 Lien vers la plateforme européenne de litiges, supprimée depuis juillet 2025
🔴 Texte gris à 1,92:1 de contraste (minimum légal : 4,5:1) · zoom bloqué
🔴 « Produits éco-responsables » : allégation environnementale non prouvée
🟠 « La boutique n°1 en France » : allégation à justifier
🟠 Vidéo YouTube et Google Fonts chargés sans consentement
```

Puis il te propose les **5 corrections les plus urgentes**, dans l'ordre, et les applique quand tu dis go.

## 🧾 La grille : 45 points

<table>
<tr><td>

**⚖️ Pages légales**
- Mentions légales (LCEN)
- Politique de confidentialité
- Politique cookies
- CGU · CGV
- Rétractation 14 j + **bouton de rétractation** (obligatoire depuis juin 2026)
- Garanties légales · médiateur
- Langue française

</td><td>

**🍪 Cookies & RGPD**
- « Refuser » aussi visible qu'« Accepter »
- Zéro traceur avant consentement *(testé en vrai)*
- Retrait du choix à tout moment
- Polices, vidéos, cartes, chat, captcha
- Formulaires · minimisation
- Suppression des données · durées
- Sous-traitants · transferts · mineurs

</td></tr>
<tr><td>

**🛒 Vente & pratiques**
- Prix total avant paiement
- Résiliation en 3 clics
- Dark patterns (fausse urgence, fausse rareté…)
- Faux avis · allégations « n°1 », « garanti », « écolo »
- Licences : polices, images, icônes, code
- Désinscription des e-mails

</td><td>

**♿ Accessibilité & 🔐 Sécurité**
- Textes alternatifs · contrastes · zoom
- Navigation au clavier · focus visible
- Déclaration d'accessibilité (RGAA / EAA)
- **OWASP Top 10 2025** complet
- En-têtes HTTP · secrets · API
- Sécurité des fonctionnalités IA

</td></tr>
</table>

Et selon ton projet : **App Store / Google Play**, **DSA** (contenus d'utilisateurs, marketplaces), **AI Act** (chatbots), et les lois de **13 pays et régions** hors UE (Royaume-Uni, Suisse, Californie, Québec, Brésil, Inde…).

## 🚀 Installation (30 secondes)

**Claude Code — en plugin :**

```
/plugin marketplace add aminem2001/en-regle
/plugin install en-regle@en-regle
```

**Claude Code — à la main :**

```bash
git clone https://github.com/aminem2001/en-regle.git
cp -r en-regle/skills/conformite-legale ~/.claude/skills/
```

**Claude.ai :** zippe le dossier `skills/conformite-legale` et importe-le dans *Paramètres → Capacités → Skills*.

## 💬 Exemples de demandes

- « Audite mon site avant la mise en prod »
- « Mon bandeau cookies est-il conforme CNIL ? »
- « Mon e-commerce est-il en règle ? Corrige ce qui manque »
- « Fais un audit RGPD + sécurité complet »
- « Vérifie l'accessibilité de mon site »

Tu peux aussi donner **ta propre checklist** : il l'utilise comme structure du rapport et ajoute ce qu'elle a oublié.

## 🛠️ Sous le capot

Six outils, **zéro dépendance** (Python 3.8+ / Node 18+), plus un test Playwright optionnel :

| Outil | Ce qu'il vérifie |
|---|---|
| `scan_trackers.py` | 35+ services tiers, outils de consentement, pages légales |
| `audit_static.py` | Accessibilité, OWASP, secrets, dark patterns, allégations, e-mails, licences |
| `browser_probe.js` | Dans la page : cookies, requêtes tierces, bandeau, contrastes, accessibilité |
| `live_check.mjs` | Navigateur réel : avant / après « Refuser », clavier, axe-core, captures |
| `check_headers.py` | HTTPS, en-têtes de sécurité, cookies, fichiers sensibles exposés |
| `contrast.py` | Ratio WCAG et couleur conforme la plus proche |

Plus **8 modèles de pages** (mentions légales, confidentialité, cookies, CGV, CGU, retours, accessibilité, spécification du bandeau) que Claude **adapte à ton projet réel**. Pas de copier-coller générique.

## 🔒 Ses règles d'or

- **Rien n'est corrigé sans ta validation.**
- **Il n'invente jamais** ton SIRET, ton adresse ou ton hébergeur : il laisse des `[À COMPLÉTER]` bien visibles.
- **Il ne dit pas « conforme » sans avoir testé.** Si un test est impossible, il le dit.
- **Il ne teste que ton projet**, en local de préférence.
- **Il revérifie le droit récent en ligne** à chaque audit (`veille.md`), parce que les règles changent plusieurs fois par an.

## ⚠️ À savoir

En règle te fait gagner du temps et repère les problèmes les plus courants et les plus sanctionnés. Ses outils fonctionnent par détection de motifs et par tests : ils peuvent rater un cas particulier, et c'est pourquoi Claude relit chaque alerte. Enfin, ce **n'est pas un avocat**. Pour une activité réglementée, des données de santé, des mineurs ou un litige, fais valider par un professionnel.

## 🤝 Contribuer

Une règle manque ? Un pays à ajouter ? Un faux positif ? Ouvre une issue ou une PR. Pour toute règle juridique, cite la **source officielle** (Légifrance, EUR-Lex, CNIL, DGCCRF…).

## 📄 Licence

[MIT](LICENSE) — utilise-le, modifie-le, partage-le.

<div align="center">

**Si En règle t'a évité un problème, laisse une ⭐**

</div>
