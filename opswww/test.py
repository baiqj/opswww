#!/usr/local/bin/python2.7

import settings
from sshapi import *

host = 'vm1'
port = 22
username = 'root'
password = '123456'
command = 'ls -l /home'
src_path = '/root/sockClient.py'
dst_path = '/home/samba/workspace/opswww/resource/download/sockClient.py.bak'

#output = runCommand(host, port, username, password, command)
#print output
output = sftpGet(host, port, username, password, src_path, dst_path)
if not output:
	print 'success'
else:
	print output

