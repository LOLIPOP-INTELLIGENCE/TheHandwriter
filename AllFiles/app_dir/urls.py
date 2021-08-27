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
    path('h6', lambda req : views.hx( req, 6 ), name = 'h6' ),
    path('h7', lambda req : views.hx( req, 7 ), name = 'h7' ),
    path('h8', lambda req : views.hx( req, 8 ), name = 'h8' ),
    path('h9', lambda req : views.hx( req, 9 ), name = 'h9' ),
    path('h10', lambda req : views.hx( req, 10 ), name = 'h10' ),
    path('h11', lambda req : views.hx( req, 11 ), name = 'h11' ),
    path('h12', lambda req : views.hx( req, 12 ), name = 'h12' )
]