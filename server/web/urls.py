from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog', views.blog, name='blog'),
    path('blog/<slug:slug>', views.blog_read, name='blog_read'),
    path('events', views.events, name='events'),
    path('events/<slug:slug>', views.events_details, name='events_details'),
    path('events_json/', views.events_json, name='events_json'),
    path('enquiry', views.enquiry, name='enquiry'),
]
