const GulpClient = require('gulp')
const { series, src, dest } = require('gulp')
const sass = require('gulp-sass')(require('sass'))

function bootstrap() {
    const files = [
        'node_modules/bootstrap/dist/css/bootstrap.min.css',
        'node_modules/bootstrap/dist/js/bootstrap.min.js'
    ];

    return src(files).pipe(dest('_vendor'));
}

function style() {
    const files = [
        'static/*.scss'
    ];

    return GulpClient.src(files)
        .pipe(sass().on('error', sass.logError))
        .pipe(GulpClient.dest('_vendor'));
}

exports.default = series(bootstrap, style)