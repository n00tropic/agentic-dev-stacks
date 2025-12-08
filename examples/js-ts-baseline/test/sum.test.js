const { test, strictEqual } = require("node:test");
const { sum } = require("../src/sum");

test("sum adds two numbers", () => {
  strictEqual(sum(1, 2), 3);
});
