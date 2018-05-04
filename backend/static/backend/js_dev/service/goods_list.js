define(['datetimepicker'], function () {
  var fn = function () {

    // $("#id_delivery_time").datetimepicker();
    $("#id_online_time").datetimepicker();
    $("#id_offline_time").datetimepicker();

    // 触发文件上传
    $("#id_photo").on('click', function () {
      $("#id_good_photo").click();
    });

    $("#id_photo").blur(function () {
      $(this).val($("#id_good_photo").val());
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

    $(".J_update_good").on('click', function () {
      var this_id = $(this).parents('tr').attr('data-id');
      $("#update_id").val(this_id);
      $.ajax({
        url: '/backend/goods_list/',
        type: 'post',
        data: {
          'id': this_id,
          'action': 'get_good',
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        // contentType: false,
        // processData: false,
        success: function (data) {
          $("#id_name").val(data.name);
          $("#id_price").val(data.price);
          $("#id_bit").val(data.bit);
          $("#id_photo").attr('placeholder', '需要修改商品主图的点击重新上传');
          $("#id_preorder_limit").val(data.preorder_limit);
          $("#id_freight_pricing_method").val(data.freight_pricing_method);
          $("#id_delivery_time").val(data.delivery_time);
          $("#id_online_time").val(data.online_time);
          $("#id_offline_time").val(data.offline_time);
          $("#id_refund_rate").val(data.refund_rate);
          $("#id_note").val(data.note);
          $("#submit_add_good").hide();
          $("#submit_update_good").show();
          $('#good_manage_modal').find('.modal-title').text('修改用户');
          $('#good_manage_modal').modal({backdrop: 'static', keyboard: false});
        },
        error: function (data) {
          console.log("发生错误");
          console.log(data);
        }
      })
    });

    $("#submit_update_good").on('click', function () {
      var good_id = $("#update_id").val();
      good_form_validate('update_good', good_id);
      $("#form_good_manage").submit();
    });

    var good_form_validate = function (action, id) {
      var photo_require = true;
      if (id) {
        photo_require = false;
      }
      $("#form_good_manage").validate({
        // debug: true,
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
            "required": photo_require
          },
          preorder_limit: {
            "required": true,
            "isNumber": true
          },
          freight_pricing_method: {
            "required": true
          },
          delivery_time: {
            "required": true,
            "isNumber": true
          },
          online_time: {
            "required": true
          },
          offline_time: {
            "required": true
          },
          refund_rate: {
            "required": true
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
          freight_pricing_method: {
            "required": "请输入运费计价方式"
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
    };

    // 员工删除
    $(".J_delete_good").on('click', function () {
      var this_id = $(this).parents('tr').attr('data-id');
      $.ajax({
        url: '/backend/goods_list/',
        type: 'post',
        data: {
          'id': this_id,
          'action': 'delete_good',
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        // contentType: false,
        // processData: false,
        success: function (data) {
          alert(data.msg);
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
