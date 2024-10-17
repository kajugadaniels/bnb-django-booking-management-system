from home.views import *
from django.conf import settings
from django.urls import path, re_path
from django.conf.urls.static import static

app_name = 'base'

urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('rooms/', rooms, name="rooms"),
    path('room/<slug>', getRoom, name="getRoom"),
    path('booking/<booking_id>', booking, name="booking"),
    path('success/<booking_id>', paymentSuccess, name="paymentSuccess"),
    path('blogs/', blogs, name="blogs"),
    path('blog/<slug>', getBlog, name="getBlog"),
    path('contact/', contact, name="contact"),
    path('restaurant/', restaurant, name="restaurant"),
    path('food/<slug>', getFood, name="getFood"),
    path('not-found/', notFound, name="notFound"),
    
    # Catch-all pattern for 404 errors
    # re_path(r'^.*$', notFound, name='notFound'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
