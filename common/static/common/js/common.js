/*公共js*/

// 常用正则匹配

// 帐号是否合法(字母开头，允许4-20字节，允许字母数字下划线)
var reg_username = /^[a-zA-Z][a-zA-Z0-9_]{3,19}$/;

// 简单密码(长度在6~20之间，只能包含字母、数字和下划线)
var reg_password = /^[a-zA-Z0-9_]{6,20}$/;

// 中文
var reg_cn = /[\u4e00-\u9fa5]/;

// 手机号码
var reg_mobile = /^1(3|4|5|6|7|8)\d{9}$/;

// 电话号码
var reg_phone = /^0(\d{2}-{0, 1}\d{8})|(\d{3}-{0, 1}\d{7})$/ || /^1(3|4|5|6|7|8)\d{9}$/;

// Email地址
var reg_email = /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/ || /^[a-z\d]+(\.[a-z\d]+)*@([\da-z](-[\da-z])?)+(\.{1,2}[a-z]+)+$/;

// URL地址
var reg_url = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;

// jquery-validate 验证方法

// 表单方法验证--用户名
jQuery.validator.addMethod("isUsername", function (value, element) {
    return this.optional(element) || (reg_username.test(value));
}, "用户名必须是字母开头，长度在4~20之间，允许字母数字下划线");

// 表单方法验证--密码
jQuery.validator.addMethod("isPassword", function (value, element) {
    return this.optional(element) || (reg_password.test(value));
}, "密码长度必须在6~20之间，只能包含字母、数字和下划线");

// 表单方法验证--姓名
jQuery.validator.addMethod("isNick", function (value, element) {
    return this.optional(element) || (reg_password.test(value));
}, "姓名只能是中文，长度在2~8之间");

// 表单方法验证--手机号码
jQuery.validator.addMethod("isMobile", function (value, element) {
    return this.optional(element) || (reg_mobile.test(value));
}, "请填写有效电话号码");

// 表单方法验证--email
jQuery.validator.addMethod("isEmail", function (value, element) {
    return this.optional(element) || (reg_email.test(value));
}, "请填写有效电子邮箱");

// 表单方法验证--url
jQuery.validator.addMethod("isUrl", function (value, element) {
    return this.optional(element) || (reg_url.test(value));
}, "请填写有效网络链接");

