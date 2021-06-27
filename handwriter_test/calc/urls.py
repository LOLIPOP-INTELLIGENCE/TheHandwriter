from django.urls import include, path
from . import views
from django.contrib import admin
from django.shortcuts import render

urlpatterns = [
    path('', lambda req : render( req, "hm.html" ), name='hm'),
    path('add', views.add, name='add'),
    path('own_handwriting', lambda req : render( req, "io.html" ), name='own_handwriting'),
    path('upload', views.upload, name='upload'),
    path('h1', lambda req : views.hx( req, 1 ), name = 'h1' ),
    path('h2', lambda req : views.hx( req, 2 ), name = 'h2' ),
    path('h3', lambda req : views.hx( req, 3 ), name = 'h3' ),
    path('h4', lambda req : views.hx( req, 4 ), name = 'h4' ),
    path('h5', lambda req : views.hx( req, 5 ), name = 'h5' ),
    path('h6', lambda req : views.hx( req, 6 ), name = 'h6' )
]