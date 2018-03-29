define([], function () {
  var fn = function () {
    $("#add_user").on('click', function () {
      $('#user_manage_modal').find('.modal-title').text('添加用户');
      $('#submit_add_user').show();
      $('#submit_update_user').hide();
      $('#user_manage_modal').modal({backdrop: 'static', keyboard: false});
    });

    $("#form_user_manage").validate({
      rules: {
        nick: {
          "required": true
        },
        username: {
          "required": true,
          "isUsername": true
        },
        password: {
          "required": true,
          "isPassword": true
        },
        phone: {
          "required": true,
          "isMobile": true
        },
        email: {
          "isEmail": true
        }
      },
      messages: {
        nick: {
          "required": "请输入员工姓名"
        },
        username: {
          "required": "请输入登录名"
        },
        password: {
          "required": "请输入登录密码"
        },
        phone: {
          "required": "请输入员工电话"
        }
      },
      submitHandler: function () {
        var form_data = new FormData($("#form_user_manage")[0]);
        // form_data.append('action', 'add_customer_service');
        console.log(form_data);
        $.ajax({
          url: '/backend/user_manage/',
          type: 'post',
          data: form_data,
          dataType: 'json',
          headers: {
            Accept: "application/json, text/html/, application/xhtml+xml; charset=utf-8"
          },
          success: function (data) {
            console.log("删除成功");
            console.log(data);
          },
          error: function (data) {
            console.log("发生错误");
            console.log(data);
          }
        })
      }
    });

    $("#submit_user_manage").on('click', function () {
      $("#form_user_manage").submit();
    })

  };
  return {
    init: fn
  };
});
