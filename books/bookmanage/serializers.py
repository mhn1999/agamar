from rest_framework import serializers
from .models import books

class bookSerializer(serializers.ModelSerializer):
	class Meta:
		model = books
		fields =['id', 'title','profile_image', 'author', 'publisher', 'descripsion', 'created', 'buy',
                  'owner']