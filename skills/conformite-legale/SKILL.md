---
name: conformite-legale
description: Audite, teste et corrige la conformité légale et la sécurité d'un site web, d'un e-commerce, d'un SaaS ou d'une appli mobile — France, Union européenne et monde. Grille de 30 points légaux (mentions légales LCEN, RGPD, politique de confidentialité, cookies et bandeau CNIL, CGV/CGU, rétractation et bouton de rétractation, remboursement, médiateur, garanties, résiliation en 3 clics, dark patterns, faux avis, allégations, prospection e-mail, licences, accessibilité RGAA/EAA/WCAG, DSA, AI Act) + 15 points sécurité (OWASP Top 10 2025, en-têtes HTTP, secrets, API, IA). Analyse le code, teste le site dans un vrai navigateur (traceurs avant consentement, contrastes, clavier), rédige un rapport, puis corrige après validation et retest. Utilise ce skill dès que l'utilisateur veut déployer, lancer ou mettre en ligne un site ou une appli « en règle », « conforme », « sans risque juridique », ou parle de RGPD, GDPR, CNIL, cookies, bandeau cookies, mentions légales, politique de confidentialité, CGV, CGU, RGAA, accessibilité, WCAG, DGCCRF, OWASP, sécurité avant mise en production, audit légal — même s'il ne demande pas explicitement un audit.
---

# Conformité légale et sécurité des sites et applis

Objectif : qu'un site ou une appli puisse être mis en ligne **sans exposer son éditeur à une sanction ou à une action en justice**. Le skill fait tout le cycle sur le projet réel de l'utilisateur, quelle que soit sa stack :

**Analyser → Tester → Rapport → Validation par l'utilisateur → Corriger → Retester**

## Règles de conduite

- **Rien n'est corrigé avant que l'utilisateur ait validé le rapport.** L'audit et les tests ne modifient pas le projet (hors fichiers de rapport). L'utilisateur peut valider tout, une partie (« corrige 1 à 10 »), ou rien.
- **Ne jamais inventer d'informations d'identité** (SIRET, adresse, capital, hébergeur, médiateur, directeur de publication). Laisser un marqueur `[À COMPLÉTER : …]`. Un faux SIRET dans des mentions légales engage l'éditeur.
- **Le droit appliqué par défaut est français et européen.** Les règles d'autres pays s'ajoutent seulement si le projet vise ces pays.
- **Tester uniquement le projet de l'utilisateur** : en local de préférence. Aucun test de sécurité actif sur un site en production ou sur un service tiers sans son accord explicite.
- **Tu n'es pas avocat.** Dis-le une fois dans le rapport, en précisant que le rapport n'est pas un conseil juridique, ne garantit pas la conformité et que l'éditeur reste seul responsable de son site, et indique précisément quand un juriste est nécessaire (activité réglementée, données de santé, mineurs, grosses volumétries, litige en cours). Ne noie pas chaque paragraphe d'avertissements.
- **Ne pas affirmer qu'un point est conforme sans l'avoir vérifié.** Si un test n'a pas pu être fait (pas de navigateur, site qui ne démarre pas), le statut est ❓ avec la raison.

## Étape 1 — Cadrer (lire avant de demander)

Explore le projet : manifestes (`package.json`, `composer.json`, `pubspec.yaml`, `Podfile`…), routes et pages, pied de page, formulaires, scripts tiers, configuration d'hébergement, paiement, comptes, IA, e-mails, i18n. Pré-remplis tout ce que tu peux, puis pose **en un seul lot** les questions restantes :

