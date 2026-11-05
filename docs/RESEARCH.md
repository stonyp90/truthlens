# Recherche — modèles, datasets, concurrents, marché et cadre légal

*Consolidé le 5 nov. 2026 à partir de recherches sourcées. Ne constitue pas
un avis juridique. Une recherche approfondie distincte couvre les
technologies policières et universitaires (polygraphe, EyeDetect, CVSA,
IRMf, datasets) — ses résultats s'ajouteront ici.*

## 1. Briques open source retenues

- **MediaPipe Face Landmarker** (Google, Apache-2.0) : 468 landmarks +
  iris, blendshapes type ARKit — WASM navigateur + Python serveur.
  Brique principale « rétine/regard/clignements/tension ».
- **OpenCV** (BSD) : pipeline serveur v0 (mouvement, présence visage).
- **Whisper** (OpenAI, MIT) : transcription + prosodie (phase 3).
- ⚠️ **Licences des modèles d'émotions (Hugging Face)** : la majorité des
  checkpoints visage populaires sont entraînés sur AffectNet (**licence
  recherche seulement**) et plusieurs modèles vocaux sont en CC BY-NC-SA
  (**non commercial**). Un produit payant ne peut pas les reconditionner
  tels quels — chaque modèle doit passer un audit de licence.

## 2. Datasets avec vérité-terrain

- **DOLOS** : clips d'un jeu télévisé de tromperie, étiquetés
  vérité/mensonge (audio + vidéo); précisions publiées ~60–75 % selon
  protocole.
