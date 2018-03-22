from django.db import models

# Create your models here.
from common.utils.utils_datetime import datetime_2string

'''
 商品库基础模型
'''


class FreightPricingMethod(models.Model):
    '''

    '''
    name = models.CharField(verbose_name='测试名', max_length=45)


class Goods(models.Model):
    '''
    商品表
    '''
    bit = models.CharField(verbose_name='商品货号', max_length=45, unique=True, blank=True)
    name = models.CharField(verbose_name='商品名', max_length=45, blank=True)
    price = models.DecimalField(verbose_name='商品价格', max_digits=20, decimal_places=2, default=0)
    photo = models.CharField(verbose_name='商品主图', max_length=200, blank=True)
    created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    preorder_limit = models.IntegerField(verbose_name='预购数量限制', default=0)
    freight_pricing_method = models.ForeignKey('FreightPricingMethod', verbose_name='运费计价方式', on_delete=models.PROTECT)
    delivery_time = models.IntegerField(verbose_name='发货时间', default=15)
    online_time = models.DateTimeField(verbose_name='上架时间', auto_now_add=True)
    offline_time = models.DateTimeField(verbose_name='下架时间', auto_now_add=True)
    refund_rate = models.DecimalField(verbose_name='退款比率', default=0, max_digits=5, decimal_places=5)
    pc_page = models.CharField(verbose_name='PC端宝贝详情页静态文件路径', max_length=100, null=True, blank=True)
    mobile_page = models.CharField(verbose_name='手机端宝贝详情页静态文件路径', max_length=100, null=True, blank=True)
    note = models.CharField(verbose_name='备注', max_length=500, blank=True)

    def transferobj_todict(self):
        return {
            'id': self.id,
            'bit': self.bit,
            'name': self.name,
            'price': self.price,
            'photo': self.photo,
            'created': datetime_2string(self.created) if self.created else '',
            'preorder_limit': self.preorder_limit,
            'freight_pricing_method_id': self.freight_pricing_method_id,
            'delivery_time': self.delivery_time,
            'online_time': datetime_2string(self.online_time) if self.online_time else '',
            'offline_time': datetime_2string(self.offline_time) if self.offline_time else '',
            'refund_rate': self.refund_rate,
            'pc_page': self.pc_page,
            'mobile_page': self.mobile_page,
            'note': self.note
        }


class GoodsPhoto(models.Model):
    '''
    商品相关图
    '''
    goods = models.ForeignKey('Goods', verbose_name='关联商品', on_delete=models.PROTECT)
    photo = models.CharField(verbose_name='商品图片', max_length=200, blank=True)


class GoodsProperty(models.Model):
    '''
    商品属性
    '''
    goods = models.ForeignKey('Goods', verbose_name='关联商品', on_delete=models.PROTECT)
    name = models.CharField(verbose_name='属性名', max_length=45, blank=True)
    value = models.CharField(verbose_name='属性值', max_length=500, blank=True)


class GoodsCategory(models.Model):
    '''
    商品分类
    '''
    name = models.CharField(verbose_name='商品类目名称', max_length=45, blank=True)
    icon = models.CharField(verbose_name='图标', max_length=45, null=True, blank=True)
    ranking = models.IntegerField(verbose_name='排序', default=-1)
    note = models.CharField(verbose_name='备注', max_length=500, blank=True)
    is_active = models.BooleanField(verbose_name='是否可用', default=1)


class GoodsHasGoodsCategory(models.Model):
    '''
    商品和商品类目关联表
    '''
    goods = models.ForeignKey('Goods', verbose_name='关联商品', on_delete=models.PROTECT)
    goods_category = models.ForeignKey('GoodsCategory', verbose_name='关联商品分类', related_name='goodscategory', on_delete=models.PROTECT)


class Specification(models.Model):
    '''
    规格表
    '''
    name = models.CharField(verbose_name='规格名称', max_length=45, unique=True)
    note = models.CharField(verbose_name='备注', max_length=500, blank=True)


class SpecificationChoice(models.Model):
    '''
    规格选项
    '''
    specification = models.ForeignKey('Specification', verbose_name='关联规格表', on_delete=models.PROTECT)
    value = models.CharField(verbose_name='属性值', max_length=45, blank=True)
    label = models.CharField(verbose_name='标签', max_length=45, blank=True)
    is_active = models.BooleanField(verbose_name='是否可用')


class GoodsSpecificationChoice(models.Model):
    '''
    商品和规格关联表
    '''
    goods = models.ForeignKey('Goods', verbose_name='关联商品表', on_delete=models.PROTECT)
    specification_choice = models.ForeignKey('SpecificationChoice', verbose_name='关联规格选项表', related_name='specificationchoice', on_delete=models.PROTECT)
    photo = models.CharField(verbose_name='图片路径', max_length=200, null=True, blank=True)
    note = models.CharField(verbose_name='备注', max_length=500, blank=True)
    is_active = models.BooleanField(verbose_name='是否可用')


class GoodsSku(models.Model):
    '''
    商品sku
    '''
    goods = models.ForeignKey('Goods', verbose_name='关联商品表', on_delete=models.PROTECT)
    name = models.CharField(verbose_name='名称', max_length=100, blank=True)
    photo = models.CharField(verbose_name='图片路径', max_length=200, blank=True)
    price = models.DecimalField(verbose_name='价格', max_digits=20, decimal_places=2)
    note = models.CharField(verbose_name='备注', max_length=500, blank=True)
    is_active = models.BooleanField(verbose_name='是否可用', default=1)


class GoodsSkuSpecification(models.Model):
    '''
    商品sku和商品规格选项关联表
    '''
    goods_sku = models.ForeignKey('GoodsSku', verbose_name='关联商品sku', on_delete=models.PROTECT)
    goods_specification_choice = models.ForeignKey('GoodsSpecificationChoice', verbose_name='关联商品规格选项关联表', related_name='goodsspecificationchoice', on_delete=models.PROTECT)
