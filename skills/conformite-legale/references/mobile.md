# Applis mobiles : droit applicable et exigences des stores

Une appli est soumise aux mêmes lois qu'un site (RGPD, consommation, accessibilité, DSA, AI Act). S'y ajoutent les règles des stores, qui entraînent un **rejet ou un retrait** en cas de manquement : c'est souvent le premier risque concret.

## Droit applicable

- **Traceurs dans les applis** : l'article 82 s'applique aussi aux SDK (publicité, analytics, attribution). La CNIL a publié une recommandation sur les applications mobiles (2024) : consentement avant d'activer les SDK non essentiels, information claire, permissions demandées au moment utile et justifiées.
- **Permissions** (localisation, contacts, caméra, micro, photos) : seulement si nécessaires, expliquées, demandées en contexte.
- **Mentions légales, politique de confidentialité et CGU/CGV** : accessibles **dans l'appli** (écran « À propos » ou « Paramètres ») et sur la fiche du store.
- **Achats intégrés et abonnements** : prix clairs, résiliation (voir `saas-plateformes.md`) ; si l'abonnement passe par Apple ou Google, indiquer comment résilier via le store.
- **Accessibilité** : EAA si l'appli permet d'acheter (e-commerce) ; viser WCAG 2.1 AA / EN 301 549 (tailles dynamiques, VoiceOver, TalkBack, contrastes).

## Apple App Store

- **URL de politique de confidentialité** obligatoire dans App Store Connect et accessible dans l'appli.
- **App Privacy details** (« étiquettes nutritionnelles ») : déclarer précisément les données collectées, y compris par les SDK tiers.
- **Privacy manifest** (`PrivacyInfo.xcprivacy`) : déclarer les « required reason APIs » et les domaines de suivi ; les SDK tiers courants doivent fournir le leur.
- **App Tracking Transparency** : demander l'autorisation avant tout suivi entre applis et sites d'autres entreprises (IDFA, partage publicitaire).
- **Suppression du compte dans l'appli** obligatoire si l'appli permet d'en créer un.
- **Sign in with Apple** ou option équivalente respectueuse de la vie privée si l'appli propose une connexion via des services tiers (Google, Facebook), sauf exceptions.
- **Statut de « trader » (DSA)** : déclaration obligatoire pour distribuer dans l'UE ; les coordonnées des professionnels sont affichées sur la fiche.
- **Applis pour enfants** (catégorie Kids) : pas de publicité ciblée ni d'analytics tiers, contrôle parental avant les liens externes et achats.
- **IA générative et contenu publié par les utilisateurs** : modération, signalement, blocage d'utilisateurs exigés (règle 1.2).

## Google Play

- **Politique de confidentialité** : URL dans la Play Console et lien dans l'appli.
- **Section « Sécurité des données »** (Data safety) : déclaration exacte des données collectées et partagées, y compris par les SDK.
- **Suppression du compte** : dans l'appli **et** via une URL web accessible sans réinstaller l'appli.
- **Prominent disclosure** : écran d'information avant la collecte de données sensibles (localisation en arrière-plan, contacts…).
- **Statut de trader (DSA)** pour l'UE.
- **Familles** : règles spécifiques si l'appli vise des enfants (SDK certifiés, pas d'identifiants publicitaires).
- **Niveau d'API cible** à jour, sinon l'appli n'est plus proposée aux nouveaux utilisateurs.

## À vérifier dans le code

- SDK présents (Firebase Analytics, Facebook SDK, AppsFlyer, Adjust, AdMob, OneSignal, Sentry…) et leur activation **avant** consentement.
- `Info.plist` : textes `NS…UsageDescription` explicites, en français si l'appli vise la France.
- `AndroidManifest.xml` : permissions déclarées réellement utilisées.
- Écran de suppression de compte, liens légaux dans les paramètres, bandeau ou écran de consentement au premier lancement.