| Question | Pourquoi |
|---|---|
| Statut de l'éditeur (particulier, EI/micro, société, association, public) et taille (< 10 salariés et < 2 M€ ? > 250 M€ de CA ?) | Mentions obligatoires, exemptions accessibilité, RGAA |
| Type (vitrine, blog, e-commerce, SaaS, marketplace, appli, contenus d'utilisateurs) et clients (B2C, B2B) | Blocs de règles applicables |
| Pays visés | Lois étrangères (`references/international.md`) |
| Mineurs ? Données sensibles ? Activité réglementée ? IA ? | Règles spécifiques, avis juridique |
| Comment lancer le site en local (commande, port) ou URL de préproduction | Indispensable pour les tests en navigateur |
| Informations d'identité disponibles (SIRET, hébergeur, médiateur…) | Pour remplir les pages sans rien inventer |

Si l'utilisateur ne sait pas, prends l'hypothèse la plus protectrice et note-la.

## Étape 2 — Analyser le code

**Toutes les stacks** : les scripts lisent JS/TS, PHP (Twig, Blade, Latte), Python (Jinja, Django), Ruby (ERB, Slim, Haml), Java/Kotlin (JSP, Thymeleaf, FreeMarker), C# (Razor, Blazor), Go, Elixir, Rust, Swift, Dart et HTML. **Sans accès au code** (Shopify, Wix, Squarespace, Webflow, site d'un prestataire) : saute les analyses statiques, fais toute l'étape 3 sur l'URL en ligne (`live_check.mjs`, `check_headers.py`) et lis le texte de chaque page dans le navigateur à la place de `extract_texts.py` ; note dans le rapport que le code n'a pas été audité. Pour WordPress, audite aussi la liste des extensions actives (traceurs et bandeaux sont souvent des extensions).

Lance les deux analyses statiques (Python 3.8+, aucune dépendance) :

```bash
python3 <skill>/scripts/scan_trackers.py <projet>    # traceurs, bandeau, pages légales, services tiers
python3 <skill>/scripts/audit_static.py <projet>     # accessibilité, sécurité OWASP, dark patterns, allégations, e-mails, licences
```

Puis audite les dépendances avec l'outil de la stack (`npm audit --omit=dev`, `pnpm audit`, `pip-audit`, `composer audit`…). Si `gitleaks` ou `trufflehog` sont installés, lance-les aussi.

Les scripts donnent des indices : **lis chaque occurrence importante** pour confirmer ou écarter. Les commentaires du code sont ignorés et les mots cités dans un texte (« OpenAI », « checkout ») ne comptent pas comme une intégration ; un constat restant peut quand même être un faux positif : écarte-le en le disant, ne le recopie pas tel quel dans le rapport.

## Étape 2 bis — Lecture intégrale (obligatoire)

Un script ne comprend pas le sens d'une phrase. **Chaque texte visible et chaque traitement de données doit être lu par toi**, pas échantillonné.

1. **Inventaire des textes** :
   ```bash
   python3 <skill>/scripts/extract_texts.py <projet> --out textes-visibles.md
   ```
   Il liste, fichier par fichier et ligne par ligne, toutes les phrases affichées (pages, composants, traductions, attributs `alt`/`aria-label`/`placeholder`, métadonnées, e-mails). Lis **toutes** les lignes, dans toutes les langues du site.
2. **Pour chaque phrase**, cherche :
   - **Allégation non prouvable** (point 23) : chiffres, scores, « garanti », « n°1 », délais promis, taille de l'entreprise (« notre équipe » pour un indépendant), certifications, clients ou résultats cités.
   - **Promesse contractuelle** : « devis gratuit sous 48 h », « remboursé », « sans engagement » — elle engage l'éditeur et doit être tenable et cohérente avec les CGV.
   - **Mentions obligatoires** (points 1, 7, 19) : comparer **mot à mot** avec l'immatriculation (Kbis/INSEE : nom, forme, adresse de l'établissement, RCS/RNE, TVA). Une adresse ou un RCS différent du Kbis est un constat.
   - **Dark patterns et pression** (point 21) : urgence, rareté, culpabilisation, consentement forcé.
   - **Accessibilité du libellé** (points 26, 29) : nom accessible cohérent avec le texte visible, liens explicites, langue.
   - **Marques et contenus tiers** (point 24) : logos, noms de marques, images, citations.
