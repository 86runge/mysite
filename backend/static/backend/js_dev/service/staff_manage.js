define([], function () {
  var fn = function () {
    $("#add_staff").on('click', function () {
      $('#staff_manage_modal').find('.modal-title').text('添加用户');
      $("#form_staff_manage")[0].reset();
      $("label.error").hide();
      $('#staff_manage_modal').modal({backdrop: 'static', keyboard: false});
    });

    $(".J_update_staff").on('click', function () {
      var this_id = $(this).parents('tr').attr('data-id');
      $.ajax({
        url: '/backend/staff_manage/',
        type: 'post',
        data: {
          'id': this_id,
          'action': 'get_staff',
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        // dataType: 'json',
        // contentType: false,
        // processData: false,
        success: function (data) {
          console.log(data);
          $('#staff_manage_modal').find('.modal-title').text('修改用户');
          $('#staff_manage_modal').modal({backdrop: 'static', keyboard: false});
        },
        error: function (data) {
          console.log("发生错误");
          console.log(data);
        }
      })

    });

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
        var form_data = new FormData($("#form_staff_manage")[0]);
        form_data.append('action', 'add_staff');
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
            alert("添加成功");
            $('#staff_manage_modal').modal('hide');
            // window.location.reload();
          },
          error: function (data) {
            console.log("发生错误");
            console.log(data);
          }
        })
      }
    });

    $("#submit_staff_manage").on('click', function () {
      $("#form_staff_manage").submit();
    })

  };
  return {
    init: fn
  };
});
