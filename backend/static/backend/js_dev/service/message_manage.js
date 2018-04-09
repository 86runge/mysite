define([], function () {
  var fn = function () {
    // 添加消息
    $("#add_message").on('click', function () {
      $('#message_manage_modal').find('.modal-title').text('添加消息');
      $("#submit_add_message").show();
      $("#submit_update_message").hide();
      $('#message_manage_modal').modal({backdrop: 'static', keyboard: false});
    });

    // 提交添加消息
    $("#submit_add_message").on('click', function () {
      message_form_validate('add_message', '');
      $("#form_message_manage").submit();
    });

    // 修改消息
    $(".J_update_message").on('click', function () {
      var this_id = $(this).parents('tr').attr('data-id');
      $("#update_id").val(this_id);
      $.ajax({
        url: '/backend/message_manage/',
        type: 'post',
        data: {
          'id': this_id,
          'action': 'get_message',
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        // contentType: false,
        // processData: false,
        success: function (data) {
          $("#id_msg_group").val(data.msg_group);
          $("#id_msg_title").val(data.msg_title);
          $("#id_msg_note").val(data.msg_note);
          $("#id_msg_start").val(data.msg_start);
          $("#id_msg_end").val(data.msg_end);
          $("#submit_add_message").hide();
          $("#submit_update_message").show();
          $('#message_manage_modal').find('.modal-title').text('修改消息');
          $('#message_manage_modal').modal({backdrop: 'static', keyboard: false});
        },
        error: function (data) {
          console.log("发生错误");
          console.log(data);
        }
      })
    });

    // 提交修改消息
    $("#submit_update_message").on('click', function () {
      var this_id = $("#update_id").val();
      message_form_validate('update_message', this_id);
      $("#form_message_manage").submit();
    });

    // 消息表单验证
    var message_form_validate = function (action, id) {
      $("#form_message_manage").validate({
        rules: {
          msg_group: {
            "required": true
          },
          msg_title: {
            "required": true
          },
          msg_note: {
            "required": true
          }
        },
        messages: {
          msg_group: {
            "required": '请选择消息分组'
          },
          msg_title: {
            "required": '请输入消息标题'
          },
          msg_note: {
            "required": '请输入消息内容'
          }
        },
        submitHandler: function () {
          var form_data = new FormData($("#form_message_manage")[0]);
          form_data.append('action', action);
          form_data.append('id', id);
          form_data.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
          $.ajax({
            url: '/backend/message_manage/',
            type: 'post',
            data: form_data,
            dataType: 'json',
            contentType: false,
            processData: false,
            success: function (data) {
              alert(data.msg);
              $('#message_manage_modal').modal('hide');
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

    // 消息删除
    $(".J_delete_message").on('click', function () {
      var this_id = $(this).parents('tr').attr('data-id');
      $.ajax({
        url: '/backend/message_manage/',
        type: 'post',
        data: {
          'id': this_id,
          'action': 'delete_message',
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        // contentType: false,
        // processData: false,
        success: function (data) {
          alert(data.msg);
          $('#message_manage_modal').modal('hide');
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
