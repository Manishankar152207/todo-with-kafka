from django.shortcuts import render, get_object_or_404
from .models import Task
from .serializers import TaskSerializer
from rest_framework import status, viewsets
from mainapp.helpers import activity_feed
# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def destroy(self, request, pk=None):
        task = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(task)
        activity_feed(serializer.data, "DEL")
        return super().destroy(request=request, pk=pk)
