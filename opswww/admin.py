from django.contrib import admin
from models import *

class HostlistAdmin(admin.ModelAdmin):
	
	#inlines = [ChoiceInline]
	
	list_display = ('ip','hostname','server_class','os_version','kernel_version')
	#list_filter = ['hostname']
	search_fields = ['hostname']
	
admin.site.register(Hostlist, HostlistAdmin)