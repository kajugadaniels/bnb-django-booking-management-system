from django.urls import path
from django.conf import settings
from home.views import *
from django.conf.urls.static import static

app_name = 'base'

urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('rooms/', rooms, name="rooms"),
    path('room/<slug>', getRoom, name="getRoom"),
    path('booking/<booking_id>', booking, name="booking"),
    path('success/<booking_id>', paymentSuccess, name="paymentSuccess"),
    path('contact/', contact, name="contact"),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)