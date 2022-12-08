from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('buy', views.checkout, name='checkout'),
    path('download', views.summary, name='summary'),
    path('payment', views.payment, name='payment'),
]