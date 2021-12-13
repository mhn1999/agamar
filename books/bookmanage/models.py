from django.db import models
from authentication.models import CustomUser
import uuid
from django.db.models.deletion import CASCADE
# Create your models here.
class books(models.Model):
    buy_type=(
        ('0','sell'),
        ('1','rent'),
        ('2','gift'),
    )
    book_category=(('0','داستان و رمان'), ('1','ادبیات'),('2') )
    #id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
    id = models.BigAutoField(primary_key=True)
    price=models.IntegerField(null=True, blank=True)
    title=models.CharField(max_length=200)
    author=models.CharField(max_length=200)
    publisher=models.CharField(max_length=200)
    descripsion=models.TextField(null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    #category=models.CharField
    profile_image=models.ImageField(null=True, blank=True, upload_to='media/profiles/', default='media/profiles/books-default.png' )
    owner=models.ForeignKey(CustomUser, on_delete=CASCADE)
    buy=models.CharField(max_length=200,choices=buy_type, null=True)

    def __str__(self):
        return self.title
