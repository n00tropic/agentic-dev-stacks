"use strict";

module.exports = (...args) => {
  const params = args.slice(0, -1);
  return params.join("");
};
