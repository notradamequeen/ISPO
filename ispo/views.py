from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, RequestContext

def home(request):
	return render_to_response('home.html', locals(), context_instance=RequestContext(request))