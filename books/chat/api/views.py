from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from chat.models import Chat, Contact
from chat.views import get_user_contact



class ChatListView(ListAPIView):
    pass


class ChatDetailView(RetrieveAPIView):
    pass


class ChatCreateView(CreateAPIView):
    pass


class ChatUpdateView(UpdateAPIView):
    pass


class ChatDeleteView(DestroyAPIView):
    pass