module.paths.push('/usr/local/lib/node_modules');
var gulp = require('gulp');
var htmlmin = require('gulp-htmlmin');
gulp.task('html', function() {
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
    return gulp.src('index.html')
        .pipe(htmlmin(options))
        .pipe(gulp.dest('html'));
});
