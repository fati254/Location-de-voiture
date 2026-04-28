from django.urls import path
from .views import home, CarListView , contact, propos , avis

urlpatterns = [
    path('', home, name='home'), #accueil
    path('list/', CarListView.as_view(), name='cars_list'), #as_view pour les class
    path('contact/',contact, name='contact'),
    path('propos/',propos, name= 'propos'),
    path('avis/',avis, name='avis'),

]