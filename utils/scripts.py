from ..mysite.vtrees.models import Videos

def description_search(description:str)->list(list(str),list(str)):
    pass


def register_channel_info(channelID:str, type:int)->None:
    pass

def calculate_channel_sited_sum(channelID:str)->None:
    pass

def calculate_channel_mentioned_sum(channelID:str)->None:
    pass

def register_video_info(videoID:str)->None:
    pass

def register_video_detail(videoID:str)->None:
    pass

def calculate_video_sited(videoID:str)->None:
    pass

def register_post(channelID:str,videoID:str)->None:
    pass

def register_parent(videoID_parent:str,videoID_child:str)->None:
    pass

def register_mention(channelID:str,videoID:str)->None:
    pass
