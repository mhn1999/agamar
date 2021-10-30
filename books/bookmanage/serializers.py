from rest_framework import serializers
from .models import books

class bookSerializer(serializers.ModelSerializer):
	class Meta:
		model = books
		fields =['id', 'title','book_manage', 'author', 'publisher', 'descripsion', 'created', 'buy',
                  'owner']
