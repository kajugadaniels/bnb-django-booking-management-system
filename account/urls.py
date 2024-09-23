from django.urls import path
from django.conf import settings
from account.views import *
from django.conf.urls.static import static

app_name = 'auth'

urlpatterns = [
    # path('login/', user_login, name="login"),
    # path('register/', user_register, name="register"),
    # path('logout/', user_logout, name='logout'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)