from django.db import models
from authentication.models import CustomUser
import uuid
from django.db.models.deletion import CASCADE
# Create your models here.
class books(models.Model):
    buy_type=(
        (0,'sell'),
        (1,'rent'),
        (2,'gift'),
    )
    title=models.CharField(max_length=200)
    author=models.CharField(max_length=200)
    publisher=models.CharField(max_length=200)
    descripsion=models.TextField(null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    #category=models.CharField
    #picture=
    user=models.ForeignKey(CustomUser, on_delete=CASCADE)
    buy=models.CharField(max_length=200,choices=buy_type, null=True)
    id=models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title
