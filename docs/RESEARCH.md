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

## 12. Frontière 2024–2026 — et comment la battre

*Recherche stricte 2024–2026 (défis officiels lus en texte primaire ;
réserves signalées sur les préprints).*

**Défis officiels (les seuls chiffres comparables)** :
- **SVC 2025** (ACM MM, 21 équipes, cross-domain) : vainqueur 62,44 %
  ACC / 43,89 % F1; 2e (MMPDA, adaptation progressive multi-source) :
  60,43 % / 56,99 % F1.
- **SVC 2026** (CVPRW, 22 équipes, DOLOS protocole I) : vainqueur
  71,35 % ACC / 63,90 % F1 — méthode : pont descripteurs AU/affect →
  langage naturel + LLM; les 2e/3e sont des classifieurs dégénérés
  (F1 de 7,69 % et 11,31 %) : le champ est fragile, pas saturé.
- Cross-dataset 2024 : 58,58 % (single-to-single), 59,69 % (MM-IDGM).
- MLLM zéro-shot : GPT-4o 59,51 %, Gemini 3 Pro 62,13 %, Qwen-VL-Max
  54,32 % sur DOLOS. DeceptionX fine-tuné (7B) : 70,12 % DOLOS,
  61,41 % Bag-of-Lies, 60,58 % MU3D.
- ⚠️ **Correction** : le « GPT-5 zéro-shot 75 % » (Sensors 2025) est
  contredit par les évaluations systématiques (50–62 %); protocole non
  détaillé, non comparable. Même réserve pour ThinkDeception (73,76 %
  revendiqués, disjonction des splits non vérifiable) et les claims
  85–94 % : l'étalement des chiffres publiés vient de protocoles
  incompatibles et de fuites de sujets, pas d'un progrès réel.
- **Sueur par caméra RGB : aucun travail revu par les pairs 2024–2026
  trouvé.** La frontière sudomoteur est thermique (proxy type-EDA
  thermique, 2026; température du nez sensible au type de tromperie,
  Sci Rep 2025 — mais une étude 2024 montre que la véracité seule ne
  module pas la température faciale). Notre signal « brillance
  spéculaire » reste donc classé expérimental, à valider nous-mêmes.
- rPPG : excellent en intra-dataset (MAE 0,27 sur PURE) mais
  effondrement cross-domaine confirmé en 2026 (meilleur MAE 10,61,
  r = 0,26 sur domaine inédit).
- Marché 2024–2026 : l'argent va à la détection de **deepfakes**
  (Clarity, 16 M$ seed 2024, rachetée par Deel; GetReal, 17,5 M$
  série A 2025) — **aucun financement trouvé pour un score de
  « mensonge comportemental »** : le créneau produit est libre, à
  condition de rester dans le positionnement indice/coaching.

**Les 5 faiblesses de l'état de l'art → nos réponses (déjà au repo ou
à la roadmap)** :
1. Effondrement cross-dataset → adaptation progressive multi-source
   (CORAL/MMD/GRL, MMPDA) + pont descripteurs → langage + LLM.
2. Fuite de sujets → protocole **sujet-disjoint publié** +
   leave-one-dataset-out + ré-évaluation indépendante.
3. Pas de baseline individuelle → questions de contrôle + z-scores
   intra-sujet (déjà notre principe n° 1).
4. Aucune calibration (seuil 0,5 partout; F1 de 7,69 % en SVC 2026) →
   calibration par domaine + **prédiction conforme avec abstention**
   (notre zone « indéterminé ») + adaptation au test.
5. Pas de porte qualité + verbal non vérifié → notre **porte pixels**
   (déjà livrée) + module LLM de cohérence factuelle intra-entretien
   (faits vérifiables seulement, pas de chaîne de pensée libre).

