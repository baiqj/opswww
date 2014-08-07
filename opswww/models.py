from django.db import models

class Hostlist(models.Model):
	ip = models.CharField(max_length=15)
	hostname = models.CharField(max_length=30)
	server_class = models.CharField(max_length=30)
	kernel_version = models.CharField(max_length=50)
	root_password = models.CharField(max_length=20)
	
	def __unicode__(self):
		return self.ip