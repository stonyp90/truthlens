/**
 * TruthLens — moteur de fusion de signaux (partagé web + extension).
 *
 * IMPORTANT (honnêteté scientifique) : il n'existe aucun signal, ni aucune
 * combinaison de signaux, qui prouve qu'une personne ment. Ce moteur produit
 * un INDICE DE TENSION / INCONGRUENCE (0-100) à partir de signaux observables
 * (clignements, regard, mouvements de tête, micro-mouvements répétés,
 * tension faciale via blendshapes quand disponibles). L'indice n'est PAS
 * une probabilité de mensonge et ne doit jamais être présenté comme tel
 * dans l'interface. Voir docs/SCIENCE_AND_LIMITS.md.
 */

// Poids initiaux — À RECALIBRER sur datasets étiquetés (DOLOS, Bag-of-Lies…)
// avant tout usage réel. Voir docs/ROADMAP.md (phase validation).
export const WEIGHTS = {
  blinkDeviation: 0.18, // écart du taux de clignement vs baseline du sujet
  gazeAversion: 0.16, // proportion de regards hors axe caméra/interlocuteur
  headMovement: 0.16, // vélocité / instabilité de la tête
  repetitiveMovement: 0.14, // autocorrélation des micro-mouvements (tics, tapotements)
  facialTension: 0.20, // blendshapes : sourcils, mâchoire, lèvres pincées
  freeze: 0.16, // suppressions soudaines de mouvement ("figement")
  pulseInstability: 0.12, // rPPG : pouls à distance instable (backend seulement)
};

/** Applique des poids externes (ex. packages/weights.json servi au web,
 * écrit par la boucle d'auto-amélioration tools/selftune.py). */
export function applyWeights(external) {
  if (!external) return WEIGHTS;
  const w = external.weights || external;
  for (const k of Object.keys(WEIGHTS)) {
    if (Number.isFinite(w[k])) WEIGHTS[k] = w[k];
  }
  return WEIGHTS;
}

const clamp01 = (x) => Math.min(1, Math.max(0, x));

/** Normalise un taux de clignement (clign./min) en écart 0..1 vs baseline. */
export function blinkDeviationScore(blinksPerMin, baselinePerMin = 17) {
  if (!Number.isFinite(blinksPerMin)) return null;
  // Écart relatif : 0 = identique à la baseline, 1 = écart >= 100 %
  return clamp01(Math.abs(blinksPerMin - baselinePerMin) / baselinePerMin);
}

/** Score de répétition : pics d'autocorrélation de la série de mouvement. */
export function repetitionScore(motionSeries) {
  if (!motionSeries || motionSeries.length < 16) return null;
  const mean = motionSeries.reduce((a, b) => a + b, 0) / motionSeries.length;
  const centered = motionSeries.map((v) => v - mean);
  const energy = centered.reduce((a, b) => a + b * b, 0);
  if (energy === 0) return 0;
  let best = 0;
  for (let lag = 2; lag <= Math.floor(motionSeries.length / 2); lag++) {
    let sum = 0;
    for (let i = 0; i + lag < centered.length; i++) sum += centered[i] * centered[i + lag];
    best = Math.max(best, sum / energy);
  }
  return clamp01(best);
}

/** "Figement" : chute brutale de mouvement par rapport à la fenêtre précédente. */
export function freezeScore(motionSeries, window = 10) {
  if (!motionSeries || motionSeries.length < window * 2) return null;
  const recent = motionSeries.slice(-window);
  const before = motionSeries.slice(-window * 2, -window);
  const avg = (a) => a.reduce((x, y) => x + y, 0) / a.length;
  const b = avg(before);
  if (b === 0) return 0;
  return clamp01(1 - avg(recent) / b);
}

/**
 * Fusionne les signaux disponibles en un indice 0..100 + confiance 0..1.
 * Les signaux absents (null) sont ignorés et les poids renormalisés.
 * La confiance dépend de la couverture (visage visible, durée, nb de signaux).
 */
export function fuseSignals(signals, coverage = {}) {
  let weighted = 0;
  let totalWeight = 0;
  const used = {};
  for (const [key, weight] of Object.entries(WEIGHTS)) {
    const v = signals[key];
    if (v === null || v === undefined || !Number.isFinite(v)) continue;
    weighted += weight * clamp01(v);
    totalWeight += weight;
    used[key] = Math.round(clamp01(v) * 100);
  }
  if (totalWeight === 0) return { index: null, confidence: 0, signals: used };

  const raw = weighted / totalWeight; // 0..1
  // Courbe douce : évite les extrêmes non justifiés (jamais 0 ni 100 affichés)
  const index = Math.round(5 + raw * 90);

  const faceRatio = coverage.faceVisibleRatio ?? 0;
  const duration = coverage.durationSec ?? 0;
  const signalCoverage = totalWeight; // part des poids couverts (0..1)
  const confidence = clamp01(
    0.45 * faceRatio + 0.25 * Math.min(1, duration / 60) + 0.3 * signalCoverage,
  );

  return {
    index,
    confidence: Math.round(confidence * 100) / 100,
    signals: used,
    disclaimer:
      "Indice de tension/incongruence observable — pas une preuve de mensonge.",
  };
}
