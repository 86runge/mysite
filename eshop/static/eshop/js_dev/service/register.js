// register.js

define('register' ,['validation'], function () {

    var fn = function () {

        // 前端验证表单
        $("#form_register").validate({
            rules: {
                username: {
                    "required": true,
                    "isUsername": true
                },
                password: {
                    "required": true,
                    "isPassword": true
                },
                again_password: {
                    "required": true,
                    "equalTo": "#id_password"
                },
                nick: {
                    "required": true,
                    "isNick": true
                },
                phone: {
                    "required": true,
                    "isMobile": true
                },
                email: {
                    "isEmail": true
                },
                verify_code: {
                    "require": true
                }
            },
            messages: {
                username: {
                    "required": "请输入用户名"
                },
                password: {
                    "required": "请输入密码"
                },
                again_password: {
                    "required": "请再次输入密码",
                    "equalTo": "两次输入的密码不一致"
                },
                nick: {
                    "required": "请输入姓名"
                },
                phone: {
                    "required": "请输入电话号码"
                },
                verify_code: {
                    "require": "请输入验证码"
                }
            },
            submitHandler: function (form) {
                console.log(form);
            }
        });

    };
    return {
        init: fn
    };
});
