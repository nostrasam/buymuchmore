from rest_framework import serializers
from .models import *

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id','recipient','type','message','content_object','created_at','is_read','action_url',)

        def get_content_object(self,obj):
            # get the string representation of the related object
            if obj.content_object:
                return str(obj.content_object)
            return None
