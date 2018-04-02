define([], function () {
  var fn = function () {
    $("#add_permission").on('click', function () {
      $('#permission_manage_modal').find('.modal-title').text('添加权限');
      $("#form_permission_manage")[0].reset();
      $("label.error").hide();
      $("#submit_add_permission").show();
      $("#submit_update_permission").hide();
      $('#permission_manage_modal').modal({backdrop: 'static', keyboard: false});
    });

    var form_validate = function (action, id) {
      $("#form_permission_manage").validate({
        rules: {
          name: {
            "required": true
          },
          content_type: {
            "required": true
          },
          codename: {
            "required": true
          }
        },
        messages: {
          name: {
            "required": '请输入权限名'
          },
          content_type: {
            "required": '请选择归属类型'
          },
          codename: {
            "required": '权限码'
          }
        },
        submitHandler: function () {
          var form_data = new FormData($("#form_staff_manage")[0]);
          form_data.append('action', action);
          form_data.append('staff_id', id);
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
              // window.location.reload();
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
