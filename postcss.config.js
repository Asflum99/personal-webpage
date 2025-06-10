const { purgeCSSPlugin } = require("@fullhuman/postcss-purgecss");

module.exports = {
  plugins: [
    purgeCSSPlugin({
      content: ["./templates/**/*.html"],
      dynamicAttributes: ['data-bs-popper']
    }),
  ],
};
