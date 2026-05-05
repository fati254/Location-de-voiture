from django.urls import path
from .views import home, CarListView , contact, propos , avis
from .views import home, cars_list, contact, propos, avis
urlpatterns = [
    path('', home, name='home'), #accueil
   path('list/', cars_list, name='cars_list'),#as_view pour les class
    path('contact/',contact, name='contact'),
    path('propos/',propos, name= 'propos'),
    path('avis/',avis, name='avis'),

]
