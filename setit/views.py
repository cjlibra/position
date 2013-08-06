#coding:utf-8
# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect

from django.shortcuts import render_to_response
from setit.models import *

import json


def getwhereis(request):
	mapid = request.GET["mapid"]
	mapobj = get_object_or_404(Maps, pk=int(mapid))
	labels = Labels.objects.all()
	oinfolist = []
	count =0
	for label in labels :
		oneinfo ={}		
		try:
			winfoget = whereinfo.objects.filter(label=label).order_by("-realtime")[0]
		except:
			continue
		if winfoget.stayer.address.whichmap != mapobj :
			continue
		oneinfo["id"] = winfoget.label.serialno
		oneinfo["name"] = winfoget.label.attachwho.name
		oneinfo["x"] = winfoget.stayer.address.xpixel
		oneinfo["y"] = winfoget.stayer.address.ypixel
		oinfolist.append(oneinfo)
		 
	return  HttpResponse(json.dumps(oinfolist))
		
def showmonitor(request):
	cmdid = request.GET["cmdid"]
	if ( cmp(cmdid ,"0") == 0) :
		datalists = Maps.objects.all()
	
		
		return render_to_response('showmonitor_select.html',{'datalists':datalists})
	
	
	mapget = get_object_or_404(Maps, pk=int(cmdid))
	positions = addresses.objects.filter(whichmap=mapget)
	
	return render_to_response('showmonitor.html',{'mapsrcfile':"upload/" + str(mapget.map),'positions':positions,'mapid':cmdid})

def setmap(request):
	datalists = Maps.objects.all()
	
		
	return render_to_response('setmap.html',{'datalists':datalists})
	
def showstayer(request):
	mapid = request.GET["mapid"]
	mapobj = get_object_or_404(Maps, pk=int(mapid))
	addrs = addresses.objects.filter(whichmap=mapobj)
	addrsinfo=[]
	for addr in addrs:
		oneaddrinfo={}
		oneaddrinfo["addr"]= addr.address
		oneaddrinfo["x"]=addr.xpixel
		oneaddrinfo["y"]=addr.ypixel
		addrsinfo.append(oneaddrinfo)
	return HttpResponse(json.dumps(addrsinfo))


def possubmit(request):
	whichmap = request.POST["hidden1"]
	whereis = request.POST["mapcomments"]
	xpixel = request.POST["xpixel"]
	ypixel = request.POST["ypixel"]
	if (whichmap == "" or whereis == "" or xpixel=="" or ypixel=="") :
		return  HttpResponse("<h1>输入出错</h1>")
	mapget = get_object_or_404(Maps, pk=int(whichmap))
	selectmapsrc = "upload/" +str( mapget.map)
	addr = addresses(whichmap=mapget ,address=whereis,xpixel=int(xpixel),ypixel=int(ypixel))
	addr.save()
	#return HttpResponse("""<h1>成功添加基站</h1><a href="javascript:window.history.go(-1)">回到前一页</a>""")
	return render_to_response('mappic.html',{'selectmapsrc':selectmapsrc, 'mapid':mapget.id})