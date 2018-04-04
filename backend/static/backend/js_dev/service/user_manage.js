define([], function () {
  var fn = function () {
    // 修改用户
    $(".J_update_user").on('click', function () {
      var this_id = $(this).parents('tr').attr('data-id');
      $("#update_id").val(this_id);
      $.ajax({
        url: '/backend/user_manage/',
        type: 'post',
        data: {
          'id': this_id,
          'action': 'get_user',
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        // contentType: false,
        // processData: false,
        success: function (data) {
          $("#id_nick").val(data.nick);
          $("#id_username").val(data.username);
          $("#id_password").attr('placeholder', '需要修改密码请输入新密码');
          $("#id_phone").val(data.phone);
          $("#id_email").val(data.email);
          // if (data.is_staff) {
          //   $("#is_staff_yes").prop('checked', true)
          // } else {
          //   $("#is_staff_no").prop('checked', true)
          // }
          if (data.is_active) {
            $("#is_active_yes").prop('checked', true)
          } else {
            $("#is_active_no").prop('checked', true)
          }
          $("#submit_add_user").hide();
          $("#submit_update_user").show();
          $('#user_manage_modal').find('.modal-title').text('修改用户');
          $('#user_manage_modal').modal({backdrop: 'static', keyboard: false});
        },
        error: function (data) {
          console.log("发生错误");
          console.log(data);
        }
      })
    });

    // 提交修改用户
    $("#submit_update_user").on('click', function () {
      var this_id = $("#update_id").val();
      user_form_validate('update_user', this_id);
      $("#form_user_manage").submit();
    });

    // 权限表单验证
    var user_form_validate = function (action, id) {
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
          form_data.append('action', action);
          form_data.append('id', id);
          form_data.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
          $.ajax({
            url: '/backend/user_manage/',
            type: 'post',
            data: form_data,
            dataType: 'json',
            contentType: false,
            processData: false,
            success: function (data) {
              alert(data.msg);
              $('#user_manage_modal').modal('hide');
              window.location.reload();
            },
            error: function (data) {
              console.log("发生错误");
              console.log(data);
            }
          })
        }
      });
    };

    // 用户删除
    $(".J_delete_user").on('click', function () {
      var this_id = $(this).parents('tr').attr('data-id');
      $.ajax({
        url: '/backend/user_manage/',
        type: 'post',
        data: {
          'id': this_id,
          'action': 'delete_user',
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        // contentType: false,
        // processData: false,
        success: function (data) {
          alert(data.msg);
          $('#user_manage_modal').modal('hide');
          window.location.reload();
        },
        error: function (data) {
          console.log("发生错误");
          console.log(data);
        }
      })
    });
  };

  return {
    init: fn
  };
});