- **Bag-of-Lies** : enregistrements contrôlés vérité/mensonge.
- **MU3D** : tromperie multi-démographique (utile pour l'équité).
- **Real-Life Deception Detection** (Univ. of Michigan) : vidéos de
  procès réels étiquetées par l'issue du dossier.

## 3. Ce que la science établit (sources dans §6)

- Méta-analyse **Bond & DePaulo (2006)** — 206 études, 24 483 juges :
  les humains détectent le mensonge à **~54 %**, à peine au-dessus du
  hasard; l'expérience professionnelle n'améliore pas significativement.
- **National Research Council (2003)** : la précision du polygraphe est
  insuffisante pour un dépistage de sécurité à grande échelle.
- **Barrett et al. (2019)**, revue de >1 000 études : pas de correspondance
  1-pour-1 entre expression faciale et émotion — et encore moins entre
  visage et mensonge.
- Détection par le visage, études indépendantes : **50–70 %** sur le
  terrain, contre 72–97 % annoncés en laboratoire contrôlé (non
  généralisables).
- **Conclusion produit** : vendre un *score de signaux/incohérences à
  vérifier* avec incertitude affichée — jamais un verdict « ment / ne
  ment pas », jamais « 100 % » (ce claim exposerait à des accusations de
  pratiques trompeuses).

## 4. Concurrents

### Converus — EyeDetect / VerifEye (concurrent direct)
- Lehi, Utah; lancé en 2014, issu de l'University of Utah. Mesure à
  60 mes./s dilatation pupillaire, clignements et comportement de lecture
  pendant un test vrai/faux de 15–30 min.
- Précision **revendiquée : 86–88 %** (dépistage), ~90 % (test dirigé) —
  études surtout affiliées à l'entreprise; algorithme non auditable.
- Modèle : station ~4 000 $ US, scoring **50–150 $/test**, prix final
  200–400 $ (jusqu'à ~800 $ lié à un tribunal), volume pré-emploi
  25–75 $/test; revendique >1 000 clients dans >60 pays, >100 agences
  d'application de la loi aux É.-U.; vente via GSA Schedule.
- Incertitude : on ne sait pas si l'EPPA (qui restreint les polygraphes
  chez les employeurs privés US) s'applique à EyeDetect.

### HireVue — le précédent à ne pas répéter
- A noté les expressions faciales des candidats (via Affectiva) pendant
  des années. **Janvier 2021 : retrait de l'analyse faciale**, après une
  plainte d'EPIC à la FTC (2019) et les critiques de l'ACLU.
- Raison officielle : l'analyse visuelle n'ajoutait qu'**~0,25 %** de
  précision dans la plupart des cas (~4 % rôles face-client). Aujourd'hui :
  contenu verbal seulement + audits de biais.

### iBorderCtrl — le cas d'école européen
- Projet UE Horizon 2020 (2016–2019), **4,5 M€**; avatar qui interroge le
  voyageur et analyse les micro-gestes (« Silent Talker »).
- **~75–76 % en laboratoire sur 32 acteurs seulement**, ~24 % de faux
  positifs rapportés ensuite; jamais déployé à grande échelle; dénoncé
  comme pseudoscience par chercheurs et ONG.

### Analyse d'émotions généraliste (indirects)
- **Affectiva / Smart Eye** (spin-off MIT Media Lab, acquise ~73,5 M$ US
  en 2021) : automobile (surveillance du conducteur, obligatoire UE) et
  tests pub/médias; licences sur devis.
- **Hume AI** : API de mesure d'expressions; prix publics historiques
  ~0,083 $/min vidéo+audio, 0,064 $/min audio, 0,002 $/image; forfaits
  3–500 $/mois (vérifier la disponibilité actuelle avant de bâtir dessus).
- Constat : les acteurs rentables vendent de l'**émotion/engagement**,
  pas du « mensonge » — positionnement délibéré pour rester vendables.

## 5. Cadre légal

### Union européenne — AI Act (Règlement 2024/1689)
- **Interdit depuis le 2 fév. 2025 (art. 5(1)(f))** : inférer les émotions
  **au travail et en éducation** (sauf médical/sécurité). Sanctions :
  jusqu'à 35 M€ ou 7 % du CA mondial.
- **Haut risque (Annexe III)** : recrutement/gestion des travailleurs,
  application de la loi (« polygraphes ou outils similaires »),
  frontières, justice. Obligations reportées au 2 déc. 2027 (Digital
  Omnibus — à revérifier au lancement).
- **Transparence (art. 50(3))** : informer clairement les personnes
  exposées à un système de reconnaissance d'émotions. RGPD art. 9 :
  la biométrie est une catégorie spéciale.

### Québec — Loi 25 et LCCJTI
- La mesure faciale = renseignement **sensible**, biométrique si elle
  caractérise la personne.
- **Art. 44 LCCJTI** : divulgation **préalable à la CAI** + **consentement
  exprès**; en cas de refus, offrir une alternative non biométrique.
- **Art. 45** : toute banque de caractéristiques biométriques déclarée à
  la CAI **≥ 60 jours avant** mise en service; la CAI peut l'interdire
  (précédent Metro inc., fév. 2025).
- **Test de nécessité** : objectif légitime + collecte proportionnelle;
  le consentement ne guérit pas un défaut de nécessité.
- **ÉFVP obligatoire** avant communication hors Québec (art. 17).
- Sanctions : jusqu'à 10 M$ CA / 2 % du CA (administratif), 25 M$ / 4 %
  (pénal).

### Canada — LPRPDE et directives du CPVP (11 août 2025)
- Biométrie = sensible; but approprié (légitimité, efficacité,
  proportionnalité, intrusion minimale); consentement exprès en règle
  générale; préférence pour le traitement **sur l'appareil** (1:1) plutôt
  qu'une base centralisée (1:N); pas d'extraction secondaire sans nouveau
  consentement. Précédent Clearview AI : « publiquement accessible » ≠
  consentement.

### Risques sectoriels
- **RH** : interdit UE au travail; Illinois AI Video Interview Act et
  NYC Local Law 144 (avis + audit de biais) aux É.-U.
- **Justice/police/frontières** : haut risque UE; un score non explicable
  est pratiquement inutilisable comme preuve.
- **Assurance/crédit** : jamais de refus fondé sur le seul signal.
- **Consentement de TOUTES les personnes filmées** — pas seulement de
  celle qui téléverse : c'est le risque n° 1 du modèle « gratuit si tu
  uploades »; le produit doit l'encadrer (attestation + détection
  multi-visages + usage personnel/éditorial).

## 6. Marché (chiffres sourcés, périmètres divergents)

