# TruthLens — Plan d'affaires détaillé

*Version 1.0 — 5 novembre 2026. Document de travail; les chiffres sont des
hypothèses à valider, pas des promesses.*

---

## 1. Résumé exécutif

TruthLens est un outil d'**analyse vidéo de signaux de tension et
d'incongruence** (regard/rétine, clignements, micro-mouvements répétitifs,
figement, tension faciale, rythme), offert sous deux formes :

1. **Un site web** où l'on téléverse une vidéo et obtient une analyse
   (timeline seconde par seconde, signaux détaillés, rapport exportable).
2. **Une extension Chrome** qui ajoute un **calque en temps réel** par-dessus
   n'importe quelle vidéo lue dans le navigateur (MP4, HLS, YouTube…),
   et un **mode serveur** pour les flux HLS/SRT professionnels.

**Positionnement honnête — c'est notre différenciateur, pas notre faiblesse.**
Aucun produit au monde ne détecte le mensonge à 100 %; la science est claire
(voir `docs/SCIENCE_AND_LIMITS.md`). Tous les concurrents qui promettent
« 95–99 % de détection de mensonge » vendent du vent et s'exposent légalement.
TruthLens vend un **indice mesuré, transparent, avec ses taux d'erreur
publiés** : c'est l'outil des gens qui veulent mieux observer — journalistes,
négociateurs, formateurs, créateurs, chercheurs — pas un juge automatique.

## 2. Produit

### 2.1 Offre gratuite (acquisition)
- Upload de vidéo (analyse locale dans le navigateur, ou serveur éphémère)
- Extension Chrome : calque temps réel local, illimité
- Rapport de base : indice global, timeline, 3 signaux principaux
- **Pourquoi gratuit** : chaque analyse consentie (opt-in explicite,
  séparé) peut contribuer au dataset d'amélioration; le gratuit crée le
  volume, la confiance et le référencement (« analyse ta vidéo »).

### 2.2 Offre payante — le temps réel et la profondeur
| Plan | Prix cible (CAD) | Inclus |
|---|---|---|
| **Pro** | 19 $/mois | Temps réel serveur (HLS/SRT), tous les signaux (rétine, rPPG expérimental, voix), rapports PDF brandés, historique 12 mois, 20 h de flux/mois |
| **Team** | 79 $/mois / siège min. 3 | Pro + espaces partagés, comparaisons multi-vidéos, support prioritaire |
| **API / Entreprise** | sur mesure, dès 499 $/mois | API temps réel, webhooks, hébergement CA dédié, DPA Loi 25, SLA |
| **À l'usage** | 0,50 $/min de flux | Temps réel sans abonnement (créateurs occasionnels) |

Le payant commence exactement là où les coûts commencent : **le temps
réel hébergé** (GPU, bande passante, ingestion continue). L'upload
différé reste gratuit parce qu'il roule sur l'appareil de l'utilisateur.

### 2.3 Ce qu'on ne vendra jamais
- Un verdict « il ment » pour une décision d'embauche, d'assurance,
  de justice, de garde ou de frontière (interdit ou à haut risque dans
  plusieurs juridictions — section 7).
- Des données biométriques d'utilisateurs à des tiers.

## 3. Marché

- **Marché adjacent mesuré** : l'« affective computing » (analyse
  d'émotions) est évalué à plusieurs dizaines de milliards $ US à
  l'échelle mondiale avec une croissance annuelle > 20 % selon les firmes
  d'études (chiffres exacts et sources dans `docs/RESEARCH.md`).
- **Segments de départ (légaux et payants)** :
  1. **Créateurs et médias** : analyser des entrevues publiques, des
     débats, du contenu « body language » — énorme demande organique
     (YouTube/TikTok), faible risque légal (personnes publiques, contenu
     publié, usage commenté/éditorial).
  2. **Formation** : négociation, vente, prise de parole, entraînement
     média — l'utilisateur analyse **ses propres** vidéos.
  3. **Journalisme / vérification** : repérage de passages « à revérifier »
     dans de longues entrevues (l'indice trie, l'humain décide).
  4. **Recherche académique** : licence de la plateforme + dataset consenti.
  5. **Divertissement** : poker, jeux sociaux, émissions — analyse
     consentie des participants.
- **Segments exclus au départ** : RH/recrutement, assureurs, forces de
  l'ordre, immigration (voir risques légaux, section 7).

## 4. Concurrence

| Acteur | Approche | Faiblesse exploitable |
|---|---|---|
| Converus (EyeDetect) | dilatation pupillaire, tests surveillés | fermé, coûteux, controversé scientifiquement |
| Logiciels « lie detector » grand public | webcam + prétentions 95 %+ | aucune validation publiée, risque légal |
| Anciennes plateformes d'entrevue IA (analyse faciale) | scoring de candidats | retraits après backlash (ex. HireVue a abandonné l'analyse faciale en 2021) |
| Polygraphe traditionnel | capteurs contact, examinateur | lent, cher, inadmissible dans bien des contextes |

