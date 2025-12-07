"use strict";

const { src, dest, series, parallel, watch } = require("gulp");
const postcss = require("gulp-postcss");
const autoprefixer = require("autoprefixer");
const cssnano = require("cssnano");
const zip = require("gulp-zip");
const { deleteAsync } = require("del");

const paths = {
  styles: "src/css/**/*.css",
  scripts: "src/js/**/*.js",
  layouts: "src/layouts/**/*.hbs",
  partials: "src/partials/**/*.hbs",
  helpers: "src/helpers/**/*.js",
  images: "src/img/**/*",
};

const buildDir = "build/ui-bundle";

function clean() {
  return deleteAsync(["build"]);
}

function styles() {
  return src(paths.styles)
    .pipe(postcss([autoprefixer(), cssnano({ preset: "default" })]))
    .pipe(dest(`${buildDir}/css`));
}

function scripts() {
  return src(paths.scripts).pipe(dest(`${buildDir}/js`));
}

function layouts() {
  return src(paths.layouts).pipe(dest(`${buildDir}/layouts`));
}

function partialsTask() {
  return src(paths.partials).pipe(dest(`${buildDir}/partials`));
}

function helpersTask() {
  return src(paths.helpers).pipe(dest(`${buildDir}/helpers`));
}

function images() {
  return src(paths.images, { allowEmpty: true }).pipe(dest(`${buildDir}/img`));
}

function bundleZip() {
  return src(`${buildDir}/**/*`, { base: buildDir })
    .pipe(zip("ui-bundle.zip"))
    .pipe(dest("build"));
}

const build = series(
  clean,
  parallel(styles, scripts, layouts, partialsTask, helpersTask, images),
  bundleZip,
);

function watchFiles() {
  return watch("src/**/*", build);
}

exports.clean = clean;
exports.styles = styles;
exports.build = build;
exports.bundle = build;
exports.watch = watchFiles;
exports.default = build;
