from django.urls import path
from . import views

urlpatterns = [
    path('q1/', views.q1_synchronous_demo, name='q1_synchronous'),
    path('q2/', views.q2_same_thread_demo, name='q2_same_thread'),
    path('q3/', views.q3_same_transaction_demo, name='q3_same_transaction'),
]