**Notre angle** : navigateur d'abord (aucune installation lourde), temps
réel sur les flux que les gens regardent déjà, transparence scientifique
publiée, prix grand public.

## 5. Stratégie données (« les milliards d'échantillons »)

Le volume brut ne sert à rien sans vérité-terrain. Plan en 3 couches :

1. **Datasets licenciés/publics** (DOLOS ~1 700 clips étiquetés,
   Bag-of-Lies, MU3D, Real-Life Deception Detection) : calibration et
   **publication de nos taux d'erreur réels** par version.
2. **Collecte consentie propriétaire** : plateforme de « jeu vérité/
   mensonge » rémunérée; objectif 10 000 clips étiquetés en année 1,
   100 000 en année 2 — chaque clip avec consentement, protocole et
   métadonnées (éclairage, angle, langue).
3. **Opt-in produit** : les utilisateurs gratuits peuvent (jamais par
   défaut) donner une vidéo analysée + leur auto-évaluation; ces données
   servent à la robustesse (angles, éclairages), pas à prétendre une
   vérité-terrain qu'elles n'ont pas.

Modèles de départ : open source d'abord (MediaPipe Face Landmarker,
modèles FER/gaze de Hugging Face — inventaire dans `docs/RESEARCH.md`),
fine-tuning seulement quand la couche 2 fournit des données propres.

## 6. Go-to-market

1. **Lancement gratuit** : extension Chrome + site, démo publique sur des
   débats politiques télévisés (contenu public, angle éditorial assumé).
2. **Contenu** : chaîne « TruthLens analyse… » (entrevues virales) —
   chaque vidéo ramène à l'extension. Une image vaut mille mots : la
   démo se vend seule.
3. **Product Hunt + communautés** (journalisme de données, poker,
   négociation) — semaine de lancement.
4. **Conversion** : le gratuit limite le temps réel serveur et les
   rapports avancés → Pro à 19 $.
5. **B2B** : pilotes payants avec écoles de formation et médias (3 pilotes
   visés au T2 2027).

## 7. Risques et cadre légal (à gérer dès le jour 1)

- **EU AI Act** : la reconnaissance d'émotions est **interdite** en milieu
  de travail et d'éducation, et classée à haut risque ailleurs; notre
  positionnement « indice de tension, pas d'émotion ni de mensonge »
  et l'exclusion des segments RH/éducation sont des choix de conformité
  autant que d'éthique.
- **Québec — Loi 25 / CA** : les mesures biométriques sont des
  renseignements sensibles; consentement explicite, évaluation des
  facteurs relatifs à la vie privée (EFVP) avant le mode serveur,
  hébergement au Canada, suppression sur demande.
- **Responsabilité marketing** : aucun claim « détecte les mensonges à
  X % » sans étude publiée et revue; le disclaimer est intégré aux
  rapports, non retirable.
- **Biais** : performance variable selon éclairage, teint, lunettes,
  neurodivergence — à mesurer et publier par sous-groupe dès la phase 2;
  l'indice est désactivé si la confiance de mesure est trop basse.

## 8. Finances — hypothèses (à valider)

| | Année 1 | Année 2 | Année 3 |
|---|---|---|---|
| Utilisateurs gratuits (cumul) | 25 000 | 120 000 | 400 000 |
| Conversion Pro (2–3 %) | ~600 | ~3 000 | ~10 000 |
| Revenu récurrent annuel (fin d'année) | ~140 k$ | ~700 k$ | ~2,3 M$ |
| Pilotes/API B2B | 25 k$ | 150 k$ | 500 k$ |
| Coûts infra (GPU temps réel, stockage) | 30 k$ | 120 k$ | 380 k$ |
| Coûts données (collecte consentie) | 20 k$ | 60 k$ | 120 k$ |

Point mort visé : ~1 200 abonnés Pro (coûts fixes minces : produit
navigateur d'abord, infonuagique à l'usage, aucune équipe de vente en
année 1).

## 9. Jalons

- **T4 2026** : v0.1 publique (ce dépôt), extension soumise au Chrome Web Store.
- **T1 2027** : v0.2 visage complet (rétine/clignements/blendshapes),
  calibration DOLOS publiée.
- **T2 2027** : v1.0 Pro — temps réel HLS/SRT hébergé, Stripe, 3 pilotes B2B.
- **T3 2027** : dataset consenti v1 (10 k clips), page de résultats publique.
- **T4 2027** : API entreprise, EFVP Loi 25 complétée, expansion EN/FR/ES.

## 10. Équipe et besoins

- Fondateur (produit/ingénierie), 1 dev ML/vision, 1 conseiller
  scientifique (psychologie de la tromperie), 1 avis juridique
  vie privée/IA avant le lancement payant.
- Financement visé au départ : revenus + subventions R-D (RS&DE/CRÉIQ —
  le projet est un vrai programme de R-D : incertitude scientifique
  documentée, hypothèses testées, taux d'erreur mesurés).
