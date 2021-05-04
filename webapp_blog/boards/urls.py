from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
     path('', views.index, name = 'index'),
     path('contact',views.contact, name = 'contact' ),
     path('home',views.HomeView.as_view(), name = 'home' ),
]