import logging
from home.forms import *
from home.models import *
from decimal import Decimal
from datetime import datetime
from django.db.models import Avg
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

def home(request):
    rooms = Room.objects.prefetch_related('images').all()

    featuredRooms = list(rooms)
    random.shuffle(featuredRooms)
    featuredRooms = featuredRooms[:4]

    highestPriceRoom = Room.objects.order_by('-id')[:3]
    
    # Get the selected currency from the query params or session (default to RWF)
    selected_currency = request.GET.get('currency', request.session.get('currency', 'RWF'))

    # Store selected currency in session
    request.session['currency'] = selected_currency

    # Collect review data for each room in featuredRooms
    for room in featuredRooms:
        review_data = room.get_review_data()
        room.total_reviews = review_data['total_reviews']
        room.overall_rating = review_data['overall_rating']

    # Collect review data for each room in highestPriceRoom
    for room in highestPriceRoom:
        review_data = room.get_review_data()
        room.total_reviews = review_data['total_reviews']
        room.overall_rating = review_data['overall_rating']

    settings = Setting.objects.first()

    context = {
        'featuredRooms': featuredRooms,
        'highestPriceRoom': highestPriceRoom,
        'settings': settings,
        'selected_currency': selected_currency,
    }

    return render(request, 'index.html', context)


def about(request):
    team = Team.objects.all()
    testimonies = Testimony.objects.filter(status=True)

    happy_people_count = testimonies.count()

    # Calculate the average rating
    average_rating = testimonies.aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating, 2)
    settings = Setting.objects.first()

    context = {
        'team': team,
        'testimonies': testimonies,
        'happy_people_count': happy_people_count,
        'average_rating': average_rating,
        'settings': settings
    }

    return render(request, 'about.html', context)

def rooms(request):
    rooms = Room.objects.prefetch_related('images', 'amenities').order_by('-created_at').all()
    rooms_count = rooms.count()

    # Default currency is RWF
    selected_currency = request.GET.get('currency', request.session.get('currency', 'RWF'))
    
    # Store selected currency in the session
    request.session['currency'] = selected_currency

    # Collect review data for each room
    for room in rooms:
        review_data = room.get_review_data()
        room.total_reviews = review_data['total_reviews']
        room.overall_rating = review_data['overall_rating']

    settings = Setting.objects.first()

    context = {
        'rooms': rooms,
        'rooms_count': rooms_count,
        'settings': settings,
        'selected_currency': selected_currency,  # Pass selected currency to the template
    }

    return render(request, 'rooms/index.html', context)

def getRoom(request, slug):
    room = get_object_or_404(Room, slug=slug)
    reviews = RoomReview.objects.filter(room=room).order_by('-created_at')
    total_reviews = reviews.count()

    # Collect average ratings
    avg_location = reviews.aggregate(Avg('location'))['location__avg'] or 0
    avg_staff = reviews.aggregate(Avg('staff'))['staff__avg'] or 0
    avg_cleanliness = reviews.aggregate(Avg('cleanliness'))['cleanliness__avg'] or 0
    avg_value_for_money = reviews.aggregate(Avg('value_for_money'))['value_for_money__avg'] or 0
    avg_comfort = reviews.aggregate(Avg('comfort'))['comfort__avg'] or 0
    avg_facilities = reviews.aggregate(Avg('facilities'))['facilities__avg'] or 0
    avg_free_wifi = reviews.aggregate(Avg('free_wifi'))['free_wifi__avg'] or 0

    overall_rating = (
        avg_location + avg_staff + avg_cleanliness + avg_value_for_money + avg_comfort + avg_facilities + avg_free_wifi
    ) / 7

    # Get the selected currency from the query params or session (default to RWF)
    selected_currency = request.GET.get('currency', request.session.get('currency', 'RWF'))

    # Store selected currency in the session
    request.session['currency'] = selected_currency

    if request.method == 'POST':
        form = BookingForm(request.POST)
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

        # If the form is valid, create the booking
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.checkInDate = check_in_date
            booking.checkOutDate = check_out_date
            booking.status = 'pending'  # Set status to pending
            booking.payment_status = 'pending'  # Set payment status to pending
            booking.save()

            # Redirect to the booking confirmation page
            return redirect('base:booking', booking_id=booking.id)  # Adjust redirect to your success page

    else:
        form = BookingForm()

    settings = Setting.objects.first()

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
        'settings': settings,
        'selected_currency': selected_currency  # Pass selected currency to the template
    }

    return render(request, 'rooms/show.html', context)

def booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Access the room through the booking
    room = booking.room

    length_of_stay = (booking.checkOutDate - booking.checkInDate).days

    reviews = RoomReview.objects.filter(room=room).order_by('-created_at')
    total_reviews = reviews.count()

    # Calculate averages for each review category
    avg_location = reviews.aggregate(Avg('location'))['location__avg'] or 0
    avg_staff = reviews.aggregate(Avg('staff'))['staff__avg'] or 0
    avg_cleanliness = reviews.aggregate(Avg('cleanliness'))['cleanliness__avg'] or 0
    avg_value_for_money = reviews.aggregate(Avg('value_for_money'))['value_for_money__avg'] or 0
    avg_comfort = reviews.aggregate(Avg('comfort'))['comfort__avg'] or 0
    avg_facilities = reviews.aggregate(Avg('facilities'))['facilities__avg'] or 0
    avg_free_wifi = reviews.aggregate(Avg('free_wifi'))['free_wifi__avg'] or 0

    overall_rating = (avg_location + avg_staff + avg_cleanliness + avg_value_for_money + avg_comfort + avg_facilities + avg_free_wifi) / 7

    # Get the selected currency from the query params or session (default to RWF)
    selected_currency = request.GET.get('currency', request.session.get('currency', 'RWF'))

    # Store selected currency in the session
    request.session['currency'] = selected_currency

    settings = Setting.objects.first()

    context = {
        'room': room,
        'booking': booking,
        'total_reviews': total_reviews,
        'overall_rating': overall_rating,
        'check_in_date': booking.checkInDate,
        'check_out_date': booking.checkOutDate,
        'length_of_stay': length_of_stay,
        'settings': settings,
        'selected_currency': selected_currency  # Pass selected currency to the template
    }

    return render(request, 'booking.html', context)

def paymentSuccess(request, booking_id):
    settings = Setting.objects.first()

    # Retrieve the booking by ID
    booking = get_object_or_404(Booking, id=booking_id)

    # Extract transaction details from Flutterwave's redirect response
    transaction_id = request.GET.get('transaction_id')  # Adjust if Flutterwave uses a different key
    currency = request.GET.get('currency') or request.session.get('currency', 'RWF')  # Get from GET or session
    payment_status = request.GET.get('status', '').lower()  # Ensure to match Flutterwave's status value

    # Log the received parameters for debugging
    logger = logging.getLogger(__name__)
    logger.debug(f"PaymentSuccess received: transaction_id={transaction_id}, currency={currency}, status={payment_status}")

    # Verify the transaction status and update only if the payment was successful
    if payment_status == 'successful':
        booking.transactionId = transaction_id
        booking.payment_status = 'paid'
        booking.currency = currency
        booking.payment_date = timezone.now()  # Track when the payment was processed

        # Determine payment_amount based on the selected currency
        if currency == 'USD':
            booking.payment_amount = Decimal(booking.room.price_usd)
        else:
            booking.payment_amount = Decimal(booking.room.price_rwf)

        # Optionally update the booking status to 'confirmed'
        booking.status = 'confirmed'
        booking.save()

        # Prepare context with booking details
        context = {
            'settings': settings,
            'booking': booking
        }

        return render(request, 'success.html', context)
    else:
        # Handle unsuccessful payment cases
        return HttpResponse("Payment not successful. Please try again or contact support.", status=400)

def blogs(request):
    blogs = Blog.objects.all().order_by('-created_at')
    settings = Setting.objects.first()

    context = {
        'blogs': blogs,
        'settings': settings
    }

    return render(request, 'blogs/index.html', context)

def getBlog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    settings = Setting.objects.first()

    context = {
        'blog': blog,
        'settings': settings
    }

    return render(request, 'blogs/show.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            contact_message = form.save()

            # Send an email
            # send_mail(
            #     subject=f"New Contact Form Submission: {contact_message.subject}",
            #     message=f"Message from {contact_message.name} ({contact_message.email}):\n\n{contact_message.message}",
            #     from_email={contact_message.email},
            #     recipient_list=['kajugadaniels@gmail.com'],  # replace with the recipient's email
            # )

            # Show a success message
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('base:contact')
        else:
            messages.error(request, 'There was an error submitting your message. Please try again.')
    else:
        form = ContactForm()

    settings = Setting.objects.first()

    context = {
        'form': form,
        'settings': settings
    }

    return render(request, 'contact.html', context)

def restaurant(request):
    restaurant = Food.objects.all().order_by('-created_at')
    settings = Setting.objects.first()

    selected_currency = request.GET.get('currency', request.session.get('currency', 'RWF'))
    request.session['currency'] = selected_currency

    context = {
        'restaurant': restaurant,
        'settings': settings,
        'selected_currency': selected_currency,
    }
    return render(request, 'restaurant/index.html', context)

def getFood(request, slug):
    food = get_object_or_404(Food, slug=slug)
    settings = Setting.objects.first()

    selected_currency = request.GET.get('currency', request.session.get('currency', 'RWF'))
    request.session['currency'] = selected_currency

    context = {
        'food': food,
        'settings': settings,
        'selected_currency': selected_currency,
    }
    return render(request, 'restaurant/show.html', context)

def notFound(request):
    settings = Setting.objects.first()

    context = {
        'settings': settings,
    }

    return render(request, '404.html', context)