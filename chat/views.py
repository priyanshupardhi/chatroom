from django.db.models.expressions import DatabaseDefault
from django.http import response
from .models import Message
from rest_framework.views import APIView
from rest_framework.response import Response
from chat.serializers import LoginSerializer, MessageSerializer

class LoginAPI(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        print(serializer)

        if not serializer.is_valid():
            return Response(status=400, data="Invalid username")
        request.session["username"] = request.data.get("username")
        return Response(status=200, data="Successfully Logged In")
    
class ChatRoomAPI(APIView):
    def get(self, request, room_name="general"):
        username = request.session.get("username")
        message = Message.objects.filter(room_name=room_name).order_by("-timestamp"[:20])
        if not username:
            return Response(status=401, data="Not found")
        data = [m.to_dict for m in reversed(message)]

        result = MessageSerializer(message, many=True)
        
        return Response(status=200, data=result.data)

    