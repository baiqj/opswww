#!/usr/local/bin/python2.7

from fabric.api import *

class Fabhandler():
	
	def __init__(self, host, passwd, command='', srcpath='', dstpath=''):
		self.host = host
		self.passwd = passwd
		self.command = command
		self.srcpath = srcpath
		self.dstpath = dstpath
	
#	env.password = self.passwd

	def fabrun(self):
		env.password = self.passwd
		with settings(warn_only=True, host_string=self.host), hide('running','stdout','stderr'):
			return run(self.command)
			# return result OR  
			# some string like 
			# cannot access /root/adfa: No such file or directory
			# /bin/bash: hello: command not found
	

	def fabget(self):
		env.password = self.passwd
		with settings(warn_only=True, host_string=self.host):
			get(self.srcpath, self.dstpath)
			# return None
		

	def fabput(self):
		env.password = self.passwd
		with settings(warn_only=True, host_string=self.host), hide('running','stdout','stderr'):
			put(self.srcpath, self.dstpath)
