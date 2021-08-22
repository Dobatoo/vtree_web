import datetime
from typing_extensions import TypeGuard
#from home.username.workspace.vtree_web.mysite.vtrees.views import video #???
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import OneToOneField
from django.utils import timezone

# Create your models here.

class Videos_info(models.Model):
    #basic info
    videos_id = models.SlugField(max_length=11,primary_key=True)
    videos_title = models.CharField(max_length=100)
    videos_published = models.DateTimeField()
    

    def __str__(self) -> str:
        return self.videos_title + "(" + self.videos_id + ")"

    #def was_updated_within24h(self) -> bool:
    #    return self.videos_lastupdate >= timezone.now() - datetime.timedelta(days=1)

class Videos_detail(models.Model):
    #id
    videos_id = models.OneToOneField(
        'Videos_info',
        on_delete=models.CASCADE,
        primary_key=True
    )
    #detail
    videos_description = models.TextField(max_length=5000)
    videos_count_original = models.BigIntegerField(default=0)
    videos_detail_lastupdate = models.DateTimeField()
    #view count sited
    videos_count_sited = models.BigIntegerField(default=0)
    videos_count_sited_lastupdate = models.DateTimeField(null=True,blank=True)

    def __str__(self) -> str:
        return self.videos_id + "(" + self.videos_count_original + ")"

    def was_sited_counted(self)->bool:
        return self.videos_count_sited_lastupdate is not None


class Channels_info(models.Model):
    channels_id = models.SlugField(max_length=24,primary_key=True)
    channels_title = models.CharField(max_length=100)
    channels_count_total = models.BigIntegerField(default=0)
    channels_icon_url = models.URLField()
    channels_isRegistered = models.BooleanField(default=False)
    channels_info_lastupdate = models.DateTimeField()

    def __str__(self) -> str:
        return self.channels_title + "("+ self.channels_id +")"

    def isRegistered(self)->bool:
        return self.channels_isRegistered

class Channels_detail(models.Model):
    channels_id = models.OneToOneField(
        'Channels_info',
        on_delete=models.CASCADE,
        primary_key=True
    )
    channels_count_sited_sum = models.BigIntegerField(default=0)
    channels_count_sited_sum_lastupdate = models.DateTimeField(null=True,blank=True)
    channels_count_mentioned_sum = models.BigIntegerField(default=0)
    channels_count_mentioned_sum_lastupdate = models.DateTimeField(null=True,blank=True)

    def __str__(self) -> str:
        return self.channels_id

    def was_sited_sum_counted(self)->bool:
        return self.channels_count_sited_sum_lastupdate is not None
    
    def was_mentioned_sum_counted(self)->bool:
        return self.channels_count_mentioned_sum_lastupdate is not None


class Posts(models.Model):
    posts_video_id = models.OneToOneField(
        'Videos_info',
        on_delete=models.CASCADE,
        primary_key=True
    )
    posts_channel_id = models.SlugField(max_length=24)

    def __str__(self) -> str:
        return self.posts_channel_id + " posted "+ self.posts_video_id

class Mentions(models.Model):
    mentions_video_id = models.ForeignKey(
        'Videos_info',
        on_delete=models.CASCADE
    )
    mentions_channel_id = models.SlugField(max_length=24)
    UniqueConstraint(
        fields=['mentions_video_id', 'mentions_channel_id'],
        name='Mentions_primary_key'
    )

    def __str__(self) -> str:
        return self.mentions_channel_id + "is mentioned in" + self.mentions_video_id

class Children(models.Model):
    children_video_child = models.ManyToManyField(
        'Videos_info',
        related_name='child_table'
    )
    children_video_parent = models.ManyToManyField(
        'Videos_info',
        related_name='parent_table'
    )
    UniqueConstraint(
        fields=['children_video_child', 'children_video_parent'],
        name='Children_primary_key'
    )

    def __str__(self) -> str:
        return self.children_video_child + "is child of"+ self.children_video_parent
