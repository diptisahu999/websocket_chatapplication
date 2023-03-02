from api.views import chat_box
from django.urls import path
from .import views

urlpatterns = [
    path("chat/<str:chat_box_name>/",views.chat_box, name="chat"),
]