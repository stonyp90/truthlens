/**
 * TruthLens — porte qualité et adaptation de flux.
 *
 * Règle d'Anthony (5 nov. 2026) : on ne dit pas de menteries. Si les pixels
 * ne sont pas là, on ne peut pas savoir — l'engine DOIT refuser ou dégrader
 * honnêtement plutôt que d'inventer un score. Chaque signal déclare donc
 * ses exigences minimales (largeur du visage en pixels, fps, netteté…),
 * et seuls les signaux dont les exigences sont satisfaites sont activés.
 *
 * Deuxième règle : le flux de l'utilisateur doit être compatible avec
 * l'engine, ou l'engine s'adapte à son flux (voir adaptStream).
 */

// Exigences minimales par signal — valeurs de départ, à recalibrer en phase 2.
export const SIGNAL_REQUIREMENTS = {
  headMovement: { faceWidthPx: 60, fps: 10, label: "Mouvements de tête" },
  repetitiveMovement: { faceWidthPx: 60, fps: 15, label: "Tics / mouvements répétitifs" },
  freeze: { faceWidthPx: 40, fps: 10, label: "Figement" },
  blinkDeviation: { faceWidthPx: 90, fps: 15, label: "Clignements (EAR)" },
  facialTension: { faceWidthPx: 110, fps: 15, label: "Tension faciale (blendshapes / AU)" },
  gazeAversion: { faceWidthPx: 140, fps: 15, label: "Regard / iris" },
  pupil: { faceWidthPx: 220, fps: 15, label: "Dilatation pupillaire" },
  sweatSpecular: { faceWidthPx: 160, fps: 10, label: "Sueur — brillance spéculaire (front, nez, lèvre sup.)" },
  skinColor: { faceWidthPx: 120, fps: 20, label: "Rougeur / pâleur (chrominance peau)" },
  rppg: { faceWidthPx: 120, fps: 20, label: "Fréquence cardiaque à distance (rPPG)" },
  swallowing: { faceWidthPx: 130, fps: 15, label: "Déglutition (pomme d'Adam / cou)" },
  microExpression: { faceWidthPx: 200, fps: 60, label: "Micro-expressions" },
};

/**
 * Évalue la qualité d'une source et active/désactive les signaux en conséquence.
 * input: { faceWidthPx, fps, sharpness (0..1), luminance (0..255), isColor }
 * Retourne le palier, les signaux actifs, ceux refusés AVEC la raison,
 * et un verdict : si le palier est "insufficient", l'engine ne produit
 * AUCUN indice ("on ne peut pas savoir avec cette qualité").
 */
export function assessQuality(input) {
  const face = input.faceWidthPx ?? 0;
  const fps = input.fps ?? 0;
  const sharpness = input.sharpness ?? 1;
  const luminance = input.luminance ?? 128;
  const isColor = input.isColor ?? true;

  const enabled = [];
  const disabled = [];
  for (const [key, req] of Object.entries(SIGNAL_REQUIREMENTS)) {
    const reasons = [];
    if (face < req.faceWidthPx) reasons.push(`visage ${face}px < ${req.faceWidthPx}px requis`);
    if (fps < req.fps) reasons.push(`${fps} ips < ${req.fps} ips requises`);
    if ((key === "sweatSpecular" || key === "skinColor" || key === "rppg") && !isColor)
      reasons.push("vidéo couleur requise");
    if ((key === "sweatSpecular" || key === "skinColor") && (luminance < 40 || luminance > 225))
      reasons.push("éclairage hors plage (sous/surexposé)");
    if ((key === "gazeAversion" || key === "pupil") && sharpness < 0.4)
      reasons.push("image trop floue");
    (reasons.length ? disabled : enabled).push(
      reasons.length ? { signal: key, label: req.label, reasons } : { signal: key, label: req.label },
    );
  }

  let tier = "insufficient";
  if (face >= 200 && fps >= 30) tier = "excellent";
  else if (face >= 130 && fps >= 20) tier = "good";
  else if (face >= 80 && fps >= 15) tier = "basic";

  return {
    tier,
    canScore: tier !== "insufficient",
    verdict:
      tier === "insufficient"
        ? "Qualité insuffisante : on ne peut pas savoir. Augmente la résolution, rapproche le visage ou améliore l'éclairage."
        : null,
    enabledSignals: enabled,
    disabledSignals: disabled,
    input: { faceWidthPx: face, fps, sharpness, luminance, isColor },
  };
}

/**
 * Compatibilité de flux : l'engine s'adapte au flux de l'utilisateur.
 * kind : "mp4" | "webcam" | "webrtc" | "hls" | "srt" | "youtube" | "rtmp"
 * Retourne le plan d'ingestion et les adaptations appliquées.
 */
export function adaptStream(profile) {
  const kind = (profile.kind || "").toLowerCase();
  const plan = { kind, ingest: null, adaptations: [], notes: [] };

  switch (kind) {
    case "mp4":
    case "webm":
      plan.ingest = "browser-native";
      plan.notes.push("Fichier lu par le navigateur : analyse locale directe.");
      break;
    case "webcam":
    case "webrtc":
      plan.ingest = "browser-native";
      plan.notes.push("Flux vivant du navigateur : MediaPipe en temps réel.");
      break;
    case "hls":
      plan.ingest = "browser-or-server";
      plan.notes.push(
        "HLS : lu par le navigateur si le lecteur le décode (MSE/natif); sinon relais serveur ffmpeg → frames.",
      );
      break;
    case "youtube":
    case "vimeo":
      plan.ingest = "browser-overlay";
      plan.notes.push(
        "Plateforme : calque sur le <video> de la page; si les pixels sont protégés (CORS), mode métadonnées + ingestion serveur par URL.",
      );
      break;
    case "srt":
    case "rtmp":
      plan.ingest = "server-relay";
      plan.adaptations.push("ffmpeg : ingestion du flux, extraction à 2-10 ips, échelle adaptée au visage détecté");
      plan.notes.push(
        "Le SRT/RTMP n'est pas lisible par un navigateur : relais serveur obligatoire avant analyse (mode Pro).",
      );
      break;
    default:
      plan.ingest = "unknown";
      plan.notes.push("Type de flux non reconnu : fournir un fichier MP4/WebM, une URL HLS ou un flux SRT.");
  }

  if ((profile.fps ?? 30) > 30) plan.adaptations.push("Sous-échantillonnage à 30 ips pour les signaux lents; micro-expressions gardées à pleine cadence si fps ≥ 60.");
  if ((profile.width ?? 1920) < 640) plan.adaptations.push("Résolution faible : signaux fins désactivés par la porte qualité (voir assessQuality).");
  return plan;
}
