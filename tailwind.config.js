/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{njk,md,html}"],
  theme: {
    extend: {
      colors: {
        navy: {
          950: "#050b18",
          900: "#0a1730",
          800: "#0f2247",
          700: "#153161",
        },
        techblue: {
          500: "#2f7dfa",
          400: "#5b9bff",
          300: "#8ec0ff",
          50: "#eff6ff",
        },
      },
      fontFamily: {
        sans: [
          "Pretendard Variable",
          "Pretendard",
          "-apple-system",
          "BlinkMacSystemFont",
          "system-ui",
          "Roboto",
          '"Noto Sans KR"',
          "sans-serif",
        ],
      },
    },
  },
  plugins: [require("@tailwindcss/typography"), require("@tailwindcss/forms")],
};
