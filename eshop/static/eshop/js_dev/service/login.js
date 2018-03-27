// login.js

define(['validation'], function () {
  var fn = function () {
    $("#form_login").validate({
      rules: {
        username: {
          "required": true
        },
        password: {
          "required": true
        }
      },
      messages: {
        username: {
          "required": "请输入用户名"
        },
        password: {
          "required": "请输入密码"
        }
      },
      submitHandler: function () {
        $.ajax({
          url: '/eshop/login/',
          type: 'post',
          data: {
            username: $("#id_username").val(),
            password: $("#id_password").val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
          },
          headers: {
            Accept: "application/json, text/html/, application/xhtml+xml; charset=utf-8"
          },
          success: function (data) {
            console.log(data);
            alert(data.msg);
            if (data.status === 0) {
              location.href = 'http://' + location.host;
            }
          },
          error: function (data) {
            alert("发生错误");
            console.log(data);
          }
        })
      }

    });
  };
  return {
    init: fn
  };
});
