from django.contrib import admin
from opswww.opswww.models import *

class HostlistAdmin(admin.ModelAdmin):
	fieldsets = [
		('ip', {'fields':['ip','hostname','server_class','kernel_version','root_password']}),
	]
	#inlines = [ChoiceInline]
	
	list_display = ('ip','hostname','server_class','kernel_version','root_password')
	#list_filter = ['pub_date']
	#search_fields = ['question']
	
admin.site.register(Hostlist, HostlistAdmin)