from django.db import models

class Hostlist(models.Model):
	ip = models.IPAddressField(max_length=15)
	hostname = models.CharField(max_length=30, blank=True)
	server_class = models.CharField(max_length=30, blank=True)
	kernel_version = models.CharField(max_length=50, blank=True)
	ssh_port = models.IntegerField(max_length=5, blank=True)
	username = models.CharField(max_length=10, blank=True)
	root_password = models.CharField(max_length=20, blank=True)
	os_version = models.CharField(max_length=50, blank=True)
	
	def __unicode__(self):
		return self.ip
	
	#default ordering rule
	class Meta:
		ordering = ['server_class']