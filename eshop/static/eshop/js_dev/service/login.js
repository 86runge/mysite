// login.js

define(['validation'], function () {
    var fn = function () {
        $("#form_login").validate({
            rules: {
                username: {
                    "required": true
                },
                password: {
                    "required": true
                }
            },
            messages: {
                username: {
                    "required": "请输入用户名"
                },
                password: {
                    "required": "请输入密码"
                }
            },
            submitHandler: function () {
                $.ajax({
                    url: '/eshop/login/',
                    type: 'post',
                    dataType: 'json',
                    data: {
                        username: $("#id_username").val(),
                        password: $("#id_password").val(),
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
                    headers: {
                        Accept: "application/json, text/html/, application/xhtml+xml; charset=utf-8"
                    },
                    success: function () {
                        alert("恭喜你，登录成功！");
                    },
                    error: function () {
                        alert("发生错误");
                    }
                })
            }

        });
    };
    return {
        init: fn
    };
});
