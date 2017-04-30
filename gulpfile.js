module.paths.push('/usr/local/lib/node_modules');
var gulp = require('gulp'),
    htmlmin = require('gulp-htmlmin'),
    options = {
        collapseWhitespace: true,
        collapseBooleanAttributes: true,
        removeComments: true,
        removeEmptyAttributes: true,
        removeScriptTypeAttributes: true,
        removeStyleLinkTypeAttributes: true,
        minifyJS: true,
        minifyCSS: true
    };
gulp.task('html', function () {
    gulp.src('index.js')
        .pipe(htmlmin(options))
        .pipe(gulp.dest('html'));
    gulp.src('index.html')
        .pipe(htmlmin(options))
        .pipe(gulp.dest('html'));
    gulp.src('2048.html')
        .pipe(htmlmin(options))
        .pipe(gulp.dest('html'));
    gulp.src('clan.html')
        .pipe(htmlmin(options))
        .pipe(gulp.dest('html'));
});