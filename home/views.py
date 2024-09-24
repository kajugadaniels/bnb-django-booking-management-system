from home.forms import *
from home.models import *
from django.db.models import Avg
from django.contrib import messages
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
    reviews = RoomReview.objects.filter(room=room).order_by('-created_at')

    total_reviews = reviews.count()

    avg_location = reviews.aggregate(Avg('location'))['location__avg'] or 0
    avg_staff = reviews.aggregate(Avg('staff'))['staff__avg'] or 0
    avg_cleanliness = reviews.aggregate(Avg('cleanliness'))['cleanliness__avg'] or 0
    avg_value_for_money = reviews.aggregate(Avg('value_for_money'))['value_for_money__avg'] or 0
    avg_comfort = reviews.aggregate(Avg('comfort'))['comfort__avg'] or 0
    avg_facilities = reviews.aggregate(Avg('facilities'))['facilities__avg'] or 0
    avg_free_wifi = reviews.aggregate(Avg('free_wifi'))['free_wifi__avg'] or 0

    overall_rating = (avg_location + avg_staff + avg_cleanliness + avg_value_for_money + avg_comfort + avg_facilities + avg_free_wifi) / 7

    # Handle the review form submission
    if request.method == 'POST':
        form = RoomReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.room = room  # Associate the review with the room
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('base:getRoom', slug=room.slug)  # Adjust the URL name as needed
    else:
        form = RoomReviewForm()

    context = {
        'room': room,
        'reviews': reviews,
        'total_reviews': total_reviews,
        'overall_rating': overall_rating,
        'avg_location': avg_location,
        'avg_staff': avg_staff,
        'avg_cleanliness': avg_cleanliness,
        'avg_value_for_money': avg_value_for_money,
        'avg_comfort': avg_comfort,
        'avg_facilities': avg_facilities,
        'avg_free_wifi': avg_free_wifi,
        'form': form,
    }

    return render(request, 'rooms/show.html', context)