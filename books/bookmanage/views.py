import re
from django.db.models.fields import NullBooleanField
from django.shortcuts import render
from django.http import JsonResponse, multipartparser
from rest_framework import permissions, status, generics
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from .serializers import bookSerializer
from django.db.models import Q
from authentication.models import CustomUser

from django.core.files.uploadedfile import InMemoryUploadedFile
import base64
import io
from PIL import Image
from rest_framework.parsers import MultiPartParser,FormParser

from .models import books 

# Create your views here.
class bookList(APIView):
	def get(self,request):
		book = books.objects.all().order_by('-created')
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
	parser_classes=[MultiPartParser, FormParser]
	def post(self,request):
		serializer = bookSerializer(data=request.data, partial=True)

		if serializer.is_valid():
			serializer.save()

		return Response({"message": serializer.data})


class bookUpdate(APIView):
	permissions = [permissions.IsAuthenticated]
	parser_classes=[MultiPartParser, FormParser]
	def post(self,request,pk):	
		book = books.objects.get(id=pk)
		serializer = bookSerializer(instance=book, data=request.data ,partial=True)

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
		print(request.data)
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
			if (ad_price_min==""):
				ad_price_min="0"
		else:
			ad_price_min="0"
		if ("ad_price_max" in request.data):
			ad_price_max=request.data["ad_price_max"]
			if(ad_price_max==""):
				ad_price_max="1000000"
		else:
			ad_price_max="1000000"
		if ("ad_date_to" in request.data):
			ad_date_to=request.data["ad_date_to"]
			if ad_date_to=="":
				ad_date_to="2022-11-13T12:12:51.295411Z"
		else:
			ad_date_to="2022-11-13T12:12:51.295411Z"
		if ("ad_date_from" in request.data):
			ad_date_from=request.data["ad_date_from"]
			if ad_date_from=="":
				ad_date_from="2020-11-13T12:12:51.295411Z"	
		else:
			ad_date_from="2020-11-13T12:12:51.295411Z"	
		if ("buy" in request.data):
			s_buy=request.data["buy"]	
		else:
			s_buy=""			
		l_buy=re.split(',|\[|\]',s_buy)
		if l_buy[1]=='1':
			l_buy[1]='0'
		if l_buy[2]=='1':
			l_buy[2]='1'
		if l_buy[3]=='1':
			l_buy[3]='2'

		if "category" in request.data:
			category_buy=request.data["category"]
			for i in category_buy:
				if i==category_buy[0]:
					Qbook=books.objects.distinct().filter(category__exact=i)
				else:
					Qbook= Qbook | books.objects.distinct().filter(category__exact=i)
			print(Qbook)
		else:
			Qbook=[]
		book=books.objects.distinct().filter(Q(title__icontains=s_title) & Q(publisher__icontains=s_publisher) & Q(author__icontains=s_author)
				& Q(created__range=[ad_date_from, ad_date_to]) & Q(price__range=[int(ad_price_min), int(ad_price_max)]) & (Q(buy__icontains=l_buy[1]) | Q(buy__icontains=l_buy[2]) | Q(buy__icontains=l_buy[3]) ))
		if Qbook !=[]:
			book= book & Qbook
		#print(book)
		serializer = bookSerializer(book, many=True)
		return Response(serializer.data)	
		# & Q(price__range=[ad_price_min, ad_price_max])
# adding and getting favourites
class add_to_favourites(APIView):
	permissions = [permissions.IsAuthenticated]
	def post(self,request,pk):	
		book = books.objects.get(id=pk)
		user=request.user
		user.favourite.add(book)
		return Response({"message":"item succesgully added to favourites"})
#ordering books
class add_to_buylist(APIView):
	permissions = [permissions.IsAuthenticated]
	def post(self,request,pk):	
		book = books.objects.get(id=pk)
		user=request.user
		user.books_ordered.add(book)
		return Response({"message":"item succesgully added to basket"})

class get_favourites(APIView):
	permissions = [permissions.IsAuthenticated]
	def get(self,request):
		user=request.user
		book = user.favourite.all()
		serializer = bookSerializer(book, many=True)
		return Response(serializer.data)	

'''
class bookimage(APIView):
	#permissions = [permissions.IsAuthenticated]
	def post(self,request):

		img = decodeDesignImage(data=request.data["profile_image"])
		book=books.objects.get(id=request.data["id"])
		print(book.profile_image)
		print(img)
		img_io = io.BytesIO()
		img.save(img_io, format='JPEG')
		design.image = InMemoryUploadedFile(img_io, field_name=None, name=token+".jpg", content_type='image/jpeg', size=img_io.tell, charset=None)
		design.save()
		#if img.is_valid():
		#book.profile_image=img
		#book.save()

		return Response({"message": img.data})
def decodeDesignImage(data):
    try:
        data = base64.b64decode(data.encode('UTF-8'))
        buf = io.BytesIO(data)
        img = Image.open(buf)
        return img
    except:
        return None
		'''