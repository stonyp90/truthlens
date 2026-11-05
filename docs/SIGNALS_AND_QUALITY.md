# Inventaire exhaustif des signaux + porte qualité + adaptation de flux

*Directive d'Anthony, 5 nov. 2026 : aller chercher TOUTES les informations
susceptibles de donner un petit pourcentage de plus — et ne jamais dire
de menteries : si les pixels ne sont pas là, on ne peut pas savoir.*

## 1. Tous les signaux physiques visuels (et leurs exigences)

| Signal | Ce qu'on observe | Exigence minimale | Fiabilité honnête |
|---|---|---|---|
| **Sueur** | brillance spéculaire qui augmente (front, nez, lèvre supérieure), gouttes visibles | visage ≥160 px, couleur, éclairage 40–225 | émergent; confondu avec peau grasse/chaleur — signal faible, jamais seul |
| **Tics** | mouvements brusques répétés (œil, bouche, épaule) | visage/corps ≥60 px, ≥15 ips | détectable comme *répétition*; cause non spécifique |
| **Mouvements répétitifs** | balancement, tapotement, auto-contact (main au visage) | ≥60 px, ≥15 ips | autocorrélation robuste |
| **Clignements** | taux, durée, écart vs baseline du sujet | visage ≥90 px, ≥15 ips | mesurable proprement (EAR / blendshapes) |
| **Regard / iris** | aversion, fixité, saccades | visage ≥140 px, netteté ok | agrégé seulement (± plusieurs degrés) |
| **Pupille** | dilatation (charge cognitive) | visage ≥220 px, éclairage stable | très fragile; désactivé si l'éclairage varie |
| **Micro-expressions** | AU fugaces 1/25–1/5 s | visage ≥200 px **et ≥60 ips** | **une vidéo 30 ips en manque la majorité** — le signal est refusé sous 60 ips, point |
| **Tension faciale** | AU sourcils/mâchoire/lèvres (FACS) | visage ≥110 px | blendshapes MediaPipe / AU LibreFace |
| **Rougeur / pâleur** | chrominance de la peau | visage ≥120 px, couleur, éclairage stable | lié au rPPG; sensible à la balance des blancs |
| **rPPG (cœur)** | variations de couleur → FC et variabilité | visage ≥120 px, ≥20 ips, compression faible | MAE labo ~2–5 bpm; s'effondre en mouvement/mauvaise lumière |
| **Déglutition** | pomme d'Adam, cou, salivation | visage/cou ≥130 px | signal d'appoint seulement |
| **Respiration** | montée des épaules/poitrine | cadre ≥ mi-buste | rythme seulement |
| **Figement** | chute soudaine de mouvement | ≥40 px, ≥10 ips | robuste, très non spécifique |
| **Posture / recul** | inclinaison, retrait du tronc | cadre large | contextuel |
| **Voix (audio)** | pauses, débit, jitter, hésitations (Whisper + prosodie) | audio propre | dans DOLOS, l'audio seul ≈ 59 % |
| **Contenu verbal** | contradictions, détails, structure (LLM sur transcript) | transcript fiable | modalité des papiers les plus forts en multimodal |

**Principe de fusion** : aucun de ces signaux ne vaut quoi que ce soit
seul. Le gain vient de la *combinaison* + de la *baseline individuelle*
(on compare la personne à elle-même). Chaque signal activé ajoute son
poids; chaque signal refusé par la porte qualité est **affiché comme
refusé, avec sa raison** — jamais comblé en silence.

## 2. Porte qualité — la règle « pas assez de pixels = on ne sait pas »

Avant tout score, `assessQuality()` (packages/quality.js / .py) mesure :
largeur du visage en pixels, ips, netteté, luminance, couleur.

| Palier | Condition | Comportement |
|---|---|---|
| **insufficient** | visage <80 px ou <15 ips (ex.) | **Aucun indice produit.** Message : « Qualité insuffisante : on ne peut pas savoir » + quoi corriger |
| **basic** | visage ≥80 px, ≥15 ips | tête, tics, figement, clignements |
| **good** | visage ≥130 px, ≥20 ips | + tension faciale, regard, sueur, rPPG, déglutition |
| **excellent** | visage ≥200 px, ≥30 ips | + pupille; micro-expressions seulement si ≥60 ips |

Le rapport liste toujours les signaux **activés** et **refusés (raison)**.
La confiance affichée baisse avec chaque refus.

## 3. Compatibilité et adaptation des flux

À l'ouverture d'une source, `adaptStream()` établit le plan :

| Flux | Ingestion | Adaptation |
|---|---|---|
| MP4 / WebM (fichier) | navigateur, local | directe |
| Webcam / WebRTC | navigateur, temps réel | MediaPipe sur le flux vivant |
| HLS (.m3u8) | navigateur si décodable (MSE/natif), sinon serveur | relais ffmpeg → frames si le navigateur ne décode pas |
| YouTube / Vimeo | calque sur le `<video>` de la page | pixels protégés (CORS) → mode métadonnées + ingestion serveur par URL |
| SRT / RTMP | **serveur obligatoire** (aucun navigateur ne les lit) | ffmpeg : extraction 2–10 ips, échelle recalculée sur le visage détecté |
| >30 ips | — | sous-échantillonné à 30 ips pour les signaux lents; pleine cadence conservée si micro-expressions possibles (≥60 ips) |
| <640 px de large | — | avertissement + signaux fins désactivés par la porte qualité |

Vérifications à l'entrée (tous les flux) : codec, résolution, ips réels
(pas ceux annoncés), débit, présence d'une piste audio, dérive
d'horodatage. Si le flux dévie de ce qui est annoncé, le plan est
recalculé et l'utilisateur est informé — jamais d'analyse silencieuse
sur un flux dégradé.
