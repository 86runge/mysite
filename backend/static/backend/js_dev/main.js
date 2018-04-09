// main.js

// 使用require.config()方法，我们可以对模块的加载行为进行自定义。
// require.config()就写在主模块（main.js）的头部。参数就是一个对象，
// 这个对象的paths属性指定各个模块的加载路径。

require.config({
  map: {
    '*': {
      'css': '/static/common/plugins/require/css.min.js'
    }
  },
  paths: {
    "jquery": "/static/common/plugins/jquery/jquery.min",
    "bootstrap": "/static/common/plugins/bootstrap/js/bootstrap.min",
    "switch": "/static/common/plugins/bootstrap-switch/js/bootstrap-switch.min",
    "validation": "/static/common/plugins/jquery-validation/jquery.validate.min",
    "daterangepicker": "/static/common/plugins/daterangepicker/jquery.daterangepicker",
    "datetimepicker": "/static/common/plugins/datetimepicker/jquery.datetimepicker.min",
    "common": "/static/common/js/common"
  },
  shim: {
    "bootstrap": {
      deps: ['jquery']
    },
    "common": {
      deps: ['jquery', 'validation']
    },
    "switch": {
      deps: ['css!/static/common/plugins/bootstrap-switch/css/bootstrap-switch.min.css']
    },
    "daterangepicker": {
      deps: ['/static/common/plugins/daterangepicker/moment.min.js', '/static/common/plugins/jquery-ui/jquery-ui.min.js', 'css!/static/common/plugins/jquery-ui/jquery-ui.min.css', 'css!/static/common/plugins/daterangepicker/jquery.daterangepicker.css']
    },
    "datetimepicker": {
      deps: ['/static/common/plugins/jquery-ui/jquery-ui.min.js', 'css!/static/common/plugins/jquery-ui/jquery-ui.min.css', 'css!/static/common/plugins/datetimepicker/jquery.datetimepicker.css']
    }
  },
  urlArgs: "v=" + (new Date()).getTime()
});

// 另一种则是直接改变基目录（baseUrl）。

// require.config({
//     baseUrl: "../common",
//     paths: {
//         "jquery": "jquery.min",
//         "kindeeditor": "kindeditor",
//         "system": "system",
//     },
//     // 这个对象除了有前面说过的paths属性之外，还有一个shim属性，专门用来配置不兼容的模块。
//     // 具体来说，每个模块要定义（1）exports值（输出的变量名），表明这个模块外部调用时的名称；
//     // （2）deps数组，表明该模块的依赖性。
//     shim: {
//         kindeeditor: {
//             deps: ['jquery'],
//             exports: 'kindeeditor'
//         },
//         system: {
//             deps: ['jquery'],
//             exports: 'system'
//         }
//     }
// });

// 如果某个模块在另一台主机上，也可以直接指定它的网址，比如：

// require.config({
//   paths: {
//     "jquery": "https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min"
//   }
// });


// 按需加载模块
require(['require', 'jquery', 'bootstrap', 'common'], function (require, $, bootstrap, common) {
  // 载入jquery,bootstrap等公共组件

  var current_model = $('body').attr('id');
  if (current_model) {
    require(['./service/' + current_model + '.min'], function (X) {
      X.init();
    });
  }

});
