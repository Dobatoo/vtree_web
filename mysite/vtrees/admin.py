from django.contrib import admin
from .models import Videos_info, Videos_detail, Channels_info, Channels_detail, Posts, Mentions, Children

# Register your models here.
admin.site.register(Videos_info)
admin.site.register(Videos_detail)
admin.site.register(Channels_info)
admin.site.register(Channels_detail)
admin.site.register(Posts)
admin.site.register(Mentions)
admin.site.register(Children)
