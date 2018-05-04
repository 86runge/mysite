# mysite
# Django 项目

##表单提交

    1.action 添加url

    2.ajax 提交

##备注

    1.表单提交数据默认提交 含有name的表单控件的value值

    2.表单上传文件需要给表单添加 enctype="multipart/form-data" 属性，该属性让表单可以上传二进制文件
    特别注意的是，只有当request方法是POST，且发送request的<form>有属性enctype="multipart/form-data"时，request.FILES中包含文件数据，否则request.FILES为空。

    3.ajax 提交表单上传数据到后台有以下两种方式
        contentType 主要设置你发送给服务器的格式，dataType设置你收到服务器数据的格式。在post和get中contentType的默认值都是：application/x-www-form-urlencoded，
        这种格式的特点就是，name/value 成为一组，每组之间用 & 联接，而 name与value 则是使用 = 连接。如： wwwh.baidu.com/q?key=fdsa&lang=zh 这是get ,
        而 post 请求则是使用请求体，参数不在 url 中，在请求体中的参数表现形式也是: key=fdsa&lang=zh的形式。
        键值对这样组织在一般的情况下是没有什么问题的，这里说的一般是，不带嵌套类型JSON，也就是 简单的JSON，但是在一些复杂的情况下就有问题了。
        例如在 ajax 中你要传一个复杂的 json 对像，也就说是对象嵌数组，数组中包括对象， application/x-www-form-urlencoded 这种形式是没有办法将复杂的 JSON 组织成键值对形式,
        你传进去可以发送请求，但是服务端收到数据为空， 因为 ajax 没有办法知道怎样处理这个数据。 http 还可以自定义数据类型，于是就定义一种叫 application/json 的类型。
        这种类型是 text ， 我们 ajax 的复杂JSON数据，用 JSON.stringify序列化后，然后发送，在服务器端接到然后用 JSON.parse 进行还原就行了，这样就能处理复杂的对象了。
        processData: 默认情况下，通过data选项传递进来的数据，如果是一个对象(技术上讲只要不是字符串)，都会处理转化成一个查询字符串，以配合默认内容类型 "application/x-www-form-urlencoded"。
        如果要发送 DOM 树信息或其它不希望转换的信息，请设置为 false。
        1).直接在ajax
            data: {
                username: $("#id_username").val(),
                password: $("#id_password").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            }
        2).利用FormData 创建对象 var form_data = new FormData($("#form_user_manage")[0]);
            form_data.append('action', 'add_user');
            data: form_data
            但此时ajax要设置以下属性：
            contentType: false,
            processData: false,

models:
    生成0001等文件
    python manage.py makemigrations
    根据0001等文件生成表
    python manage.py migrate
    如果没有生成表则执行下面的语句生成sql
    python manage.py sqlmigrate app_name 0001
