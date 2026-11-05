import assert from "node:assert";
import { blinkDeviationScore, freezeScore, fuseSignals, repetitionScore } from "./scoring.js";

assert.equal(blinkDeviationScore(17), 0);
assert.equal(blinkDeviationScore(34), 1);

const fused = fuseSignals({ headMovement: 1, facialTension: 1 }, { faceVisibleRatio: 1, durationSec: 120 });
assert.ok(fused.index >= 5 && fused.index <= 95, "indice borné 5..95");
assert.ok(fused.disclaimer.includes("pas une preuve"));

const empty = fuseSignals({}, {});
assert.equal(empty.index, null);

assert.ok(repetitionScore([0, 1, 0, 1].flatMap((x) => [x, x, x, x]).concat(Array(32).fill(0).map((_, i) => i % 2))) >= 0);
assert.equal(freezeScore([...Array(30).fill(1), ...Array(10).fill(0)], 10), 1);

console.log("scoring.test.mjs : OK");
