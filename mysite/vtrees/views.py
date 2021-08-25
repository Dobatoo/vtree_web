#from django import template
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
#from django.template import context, loader
from django.urls import reverse
from .models import Channels_detail, Channels_info, Posts, Videos_info, Videos_detail, Children

# Create your views here.
def index(request):
    channels_list = Channels_info.objects.all()
    #template = loader.get_template('vtrees/index.html')
    context = {
        'channels_list': channels_list,
    }
    return render(request, 'vtrees/index.html', context)
    #return HttpResponse(template.render(context, request))
    #return HttpResponse("Hello, world! This is vtree top!")

def video(request, videos_id):
    video_info = get_object_or_404(Videos_info, pk=videos_id)
    video_detail = get_object_or_404(Videos_detail, pk=video_info)
    video_sited = Children.objects.filter(children_video_parent = videos_id)
    context = {
        'video_info':video_info,
        'video_detail':video_detail,
        'video_sited':video_sited
        }
    #try:
        #video = Videos.objects.get(pk=videos_id)
    #except Videos.DoesNotExist:
        #raise Http404("Video does not exist")
    return render(request, 'vtrees/video.html', context)

def channel(request, channels_id):
    channel_info = get_object_or_404(Channels_info, pk=channels_id)
    channel_detail = get_object_or_404(Channels_detail, pk=channel_info)
    posts = Posts.objects.filter(posts_channel_id = channels_id).order_by('-posts_video_id__videos_published')[:5]
    context =  {
        'channel_info':channel_info,
        'channel_detail':channel_detail,
        'posts':posts
        }
    return render(request, 'vtrees/channel.html', context)

def channel_posts(request, channels_id):
    channel_info = get_object_or_404(Channels_info, pk=channels_id)
    posts = Posts.objects.filter(posts_channel_id = channels_id).order_by('-posts_video_id__videos_published').all()
    context =  {
        'channel_info':channel_info,
        'posts':posts
        }
    return render(request, 'vtrees/channel_posts.html', context)

def count_register(request, videos_id):
    video_detail = get_object_or_404(Videos_detail, pk=videos_id)
    inputted_count = request.POST['videos_count_original']
    video_detail.videos_count_original = int(inputted_count)
    video_detail.save()
    r=reverse('vtrees:video', kwargs={'videos_id':video_detail.videos_id})
    print(r)
    return HttpResponseRedirect(r)
