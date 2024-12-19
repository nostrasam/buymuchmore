from django.urls import path
from .views import *

urlpatterns = [
    path('notifications/',NotificationListView.as_view()),
    path('notification/<int:notification_id>/',NotificationDetailView.as_view())
]