**Scores cibles officiels de TruthLens (à publier, protocole gelé)** :
- DOLOS sujet-disjoint : **≥ 75 % ACC / ≥ 75 % F1 / AUC ≥ 0,82**
- Cross-dataset inédit (Box of Lies, Real-Life Trial) : **≥ 65 % ACC /
  ≥ 60 % F1**; leave-one-dataset-out ≥ 65 %
- Écart entre sous-groupes ≤ 5 pts; erreur de calibration ECE ≤ 0,05;
  couverture conforme 90 % ± 2; abstention ≤ 20 % avec ≥ 80 % de
  précision sur les cas retenus.

## 13. Veille — 7 nov. 2026

**Rien de nouveau qui change la donne dans les dernières 24–48 h**, mais
deux rattrapages importants (manqués par les veilles précédentes) et des
confirmations rPPG. Vérifié le 7 nov. 2026, 07h40 (heure de Toronto).

### 13.1 Plafond de la détection verbale automatique — méta-analyse (8 oct. 2026)
- Loconte et al., « A persistent accuracy ceiling in automated verbal
  deception detection », arXiv:2610.12118 (8 oct. 2026). Méta-analyse de
  25 ans : 289 rapports, 6 136 modèles, 3 653 modèles méta-analysés dans
  97 jeux de données.
