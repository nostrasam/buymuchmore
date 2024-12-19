from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.generics import *
# Create your views here.

class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        return Notification.objects.filter(recepient=self.request.user)
    

class NotificationDetailView(RetrieveUpdateAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(recepient=self.request.user).get(id=self.kwargs['notification_id'])
    
    def perform_update(self, serializer):
        serializer.save(is_read=True)