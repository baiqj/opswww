from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render_to_response, RequestContext
from django import forms
from models import *
from mimetypes import guess_type
import settings
import os
import time
import Queue
import threading

from models import *
from sshapi import *


def indexPage(request):
    return render_to_response('index.html')

def hostList(request):
    '''
    kvnull = Hostlist.objects.filter(kernel_version='')
    osnull = Hostlist.objects.filter(os_version='')
    if kvnull:
        shell_command = 'uname -s -r'
        for host in kvnull:
            return_value = runCommand(host.ip, host.ssh_port, host.username, host.root_password, shell_command)
            host.kernel_version = return_value
            host.save()
			
	#only CentOS
    if osnull:
        shell_command = 'cat /etc/redhat-release'
        for host in osnull:
            return_value = runCommand(host.ip, host.ssh_port, host.username, host.root_password, shell_command)
            host.os_version = return_value
            host.save()
    '''
	
    hostlist_obj = Hostlist.objects.all()
    return render_to_response('host_list.html', {'hl':hostlist_obj})
        
def hostDetail(request, host_id):
    try:
        host_obj = Hostlist.objects.get(id = host_id)
    except:
        print '404'
        
    context = {'host_obj':host_obj}
    return render_to_response('host_detail.html', context)

def flushHostList(request):
    
    from remote_host_status import perfStatus
    
    #set the num of thread
    nthread = 5
    
    host = '10.0.0.81'
    port = 22
    username = 'root'
    password = '123456'
    
    host_queue = Queue.Queue()
    hostlist_obj = Hostlist.objects.all()
    
    for host_obj in hostlist_obj:
        host = host_obj.ip
        port = host_obj.ssh_port
        username = host_obj.username
        password = host_obj.root_password
        hpup = [host, port, username, password]
        host_queue.put(hpup)
                
    thread_list = []
    for i in range(nthread):
        th = threading.Thread(target = perfStatus, args = (host_queue,))
        thread_list.append(th)
        
    for i in range(nthread):
        thread_list[i].start()
        
    for i in range(nthread):
        thread_list[i].join()
    
    '''
    status_dict = perfStatus(host, port, username, password)
    
    #Table Output
    response_str = '<table border="1">'
    for key in status_dict:
        response_str += ('<tr>' + '<td>' + str(key) + '</td>' + '<td>' + str(status_dict[key]) + '</td>' + '</tr>' + '<br/>')
    response_str += '</table>'
    '''
    
    return render_to_response('host_list.html', {'hl':hostlist_obj})
    


''' TEST PAGE '''    
def testPage(request):
    return render_to_response('base.html')

def download(request, filename):

    filepath = os.path.join(settings.DOWNLOAD_DIR, filename)
    wrapper = FileWrapper(open(filepath, 'rb'))
    content_type = guess_type(filepath)[0]
    #	Using mimetype keyword argument is deprecated, use content_type instead
    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    #print response
    return response


def upload(request):

    if request.method == 'POST':
        #print request.POST
        #print request.FILES
        uploaded_filepath = os.path.join(settings.UPLOAD_DIR, request.FILES['upload_file'].name)
        f = open(uploaded_filepath, 'wb')
        s = request.FILES['upload_file']
        for chunk in s.chunks():
            f.write(chunk)
        f.close()
        #return HttpResponseRedirect(reverse('opswww.opswww.views.success'))
        return HttpResponse('Ok!')
	
    return render_to_response('upload.html', context_instance=RequestContext(request))


##  test area  ##

def transfer(request):
    return render_to_response('file_transfer.html')
	

	
def xmpp_manage(request):
    return render_to_response('xmpp_manage.html')
	
def file_transfer(request):
    if request.GET:
        print request.GET
        ##<QueryDict: {u'selected_hosts': [u'3', u'4'], u'remotepath': [u'/home'], u'selected_file': [u'IMG_1181.JPG', u'access_api_192_59.log']}>
        #request.GET['selected_hosts']
        #sftpPut(host, port, username, password, src_path, dst_path):
				
    hl = Hostlist.objects.all()
    filelist = []
    
    for f in os.listdir(settings.UPLOAD_DIR):
        f_abs = os.path.join(settings.UPLOAD_DIR, f)
        fsize = int(os.path.getsize(f_abs))/1024
        ftime = time.strftime('%Y-%m-%d %H:%M',time.localtime(os.stat(f_abs).st_mtime))
        filelist.append({'fname':f, 'ftime':ftime, 'fsize':fsize})
    return render_to_response('file_transfer.html', {'hl':hl, 'filelist':filelist})