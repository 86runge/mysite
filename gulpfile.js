var gulp = require('gulp'),
    less = require('gulp-less'),
    autoprefixer = require('gulp-autoprefixer'),
    cleanmin = require('gulp-clean-css'),
    concat = require('gulp-concat'),
    uglify = require('gulp-uglify'),
    del = require('del'),
    rename = require('gulp-rename');

var url_eshop = 'eshop/static/eshop/';
var url_backend = 'backend/static/backend/';
var url_common = 'common/static/common/';

var css_option = {
    advanced: false,//类型：Boolean 默认：true [是否开启高级优化（合并选择器等）]
    compatibility: 'ie7',//保留ie7及以下兼容写法 类型：String 默认：''or'*' [启用兼容模式； 'ie7'：IE7兼容模式，'ie8'：IE8兼容模式，'*'：IE9+兼容模式]
    keepBreaks: true,//类型：Boolean 默认：false [是否保留换行]
    keepSpecialComments: '*'
    //保留所有特殊前缀 当你用autoprefixer生成的浏览器前缀，如果不加这个参数，有可能将会删除你的部分前缀
};

var js_option = {
    mangle: true, //排除混淆关键字
    compress: true //类型：Boolean 默认：true 是否完全压缩
};

// less预编译
gulp.task('less', function () {
    gulp.src([url_common + 'css/*.css', url_eshop + 'less/*.less'])
        .pipe(less())
        .pipe(autoprefixer())
        .pipe(cleanmin(css_option))
        .pipe(concat('main.css'))
        .pipe(rename(function (path) {
            path.basename += '.min';
        }))
        .pipe(gulp.dest(url_eshop + 'css'));
    gulp.src([url_common + 'css/*.css', url_backend + 'less/*.less'])
        .pipe(less())
        .pipe(autoprefixer())
        .pipe(cleanmin(css_option))
        .pipe(concat('main.css'))
        .pipe(rename(function (path) {
            path.basename += '.min';
        }))
        .pipe(gulp.dest(url_backend + 'css'));
});

// js文件, js压缩
gulp.task('js', function () {
    gulp.src([url_eshop + 'js/*.js'])
        .pipe(uglify(js_option))
        .pipe(rename(function (path) {
            path.basename += '.min';
        }))
        .pipe(gulp.dest(url_eshop + 'js_dev'));
    gulp.src([url_backend + 'js/*.js'])
        .pipe(uglify(js_option))
        .pipe(rename(function (path) {
            path.basename += '.min';
        }))
        .pipe(gulp.dest(url_backend + 'js_dev'));
});


// 第三方库文件, 直接产出, 不处理
// gulp.task('plugin', function () {
//     gulp.src(url_backend + 'plugin/**')
//         .pipe(gulp.dest(url_backend + 'js'));
// });

gulp.task('watch', function () {
    gulp.watch([url_eshop + 'less/*.less', url_backend + 'less/*.less'], ['less']);
    gulp.watch([url_eshop + 'js/*.js', url_backend + 'js/*.js'], ['js']);
});

// 启动任务
gulp.task('default', ['less', 'js', 'watch']);

// cnpm install gulp gulp-autoprefixer gulp-less gulp-clean-css gulp-concat gulp-uglify gulp-rename del --save-dev
