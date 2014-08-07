from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from django import forms
from mimetypes import guess_type
import settings
import os


def index_page(request):
	return render_to_response('index.html')

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
	return render_to_response('transfer.html')
	
def host_manage(request):
	return render_to_response('host_manage.html')
	
def xmpp_manage(request):
	return render_to_response('xmpp_manage.html')
