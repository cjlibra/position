from django.conf.urls import patterns, include, url
from django.conf import settings
from   setit.views  import *

#from django.views.generic  import redirect_to  
from django.views.generic import RedirectView  

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'position.views.home', name='home'),
    # url(r'^position/', include('position.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	url(r'^admin/setmap', setmap),
	url(r'^possubmit',possubmit),
	url(r'^showmonitor',showmonitor),
	url(r'^getwhereis',getwhereis),
	url(r'^showstayer',showstayer),
	
    url(r'^admin/', include(admin.site.urls)),
	##url(r'^/$', redirect_to, {'url': '/upload/main/main.html'}), 
	url(r'^$', RedirectView.as_view(url='/upload/main/main.html')),  
	
	
	url(r'^upload/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
)
