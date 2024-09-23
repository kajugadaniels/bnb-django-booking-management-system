from home.models import *
from django.shortcuts import render, get_object_or_404

def home(request):
    rooms = Room.objects.prefetch_related('images').all()

    featuredRooms = list(rooms)
    random.shuffle(featuredRooms)
    featuredRooms = featuredRooms[:4]

    highestPriceRoom = Room.objects.order_by('-price')[:3]

    context = {
        'featuredRooms': featuredRooms,
        'highestPriceRoom': highestPriceRoom,
    }

    return render(request, 'index.html', context)

def rooms(request):
    rooms = Room.objects.prefetch_related('images').order_by('-created_at').all()

    context = {
        'rooms': rooms,
    }

    return render(request, 'rooms/index.html', context)

def getRoom(request, slug):
    room = get_object_or_404(Room, slug=slug)

    context = {
        'room': room,
    }

    return render(request, 'rooms/show.html', context)