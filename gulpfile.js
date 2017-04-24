module.paths.push('/usr/local/lib/node_modules');
var gulp = require('gulp');
var htmlmin = require('gulp-htmlmin');
var options = {
    collapseWhitespace: true,
    collapseBooleanAttributes: true,
    removeComments: true,
    removeEmptyAttributes: true,
    removeScriptTypeAttributes: true,
    removeStyleLinkTypeAttributes: true,
    minifyJS: true,
    minifyCSS: true
};
gulp.task('html', function() {
    return gulp.src('index.html')
        .pipe(htmlmin(options))
        .pipe(gulp.dest('html'));
});
gulp.task('g1', function() {
    return gulp.src('2048.html')
        .pipe(htmlmin(options))
        .pipe(gulp.dest('html'));
});

gulp.task('clan', function() {
    return gulp.src('clan.html')
        .pipe(htmlmin(options))
        .pipe(gulp.dest('html'));
});
