define([], function () {
  var fn = function () {
    // 获取验证码
    $("#get_verify_code").on('click', function () {
      var code = $.get_code();
      alert(code);
      console.log(code);
      $("#get_code").val(code);
      $("#id_verify_code").val('');
    });

    // 前端验证表单
    $("#form_forget_password").validate({
      // debug: true,
      ignore: "#get_code",
      rules: {
        username: {
          "required": true,
          "isUsername": true
        },
        password: {
          "required": true,
          "isPassword": true
        },
        again_password: {
          "required": true,
          "equalTo": "#id_password"
        },
        verify_code: {
          "required": true,
          "equalTo": "#get_code"
        }
      },
      messages: {
        username: {
          "required": "请输入用户名"
        },
        password: {
          "required": "请输入密码"
        },
        again_password: {
          "required": "请再次输入密码",
          "equalTo": "两次输入的密码不一致"
        },
        verify_code: {
          "required": "请输入验证码",
          "equalTo": "验证码输入错误"
        }
      },
      submitHandler: function () {
        $.ajax({
          url: '/eshop/forget_password/',
          type: 'post',
          dataType: 'json',
          data: {
            username: $("#id_username").val(),
            password: $("#id_password").val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
          },
          success: function () {
            alert("恭喜你，新密码修改成功！");
          },
          error: function () {
            alert("发生错误");
          }
        })
      }
    });


  };
  return {
    init: fn
  };
});
