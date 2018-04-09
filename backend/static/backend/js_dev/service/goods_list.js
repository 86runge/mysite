define(['datetimepicker'], function () {
  var fn = function () {

    $("#id_delivery_time").datetimepicker();
    $("#id_online_time").datetimepicker();
    $("#id_offline_time").datetimepicker();

    // 触发文件上传
    $("#id_photo").on('click', function () {
      $("#id_good_photo").click();
    });

    $("#add_good").on('click', function () {
      $(".modal-title").text('添加商品');
      $("#submit_add_good").show();
      $("#submit_update_good").hide();
      $("#good_manage_modal").modal({backdrop: 'static', keyboard: false});
    });

    $("#submit_add_good").on('click', function () {
      good_form_validate('add_good', '');
      $("#form_good_manage").submit();
    });

    var good_form_validate = function (action, id) {
      $("#id_photo").val($("#id_good_photo").val());
      $("#form_good_manage").validate({
        // debug: true,
        ignore: "#id_good_photo",
        rules: {
          name: {
            "required": true
          },
          price: {
            "required": true,
            "isPrice": true
          },
          bit: {
            "required": true
          },
          photo: {
            "required": true
          },
          preorder_limit: {
            "required": true,
            "isNumber": true
          },
          delivery_time: {
            "required": true
          },
          online_time: {
            "required": true
          },
          offline_time: {
            "required": true
          },
          refund_rate: {
            "required": true,
            "isNumber": true
          }
        },
        messages: {
          name: {
            "required": "请输入商品名"
          },
          price: {
            "required": "请输入商品价格"
          },
          bit: {
            "required": "请输入商品货号"
          },
          photo: {
            "required": "请上传商品主图"
          },
          preorder_limit: {
            "required": "预购数量限制"
          },
          delivery_time: {
            "required": "请选择发货时间"
          },
          online_time: {
            "required": "请选择上架时间"
          },
          offline_time: {
            "required": "请选择下架时间"
          },
          refund_rate: {
            "required": "请输入退款比率"
          }
        },
        submitHandler: function () {
          var form_data = new FormData($("#form_good_manage")[0]);
          form_data.append('action', action);
          form_data.append('id', id);
          form_data.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
          $.ajax({
            url: '/backend/goods_list/',
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
      })
    }

  };
  return {
    init: fn
  };
});
