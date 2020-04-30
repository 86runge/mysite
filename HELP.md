## WXP开发帮助文档

---
### 环境搭建
##### 开发环境
###### Step1
项目环境为 **python3.6.3** ，当系统环境为 **python2.x** 时，建议将python3安装目录里的快捷方式 **python.exe** 重命名为 **python3.exe**。
###### Step2
在pycharm中创建单独的虚拟开发环境 site_env，python解释器要选python3.6.3，pycharm默认会安装好pip。
###### Step3
在 wxp_env 文件夹下打开Git Bash命令行，利用git clone命令下载 site 项目代码到本地。在pycharm中打开wxp项目，将当前项目开发环境设置为Step2中新建的 site_env。
###### Step4
在pycharm中打开Terminal命令行，确认是在 site_env环境下，然后执行  
`pip install -r requirements.txt`
###### Step5
在cmd或者bash中开启memcache，执行  
`memcached -p 11211 -vvv`

##### 生产环境部署
在 wxp_env环境下，执行  
`python manage.py makemigrations`  
`python manage.py collectstatic`


### 目录结构
**示例：**

    site                                   项目根目录
     |- backend                            app根目录
         |- management                     manage.py指令扩展目录
         |   |- commands                   manage.py指令扩展目录
         |- migrations                     数据迁移文件目录
         |- static                         静态资源目录
         |   |- backend                    命名空间
         |       |- css                    css文件目录
         |       |- images                 图片目录
         |       |- js                     js文件目录
         |- templates                      模板文件目录
         |   |- backend                    命名空间
         |       |- demo                   静态html文件目录
         |- templatetags                   模板自定义标记文件目录
    
### 工具模块

###### memcache
导入
    
    >>> from django.core.cache import cache
    
等价于
    
    >>> from django.core.cache import caches
    >>> cache = caches['default']
    
基础操作
    
    >>> cache.set('my_key', 'hello, world!', 30)
    >>> cache.get('my_key')
    >>> cache.delete('my_key')
    >>> cache.clear()
    
###### logging
配置文件

- _django/utils/log.py_
- _site/site/settings.py_

导入
    
    import logging
    logger = logging.getLogger('wxp.%s' % __name__)
    
接口调用

- **logger.debug()**
- **logger.info()**
- **logger.warning()**
- **logger.error()**
- **logger.critical()**

---
- **logger.log()**
- **logger.exception()**

gulp 构建

- 1 安装 node 环境、npm , 推荐使用 cnpm
- 2 在 package.json 所在目录里运行
 ````
cnpm install gulp gulp-less gulp-autoprefixer gulp-clean-css gulp-concat gulp-uglify gulp-rename del --save-dev
````
- 3 直接在gulpfile.js所在目录里运行 gulp 即可运行
