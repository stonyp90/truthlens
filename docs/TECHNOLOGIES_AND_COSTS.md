# Comment ça marche, technologie par technologie — et ce que ça coûte

*Le document « dans le fond » de TruthLens : pour détecter les signes de
tromperie sur une vidéo, voici chaque technologie, ce qu'elle fait dans
le pipeline, et son coût réel. Règle de conception d'Anthony : ça doit
se faire, et ça ne doit pas coûter trop cher.*

## Le pipeline complet (une vidéo, de l'entrée au score)

```
Vidéo (fichier, YouTube, HLS, SRT…)
  → 1. Adaptation du flux      on sonde le flux réel, on le convertit si besoin
  → 2. Porte qualité           assez de pixels sur le visage ? sinon on refuse
  → 3. Extraction des signaux  visage, yeux, peau, voix, mots — en parallèle
  → 4. Baseline individuelle   on compare la personne à ELLE-MÊME (début calme)
  → 5. Fusion                  chaque signal vote avec son poids calibré
  → 6. Score calibré           probabilité + zone « indéterminé » si incertain
```

## Technologie par technologie

### A. Celles qui roulent GRATUITEMENT sur l'appareil de l'utilisateur (0 $)

| Technologie | Ce qu'elle fait | Coût |
|---|---|---|
| **MediaPipe Face Landmarker** (Google, WASM) | 478 points du visage + iris + 52 blendshapes, en direct dans le navigateur : clignements, regard, tension sourcils/bouche/mâchoire, pose de tête | **0 $** — open source, tourne sur le téléphone/PC de l'utilisateur |
| **Analyse de mouvement** (notre code) | tics, mouvements répétitifs (autocorrélation), figement, balancement | **0 $** |
| **rPPG classique (POS/CHROM)** | rythme cardiaque depuis les variations de couleur de la peau | **0 $** — algorithmes publiés, notre implémentation, CPU seulement |
| **Sueur — brillance spéculaire** | suit l'augmentation de brillance (front, nez, lèvre supérieure) | **0 $** à calculer — mais **expérimental** : aucun papier 2024-2026 revu ne le valide en RGB; on le mesure, on ne le vend pas comme prouvé |
| **ONNX Runtime Web + petit modèle d'expressions** | classification d'expressions image par image, dans le navigateur | **0 $** (vérifier la licence du modèle choisi) |
| **Porte qualité + adaptation de flux** (notre code) | mesure les pixels du visage, les ips, la lumière; choisit le plan d'ingestion | **0 $** |

👉 **Tout le produit gratuit vit ici.** Aucun serveur à payer : l'appareil
de l'utilisateur fait le travail. C'est ce qui rend le modèle
« gratuit si tu uploades » viable.

### B. Celles qui coûtent un petit serveur CPU (le mode upload hébergé)

| Technologie | Ce qu'elle fait | Coût |
|---|---|---|
| **LibreFace / OpenFace** (serveur) | unités d'action FACS précises (intensité), regard — l'analyse lourde des uploads | Petit VPS CPU : **~10–25 $/mois** pour démarrer (licences à vérifier : usage commercial séparé pour OpenFace) |
| **Whisper** (transcription) | transforme la voix en texte horodaté → pauses, débit, hésitations + le contenu verbal | CPU lent mais gratuit en auto-hébergé; modèle `small/base` suffit au départ |
| **ffmpeg** | relais et conversion des flux (HLS, SRT → images) | **0 $** (open source) + le même VPS |
| **Backend FastAPI** (le nôtre) | file d'attente, rapports, WebSocket temps réel | inclus dans le VPS |

### C. Le seul poste qui coûte vraiment : le gros modèle multimodal (mode Pro)

| Option | Ce qu'elle fait | Coût |
|---|---|---|
| **API de grand modèle** (par appel) | le « juge » de la méthode gagnante SVC 2026 : il reçoit les descripteurs convertis en langage + des images clés et raisonne dessus | **à l'usage** (~quelques cents par minute de vidéo selon le fournisseur) — 0 $ fixe, on ne paie que ce qui est analysé |
| **Modèle ouvert 7B fine-tuné** (type DeceptionX) auto-hébergé | même rôle, chez nous | GPU loué **à l'heure seulement quand ça roule** (~0,50–1,50 $/h de GPU grand public) ou serveur GPU ~100–300 $/mois si le volume le justifie |
| **Fine-tuning initial** (LoRA sur DOLOS etc.) | adapte le modèle ouvert à notre tâche | **ponctuel** : quelques heures de GPU loué = **dizaines de dollars**, pas des milliers |

👉 On ne construit **jamais** un modèle de zéro (ça, ce sont les
milliards). On prend des modèles ouverts déjà entraînés, on les
**branche** et on les **ajuste** (fine-tuning léger). C'est toute la
différence entre un projet à 200 $/mois et un projet à 2 M$.

### D. Celles qu'on EXCLUT (cher, matériel, ou invalide)

| Technologie | Pourquoi dehors |
|---|---|
| Caméra thermique / infrarouge | matériel spécialisé par poste, impossible sur les vidéos du public |
| EEG / casques | matériel + protocole de labo, pas de vidéo |
| IRMf | une machine de plusieurs M$ — et exclue des tribunaux |
| Analyse de stress vocal (CVSA) | validée au niveau du hasard — on ne paie pas pour du bruit |
| Polygraphe | capteurs sur le corps, pas une technologie vidéo |

## Le budget de démarrage, blanc noir

| Poste | Coût |
|---|---|
| Produit gratuit (extension + site, analyse locale) | **0 $/mois** d'infrastructure |
| Hébergement site + backend CPU (uploads, relais HLS/SRT) | ~15–30 $/mois |
| Mode Pro — juge multimodal | à l'usage (API) ou GPU à l'heure; **aucun coût fixe** au départ |
| Fine-tuning initial + évaluations | ~50–150 $ **une fois** (GPU loué) |
| Datasets de calibration | 0 $ en recherche (licences académiques à respecter; DOLOS = non commercial — la version commerciale exige notre propre dataset consenti, voir le plan d'affaires) |
| **Total pour lancer et opérer le MVP** | **de l'ordre de 20–50 $/mois** |

La structure de coûts épouse la monétisation : le gratuit coûte ~0 $
parce qu'il roule chez l'utilisateur; le payant (temps réel hébergé,
juge multimodal) est exactement ce qui coûte — et il est facturé à
l'usage ou en abonnement Pro.
