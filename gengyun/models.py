#coding=utf-8
from __future__ import unicode_literals

from django.db import models
from  django.contrib.auth.models import User

# Create your models here.


class   gengyuns(models.Model):
    user_id = models.ForeignKey(User,verbose_name="用户",help_text="用户绑定")
    name =  models.CharField(max_length=255,verbose_name="耕耘",help_text="开垦荒地")
    text = models.TextField(verbose_name="荒地描述",blank=True)
    create_date = models.DateTimeField(auto_created=True)
    update_date = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return "{0}({1})".format(self.user_id,self.name)


class zhongzi(models.Model):
    gengyuns_id = models.ForeignKey(gengyuns,verbose_name="耕耘",help_text="绑定荒地")
    user_id = models.ForeignKey(User, verbose_name="用户", help_text="用户绑定")
    name = models.CharField(max_length=255,verbose_name="播种")
    text = models.TextField(verbose_name="种子描述")
    create_date = models.DateTimeField(auto_created=True)
    update_date = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return "{0}({1})".format(self.gengyuns_id,self.name)

#附件
class fujian(models.Model):
    name = models.CharField(max_length=255,verbose_name="附件名称")
    up_file =  models.FileField(upload_to="./gengyun/static/update/%Y%m%d",verbose_name="附件上传")
    wenzhang_neirong_id = models.ForeignKey("zhishidian")
    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = '上传附件'
        verbose_name_plural = '上传附件'


class zhishidian(models.Model):
    zhongzi_id= models.ForeignKey(zhongzi,verbose_name="二级主题",help_text="关联二级标题")
    name = models.CharField(max_length=255,verbose_name="主题")
    text = models.TextField(verbose_name="知识点内容")
    create_date = models.DateTimeField(auto_created=True)
    update_date = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.name