3. **Cartographie des données (RGPD/CNIL)** : liste **chaque** collecte ou envoi de données dans le code — formulaires, `fetch`/appels serveur, API tierces, e-mails, journaux (`console.log`, logger), adresse IP (limitation, statistiques), `localStorage`/`sessionStorage`/cookies, polices et scripts externes. Puis vérifie dans **les deux sens** :
   - tout ce que fait le code figure dans la politique de confidentialité (finalité, base légale, durée, destinataire, transfert hors UE) ;
   - tout ce que dit la politique existe réellement dans le code (une politique qui décrit un traitement inexistant est elle-même inexacte).
4. **Accessibilité (RGAA)** : au-delà d'axe-core, vérifie à la lecture du code les critères qu'aucun outil automatique ne couvre : animations et contenus en mouvement (pause, `prefers-reduced-motion`), alternatives des contenus non textuels, ordre de lecture, messages d'erreur des formulaires, changements de contexte, textes en image.
5. Note dans le rapport la section **« Lecture intégrale »** : nombre de fichiers et de textes relus, et chaque constat avec `fichier:ligne`. Ne conclus pas sur un point légal tant que cette lecture n'est pas faite.

## Étape 3 — Tester le site en fonctionnement

Les tests en navigateur sont **obligatoires** pour les points 9, 10, 11, 27 et 28 : un bandeau peut exister dans le code et laisser passer Google Analytics.

1. **Lancer le site** : commande de dev ou de preview du projet (ou URL de préproduction fournie). Si le site ne démarre pas, essaie de le faire démarrer (dépendances, variables d'environnement d'exemple) ; à défaut, marque les points concernés ❓ et dis pourquoi.
2. **Tester avec un navigateur**, par ordre de préférence :
   - **Playwright disponible** (ou installable avec l'accord de l'utilisateur) : `node <skill>/scripts/live_check.mjs <url> <url/page2> … --axe`. Il teste en session neuve les cookies (y compris HttpOnly) et les requêtes avant consentement, clique sur « Refuser », revérifie, teste la navigation au clavier, lance axe-core et prend des captures.
   - **Outil navigateur de la session** (navigateur intégré, Claude in Chrome, Playwright MCP, DevTools MCP) : ouvre le site dans une session sans cookies, exécute le contenu de `scripts/browser_probe.js` comme expression JavaScript sur chaque page clé, lis les cookies et les requêtes réseau, clique sur « Refuser », recommence ; teste la touche Tab sur la page d'accueil, le bandeau, un formulaire et le tunnel de commande.
   - **Aucun navigateur** : demande à l'utilisateur de coller `browser_probe.js` dans la console de son navigateur en navigation privée et de te renvoyer le résultat.
3. **Pages à tester au minimum** : accueil, une page de contenu, formulaire de contact ou d'inscription, fiche produit, panier et étape de paiement (sans payer), espace compte, pages légales.
   - `live_check.mjs` cherche Playwright et `@axe-core/playwright` **dans le dossier courant** : installe-les au même endroit (`npm i -D playwright @axe-core/playwright && npx playwright install chromium`) et lance le script depuis ce dossier.
   - S'il n'y a **ni cookie ni requête vers un traceur**, l'absence de bouton « Refuser » est normale : le script l'affiche « ➖ sans objet ».
   - Si une page renvoie une **protection anti-robots** (Vercel Security Checkpoint, Cloudflare…), le script l'affiche « ❓ page bloquée » au lieu de tester la page de contrôle : refais les tests sur la version de production lancée en local. `check_headers.py` fait de même pour les en-têtes.
   - Les éléments des outils de développement (barre Next.js, Vite, Astro…) sont ignorés au test clavier. Si le script signale un **serveur de développement**, refais les tests d'en-têtes et de scripts sur la version de production (`build` puis `start`/`preview`), car la politique de sécurité et les scripts y sont différents.
