from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    name = models.CharField(max_length=300)
    username = models.CharField(max_length=300, unique=True)
    email = models.CharField(max_length=400, unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.IntegerField(default=0 , null=True)
    profile_image=models.ImageField(null=True, blank=True , upload_to='media/profiles/', default='media/profiles/default_profile_picture.png')
    address = models.TextField()
    is_private_person = models.BooleanField(default=False)
    is_book_store = models.BooleanField(default=False)
    favourite=models.ManyToManyField('bookmanage.books')
    def __str__(self):
        return self.name
