from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservation_list, name='reservation_list'),
    path('create/<int:car_id>/', views.create_reservation, name='create_reservation'),
    path('success/', views.reservation_success, name='reservation_success'),
]
