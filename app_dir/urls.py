from django.urls import include, path
from . import views
from django.contrib import admin
from django.shortcuts import render

urlpatterns = [
    path('', lambda req : render( req, "hm.html" ), name='hm'),
    path('res', views.serveImgPostReq, name = 'res' ),
    path('result/<slug:path>', views.renderResult, name = 'result'),
    path('add', views.add, name='add'),
    path('own_handwriting', lambda req : render( req, "io.html" ), name='own_handwriting'),
    path('upload', views.upload, name='upload'),
]