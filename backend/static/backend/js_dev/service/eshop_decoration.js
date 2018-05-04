define([], function () {
    var fn = function () {
        // 上传文件
        $("#select_upload_file").on('click', function () {
            $("[name=upload_file]").click();
        });

        $("#upload_file").on('click', function () {
            var form_data = new FormData($("#form_upload_file")[0]);
            form_data.append('action', 'upload_file');
            form_data.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
            $.ajax({
                url: '/backend/eshop_decoration/',
                type: 'POST',
                data: form_data,
                dataType: 'json',
                async: false,
                cache: false,
                contentType: false,
                processData: false,
                success: function (data) {
                    console.log(data);
                },
                error: function (data) {
                    console.log(data);
                }
            })
        });

        // 下载文件
        var file_path = $(".wei-img").attr('src').replace('media/', '');
        $("#download_file").attr('href', '/common/file_download/?file_path=' + file_path);

        // 表格导入
        $("#select_import_file").on('click', function () {
            $("[name=excel]").click();
        });

        $(".J_import").on('click', function () {
            var form_data = new FormData($("#import_excel")[0]);
            form_data.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
            $.ajax({
                url: '/backend/excel_import/',
                type: 'post',
                data: form_data,
                dataType: 'json',
                contentType: false,
                processData: false,
                success: function (data) {
                    var tr_list = JSON.parse(data.data);
                    console.log(tr_list);
                    for (var i in tr_list) {
                        var operate = '<div class="btn-group"><a class="dropdown-toggle btn-s1" data-toggle="dropdown">管理<span class="caret"></span></a><ul class="dropdown-menu"><li><a href="javascript:;" class="J_update_user">修改</a></li><li><a href="javascript:;" class="J_delete_user">删除</a></li></ul></div>'
                        $("#import_tbody").append("<tr data-id=" + tr_list[i].id + ">"
                            + "<td>" + tr_list[i].姓名 + "</td>"
                            + "<td>" + tr_list[i].用户名 + "</td>"
                            + "<td>" + tr_list[i].电话 + "</td>"
                            + "<td>" + tr_list[i].电子邮箱 + "</td>"
                            + "<td>" + tr_list[i].是否是员工 + "</td>"
                            + "<td>" + tr_list[i].是否激活 + "</td>"
                            + "<td>" + tr_list[i].添加时间 + "</td>"
                            + "<td>" + operate + "</td>"
                            + "</tr>")
                    }
                },
                error: function (data) {
                    console.log(data)
                }
            })
        });

    };
    return {
        init: fn
    };

});
