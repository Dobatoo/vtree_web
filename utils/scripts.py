import datetime, re
from typing import List, Tuple
import youtube_api
from django.utils import timezone
from ..mysite.vtrees.models import Channels_detail, Channels_info, Children, Mentions, Posts, Videos_detail, Videos_info

def description_search(description:str)->list(list(str),list(str)):#sited_videos,mentioned_channels
    sited_videos = []
    mentioned_channels = []
    pattern_watch = re.compile('https://www.youtube.com/watch\?v=\w{11}')
    pattern_be = re.compile('https://youtu.be/\w{11}')
    pattern_channel = re.compile('https://www.youtube.com/channel/\w{24}')
    sited_videos.extend([v.split("=")[1] for v in pattern_watch.findall(description)])
    sited_videos.extend([v.split("/")[3] for v in pattern_be.findall(description)])
    mentioned_channels.extend([c.split("/")[4] for c in pattern_channel.findall(description)])
    return [sited_videos,mentioned_channels]

def publishedAt_to_datetime(publishedAt:str)->datetime:
    return datetime.datetime.strptime(publishedAt, '%Y-%m-%dT%H:%M:%SZ')

def register_channel_info(channelID:str, isRegistered:bool)->None:
    info = youtube_api.api_channel_info(channelID) #(id,name,icon,viewcount)
    c = Channels_info(
        channels_id = channelID,
        channels_title = info[1],
        channels_count_total = info[3],
        channels_icon_url = info[2],
        channels_isRegistered = isRegistered,
        channels_info_lastupdate = timezone.now()
        )
    c.save()

def calculate_channel_sited_mentioned_sum(channelID:str)->None:
    p = Posts.objects.filter(posts_channel_id = channelID)
    posted_videos = set(v.posts_video_id.videos_id for v in p)
    #calculate sited sum
    sited_sum = 0
    sited_videos = set(())
    for p_id in posted_videos:
        s = Children.objects.filter(children_video_parent = p_id)
        for v in s:
            v_id = v.children_video_child.videos_id
            if v_id not in posted_videos:
                sited_videos.add(v_id)
                sited_sum = sited_sum + v.children_video_child.videos_detail.videos_count_original
    #calculate mentioned_sum
    mentioned_sum = 0
    mentioned_videos = set(())
    m = Mentions.objects.filter(mentions_channel_id = channelID)
    for v in m:
        v_id = v.mentions_video_id.videos_id
        if v_id not in posted_videos and v_id not in sited_videos:
            mentioned_videos.add(v_id)
            mentioned_sum = mentioned_sum + v.mentions_video_id.videos_detail.videos_count_original
    #save
    c = Channels_detail.objects.get(channels_id = channelID)
    c.channels_count_sited_sum = sited_sum
    c.channels_count_sited_sum_lastupdate = timezone()
    c.channels_count_mentioned_sum = mentioned_sum
    c.channels_count_mentioned_sum_lastupdate = timezone.now()
    c.save()

def register_video_info(videoID:str, video_title:str, video_publishedAt:datetime)->None:
    v = Videos_info(
        videos_id = videoID,
        videos_title = video_title,
        videos_published = video_publishedAt
    )
    v.save()

def register_video_detail(videoID_list:List[str])->List[Tuple[str,str,int]]:#id,description,viewCount
    videoID_list_50 = [videoID_list[i:i+50] for i in range(0, len(videoID_list), 50)]
    video_detail_list_return = []
    for l in videoID_list_50:
        video_detail_list = youtube_api.api_video([],l)
        video_detail_list_return.extend(video_detail_list)
        for v in video_detail_list:
            v = Videos_detail(
                videos_id = v[0],
                videos_description = v[1],
                videos_count_original = v[2],
                videos_detail_lastupdate = timezone.now()
            )
            v.save()
    return video_detail_list_return

def calculate_video_sited(videoID:str)->None:
    sum = 0
    s = Children.objects.filter(
        children_video_parent = videoID
    )
    for c in s:
        n = c.children_video_child.videos_detail.videos_count_original
        sum = sum + n
    v = Videos_detail.objects.get(videos_id = videoID)
    v.videos_count_sited = sum
    v.videos_count_sited_lastupdate = timezone.now()
    v.save()

def register_post(channelID:str,videoID:str)->None:
    p = Posts(
        posts_video_id = videoID,
        posts_channel_id = channelID
    )
    p.save()

def register_parent(videoID_parent:str,videoID_child:str)->None:
    p = Children(
        children_video_child = videoID_child,
        children_video_parent = videoID_parent
    )
    p.save()

def register_mention(channelID:str,videoID:str)->None:
    m = Mentions(
        mentions_video_id = videoID,
        mentions_channel_id = channelID
    )
    m.save()


def add_new_channel(channelID:str)->None:
    #register channelinfo
    register_channel_info(channelID,True)
    #register channelpost info
    posts = youtube_api.api_search_post([], channelID)
    for v in posts:
        register_video_info(v[0], v[1],publishedAt_to_datetime(v[2]))
        #register channelpost relation
        register_post(channelID, v[0])
    #register channelpost detail
    _ = register_video_detail(posts)
    #register sited video info
    posts_5 = [[v[0] for v in posts[i:i+5]] for i in range(0, len(posts), 5)]#[[id1,id2,,,id5],[id6,,,,id10],...]
    sited = []
    for p5 in posts_5:
        sited.extend(youtube_api.api_search_sited([],p5))
    for s in sited:
        register_video_info(
            videos_id = s[0],
            videos_title = s[1],
            videos_published = publishedAt_to_datetime(v[2])
            )
        register_post(s[3],s[0])
    #register sited video detail
    sited_details = register_video_detail(sited)
    
    for d in sited_details:
        [parent_v,mentioned_c] = description_search(d[1])
        #register sited video relation
        for v in parent_v:
            register_parent(v,d[0])
        #register mentioned video   
        for c in mentioned_c:
            register_mention(c,d[0])
    #calculate sited and mentioned
    calculate_channel_sited_mentioned_sum(channelID)
    calculate_video_sited(channelID)
    #done
