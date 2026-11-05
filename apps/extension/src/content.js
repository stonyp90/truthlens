/**
 * TruthLens — content script (calque temps réel).
 *
 * S'attache à chaque <video> de la page (MP4 direct, HLS/DASH lus par le
 * lecteur du site, YouTube, Vimeo…). Échantillonne la frame courante,
 * calcule le mouvement global et affiche un badge + un panneau avec
 * l'indice de tension en direct.
 *
 * Limite connue et assumée : si la vidéo est cross-origin protégée
 * (canvas "tainted"), le navigateur interdit la lecture des pixels.
 * Dans ce cas on bascule en mode métadonnées (lecture/pause, vitesse)
 * et on l'indique dans le panneau. Le mode serveur (backend /ws/stream)
 * couvre ces cas quand l'utilisateur fournit l'URL du flux.
 */
(() => {
  if (window.__truthlensLoaded) return;
  window.__truthlensLoaded = true;

  const state = new WeakMap();

  function makePanel(video) {
    const wrap = document.createElement("div");
    wrap.className = "truthlens-panel";
    wrap.innerHTML = `
      <div class="tl-head">🔎 TruthLens <span class="tl-live">● LIVE</span></div>
      <div class="tl-score">—</div>
      <div class="tl-label">indice de tension (pas une preuve de mensonge)</div>
      <div class="tl-bar"><div></div></div>
      <div class="tl-note"></div>`;
    const style = document.createElement("style");
    style.textContent = `
      .truthlens-panel{position:absolute;z-index:2147483647;right:10px;top:10px;width:190px;
        background:rgba(10,14,20,.88);color:#e8eef4;border:1px solid #35506b;border-radius:12px;
        padding:10px 12px;font:13px system-ui,sans-serif;pointer-events:none}
      .tl-head{font-weight:700;display:flex;justify-content:space-between}
      .tl-live{color:#fb7185;font-size:11px}
      .tl-score{font-size:38px;font-weight:800;line-height:1.1}
      .tl-label{opacity:.75;font-size:11px}
      .tl-bar{height:8px;background:#223140;border-radius:99px;overflow:hidden;margin:6px 0}
      .tl-bar>div{height:100%;width:0%;background:linear-gradient(90deg,#4cc9f0,#ffb703,#fb7185)}
      .tl-note{font-size:11px;opacity:.8}`;
    document.documentElement.appendChild(style);

    const parent = video.offsetParent || video.parentElement;
    if (parent && getComputedStyle(parent).position === "static") parent.style.position = "relative";
    (parent || document.body).appendChild(wrap);
    return wrap;
  }

  const sample = document.createElement("canvas");
  sample.width = 64; sample.height = 36;
  const sctx = sample.getContext("2d", { willReadFrequently: true });

  function attach(video) {
    if (state.has(video)) return;
    const panel = makePanel(video);
    const st = { prev: null, motions: [], panel, tainted: false };
    state.set(video, st);

    setInterval(() => {
      if (video.paused || video.readyState < 2) return;
      let motion = 0;
      if (!st.tainted) {
        try {
          sctx.drawImage(video, 0, 0, 64, 36);
          const data = sctx.getImageData(0, 0, 64, 36).data;
          if (st.prev) {
            let diff = 0;
            for (let i = 0; i < data.length; i += 16) diff += Math.abs(data[i] - st.prev[i]);
            motion = diff / (64 * 36 / 4) / 255;
          }
          st.prev = data;
        } catch (e) {
          st.tainted = true; // canvas protégé (CORS) : mode métadonnées
          panel.querySelector(".tl-note").textContent =
            "Pixels protégés (CORS) : mode limité. Utilise l'analyse serveur avec l'URL du flux.";
        }
      }
      st.motions.push(motion);
      if (st.motions.length > 120) st.motions.shift();

      // Indice simple et transparent (v0) : niveau + instabilité du mouvement.
      const recent = st.motions.slice(-20);
      const avg = recent.reduce((a, b) => a + b, 0) / recent.length;
      const variance = recent.reduce((a, b) => a + (b - avg) ** 2, 0) / recent.length;
      const raw = Math.min(1, avg * 5 + Math.sqrt(variance) * 3);
      const index = Math.round(5 + raw * 90);
      panel.querySelector(".tl-score").textContent = index;
      panel.querySelector(".tl-bar > div").style.width = index + "%";
    }, 500);
  }

  const scan = () => document.querySelectorAll("video").forEach(attach);
  scan();
  new MutationObserver(scan).observe(document.documentElement, { childList: true, subtree: true });
})();
