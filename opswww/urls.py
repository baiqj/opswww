from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'opswww.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^test/$', 'opswww.views.testPage'),
    
	url(r'^$', 'opswww.views.indexPage'),
	url(r'^hostlist/$', 'opswww.views.hostList'),
	url(r'^flushostlist/$', 'opswww.views.flushHostList'),
	
    # ===	
	url(r'^xmpp_manage/$', 'opswww.views.xmpp_manage'),
	url(r'^file_transfer/$', 'opswww.views.file_transfer'),
	
    url(r'^admin/', include(admin.site.urls)),
    
	url(r'^download/filename=(?P<filename>.{1,500})/$', 'opswww.views.download'),
	url(r'^upload/$', 'opswww.views.upload'),
	url(r'^transfer/$', 'opswww.views.transfer'),
)
