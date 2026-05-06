from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservation_list, name='reservation_list'),
    path('create/<int:car_id>/', views.create_reservation, name='create_reservation'),
    path('success/', views.reservation_success, name='reservation_success'),
    path('contract/<int:reservation_id>/', views.generate_contract, name='generate_contract'),
    path('payment/<int:reservation_id>/', views.payment_page, name='payment_page'),
    path('payment/success/<int:reservation_id>/', views.payment_success, name='payment_success'),
    path('history/', views.history, name='history'),
]