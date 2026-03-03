from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("viewer/", views.meta_viewer, name="meta_viewer"),
    path("download/", views.download_file, name="download_file"),
]