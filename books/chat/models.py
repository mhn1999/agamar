from django.contrib.auth import get_user_model
from django.db import models
from authentication.models import CustomUser
User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(CustomUser, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    contact = models.ForeignKey(
        Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    reply=models.OneToOneField('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Chat(models.Model):
    participants = models.ManyToManyField(
        Contact, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return "{}".format(self.pk)