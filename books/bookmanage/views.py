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