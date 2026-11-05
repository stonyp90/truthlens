import assert from "node:assert";
import { adaptStream, assessQuality } from "./quality.js";

// Trop peu de pixels : l'engine refuse de scorer — "on ne peut pas savoir"
const low = assessQuality({ faceWidthPx: 50, fps: 30 });
assert.equal(low.tier, "insufficient");
assert.equal(low.canScore, false);
assert.ok(low.verdict.includes("on ne peut pas savoir"));

// Bonne source : la plupart des signaux actifs, mais pas les micro-expressions à 30 ips
const good = assessQuality({ faceWidthPx: 180, fps: 30, luminance: 120 });
assert.equal(good.tier, "good");
assert.ok(good.enabledSignals.some((s) => s.signal === "sweatSpecular"));
assert.ok(good.disabledSignals.some((s) => s.signal === "microExpression"));

// Sueur impossible en noir et blanc ou en surexposition
const bw = assessQuality({ faceWidthPx: 300, fps: 30, isColor: false, luminance: 250 });
assert.ok(bw.disabledSignals.some((s) => s.signal === "sweatSpecular"));

// Flux : le SRT exige un relais serveur, le MP4 est natif navigateur
assert.equal(adaptStream({ kind: "srt" }).ingest, "server-relay");
assert.equal(adaptStream({ kind: "mp4" }).ingest, "browser-native");
assert.equal(adaptStream({ kind: "hls" }).ingest, "browser-or-server");

console.log("quality.test.mjs : OK");
