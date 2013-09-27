#coding:utf-8
# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect

from django.shortcuts import render_to_response
from setit.models import *

import json
def showmainpage(request):
	return render_to_response('main.html' ,{'LANGUAGE_CODE':'zh-cn','is_popup':1})

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
		oneinfo["onlyid"]=winfoget.stayer.address.id
		oneinfo["x"] = winfoget.stayer.address.xpixel
		oneinfo["y"] = winfoget.stayer.address.ypixel
		oinfolist.append(oneinfo)
		 
	return  HttpResponse(json.dumps(oinfolist))
		
def showmonitor(request):
	cmdid = request.GET["cmdid"]
	if ( cmp(cmdid ,"0") == 0) :
		datalists = Maps.objects.all()
	
		
		return render_to_response('showmonitor_select.html',{'datalists':datalists,'LANGUAGE_CODE':'zh-cn' ,'is_popup':1 })
	
	
	mapget = get_object_or_404(Maps, pk=int(cmdid))
	positions = addresses.objects.filter(whichmap=mapget)
	
	return render_to_response('showmonitor.html',{'mapsrcfile':"media/" + str(mapget.map),'positions':positions,'mapid':cmdid})

def setmap(request):
	try :
		mapid = request.GET["cmdid"]
		mapobj = get_object_or_404(Maps, pk=int(mapid))
		return render_to_response('setmap.html',{'mapsrcfile':"/media/" + str(mapobj.map),  'mapid':mapid ,'mapname':mapobj.mapname})

	except :
		datalists = Maps.objects.all()		
		return render_to_response('setmap_select.html',{'datalists':datalists})
	

	
def showstayer(request):
	mapid = request.GET["mapid"]
	mapobj = get_object_or_404(Maps, pk=int(mapid))
	addrs = addresses.objects.filter(whichmap=mapobj)
	addrsinfo=[]
	for addr in addrs:
		Stayers = Stayer.objects.filter(address=addr )
		for onestayer in Stayers :
			stayerone = onestayer
			break
		oneaddrinfo={}
		oneaddrinfo["addr"]= addr.address
		oneaddrinfo["id"]= addr.id
		oneaddrinfo["x"]=addr.xpixel
		oneaddrinfo["y"]=addr.ypixel
		oneaddrinfo["stayno"]=stayerone.serialno
		oneaddrinfo["staycomments"]=stayerone.comments
		addrsinfo.append(oneaddrinfo)
	return HttpResponse(json.dumps(addrsinfo))


def possubmit(request):
	whichmap = request.POST["hidden1"]
	action = request.POST["hidden2"]
	addressid = request.POST["addressid"]
	if action == "3" :#删除
		addr = get_object_or_404(addresses, pk=int(addressid))
		addr.delete()
		Stayer.objects.filter(address=addr).delete()
		return HttpResponseRedirect("/admin/setmap?cmdid=%s" %whichmap) 
		
		
	
	whereis = request.POST["mapcomments"]
	xpixel = request.POST["xpixel"]
	ypixel = request.POST["ypixel"]
	apid = request.POST["apname"]
	apcomments = request.POST["apcomments"]
	if (whichmap == "" or whereis == "" or xpixel=="" or ypixel=="") :
		return  HttpResponse("<h1>输入出错</h1>")
	if action == "2" : #编辑
		addr = get_object_or_404(addresses, pk=int(addressid))
		addr.address = whereis
		addr.save()
		ap = Stayer.objects.get(address= addr)
		ap.serialno = apid
		ap.comments = apcomments
		ap.save()
		return HttpResponseRedirect("/admin/setmap?cmdid=%s" %whichmap) 
	mapget = get_object_or_404(Maps, pk=int(whichmap))
	selectmapsrc = "upload/" +str( mapget.map)
	addr = addresses(whichmap=mapget ,address=whereis,xpixel=int(xpixel),ypixel=int(ypixel))
	addr.save()
	stayer = Stayer(serialno=apid,address=addr,comments=apcomments)
	stayer.save()
	positions = addresses.objects.filter(whichmap=mapget)	 
	return HttpResponseRedirect("/admin/setmap?cmdid=%s" %whichmap) 
