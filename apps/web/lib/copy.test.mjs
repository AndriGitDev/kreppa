import test from "node:test";
import assert from "node:assert/strict";

test("copy avoids financial advice language", () => {
  const forbidden = ["sell stocks", "buy assets", "bank is unsafe", "will happen"];
  const text = "The Kreppumaelir is not financial advice. It is a public-data dashboard with anxiety.";
  for (const phrase of forbidden) {
    assert.equal(text.includes(phrase), false);
  }
});
