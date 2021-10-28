from django.urls import path
from . import views

urlpatterns = [
#	path('', views.apiOverview, name="api-overview"),
	path('book-list/', views.bookList, name="book-list"),
	path('book-detail/<str:pk>/', views.bookDetail, name="book-detail"),
	path('book-create/', views.bookCreate, name="book-create"),

	path('book-update/<str:pk>/', views.bookUpdate, name="book-update"),
	path('book-delete/<str:pk>/', views.bookDelete, name="book-delete"),
]
