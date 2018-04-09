define([], function () {
  var fn = function () {
    $("#add_staff").on('click', function () {
      $('#staff_manage_modal').find('.modal-title').text('添加用户');
      $("#submit_add_staff").show();
      $("#submit_update_staff").hide();
      $('#staff_manage_modal').modal({backdrop: 'static', keyboard: false});
    });

    $("#submit_add_staff").on('click', function () {
      form_validate('add_staff', '');
      $("#form_staff_manage").submit();
    });

    $(".J_update_staff").on('click', function () {
      var this_id = $(this).parents('tr').attr('data-id');
      $("#update_id").val(this_id);
      $.ajax({
        url: '/backend/staff_manage/',
        type: 'post',
        data: {
          'id': this_id,
          'action': 'get_staff',
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        // contentType: false,
        // processData: false,
        success: function (data) {
          // console.log(data);
          $("#id_nick").val(data.nick);
          $("#id_username").val(data.username);
          $("#id_password").attr('placeholder', '需要修改密码请输入新密码');
          $("#id_phone").val(data.phone);
          $("#id_department").val(data.department);
          $("#id_role").val(data.role);
          $("#id_superior").val(data.superior);
          $("#id_email").val(data.email);
          if (data.is_active) {
            $("#is_active_yes").prop('checked', true);
          } else {
            $("#is_active_no").prop('checked', true);
          }
          $("#submit_add_staff").hide();
          $("#submit_update_staff").show();
          $('#staff_manage_modal').find('.modal-title').text('修改用户');
          $('#staff_manage_modal').modal({backdrop: 'static', keyboard: false});
        },
        error: function (data) {
          console.log("发生错误");
          console.log(data);
        }
      })
    });

    // 提交修改
    $("#submit_update_staff").on('click', function () {
      var staff_id = $("#update_id").val();
      form_validate('update_staff', staff_id);
      $("#form_staff_manage").submit();
    });

    var form_validate = function (action, id) {
      var pwd_validate = true;
      if (id) {
        pwd_validate = false;
      }
      $("#form_staff_manage").validate({
        rules: {
          nick: {
            "required": true
          },
          username: {
            "required": true,
            "isUsername": true
          },
          password: {
            "required": pwd_validate,
            "isPassword": true
          },
          phone: {
            "required": true,
            "isMobile": true
          },
          email: {
            "isEmail": true
          },
          department: {
            "required": true
          },
          role: {
            "required": true
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
          },
          department: {
            "required": "请输入所属部门"
          },
          role: {
            "required": "请输入所属角色"
          }
        },
        submitHandler: function () {
          var form_data = new FormData($("#form_staff_manage")[0]);
          form_data.append('action', action);
          form_data.append('id', id);
          form_data.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
          console.log(form_data);
          $.ajax({
            url: '/backend/staff_manage/',
            type: 'post',
            data: form_data,
            dataType: 'json',
            contentType: false,
            processData: false,
            success: function (data) {
              alert("操作成功");
              $('#staff_manage_modal').modal('hide');
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

  };
  return {
    init: fn
  };
});
