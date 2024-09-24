from home.forms import *
from home.models import *
from datetime import datetime
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

    if request.method == 'POST':
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')

        # Convert strings to date objects
        try:
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Please select valid dates.")
            return redirect('base:getRoom', slug=room.slug)

        today = datetime.today().date()

        # Validate the dates
        if check_in_date < today:
            messages.error(request, "Check-in date cannot be in the past.")
            return redirect('base:getRoom', slug=room.slug)

        if check_out_date <= check_in_date:
            messages.error(request, "Check-out date must be after the check-in date.")
            return redirect('base:getRoom', slug=room.slug)

        # Check if the room is already booked for the selected dates
        existing_booking = Booking.objects.filter(
            room=room,
            checkInDate__lte=check_out_date,
            checkOutDate__gte=check_in_date
        ).exists()

        if existing_booking:
            messages.error(request, "These dates are already booked. Please choose different dates.")
            return redirect('base:getRoom', slug=room.slug)

        # If everything is okay, redirect to booking page with query parameters
        return redirect(f'/room/{slug}/booking?room_id={room.id}&check_in_date={check_in_date}&check_out_date={check_out_date}')

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
    }

    return render(request, 'rooms/show.html', context)

def booking(request, slug):
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

    overall_rating = (avg_location + avg_staff + avg_cleanliness + avg_value_for_money +
                      avg_comfort + avg_facilities + avg_free_wifi) / 7

    # Initialize form with None or prefilled if booking was successful
    form = BookingForm()
    success = False
    booking_id = request.GET.get('booking_id')

    # Check if a booking has been made and populate the form if booking_id exists
    if booking_id:
        booking = get_object_or_404(Booking, id=booking_id)
        form = BookingForm(instance=booking)
        success = True

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.checkInDate = request.POST.get('checkInDate')
            booking.checkOutDate = request.POST.get('checkOutDate')
            booking.save()

            # Redirect back to the same page with the booking_id in the query parameters
            return redirect(f"{request.path}?booking_id={booking.id}")

    context = {
        'room': room,
        'reviews': reviews,
        'total_reviews': total_reviews,
        'overall_rating': overall_rating,
        'form': form,
        'success': success,  # Pass success flag to show success message
        'total_length_of_stay': (form.cleaned_data['checkOutDate'] - form.cleaned_data['checkInDate']).days if form.is_valid() else None,
    }

    return render(request, 'booking.html', context)