4. **Tester les en-têtes HTTP** : `python3 <skill>/scripts/check_headers.py <url>` (ajouter `--probe-files` pour vérifier que `.env` et `.git` ne sont pas servis). De préférence sur la version de production, pas sur le serveur de développement.
5. **Contrastes** à corriger : `python3 <skill>/scripts/contrast.py <texte> <fond>` donne le ratio et une couleur conforme proche.

## Étape 4 — Évaluer selon la grille

Lis `references/checklist.md` : **30 points légaux + 15 points sécurité**. Évalue chaque point, en lisant les références utiles au projet :

| Fichier | Contenu |
|---|---|
| `references/checklist.md` | La grille complète, la méthode de test de chaque point |
| `references/france.md` | Mentions légales, statuts, langue, RGAA, EAA |
| `references/rgpd-cookies.md` | RGPD, politique de confidentialité, cookies CNIL, prospection, mineurs, transferts |
| `references/ecommerce.md` | Code de la consommation : commande, rétractation, garanties, médiateur, prix |
| `references/saas-plateformes.md` | CGU, abonnements, résiliation, DSA, AI Act |
| `references/pratiques-trompeuses.md` | Dark patterns, avis, allégations commerciales et environnementales |
| `references/licences.md` | Polices, images, icônes, code, contenus IA |
| `references/securite-owasp.md` | OWASP Top 10 2025 + 5 compléments, tests et corrections |
| `references/mobile.md` | Applis : stores, SDK, permissions |
| `references/international.md` | UK, Suisse, USA, Québec, Brésil, etc. |
| `references/corrections.md` | Comment corriger chaque problème selon la stack |
| `references/veille.md` | Règles récentes ou instables à revérifier |

**Revérifier les points instables** : pour chaque ligne de `veille.md` qui concerne le projet et dont la vérification date de plus de 3 mois, fais une recherche rapide (Légifrance, EUR-Lex, cnil.fr, DGCCRF, owasp.org en priorité) et indique le résultat dans le rapport.

## Étape 5 — Rapport, puis STOP

Écris `CONFORMITE.md` à la racine du projet avec **exactement** cette structure (comparable d'un audit à l'autre) :

```markdown
# Audit de conformité — [projet]

_Date : AAAA-MM-JJ · Périmètre : [type, B2C/B2B, pays] · Droit appliqué : France / UE [+ pays]_
_Tests réalisés : analyse du code ✅ · lecture intégrale [✅ N textes / ❓] · navigateur [✅ / ❓ raison] · en-têtes HTTP [✅ prod / ⚠️ dev / ❓] · dépendances [✅ / ❓]_

## Résumé
[Niveau global en 3 à 5 phrases. Nombre de ❌ et de ⚠️. Peut-on mettre en ligne en l'état ?]

## Les 5 corrections les plus urgentes
1. [Point n° — problème — correction — pourquoi c'est urgent]
…

## Grille légale (30 points)
| # | Point | Statut | Où (page / fichier:ligne) | Constat | Action | Gravité |
|---|---|---|---|---|---|---|
| 1 | Mentions légales | ❌ | — | Aucune page | Créer /mentions-legales (3 infos à fournir) | 🔴 |

## Sécurité (15 points)
| # | Point | Statut | Où | Constat | Action | Gravité |

## Points additionnels
[Mobile, international, DSA, AI Act, activité réglementée : seulement si applicable.]

## Traceurs et services tiers
| Service | Domaine | Chargé avant consentement ? | Consentement requis ? | Action |

## Lecture intégrale
[Fichiers et textes relus (nombre), cartographie des données dans les deux sens (code → politique, politique → code), constats avec fichier:ligne.]

## Hypothèses
## À fournir par vous
[Informations d'identité, licences, choix de médiateur…]
## Hors code (démarches)
[Registre des traitements, DPA, adhésion au médiateur, révocation de clés exposées…]
## Points revérifiés en ligne et limites
```

