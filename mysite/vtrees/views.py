#from django import template
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
#from django.template import context, loader
from .models import Videos

# Create your views here.
def index(request):
    latest_videos_list = Videos.objects.order_by('-videos_lastupdate')[:5]
    #template = loader.get_template('vtrees/index.html')
    context = {
        'latest_videos_list': latest_videos_list,
    }
    return render(request, 'vtrees/index.html', context)
    #return HttpResponse(template.render(context, request))
    #return HttpResponse("Hello, world! This is vtree top!")

def video(request, videos_id):
    video = get_object_or_404(Videos, pk=videos_id)
    #try:
        #video = Videos.objects.get(pk=videos_id)
    #except Videos.DoesNotExist:
        #raise Http404("Video does not exist")
    return render(request, 'vtrees/video.html', {'video':video})