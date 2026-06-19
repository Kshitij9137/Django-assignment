from django.urls import path
from . import views

urlpatterns = [
    path('rectangle/', views.rectangle_demo, name='rectangle_demo'),
]
