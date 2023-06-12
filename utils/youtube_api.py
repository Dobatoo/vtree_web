from apiclient.discovery import build
from apiclient.errors import HttpError
from typing import List, Tuple, Dict

API_KEYs = [

    ] #hide later
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube (keyNum:int = 0):
    youtube_url = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=API_KEYs[keyNum]
    )
    return youtube_url

def api_search_post(post_list,channelID:str,keyNum:int = 0, **kwargs:Dict[str,str]) -> List[Tuple[str,str,str]]:#video_id,video_title,video_publishedAt
    try:
        response = youtube(keyNum).search().list(
            part = 'id,snippet',
            channelId=channelID,
            maxResults = 50,
            order = 'date',
            pageToken = kwargs["pageToken"] if "pageToken" in kwargs else '',
            safeSearch='none',
            type='video',
            fields='nextPageToken,items(id(videoId),snippet(publishedAt,channelId,title))'
        ).execute()

    except HttpError as e:
        if e.resp.reason == "quotaExceeded":
            #change APIkey
            if keyNum + 1 < len(API_KEYs):
                return api_search_post(post_list,channelID,keyNum+1,kwargs)
            else:
                raise Exception("quotaExceeded")
        else:
            print ("An Http error %d occurred:\n%s" % (e.resp.status, e.content))
            raise e

    #json to list 
    for item in response.get("items", []):
        if item["snippet"]["channelId"] == channelID:
            post_list.append((item["id"]["videoId"],item["snippet"]["title"],item["snippet"]["publishedAt"]))
            
    if "nextPageToken" in response:
        nextPageToken = response["nextPageToken"]
        return api_search_post(post_list,channelID,**{"pageToken":nextPageToken})
    else:
        return post_list

def api_video(video_info_list,videoID_list:List[str],keyNum:int = 0, **kwargs:Dict[str,str]) -> List[Tuple[str,str,int]]:
    try:
        response = youtube(keyNum).videos().list(
            part = 'id,snippet,statistics',
            id = ','.join(videoID_list),
            maxResults = 50,
            #this does not work for id#pageToken = kwargs["pageToken"] if "pageToken" in kwargs else '',
            fields='nextPageToken,items(id,snippet(description),statistics(viewCount))'
        ).execute()

        #json to list 
        for item in response.get("items", []):
            video_info_list.append((item["id"],item["snippet"]["description"],item["statistics"]["viewCount"]))

        if "nextPageToken" in response:
            nextPageToken = response["nextPageToken"]
            return api_video(video_info_list,video_info_list,**{"pageToken":nextPageToken})
        else:
            return video_info_list

    except HttpError as e:
        if e.resp.reason == "quotaExceeded":
            #change APIkey
            if keyNum + 1 < len(API_KEYs):
                return api_video(video_info_list,videoID_list,keyNum+1,kwargs)
            else:
                raise Exception("quotaExceeded")
        else:
            print ("An Http error %d occurred:\n%s" % (e.resp.status, e.content))
            raise

def api_search_sited(sited_list,videoID_list:List[str], keyNum:int = 0,**kwargs:Dict[str,str]) -> List[Tuple[str,str,str,str]]:#videoId,title,publishedAt,channelID
    try:
        response = youtube(keyNum).search().list(
            part = 'id,snippet',
            maxResults = 50,
            order = 'date',
            pageToken = kwargs["pageToken"] if "pageToken" in kwargs else '',
            q=" | ".join(videoID_list) ,
            safeSearch='none',
            type='video',
            fields='nextPageToken,items(id(videoId),snippet(publishedAt,channelId,title))'
        ).execute()

    except HttpError as e:
        if e.resp.reason == "quotaExceeded":
            #change APIkey
            if keyNum + 1 < len(API_KEYs):
                return api_search_sited(sited_list,videoID_list,keyNum+1,kwargs)
            else:
                raise Exception("quotaExceeded")
        else:
            print ("An Http error %d occurred:\n%s" % (e.resp.status, e.content))
            raise

    #json to list 
    for item in response.get("items", []):
        #if item["id"]["videoId"] not in videoID_list:
        sited_list.append((item["id"]["videoId"],item["snippet"]["title"],item["snippet"]["publishedAt"],item["snippet"]["channelId"]))
    if "nextPageToken" in response:
        nextPageToken = response["nextPageToken"]
        return api_search_sited(sited_list,videoID_list,**{"pageToken":nextPageToken})
    else:
        return sited_list

def api_channel_info(channelID:str, keyNum:int = 0)->Tuple[str,str,str,int]:#(id,name,icon,viewcount)
    try:
        response = youtube(keyNum).videos().list(
            part = 'id,snippet,statistics',
            id = channelID,
            #this does not work for id#pageToken = kwargs["pageToken"] if "pageToken" in kwargs else '',
            fields='items(id,snippet(title,thumbnails(high(url))),statistics(viewCount))'
        ).execute()       

    except HttpError as e:
        if e.resp.reason == "quotaExceeded":
            #change APIkey
            if keyNum + 1 < len(API_KEYs):
                return api_channel_info(channelID,keyNum+1)
            else:
                raise Exception("quotaExceeded")
        else:
            print ("An Http error %d occurred:\n%s" % (e.resp.status, e.content))
            raise
    
    #json to list 
    item = response.get("items", [])
    return (item["id"],item["snippet"]["title"],item["snippet"]["thumbnails"]["high"]["url"],int(item["statistics"]["viewCount"]))
