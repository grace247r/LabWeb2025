from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from basic_api import views
from basic_api.views import API_objects, API_objects_detail, dosen_objects, dosen_objects_detail, mahasiswa_objects, mahasiswa_objects_detail


urlpatterns = [
    path('basic/', views.API_objects.as_view()),
    path('basic/<int:pk>/', views.API_objects_detail.as_view()),
    path('dosen/', views.dosen_objects.as_view()),
    path('dosen/<int:pk>/', views.dosen_objects_detail.as_view()),
    path('mahasiswa/', views.mahasiswa_objects.as_view()),
    path('mahasiswa/<int:pk>/', views.mahasiswa_objects_detail.as_view()),
    path('list-buku/', views.list_buku, name='list-buku'),
    path('list-buku/edit-buku/<int:id>/', views.edit_buku, name='edit-buku'),
    path('list-buku/create-buku/', views.create_buku, name='create-buku'),



]

urlpatterns = format_suffix_patterns(urlpatterns)