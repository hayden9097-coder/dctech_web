module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy({ public: "/" });
  eleventyConfig.addPassthroughCopy("admin");

  eleventyConfig.addFilter("json", function (value) {
    return JSON.stringify(value);
  });

  eleventyConfig.addCollection("cases", function (collectionApi) {
    return collectionApi.getFilteredByGlob("src/cases/*.md").sort((a, b) => {
      return (a.data.order || 0) - (b.data.order || 0);
    });
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
