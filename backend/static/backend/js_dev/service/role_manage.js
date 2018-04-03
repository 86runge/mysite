define([], function () {
  var fn = function () {
    // 添加权限
    $("#add_permission").on('click', function () {
      $('#permission_manage_modal').find('.modal-title').text('添加权限');
      $("#form_permission_manage")[0].reset();
      $("label.error").hide();
      $("#submit_add_permission").show();
      $("#submit_update_permission").hide();
      $('#permission_manage_modal').modal({backdrop: 'static', keyboard: false});
    });

    // 提交添加权限
    $("#submit_add_permission").on('click', function () {
      permission_form_validate('add_permission', '');
      $("#form_permission_manage").submit();
    });

    // 修改权限
    $(".J_update_permission").on('click', function () {
      var this_id = $(this).parents('tr').attr('data-id');
      $("#update_id").val(this_id);
      $.ajax({
        url: '/backend/role_manage/',
        type: 'post',
        data: {
          'id': this_id,
          'action': 'get_permission',
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        // contentType: false,
        // processData: false,
        success: function (data) {
          $("#id_p_name").val(data.name);
          $("#id_content_type").val(data.content_type);
          $("#id_codename").val(data.codename);
          $("#submit_add_permission").hide();
          $("#submit_update_permission").show();
          $('#permission_manage_modal').find('.modal-title').text('修改权限');
          $('#permission_manage_modal').modal({backdrop: 'static', keyboard: false});
        },
        error: function (data) {
          console.log("发生错误");
          console.log(data);
        }
      })
    });

    // 提交修改权限
    $("#submit_update_permission").on('click', function () {
      var this_id = $("#update_id").val();
      permission_form_validate('update_permission', this_id);
      $("#form_permission_manage").submit();
    });

    // 权限表单验证
    var permission_form_validate = function (action, id) {
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
            "required": '请输入权限码'
          }
        },
        submitHandler: function () {
          var form_data = new FormData($("#form_permission_manage")[0]);
          form_data.append('action', action);
          form_data.append('id', id);
          form_data.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
          $.ajax({
            url: '/backend/role_manage/',
            type: 'post',
            data: form_data,
            dataType: 'json',
            contentType: false,
            processData: false,
            success: function (data) {
              alert(data.msg);
              $('#permission_manage_modal').modal('hide');
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

    // 权限删除
    $(".J_delete_permission").on('click', function () {
      var this_id = $(this).parents('tr').attr('data-id');
      $.ajax({
        url: '/backend/role_manage/',
        type: 'post',
        data: {
          'id': this_id,
          'action': 'delete_permission',
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        // contentType: false,
        // processData: false,
        success: function (data) {
          alert(data.msg);
          $('#permission_manage_modal').modal('hide');
          window.location.reload();
        },
        error: function (data) {
          console.log("发生错误");
          console.log(data);
        }
      })
    });

    // 添加用户群
    $("#add_group").on('click', function () {
      $('#group_manage_modal').find('.modal-title').text('添加用户群');
      $("#form_group_manage")[0].reset();
      $("label.error").hide();
      $("#submit_add_group").show();
      $("#submit_update_group").hide();
      $('#group_manage_modal').modal({backdrop: 'static', keyboard: false});
    });

    // 提交添加用户群
    $("#submit_add_group").on('click', function () {
      group_form_validate('add_group', '');
      $("#form_group_manage").submit();
    });

    // 修改用户群
    $(".J_update_group").on('click', function () {
      var this_id = $(this).parents('tr').attr('data-id');
      $("#update_id").val(this_id);
      $.ajax({
        url: '/backend/role_manage/',
        type: 'post',
        data: {
          'id': this_id,
          'action': 'get_group',
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        // contentType: false,
        // processData: false,
        success: function (data) {
          $("#id_g_name").val(data.name);
          $("#id_g_notes").val(data.notes);
          if (data.is_active) {
            $("#g_active_yes").prop('checked', true);
          } else {
            $("#g_active_no").prop('checked', true);
          }
          $("#submit_add_group").hide();
          $("#submit_update_group").show();
          $('#group_manage_modal').find('.modal-title').text('修改用户群');
          $('#group_manage_modal').modal({backdrop: 'static', keyboard: false});
        },
        error: function (data) {
          console.log("发生错误");
          console.log(data);
        }
      })
    });

    // 提交修改用户群
    $("#submit_update_group").on('click', function () {
      var this_id = $("#update_id").val();
      group_form_validate('update_group', this_id);
      $("#form_group_manage").submit();
    });

    // 用户群表单验证
    var group_form_validate = function (action, id) {
      $("#form_group_manage").validate({
        rules: {
          name: {
            "required": true
          },
          permissions: {
            "required": true
          }
        },
        messages: {
          name: {
            "required": '请输入群名称'
          },
          permissions: {
            "required": '请选择群权限'
          }
        },
        submitHandler: function () {
          var form_data = new FormData($("#form_group_manage")[0]);
          form_data.append('action', action);
          form_data.append('id', id);
          form_data.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
          $.ajax({
            url: '/backend/role_manage/',
            type: 'post',
            data: form_data,
            dataType: 'json',
            contentType: false,
            processData: false,
            success: function (data) {
              alert(data.msg);
              $('#group_manage_modal').modal('hide');
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

    // 用户群删除
    $(".J_delete_group").on('click', function () {
      var this_id = $(this).parents('tr').attr('data-id');
      $.ajax({
        url: '/backend/role_manage/',
        type: 'post',
        data: {
          'id': this_id,
          'action': 'delete_group',
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        // contentType: false,
        // processData: false,
        success: function (data) {
          alert(data.msg);
          $('#group_manage_modal').modal('hide');
          window.location.reload();
        },
        error: function (data) {
          console.log("发生错误");
          console.log(data);
        }
      })
    });

    // 添加角色
    $("#add_role").on('click', function () {
      $('#role_manage_modal').find('.modal-title').text('添加角色');
      $("#form_role_manage")[0].reset();
      $("label.error").hide();
      $("#submit_add_role").show();
      $("#submit_update_role").hide();
      $('#role_manage_modal').modal({backdrop: 'static', keyboard: false});
    });

    // 提交添加角色
    $("#submit_add_role").on('click', function () {
      role_form_validate('add_role', '');
      $("#form_role_manage").submit();
    });

    // 修改角色
    $(".J_update_role").on('click', function () {
      var this_id = $(this).parents('tr').attr('data-id');
      $("#update_id").val(this_id);
      $.ajax({
        url: '/backend/role_manage/',
        type: 'post',
        data: {
          'id': this_id,
          'action': 'get_role',
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        // contentType: false,
        // processData: false,
        success: function (data) {
          console.log(data);
          $("#id_r_name").val(data.name);
          // $("#id_groups").val(data.groups);
          if (data.is_active) {
            $("#r_active_yes").prop('checked', true);
          } else {
            $("#r_active_no").prop('checked', true);
          }
          $("#id_r_notes").val(data.notes);
          $("#submit_add_role").hide();
          $("#submit_update_role").show();
          $('#role_manage_modal').find('.modal-title').text('修改角色');
          $('#role_manage_modal').modal({backdrop: 'static', keyboard: false});
        },
        error: function (data) {
          console.log("发生错误");
          console.log(data);
        }
      })
    });

    // 提交修改角色
    $("#submit_update_role").on('click', function () {
      var this_id = $("#update_id").val();
      role_form_validate('update_role', this_id);
      $("#form_role_manage").submit();
    });

    // 角色表单验证
    var role_form_validate = function (action, id) {
      $("#form_role_manage").validate({
        rules: {
          name: {
            "required": true
          },
          groups: {
            "required": true
          }
        },
        messages: {
          name: {
            "required": '请输入角色名'
          },
          groups: {
            "required": '请选择群组'
          }
        },
        submitHandler: function () {
          var form_data = new FormData($("#form_role_manage")[0]);
          form_data.append('action', action);
          form_data.append('id', id);
          form_data.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
          $.ajax({
            url: '/backend/role_manage/',
            type: 'post',
            data: form_data,
            dataType: 'json',
            contentType: false,
            processData: false,
            success: function (data) {
              alert(data.msg);
              $('#role_manage_modal').modal('hide');
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

    // 角色删除
    $(".J_delete_role").on('click', function () {
      var this_id = $(this).parents('tr').attr('data-id');
      $.ajax({
        url: '/backend/role_manage/',
        type: 'post',
        data: {
          'id': this_id,
          'action': 'delete_role',
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        // contentType: false,
        // processData: false,
        success: function (data) {
          alert(data.msg);
          $('#role_manage_modal').modal('hide');
          window.location.reload();
        },
        error: function (data) {
          console.log("发生错误");
          console.log(data);
        }
      })
    });


    // 添加部门
    $("#add_department").on('click', function () {
      $('#department_manage_modal').find('.modal-title').text('添加权限');
      $("#form_department_manage")[0].reset();
      $("label.error").hide();
      $("#submit_add_department").show();
      $("#submit_update_department").hide();
      $('#department_manage_modal').modal({backdrop: 'static', keyboard: false});
    });

    // 提交添加部门
    $("#submit_add_department").on('click', function () {
      form_validate('add_department', '');
      $("#form_department_manage").submit();
    });

    // 修改部门
    $(".J_update_department").on('click', function () {
      var this_id = $(this).parents('tr').attr('data-id');
      $("#update_id").val(this_id);
      $.ajax({
        url: '/backend/role_manage/',
        type: 'post',
        data: {
          'id': this_id,
          'action': 'get_department',
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        // contentType: false,
        // processData: false,
        success: function (data) {
          $("#id_d_name").val(data.name);
          if (data.is_active) {
            $("#d_active_yes").prop('checked', true);
          } else {
            $("#d_active_no").prop('checked', true);
          }
          $("#id_d_notes").val(data.notes);
          $("#submit_add_department").hide();
          $("#submit_update_department").show();
          $('#department_manage_modal').find('.modal-title').text('修改权限');
          $('#department_manage_modal').modal({backdrop: 'static', keyboard: false});
        },
        error: function (data) {
          console.log("发生错误");
          console.log(data);
        }
      })
    });

    // 提交修改部门
    $("#submit_update_department").on('click', function () {
      var this_id = $("#update_id").val();
      form_validate('update_department', this_id);
      $("#form_department_manage").submit();
    });

    // 部门表单验证
    var form_validate = function (action, id) {
      $("#form_department_manage").validate({
        rules: {
          name: {
            "required": true
          }
        },
        messages: {
          name: {
            "required": '请输入部门名称'
          }
        },
        submitHandler: function () {
          var form_data = new FormData($("#form_department_manage")[0]);
          form_data.append('action', action);
          form_data.append('id', id);
          form_data.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
          $.ajax({
            url: '/backend/role_manage/',
            type: 'post',
            data: form_data,
            dataType: 'json',
            contentType: false,
            processData: false,
            success: function (data) {
              alert(data.msg);
              $('#department_manage_modal').modal('hide');
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

    // 部门删除
    $(".J_delete_department").on('click', function () {
      var this_id = $(this).parents('tr').attr('data-id');
      $.ajax({
        url: '/backend/role_manage/',
        type: 'post',
        data: {
          'id': this_id,
          'action': 'delete_department',
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        // contentType: false,
        // processData: false,
        success: function (data) {
          alert(data.msg);
          $('#department_manage_modal').modal('hide');
          window.location.reload();
        },
        error: function (data) {
          console.log("发生错误");
          console.log(data);
        }
      })
    })


  };

  return {
    init: fn
  };
});
