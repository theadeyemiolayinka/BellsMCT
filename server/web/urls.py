from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('events_json/', views.events_json, name='events_json'),
]