- Précision agrégée **74,4 % (IC 95 % : 71,2–77,4 %)** ; la précision
  dépend de la qualité méthodologique (vérité-terrain vérifiable,
  équilibre des classes, procédure d'évaluation) plus que de la
  complexité du modèle — **l'adoption des embeddings et des LLM n'a pas
  amélioré la performance prédictive**.
- Seulement **12,46 %** des rapports utilisent des données à
  vérité-terrain vérifiable ; **23,96 %** seulement sont évalués sur
  données indépendantes. Conclusion des auteurs : **plafond de 70–75 %,
  peu susceptible d'être levé par les conventions de recherche
  actuelles**.
- Lecture pour Tensivue : notre cible DOLOS ≥ 75 % ACC se situe
  **au-dessus du plafond méta-analytique** — cible ambitieuse, pas un
  acquis ; elle exige le protocole sujet-disjoint + validation
  inter-corpus déjà gelé (§12). Renforce notre positionnement
  « indice + incertitude », jamais verdict.

### 13.2 WhistleAI — détection sans envoi vidéo (21 juin 2026)
- Sharma, Saran & Singla (WhistleAI), « Catching Lies Without Sending
  the Video: Privacy-Preserving Multimodal Deception Detection »,
  arXiv:2606.22699 (21 juin 2026, préprint non revu par les pairs).
- Sur Real-life Trial Deception (121 clips) : un digest compact (~250
  traits interprétables : transcription, émotion, fluidité/rythme,
  comportement facial par image, prosodie) extrait sur l'appareil
  atteint **AUC 0,741** avec un petit classifieur (équivalent à
  Gemini 2.5 Pro sur vidéo complète) ; remis à un LLM frontière,
  **AUC 0,755 avec Claude Opus 4.8, à 7,8× moins de tokens**, sans
  qu'aucun média brut ne quitte l'appareil.
- Point méthodologique fort : les auteurs démontrent que le « 75 % de
  précision » rapporté dans la littérature est un **artefact de fuite de
  locuteur** (leave-one-video-out) ; en évaluation **sujet-disjointe**,
  la précision honnête est de **~65–70 %** — cohérent avec nos §9/§12.
- ⚠️ **Code annoncé mais inaccessible** : le dépôt cité dans le papier
  (github.com/WhistleAI/lie_detection_binary) retourne **404 le
  7 nov. 2026** (vérifié deux fois, navigateur + fetch direct) —
  dépôt supprimé, renommé ou privé. Non réutilisable en l'état ; à
  revérifier avant tout usage.
- Intégrabilité : **aucun signal nouveau** — le digest reprend nos
  briques déjà prévues (Whisper + MediaPipe + prosodie, phases 2–3).
  La leçon est architecturale : le digest interprétable sur l'appareil
  + juge LLM est exactement notre positionnement (traitement local,
  Loi 25) et valide notre approche. Porte qualité inchangée.

### 13.3 rPPG — confirmations, pas de rupture
- **FaceHeart (Taïwan)** : investissement de TISI (groupe TIS Intec,
  Japon) annoncé le **6 nov. 2026** ; rPPG visage (FC + fréquence
  respiratoire) avec clearances FDA 510(k) ; SDK FaceHeart Vitals +
  miroir CardioMirror (prix CES 2025). La rPPG caméra devient un
  produit de santé grand public validé — conforte notre signal rPPG
  actif, sans changer notre porte qualité (visage ≥ 120 px, ≥ 8 s).
- **FusionPhys** (MDPI, 2026) : sur UBFC-rPPG sujet-disjoint, le
  classique **POS reste devant** (MAE FC 1,02 bpm) contre FusionPhys
  1,38 et DeepPhys 2,60 — confirme notre choix POS (§9) : les méthodes
  classiques restent les plus stables en transfert.
- **Finotti et al., Behavior Research Methods 2026** : rPPG web validée
  contre ECG (ICC 0,96, biais −1,49 bpm, n = 18, webcam Logitech C920,
  30 ips) — valide la mesure par webcam navigateur, mais n = 18 et
  **aucun participant à peau foncée** : généralisation non établie,
  notre exigence d'équité (écart ≤ 5 pts entre sous-groupes) reste
  entière.
- **SCOPE/MDFS** (Frontiers in Bioengineering and Biotechnology,
  2026) : revendique l'état de l'art intra- et cross-dataset sur
  PURE/UBFC/MMPD — chiffres non vérifiés dans le résumé ; à suivre,
  pas de changement de pile.

### 13.4 Déployé / commercial — rien de nouveau
- **EyeDetect / Converus** : pas d'annonce nouvelle dans les dernières
  48 h. Dernière version connue : EyeDetect 5.1 (fév. 2026, monitoring
  temps réel) ; revendications 86–88 % inchangées, toujours sans
  validation indépendante.
- **Deepfake** (hors champ direct, mais vague de fond) : Google
  SynthID Detector gratuit depuis le 7 oct. 2026 ; Nvidia Synthetic
  Video Detector (SIGGRAPH 2026, 92 % sur 1080p non compressée) ;
  Zoom annonce un détecteur de deepfake en direct pour déc. 2026.
  L'argent et l'attention restent sur l'authenticité vidéo, pas sur le
  mensonge comportemental — le créneau Tensivue reste libre (§12).

### 13.5 Passé en revue sans trouvaille
- arXiv (API, requête « deception detection », tri par date) : les
  10 derniers dépôts sont dominés par la **déception des LLM**
  (DecepEval, FIBS, Machine Deception Detector) — hors champ (mensonge
  d'un modèle, pas d'un humain en vidéo) ; un seul papier vidéo-humain
  pertinent (WhistleAI, §13.2).
- **MIDA** (arXiv:2511.16221) : benchmark multi-parties, jeu Werewolf,
  2 360 dialogues, vérité-terrain vérifiable ; GPT-4o et autres MLLM
  peinent. Jeu de société multi-joueurs — pas transposable à notre
  cible (une personne face caméra) ; noté, non intégré.
- Hugging Face : **aucun nouveau modèle/dataset de détection de
  mensonge** ; les sorties récentes sont de la détection de deepfakes
  (Verus-Insight-8B, Venus-DefakerOne2).
- GitHub : aucun dépôt pertinent nouveau ; un « Cool Vitals » (démo de
  concours Presage SmartSpectra, index de tromperie 0–100 % par rPPG,
  usage divertissement déclaré) — pas de preuve, pas intégrable.
- Linguistique seule : FranklinAsk (RAG, Frontiers in AI 2026) F1
  0,519 / précision 0,487 sur exercice militaire NCCA — **sous le
  hasard en précision** ; confirme que le verbal seul ne suffit pas.

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
