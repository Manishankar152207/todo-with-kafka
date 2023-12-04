from django.contrib import admin
from .models import Task
from .serializers import TaskSerializer

admin.site.site_header = "My ToDo App"
admin.site.site_title = "Admin"
admin.site.index_title = "My Dashboard"


class TaskAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ['name', 'deadline', 'is_complete']
    list_filter = ('is_complete',)

admin.site.register(Task, TaskAdmin)