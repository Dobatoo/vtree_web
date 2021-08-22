
import json
from apiclient.discovery import build
from apiclient.errors import HttpError

API_KEY = 'AIzaSyB4uBZIDnaS720IVf5qfwvYcrKSb9oiqRw' #hide later
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

video_id = 'XZKIxpJQDuA'#'FwEMauCv8q0'#,L89Mp0NCo3o'   #shout not be constatnt

youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
)

try:
#    response = youtube.videos().list(
#        part = 'snippet,statistics',
#        id = video_id,
#        fields = 'items(kind,snippet(channelId,title,description),statistics(viewCount))'
#    ).execute()
    response2 = youtube.search().list(
        part = 'id,snippet',
        maxResults = 50,
        order = 'relevance',#date
        q=video_id,
        safeSearch='none',
        type='video',
        fields='nextPageToken,items(id(videoId),snippet(title,channelTitle))'
    ).execute()
except HttpError as e:
    print ("An Http error %d occurred:\n%s" % (e.resp.status, e.content))

for item in response.get("items", []):
    #if item["kind"] != "youtube#video":
    #    continue
    print("ここから")
    print(json.dumps(item, indent=2, ensure_ascii=False))
    print("ここまで")