Il n'existe pas de marché isolé crédible « détecteur de mensonge vidéo ».
Références utilisables :

| Périmètre | Taille | Prévision | Source |
|---|---|---|---|
| Emotion AI (logiciel, étroit) | 2,14 G$ US (2024) | 13,40 G$ US (2033), TCAC 22,9 % | Grand View Research 2025 |
| Emotion Detection & Recognition (large) | 39,63 G$ US (2022) | 136,46 G$ US (2030), TCAC ~16 % | Grand View Research 2025 |
| Affective Computing (très large) | 96,19 G$ US (2025) | 339,59 G$ US (2031), TCAC 23,4 % | Mordor Intelligence 2026 |

Lecture pour le plan : TAM de référence = le périmètre étroit
(2,1 G$ en 2024). Le sous-segment adressable au départ (analyse consentie
+ temps réel formation/divertissement) n'est isolé par aucun rapport —
ne pas inventer de chiffre.

**Segments payants réalistes** : médias/pub (tests d'engagement),
formation négociation/vente/prise de parole (ses propres vidéos),
divertissement (participants consentants — c'est là que le modèle
gratuit-upload → payant-temps-réel a le moins de friction),
recherche/UX. **À éviter au lancement** : recrutement, éducation,
police/justice comme outil de décision, assurance comme motif de refus,
vidéos de tiers non consentants.

## 8. Inventaire Hugging Face vérifié (5 nov. 2026)

**Fait central : il n'existe aucun modèle « détecteur de mensonge »
pré-entraîné crédible sur Hugging Face.** Les papiers publient du code
GitHub et des chiffres, pas de poids réutilisables en production.
Ce qui existe, ce sont les briques :

| Brique | Ressource vérifiée | Notes |
|---|---|---|
| Dataset DOLOS | Pas de dataset HF téléchargeable — seulement une *paper page* (huggingface.co/papers/2303.12745); distribution via NTU, **recherche non commerciale** | 1 675 clips, 213 sujets, jeu TV *Would I Lie To You?*, annotations MUMIN (25 traits visage + 5 voix) |
| FER (expressions) | `trpakov/vit-face-expression` (ViT, FER-2013, ~71 % sur son jeu de test); `onnxmodelzoo/emotion-ferplus-8` (ONNX, roule en navigateur) | Classent une expression — ni le stress validé, ni le mensonge; scores chutent en vidéo réelle |
| rPPG (cœur à distance) | `ebowwa/vision-cardio-rppg` (PhysNet; MAE 2,8 bpm après fine-tune UBFC, « wellness/research only »); dataset `kyegorov/mcd_rppg` (600 sujets, 3 600 vidéos, ECG synchronisé — la plus substantielle) | Généralisation éclairage/teint/mouvement non garantie |
| Regard | L2CS-Net : erreur 3,92° (MPIIGaze) à 10,41° (Gaze360); paper page HF, distribution GitHub | En produit : le regard MediaPipe/OpenFace suffit en statistique agrégée |
| Micro-expressions | Aucun modèle HF de production trouvé | CASME II : 247 échantillons à 200 fps; SAMM : 159 — une webcam 30 fps manque la majorité des micro-expressions (1/25–1/5 s) structurellement |

**Rétine/pupille** : aucun modèle HF ni papier solide n'établit un signal
rétinien propre au mensonge. La dilatation pupillaire mesure la charge
cognitive / l'éveil — la même limite que le polygraphe.

**Tailles réelles des datasets de tromperie** (tout le champ repose sur
moins de ~5 000 clips étiquetés) : DOLOS 1 675 · Box of Lies 1 049 ·
Bag-of-Lies 325 (avec EEG et regard) · MU3D 320 · Real-Life Trial 121
(procès criminels réels). L'argument « milliards d'échantillons » ne
s'applique pas à cette tâche : en vie réelle, on ne sait presque jamais
avec certitude que quelqu'un a menti, donc pas de vérité-terrain à
l'échelle.

## 9. Benchmarks publiés (détection automatique par vidéo)

| Modèle | Dataset | Précision | Lecture |
|---|---|---|---|
| PECL (papier DOLOS, ICCV 2023) | DOLOS | **66,84 %** (AUC 64,6 %); visuel seul 61,4 %, audio seul 59,2 %; protocole inter-sexe : 59,0 % | Le résultat de référence des auteurs du dataset |
| DeceptionX (préprint 2026) | DOLOS / Bag-of-Lies / MU3D | 69,8 % / 61,2 % / 60,6 % | État de l'art récent; l'écart entre datasets montre la fragilité |
| GPT-5 trimodal zéro-shot (Sensors 2025) | DOLOS | 75,0 % | Un seul papier, un seul dataset — à répliquer |
| Claims 85–94 % (divers préprints) | mêmes datasets | 85–94 % | **Non établis** : non répliqués, très au-dessus du challenge officiel SVC (CVPR) qui décrit la précision comme « à peine au-dessus du hasard » en conditions difficiles |

Synthèse : **intra-dataset ~60–75 %; cross-dataset ~55–65 %**. À 65 %,
environ 1 verdict sur 3 est faux — inutilisable comme preuve, utile
comme aide à l'observation avec consentement et avertissements.

**rPPG, généralisation (étude 2025, MAE FC en bpm)** : DeepPhys 3,1
(PURE) → 9,1 (conditions nouvelles); POS classique 7,5 → 1,1. Les modèles
appris gagnent sur benchmarks propres et perdent le plus en transfert;
les méthodes classiques (POS/CHROM) sont plus stables. Et une FC parfaite
ne mesure que l'éveil : stress, effort, caféine et mensonge se recouvrent.

**Les 5 raisons pour lesquelles 100 % est impossible** : (1) aucun signal
n'est unique à la tromperie (consensus APA + NRC 2003); (2) pas de
vérité-terrain à l'échelle; (3) le jeu TV/labo ≠ la vie réelle (chute en
transfert mesurée); (4) contre-mesures et variabilité individuelle;
(5) problème du taux de base — même à 90 %/90 %, sur une population à
5 % de mensonges, la majorité des alertes sont de faux positifs (argument
central du NRC contre le dépistage).

