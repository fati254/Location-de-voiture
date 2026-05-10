from django.urls import path
from .views import home, CarListView , contact, propos , avis
from .views import home, cars_list, contact, propos, avis, ai_chat_search , notifications , mark_notification_read
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'), #accueil
    path('list/', cars_list, name='cars_list'),#as_view pour les class
    path('contact/',contact, name='contact'),
    path('propos/',propos, name= 'propos'),
    path('avis/',avis, name='avis'),
    path('ai-chat/',ai_chat_search, name='ai_chat'),
    path('notifications/', notifications, name='notifications'),
    path('notifications/read/<int:notification_id>/',mark_notification_read,name='mark_notification_read'
),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)