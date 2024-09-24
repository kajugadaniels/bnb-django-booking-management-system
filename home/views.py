from home.forms import *
from home.models import *
from django.shortcuts import render, redirect, get_object_or_404

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
    
    if request.method == 'POST':
        form = RoomReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.room = room
            review.save()
            return redirect('base:getRoom', slug=room.slug)
    else:
        form = RoomReviewForm()

    context = {
        'room': room,
        'form': form,
    }

    return render(request, 'rooms/show.html', context)