⚠️ Piège à éviter dans nos communications : les deux « APA » —
l'**American Psychological Association** (psychologues : peu de preuves
que le polygraphe détecte les mensonges) vs l'**American Polygraph
Association** (l'industrie, qui revendique 89 % dans une méta-analyse
commandée par elle-même, contestée). Ne jamais citer « 89 % APA » sans
préciser laquelle.

## 10. Pipeline de l'état de l'art (celui que TruthLens suit)

`vidéo → MediaPipe (navigateur, temps réel) ou LibreFace/OpenFace
(serveur, upload — licences commerciales à vérifier séparément)
→ séries [AU FACS, clignements, regard, pose] + rPPG POS (FC)
+ Whisper (texte, pauses, débit) → fusion entraînée sur DOLOS +
Bag-of-Lies + MU3D → indice de tension/incongruence calibré,
expliqué signal par signal.`

Formats temps réel — précision honnête : MediaPipe analyse un
`HTMLVideoElement` (webcam, MP4/WebM, WebRTC). **Le SRT n'est pas lisible
par un navigateur** : c'est un protocole d'ingestion serveur, il faut un
relais (SRT → WebRTC/HLS/WebSocket) avant analyse. Le « calque temps
réel » de l'extension couvre webcam/MP4/HLS lu par le navigateur; le SRT
passe par le worker serveur (roadmap phase 3).

## 11. Technologies policières et universitaires — recherche approfondie

*Recherche sourcée complète (rapport de 310 lignes, sources primaires :
National Academies, NIJ, arrêts de cour) — synthèse :*

