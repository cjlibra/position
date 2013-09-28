#coding:utf-8
from django.contrib import admin
from setit.models import Labelusers ,Labels ,Maps,Stayer,addresses,whereinfo,zonelimit,alarminfo
admin.site.register(Labelusers)
admin.site.register(Labels)
admin.site.register(Stayer)
admin.site.register(addresses)
admin.site.register(Maps)
admin.site.register(whereinfo)
admin.site.register(zonelimit)
admin.site.register(alarminfo)
