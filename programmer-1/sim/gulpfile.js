var gulp        = require('gulp');
var browserSync = require('browser-sync').create();
var sass        = require('gulp-sass');

gulp.task('sass', function() {
    return gulp.src(['node_modules/bootstrap/scss/bootstrap.scss', 'src/scss/*.scss'])
        .pipe(sass())
        .pipe(gulp.dest("src/static/css"))
        .pipe(browserSync.stream());
});

gulp.task('js', function() {
    return gulp.src(['node_modules/bootstrap/dist/js/bootstrap.min.js',
                     'node_modules/bootstrap/dist/js/bootstrap.min.js.map',
                     'node_modules/jquery/dist/jquery.min.js',
                     'node_modules/jquery/dist/jquery.min.js.map',
                     'node_modules/popper.js/dist/umd/popper.min.js',
                     'node_modules/popper.js/dist/umd/popper.min.js.map'])
        .pipe(gulp.dest("src/static/js"))
        .pipe(browserSync.stream());
});

gulp.task('dev', ['js', 'sass'], function() {
    browserSync.init({
        notify: false,
	open: false,
        proxy: "127.0.0.1:5000",
        port: 80
    });

    gulp.watch(['src/scss/*.scss'], ['sass']);
    gulp.watch("src/static/js/*").on('change', browserSync.reload);
    gulp.watch("src/static/css/*").on('change', browserSync.reload);
    gulp.watch("src/templates/*").on('change', browserSync.reload);
});
