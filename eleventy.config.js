module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy({ public: "/" });
  eleventyConfig.addPassthroughCopy("admin");

  eleventyConfig.addFilter("json", function (value) {
    return JSON.stringify(value);
  });

  // 제품 "주요 특징" 목록을 카드용 {title, detail} 로 정리한다(데이터 구조는 바꾸지 않는다).
  //  - 괄호가 닫히지 않은 항목은 다음 항목과 합친다(편집 중 쉼표/줄바꿈으로 갈라진 경우).
  //  - " — ", " – ", ": " 구분자가 있으면 앞은 제목, 뒤는 설명으로 나눈다. 없으면 문장 전체를 제목으로 쓴다.
  eleventyConfig.addFilter("featureItems", function (list) {
    if (!Array.isArray(list)) return [];
    const merged = [];
    for (let i = 0; i < list.length; i++) {
      let s = String(list[i] == null ? "" : list[i]).trim();
      const open = (x) => (x.match(/[(（]/g) || []).length - (x.match(/[)）]/g) || []).length;
      while (open(s) > 0 && i + 1 < list.length) {
        i += 1;
        s += ", " + String(list[i]).trim();
      }
      if (s) merged.push(s);
    }
    return merged.map((s) => {
      const m = s.match(/^(.{2,40}?)(?:\s[—–-]\s|:\s)(.+)$/);
      return m ? { title: m[1].trim(), detail: m[2].trim() } : { title: s, detail: "" };
    });
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
