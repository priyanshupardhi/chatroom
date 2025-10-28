from rest_framework import serializers

from chat.models import Message


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = "__all__"