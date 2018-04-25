from django.contrib import admin
from django.urls import path

from chat.views import RoomView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/room/', RoomView.as_view())
]
