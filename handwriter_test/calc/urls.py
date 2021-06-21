from django.urls import include, path
from . import views
from django.contrib import admin
from django.shortcuts import render

urlpatterns = [
    path('', lambda req : render( req, "home.html" ), name='home'),
    path('add', views.add, name='add'),
    path('own_handwriting', lambda req : render( req, "io.html" ), name='own_handwriting'),
    path('upload', views.upload, name='upload')

] + [ path( 'h{}'.format(i), lambda req : views.hx( req, i ), name = 'h{}'.format(i) ) for i in range(1, 7) ]