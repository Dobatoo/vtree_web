#from django import template
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
#from django.template import context, loader
from django.urls import reverse
from .models import Videos_info, Videos_detail

# Create your views here.
def index(request):
    latest_videos_list = Videos_info.objects.order_by('-videos_published')[:5]
    #template = loader.get_template('vtrees/index.html')
    context = {
        'latest_videos_list': latest_videos_list,
    }
    return render(request, 'vtrees/index.html', context)
    #return HttpResponse(template.render(context, request))
    #return HttpResponse("Hello, world! This is vtree top!")

def video(request, videos_id):
    video_info = get_object_or_404(Videos_info, pk=videos_id)
    video_detail = get_object_or_404(Videos_detail, pk=videos_id)
    #try:
        #video = Videos.objects.get(pk=videos_id)
    #except Videos.DoesNotExist:
        #raise Http404("Video does not exist")
    return render(request, 'vtrees/video.html', {'video_info':video_info,'video_detail':video_detail})

def count_register(request, videos_id):
    video_detail = get_object_or_404(Videos_detail, pk=videos_id)
    inputted_count = request.POST['videos_count_original']
    video_detail.videos_count_original = int(inputted_count)
    video_detail.save()
    r=reverse('vtrees:video', kwargs={'videos_id':video_detail.videos_id})
    print(r)
    return HttpResponseRedirect(r)
