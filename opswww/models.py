from django.db import models

class Hostlist(models.Model):
    
	ip = models.IPAddressField(max_length = 15)
	hostname = models.CharField(max_length = 30, blank = True)
	server_class = models.CharField(max_length = 30, blank = True)
	kernel_version = models.CharField(max_length = 50, blank = True)
	ssh_port = models.IntegerField()
	username = models.CharField(max_length = 10)
	root_password = models.CharField(max_length = 30)
	os_version = models.CharField(max_length = 50, blank = True)
	ping_packet_loss = models.IntegerField(null = True, blank = True)                  # %
	ping_delay = models.FloatField(null = True, blank = True)                          # 20.34 ms
	uptime = models.FloatField(null = True, blank = True)                              # 38.11 days
	loadavg = models.CharField(max_length = 15, blank = True)
	meminfo = models.CharField(max_length = 20, blank = True)
	cpu_procs = models.IntegerField(null = True, blank = True)
	last_check = models.DateTimeField(null = True, blank = True)
	
	
	def __unicode__(self):
		return self.ip
	
	#default ordering rule
	class Meta:
		ordering = ['server_class']     


''' returns
        {
            'ping': (0, 0.47707557678222656, 0.3682374954223633),
            'uptime': 38.11,                         days
            'loadavg': '0.08 0.02 0.01', 
            'meminfo': '62.85 1.99 3.00%',           G
            'cpu_procs': 24 
        }
        or
        {'ping': (100, None, None)}           # KeyError
'''

class HostlistSSH(models.Model):
    
    ip = models.IPAddressField(max_length = 15)
    ssh_port = models.IntegerField()
    username = models.CharField(max_length = 10)
    root_password = models.CharField(max_length = 30)