Statuts : ✅ OK · ⚠️ À améliorer · ❌ Manquant ou non conforme · ➖ Non applicable · ❓ Non vérifié (raison).
Gravité : 🔴 Bloquant (sanction directe, faille exploitable, contrôle fréquent) · 🟠 Important · 🟡 Recommandé.

Classe toujours en 🔴 : traceurs chargés avant consentement, absence de bouton « Refuser » équivalent, mentions légales ou politique de confidentialité absentes, absence d'information sur la rétractation ou de fonction de rétractation pour un site marchand, absence de médiateur, case de consentement pré-cochée, secret exposé, contrôle d'accès absent sur des données personnelles, injection exploitable.

**Ordre des 5 corrections urgentes** : d'abord les failles de sécurité exploitables et les secrets exposés, puis les traceurs sans consentement, puis les informations légales obligatoires manquantes, puis les pratiques trompeuses, puis l'accessibilité bloquante.

Présente ensuite à l'utilisateur un résumé court (statuts globaux, 5 urgences) et **arrête-toi** : demande ce qu'il valide (tout, une sélection de numéros, ou rien) et les informations d'identité manquantes. Ne modifie rien avant sa réponse.

## Étape 6 — Corriger (après validation)

Applique les corrections validées en suivant `references/corrections.md`, dans l'ordre de gravité, par petits lots cohérents :
- utilise la stack et les conventions du projet (composants, styles, i18n, routes) ; pars des modèles de `templates/` en supprimant tout ce qui ne s'applique pas — une politique de confidentialité qui décrit des traitements inexistants est elle-même non conforme ;
- après chaque lot : build, lint et tests du projet s'ils existent ; corrige ce que tu as cassé avant de continuer ;
- **corrections à risque** (montée de version majeure, changement d'authentification, migration de données, suppression de fonctionnalité, choix d'un prestataire payant) : propose-les, ne les applique qu'avec un accord explicite pour chacune ;
- **actions que toi seul ne peux pas faire** (révoquer une clé chez un fournisseur, adhérer à un médiateur, signer un DPA, acheter une licence) : liste-les clairement pour l'utilisateur.

| Modèle | Usage |
|---|---|
| `templates/mentions-legales.md` | Tous les sites |
| `templates/politique-confidentialite.md` | Données personnelles |
| `templates/politique-cookies.md` | Traceurs |
| `templates/bandeau-cookies.md` | Spécification du bandeau et du blocage préalable |
| `templates/cgv.md` | Vente |
| `templates/politique-retours.md` | Rétractation, retours, remboursements |
| `templates/cgu.md` | Comptes, contenus d'utilisateurs, SaaS |
| `templates/declaration-accessibilite.md` | RGAA ou EAA |

## Étape 7 — Retester et clôturer

Relance **les mêmes tests** qu'aux étapes 2, 2 bis et 3 (scripts, relecture des textes modifiés, navigateur, en-têtes). Une correction n'est ✅ que si le retest le confirme. Puis mets à jour `CONFORMITE.md` :
- ajoute une section **« Avant / après »** : tableau des points corrigés avec l'ancien et le nouveau statut, et la preuve du retest (par exemple « 0 requête vers google-analytics.com avant consentement ») ;
- liste les marqueurs `[À COMPLÉTER]` restants (`grep -rn "À COMPLÉTER"`) ;
- liste ce qui reste à faire hors code.

Termine par un message court : ce qui a été corrigé et vérifié, ce qui reste à fournir ou à faire, et si le site peut être mis en ligne.

## Mode audit seul

Si l'utilisateur demande seulement un audit (« audite », « vérifie », « dis-moi ce qui manque »), fais les étapes 1 à 5 et arrête-toi. S'il fournit sa propre liste de points, utilise-la comme structure du rapport et complète avec les points de la grille qu'elle omet, dans une section « Autres points détectés ».