| Technologie | Qui l'utilise | Précision démontrée | Statut |
|---|---|---|---|
| **Polygraphe (CQT)** | polices, GRC (pré-emploi), fédéral US | incident précis : au-dessus du hasard, sous la perfection (NRC 2003, 57 études); dépistage : insuffisant (ex. 10 000 employés/10 espions → ~1 600 innocents accusés pour en attraper 8) | **Inadmissible au criminel au Canada (R. c. Béland, 1987)**; aide à l'enquête seulement; ~50 % des coupables entraînés le battent (contre-mesures) |
| **CVSA (stress vocal)** | 1 400+ agences US (selon fabricant) | étude terrain NIJ (319 arrêtés, vérité = analyse d'urine) : **~50 % global, 15 % des menteurs**; NRC : « peu ou pas de base scientifique » | échec validé — **exclu de TruthLens** |
| **EyeDetect (Converus)** | 100+ agences US, né à l'Univ. de l'Utah | 86–88 % **revendiqués**; aucune validation indépendante (études de l'équipe interne/affiliée); chutes à ~50 % rapportées par son dir. scientifique | une seule admission Daubert connue (NM, 2018); DoD/ODNI : pas de substitut au polygraphe pour le vetting fédéral |
| **Thermique faciale** | DoDPI + Mayo Clinic (recherche) | 83 % sur **n = 20**, crime simulé (Nature, 2002) | jamais déployé ni répliqué à l'échelle |
| **IRMf** | No Lie MRI / Cephos (semblent défuntes) | 76–90 % labo intra-sujet; contre-mesures : 100 % → 33 % (Ganis 2011) | **exclue par les cours US** (Semrau, 2010 : pas de taux d'erreur réel ni de standard) |
| **EEG/P300 (Brain Fingerprinting)** | cas isolés (Harrington, Iowa) | revendique 100 %; critique 2013 : 1 seule étude labo relue (20 sujets), terrain = 4 et 6 sujets | le paradigme sous-jacent **CIT-P300 est légitime** (méta 2014 : d* = 1,89 — le plus fort effet du domaine) |
| **Michigan — Real-Life Trial** | recherche | fusion verbal + gestuel : **60–75 %** (humains ~50–59 %) | corpus de référence (121 clips) |
| **iBorderCtrl (UE)** | projet Horizon 2020, 4,5 M€ | 75,6 %/73,7 % sur personnes nouvelles, écarts-types 24–34 pts; ~95 % seulement avec fuite train/test | jamais déployé, terminé 2019 |

**Plan de fusion retenu pour TruthLens (le plus défendable)** :
1. **Contenu verbal vérifiable + entretien cognitif** (approche Vrij :
   questions inattendues, charge cognitive, vérifiabilité, SUE) — méta :
   54 % → ~71 %, le gain le plus robuste, aucune machine requise.
2. **CIT multimodal** quand des détails non publics existent :
   conductance (d* 1,55) + respiration (1,11) + cœur (0,89), ± P300
   (1,89) — protège les innocents par construction (un innocent ne
   réagit pas à un détail qu'il ignore); usage opérationnel au Japon.
3. **Audio-visuel automatique** (prosodie + visage + texte, fusion
   apprise) en appoint probabiliste : +5–10 pts, plafond réaliste
   ~70 % inter-sujets; validation sujet-disjointe et inter-corpus
   exigée avant tout usage.
4. **Thermique / rPPG** : expérimental seulement.
Exclus : VSA, micro-expressions comme preuve.
Sortie : **probabilité calibrée + zone « indéterminé »**, jamais de
décision autonome. Attente réaliste : **70–85 % sur incident spécifique**;
valeur prédictive qui s'effondre en dépistage de masse (taux de base).

## 7. Sources principales

- Converus/EyeDetect : liedetectortest.com (coûts et technologie EyeDetect)
- HireVue : aiaaic.org (registre d'incidents IA); sovaassessment.com
- iBorderCtrl : iborderctrl.no; europeanbusinessreview.eu
- Science : Bond & DePaulo 2006; National Research Council 2003;
  Barrett et al. 2019 (via waisman.wisc.edu); mcafeeinstitute.edu
- AI Act : ai-act-service-desk.ec.europa.eu (Annexe III);
  casrai.org (art. 5); pitch.law (RH)
- Loi 25 / biométrie : didit.me; workaxle.com
- CPVP 2025 : legal500.com; millerthomson.com
- Marché : grandviewresearch.com; mordorintelligence.com;
  emergenresearch.com; forasoft.com; dupple.com (Hume)
