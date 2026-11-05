# Recherche — modèles, datasets et état de l'art

*Section en cours de consolidation à partir de deux recherches sourcées
(modèles open source / Hugging Face, et marché / concurrents / cadre légal).
Les faits ci-dessous sont les points de départ vérifiés du projet.*

## Briques open source retenues pour la v0.2

- **MediaPipe Face Landmarker** (Google, Apache-2.0) : 468 landmarks +
  iris, blendshapes type ARKit — roule en WASM dans le navigateur et
  via le SDK Python côté serveur. C'est la brique « rétine/regard/
  clignements/tension » principale.
- **OpenCV** (BSD) : pipeline serveur v0 (mouvement, présence visage).
- **Whisper** (OpenAI, MIT) : transcription + alignement pour la
  prosodie (phase 3, signal voix secondaire).

## Datasets avec vérité-terrain (à licencier/vérifier un par un)

- **DOLOS** : clips d'un jeu télévisé de tromperie, étiquetés
  vérité/mensonge, avec audio et vidéo — benchmark de référence des
  papiers récents (précisions publiées ~60–75 % selon protocole).
- **Bag-of-Lies** : enregistrements contrôlés vérité/mensonge
  (vidéo, audio, EEG dans la version complète).
- **MU3D** : base de tromperie multi-démographique (utile biais/équité).
- **Real-Life Deception Detection** (Univ. of Michigan) : vidéos de
  procès réels étiquetées par l'issue du dossier.

## Ce que la littérature établit

- Pas de signal unique du mensonge; les méta-analyses trouvent des
  indices faibles et inconsistants d'un signal à l'autre.
- Les systèmes multimodaux (visage + voix + texte) font mieux que
  chaque modalité seule, en laboratoire, sur protocoles contrôlés.
- Le polygraphe : précision insuffisante pour le dépistage (National
  Research Council, 2003); position APA : pas de détecteur fiable.

*(Inventaire détaillé des modèles Hugging Face — noms, licences,
popularité — et analyse concurrents/marché : ajoutés dès le retour des
recherches en cours, avec sources.)*
