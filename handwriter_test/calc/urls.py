from django.urls import include, path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('add', views.add, name='add'),
    path('h1', views.h1, name='h1'),
    path('h2', views.h2, name='h2'),
    path('h3', views.h3, name='h3'),
    path('h4', views.h4, name='h4'),
    path('h5', views.h5, name='h5'),
    path('h6', views.h6, name='h6'),
    path('own_handwriting', views.own_handwriting, name='own_handwriting'),
    path('upload', views.upload, name='upload'),

]