from django.urls import path
from . import views

urlpatterns = [
#	path('', views.apiOverview, name="api-overview"),
	path('book-list/', views.bookList.as_view(), name="book-list"),
	path('book-detail/<str:pk>/', views.bookDetail.as_view(), name="book-detail"),
	path('book-create/', views.bookCreate, name="book-create"),

	path('book-update/<str:pk>/', views.bookUpdate.as_view(), name="book-update"),
	path('book-delete/<str:pk>/', views.bookDelete.as_view(), name="book-delete"),
]
