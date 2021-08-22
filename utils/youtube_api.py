import json,datetime
from apiclient.discovery import build
from apiclient.errors import HttpError
from typing import List, Tuple, Dict

API_KEY = 'AIzaSyB4uBZIDnaS720IVf5qfwvYcrKSb9oiqRw' #hide later
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
)

def api_search_post(post_list,channelID:str, **kwargs:Dict[str,str]) -> List[Tuple[str,str]]:
    try:
        response = youtube.search().list(
            part = 'id,snippet',
            channelId=channelID,
            maxResults = 50,
            order = 'viewCount',
            pageToken = kwargs["pageToken"] if "pageToken" in kwargs else '',
            safeSearch='none',
            type='video',
            fields='nextPageToken,items(id(videoId),snippet(channelId,title))'
        ).execute()

    except HttpError as e:
        if e.resp.reason == "quotaExceeded":
            #change APIkey
            raise Exception("quotaExceeded")
        else:
            print ("An Http error %d occurred:\n%s" % (e.resp.status, e.content))
            raise e

    #json to list 
    for item in response.get("items", []):
        if item["snippet"]["channelId"] == channelID:
            post_list.append((item["id"]["videoId"],item["snippet"]["title"]))
            
    if "nextPageToken" in response:
        nextPageToken = response["nextPageToken"]
        return api_search_post(post_list,channelID,**{"pageToken":nextPageToken})
    else:
        return post_list

def api_video(video_info_list,videoID_list:List[str], **kwargs:Dict[str,str]) -> List[Tuple[str,str,int]]:
    try:
        response = youtube.videos().list(
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
            raise
        else:
            print ("An Http error %d occurred:\n%s" % (e.resp.status, e.content))
            raise

def api_search_sited(sited_list,videoID:str,**kwargs:Dict[str,str]) -> List[Tuple[str,str,str]]:
    print("Lets go")
    try:
        response = youtube.search().list(
            part = 'id,snippet',
            maxResults = 50,
            order = 'relevance',
            pageToken = kwargs["pageToken"] if "pageToken" in kwargs else '',
            q=videoID,
            safeSearch='none',
            type='video',
            fields='nextPageToken,items(id(videoId),snippet(channelId,title))'
        ).execute()

    except HttpError as e:
        if e.resp.reason == "quotaExceeded":
            #change APIkey
            raise
        else:
            print ("An Http error %d occurred:\n%s" % (e.resp.status, e.content))
            raise

    #json to list 
    for item in response.get("items", []):
        if item["id"]["videoId"] != videoID:
            sited_list.append((item["id"]["videoId"],item["snippet"]["title"],item["snippet"]["channelId"]))
    if "nextPageToken" in response:
        nextPageToken = response["nextPageToken"]
        print("next : "+ nextPageToken)
        return api_search_sited(sited_list,videoID,**{"pageToken":nextPageToken})
    else:
        print("the final")
        return sited_list

def api_channel_info(channelID:str)->Tuple[str,str,str,int]:#(id,name,icon,viewcount)
    try:
        response = youtube.videos().list(
            part = 'id,snippet,statistics',
            id = channelID,
            #this does not work for id#pageToken = kwargs["pageToken"] if "pageToken" in kwargs else '',
            fields='items(id,snippet(title,thumbnails(high(url))),statistics(viewCount))'
        ).execute()       

    except HttpError as e:
        if e.resp.reason == "quotaExceeded":
            #change APIkey
            raise
        else:
            print ("An Http error %d occurred:\n%s" % (e.resp.status, e.content))
            raise
    
    #json to list 
    item = response.get("items", [])
    return (item["id"],item["snippet"]["title"],item["snippet"]["thumbnails"]["high"]["url"],item["statistics"]["viewCount"])