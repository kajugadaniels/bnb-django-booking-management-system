from home.models import *
from django.shortcuts import render

def home(request):
    featuredRooms = Room.objects.order_by('-created_at')[:3]
    highestPriceRoom = Room.objects.order_by('-price')[:3]

    context = {
        'featuredRooms': featuredRooms,
        'highestPriceRoom': highestPriceRoom,
    }

    return render(request, 'index.html', context)