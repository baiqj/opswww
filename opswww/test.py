#!/usr/local/bin/python2.7

from fabapi import *

fab = Fabhandler('192.168.1.119', 'helloworld', 'hello', '/root/anaconda-ks.cfg', '/root/workspace/opswww/resource/download')

#run_result = fab.fabrun()
#print '-----'
#print 'Ex:%s' % run_result

get_result = fab.fabget()
print '======'
print get_result
