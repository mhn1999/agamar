import re
from django.db.models.fields import NullBooleanField
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions, status, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import bookSerializer
from django.db.models import Q

from .models import books 

# Create your views here.
class bookList(APIView):
	def get(self,request):
		book = books.objects.all().order_by('-id')
		serializer = bookSerializer(book, many=True)
		return Response(serializer.data)
	
class bookDetail(APIView):
	def get(self,request,pk):
		book = books.objects.get(id=pk)
		serializer = bookSerializer(book, many=False)
		return Response(serializer.data)
		
'''
@api_view(['POST'])
def bookCreate(request):
	serializer = bookSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)
'''
class bookCreate(APIView):
	permissions = [permissions.IsAuthenticated]
	def post(self,request):
		serializer = bookSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()

		return Response({"message": serializer.data})

class bookUpdate(APIView):
	permissions = [permissions.IsAuthenticated]
	def post(self,request,pk):	
		book = books.objects.get(id=pk)
		serializer = bookSerializer(instance=book, data=request.data)

		if serializer.is_valid():
			serializer.save()

		return Response(serializer.data)	


class bookDelete(APIView):
	permissions = [permissions.IsAuthenticated]
	def delete(self,request,pk):
		task = books.objects.get(id=pk)
		task.delete()

		return Response('Item succsesfully delete!')
#search
class bookfind(APIView):
	def get(self,request,pk):
		book=books.objects.distinct().filter(Q(title__icontains=pk) | Q(publisher__icontains=pk) | Q(author__icontains=pk))
		serializer = bookSerializer(book, many=True)
		return Response(serializer.data)
class bookfind_a(APIView):
	def post(self,request):
		if ("author" in request.data):
			s_author=request.data["author"]
		else:
			s_author=""
		if ("title" in request.data):
			s_title=request.data["title"]
		else:
			s_title=""
		if ("publisher" in request.data):
			s_publisher=request.data["publisher"]
		else:
			s_publisher=""
		if ("ad_price_min" in request.data):
			ad_price_min=request.data["ad_price_min"]
		else:
			ad_price_min="0"
		if ("ad_price_max" in request.data):
			ad_price_max=request.data["ad_price_max"]
		else:
			ad_price_max="1000000"
		if ("ad_date_to" in request.data):
			ad_date_to=request.data["ad_date_to"]
		else:
			ad_date_to="2022-11-13T12:12:51.295411Z"
		if ("ad_date_from" in request.data):
			ad_date_from=request.data["ad_date_from"]	
		else:
			ad_date_from="2020-11-13T12:12:51.295411Z"	
		if ("buy" in request.data):
			s_buy=request.data["buy"]	
		else:
			s_buy=""			
					
		book=books.objects.distinct().filter(Q(title__icontains=s_title) & Q(publisher__icontains=s_publisher) & Q(author__icontains=s_author)
				& Q(created__range=[ad_date_from, ad_date_to]) & Q(price__range=[int(ad_price_min), int(ad_price_max)]) & Q(buy__icontains=s_buy) )
		print(book)
		serializer = bookSerializer(book, many=True)
		return Response(serializer.data)	
		# & Q(price__range=[ad_price_min, ad_price_max])	
