# mysite
# Django 项目

##表单提交

    1.action 添加url

    2.ajax 提交

##备注

    1.表单提交数据默认提交 含有name的表单控件的value值

    2.表单上传文件需要给表单添加 enctype="multipart/form-data" 属性，该属性让表单可以上传二进制文件

    3.ajax 提交表单上传数据到后台有以下两种方式
        1).直接在ajax
            data: {
                username: $("#id_username").val(),
                password: $("#id_password").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            }
            此时不能将 contentType 和 processData 属性设置成 false,即设置成默认值即可
        2).利用FormData 创建对象 var form_data = new FormData($("#form_user_manage")[0]);
            form_data.append('action', 'add_user');
            data: form_data
            但此时ajax要设置以下属性：
            contentType: false,
            processData: false,
