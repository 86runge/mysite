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
        }
      },
      messages: {
        cs_phone: {
          "required": "请输入客服电话"
        },
        cs_qq: {
          "required": "请输入客服QQ"
        }
      },
      submitHandler: function () {
        $.ajax({
          url: '/backend/basic_settings/',
          type: 'post',
          dataType: 'json',
          data: {
            cs_phone: $("#id_cs_phone").val(),
            cs_qq: $("#id_cs_qq").val(),
            cs_weixin: $("#id_cs_weixin").val(),
            cs_note: $("#id_cs_note").val(),
            action: 'add_customer_service',
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
          },
          headers: {
            Accept: "application/json, text/html/, application/xhtml+xml; charset=utf-8"
          },
          success: function () {
            console.log("添加成功");
            // alert("登录成功");
          },
          error: function (error) {
            console.log(error);
            // alert("发生错误");
          }
        })
      }
    })
  };
  return {
    init: fn
  };
});
