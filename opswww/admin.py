from django.contrib import admin
from models import *

class HostlistAdmin(admin.ModelAdmin):
	
	#inlines = [ChoiceInline]
	
	list_display = ('ip','hostname','ssh_port','os_version','kernel_version')
	#list_filter = ['hostname']
	search_fields = ['hostname']

class ServerlistAdmin(admin.ModelAdmin):
    list_display = ('servername', 'host')
    search_fields = ['servername']
	
admin.site.register(Hostlist, HostlistAdmin)
admin.site.register(Serverlist, ServerlistAdmin)