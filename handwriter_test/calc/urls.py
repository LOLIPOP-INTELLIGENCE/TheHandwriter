from django.urls import include, path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('add', views.add, name='add'),
    path('own_handwriting', views.own_handwriting, name='own_handwriting'),
    path('upload', views.upload, name='upload'),

]