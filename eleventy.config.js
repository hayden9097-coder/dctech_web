module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy({ public: "/" });
  eleventyConfig.addPassthroughCopy("admin");

  eleventyConfig.addFilter("json", function (value) {
    return JSON.stringify(value);
  });

  // 목록에서 앞의 n개만 가져오기
  eleventyConfig.addFilter("limit", function (arr, n) {
    if (!Array.isArray(arr)) return [];
    return arr.slice(0, n);
  });

  // 2026-07-31 -> 2026.07.31
  eleventyConfig.addFilter("date", function (value) {
    if (!value) return "";
    const d = value instanceof Date ? value : new Date(value);
    if (isNaN(d)) return value;
    const pad = (n) => String(n).padStart(2, "0");
    return `${d.getFullYear()}.${pad(d.getMonth() + 1)}.${pad(d.getDate())}`;
  });

  eleventyConfig.addCollection("cases", function (collectionApi) {
    return collectionApi
      .getFilteredByGlob("src/cases/*.md")
      .sort((a, b) => (a.data.order || 0) - (b.data.order || 0));
  });

  eleventyConfig.addCollection("products", function (collectionApi) {
    return collectionApi
      .getFilteredByGlob("src/products/*.md")
      .sort((a, b) => (a.data.order || 0) - (b.data.order || 0));
  });

  // 최신 소식이 위로 오도록 날짜 내림차순
  eleventyConfig.addCollection("news", function (collectionApi) {
    return collectionApi
      .getFilteredByGlob("src/news/*.md")
      .sort((a, b) => new Date(b.data.date) - new Date(a.data.date));
  });

  return {
    dir: {
      input: "src",
      includes: "_includes",
      data: "_data",
      output: "dist",
    },
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
  };
};
