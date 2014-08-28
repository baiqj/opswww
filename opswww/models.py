from django.db import models

class Hostlist(models.Model):
	ip = models.IPAddressField(max_length = 15)
	hostname = models.CharField(max_length = 30, null = True)
	server_class = models.CharField(max_length = 30, null = True)
	kernel_version = models.CharField(max_length = 50, null = True)
	ssh_port = models.IntegerField(blank = True)
	username = models.CharField(max_length = 10, null = True)
	root_password = models.CharField(max_length = 20, null = True)
	os_version = models.CharField(max_length = 50, null = True)
	# ping format
	# (0, 60.39595603942871, 52.083730697631836)
	ping_packet_loss_rate = models.CharField(max_length = 10, null = True)   #34%
	ping_delay = models.IntegerField(null = True)                            #int
	
	def __unicode__(self):
		return self.ip
	
	#default ordering rule
	class Meta:
		ordering = ['server_class']     
		
		
#class Serverlist(models.Model):