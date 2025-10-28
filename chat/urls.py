from django.urls import path
from chat.views import LoginAPI, ChatRoomAPI


urlpatterns = [
    path("login", LoginAPI.as_view()),
    path("room", ChatRoomAPI.as_view())
]