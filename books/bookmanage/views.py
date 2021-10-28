from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import bookSerializer

from .models import books 

# Create your views here.
@api_view(['GET'])
def bookList(request):
	book = books.objects.all().order_by('-id')
	serializer = bookSerializer(book, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def bookDetail(request, pk):
	book = books.objects.get(id=pk)
	serializer = bookSerializer(book, many=False)
	return Response(serializer.data)

@api_view(['POST'])
def bookCreate(request):
	serializer = bookSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
def bookUpdate(request, pk):
	book = books.objects.get(id=pk)
	serializer = bookSerializer(instance=book, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
def bookDelete(request, pk):
	task = books.objects.get(id=pk)
	task.delete()

	return Response('Item succsesfully delete!')