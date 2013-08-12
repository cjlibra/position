#coding:utf-8
from django.db import models

# Create your models here.
upload_dir = r"./"
class Labelusers(models.Model):
	name = models.CharField(max_length=50,verbose_name="姓名：")
	gender_choice=(
	(0,"男"),
	(1,"女"),
	)
	picture = models.FileField(upload_to=upload_dir ,verbose_name="相片：")
	gender = models.IntegerField(choices=gender_choice,verbose_name="性别：")
	idnum = models.CharField(max_length=20,verbose_name="身份证号码：")
	comments = models.CharField(max_length=300,verbose_name="备注：")
	
	def __unicode__(self):
		return self.name
	class Meta:
		verbose_name_plural = '标签使用人'
		verbose_name = '标签使用者'

class Labels(models.Model):
	serialno = models.IntegerField(verbose_name="唯一码：")
	comments = models.CharField(max_length=300,verbose_name="注释：")
	authority = models.IntegerField(verbose_name="权限编码：")
	attachwho = models.ForeignKey(Labelusers,verbose_name="使用人：")
	
	def __unicode__(self):
		return str(self.serialno)
	class Meta:
		verbose_name_plural = '标签'
		verbose_name = '标签'

class Maps(models.Model):
	mapname = models.CharField(max_length=50,verbose_name="地图名字")
	map = models.FileField(upload_to=upload_dir ,verbose_name="地图：")
	comments = models.CharField(max_length=300,verbose_name="备注：")
	
	def __unicode__(self):
		return self.mapname
	class Meta:
		verbose_name_plural = '地图'
		verbose_name = '地图'
	
class addresses(models.Model):
	whichmap = models.ForeignKey(Maps,verbose_name="所标地图:")
	address = models.CharField(max_length=100 ,verbose_name="位置：")
	xpixel = models.IntegerField(verbose_name="x轴：")
	ypixel = models.IntegerField(verbose_name="y轴：")
	
	def __unicode__(self):
		return "%d" % self.xpixel +"-"+"%d" %self.ypixel
	class Meta:
		verbose_name_plural = '位置'
		verbose_name = '位置'
	
class Stayer(models.Model):
	serialno = models.IntegerField(verbose_name="唯一码：")
	address = models.ForeignKey(addresses,verbose_name="所在位置:")
	comments = models.CharField(max_length=300,verbose_name="备注：")
	
	def __unicode__(self):
		return   str(self.serialno)
	class Meta:
		verbose_name_plural = '基站'
		verbose_name = '基站'

class whereinfo(models.Model):
	stayer = models.ForeignKey(Stayer,verbose_name="基站：")
	label = models.ForeignKey(Labels,verbose_name="标签：")
	dttime =  models.DateTimeField(auto_now=True,verbose_name="记录时间：") 
	realtime = models.DateTimeField(verbose_name="真实时间：")
	
	def __unicode__(self):
		return u"人员位置信息"
	class Meta:
		verbose_name_plural = '人员位置信息'
		verbose_name = '人员位置信息'
	
