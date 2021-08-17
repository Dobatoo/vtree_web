import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class Videos(models.Model):
    videos_id = models.SlugField(max_length=11,primary_key=True)
    videos_title = models.TextField(max_length=100)
    videos_description = models.TextField(max_length=5000)
    videos_count_original = models.BigIntegerField(default=0)
    videos_count_sited = models.BigIntegerField(default=0)
    videos_lastupdate = models.DateTimeField(auto_now=True) #use DateTimeField

    def __str__(self) -> str:
        return self.videos_title + "(" + self.videos_id + ")"

    def was_updated_within24h(self) -> bool:
        return self.videos_lastupdate >= timezone.now() - datetime.timedelta(days=1)

