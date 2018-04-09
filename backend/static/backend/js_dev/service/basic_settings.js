define(['switch'], function () {
  var fn = function () {
    $.fn.bootstrapSwitch.defaults = {
      state: true,
      size: null,
      animate: true,
      disabled: false,
      readonly: false,
      indeterminate: false,
      inverse: false,
      radioAllOff: false,
      onColor: 'success',
      offColor: 'default',
      onText: '开启中',
      offText: '关闭中',
      labelText: '&nbsp',
      handleWidth: 'auto',
      labelWidth: 'auto',
      baseClass: 'bootstrap-switch',
      wrapperClass: 'wrapper',
      onInit: function onInit() {
      },
      onSwitchChange: function onSwitchChange() {
        // 开启关闭客服
        var this_id = $(this).parents('tr').attr('data-id');
        $.ajax({
          url: '/backend/basic_settings/',
          type: 'post',
          data: {
            'id': this_id,
            'action': 'switch_customer_service',
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
          },
          headers: {
            Accept: "application/json, text/html/, application/xhtml+xml; charset=utf-8"
          },
          success: function (data) {
            console.log("修改成功");
            console.log(data);
          },
          error: function (data) {
            console.log("发生错误");
            console.log(data);
          }
        })
      }
    };
    $(".customer-service-switch").bootstrapSwitch();

    // 添加客服
    $("#add_weixin_img").on('click', function () {
      $("#id_cs_weixin").click();
    });

    $("#customer_service_form").validate({
      rules: {
        cs_phone: {
          "required": true
        },
        cs_qq: {
          "required": true
        },
        weixin_img: {
          "required": true
        },
        service_time: {
          "required": true
        }
      },
      messages: {
        cs_phone: {
          "required": "请输入客服电话"
        },
        cs_qq: {
          "required": "请输入客服QQ"
        },
        weixin_img: {
          "required": "请上传微信二维码图片"
        },
        service_time: {
          "required": "请选择服务时间段"
        }
      },
      submitHandler: function () {
        var form_data = new FormData($("#customer_service_form")[0]);
        form_data.append('cs_weixin', $("#id_cs_weixin").val());
        form_data.append('action', 'add_customer_service');
        $.ajax({
          url: '/backend/basic_settings/',
          type: 'post',
          dataType: 'json',
          data: form_data,
          processData: false,  //必须false才会避开jQuery对 formdata 的默认处理
          contentType: false,  //必须false才会自动加上正确的Content-Type
          success: function () {
            console.log("添加成功");
          },
          error: function (error) {
            console.log(error);

          }
        })
      }
    });

    // 删除客服信息
    $(".delete-customer-service").on('click', function () {
      var this_id = $(this).parents('tr').attr('data-id');
      $.ajax({
        url: '/backend/basic_settings/',
        type: 'post',
        data: {
          'id': this_id,
          'action': 'delete_customer_service',
          csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
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
    });


  };
  return {
    init: fn
  };
});
