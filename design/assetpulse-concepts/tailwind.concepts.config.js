const base = require("../../tailwind.config.js");
module.exports = { ...base, content: ["./dist/concepts/*.html", "./src/**/*.{njk,md,html}"] };
