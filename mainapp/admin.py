from django.contrib import admin
from .models import ActivityFeed
from .serializers import ActivityFeedSerializer

class ActivityFeedAdmin(admin.ModelAdmin):
    list_display = ['user', 'data',]
    list_filter = ('user',)

admin.site.register(ActivityFeed, ActivityFeedAdmin)