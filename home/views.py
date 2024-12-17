from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import *

from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from django.db.models import Avg, Count
from django.core.mail import send_mail
from django.conf import settings
from django.core.serializers import serialize
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')

def nearby_tourist_spot(request):
    spots = TouristSpot.objects.all()
    spots_data = serialize('json', spots, fields=('id', 'name', 'description', 'latitude', 'longitude'))
    context = {
        'spots': spots_data
    }
    return render(request, 'home/nearby_tourist_spot.html', context)

def nearby_accommodation(request):
    accommodations = Accommodation.objects.all()
    accommodations_data = serialize(
        'json',
        accommodations,
        fields=('id', 'name', 'type', 'description', 'latitude', 'longitude')
    )
    context = {
        'accommodations': accommodations_data
    }
    return render(request, 'home/nearby_accommodation.html', context)


def place_details(request, pk):
    # Get the tourist spot based on the primary key (pk)
    tourist_spot = TouristSpot.objects.get(id=pk)
  
    # Check if the user is authenticated and determine if the spot is a favorite
    if request.user.is_authenticated:
        is_favorite = Favorites.objects.filter(user=request.user, tourist_spot=tourist_spot).exists()
    else:
        is_favorite = False  # Default value for unauthenticated users
        
    images = tourist_spot.images.all()
    
  
    testimonials = Testimonial.objects.filter(tourist_spot=tourist_spot)

    average_rating = testimonials.aggregate(Avg('rating'))['rating__avg'] or 0 
    
  
    total_reviews = testimonials.count()

    rating_counts = testimonials.values('rating').annotate(count=Count('rating'))
    rating_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}  
    for rating in rating_counts:
        rating_dict[rating['rating']] = rating['count']
    



    context = {
        'spot': tourist_spot,
        'images': images,
        'average': average_rating,
        'total_reviews': total_reviews,
        'rating_counts': rating_dict,
        'testimonials': testimonials,
        'is_favorite': is_favorite
     
    }
    
    return render(request, 'home/place_details.html', context)





def map_direction(request, pk):
    spot = TouristSpot.objects.get(id=pk)
    context = {
        'spot': spot
    }
    return render(request, 'home/map_direction.html', context)


def categories(request, category):
    spots = TouristSpot.objects.filter(category=category)
    context = {
        'spots': spots,
        'category': category
    }
    return render(request, 'home/categories.html', context)



def accommodations(request):
    accommodations = Accommodation.objects.filter(status = 'Approved')
    print(accommodations)
    context = {
        'accommodations': accommodations
    }
    return render(request, 'home/accommodation/accommodations.html', context)

def add_accommodation_page(request):
    city_town = get_city_town_choices()
    context = {
        'city_town': city_town
    }
    return render(request, 'home/accommodation/add_accommodation.html', context)

def add_accommodation(request):
    if request.method == 'POST':
        try:
            # Get data from the HTML form
            name = request.POST.get('name')
            type = request.POST.get('type')
            description = request.POST.get('description')
            city_town = request.POST.get('city_town')
            address = request.POST.get('address')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            
            # Create and save the Accommodation instance
            accommodation = Accommodation(
                manager=request.user,
                name=name,
                type=type,
                description=description,
                city_town=city_town,
                address=address,
                latitude=latitude,
                longitude=longitude
            )
            accommodation.save()

            # Process each uploaded image
            images = request.FILES.getlist('images')
            for image in images:
                AccomodationImage.objects.create(accomodation=accommodation, image=image)
                
            # Prepare email content
            subject = "Accommodation Under Review"
            message = f"""
            Dear {request.user.first_name},

            Thank you for submitting your accommodation "{name}" for review. 
            
            Our team is currently reviewing the details you provided:
            - Accommodation Name: {name}
            - Type: {type}
            - Description: {description}
            - Address: {address}, {city_town}
            - Latitude/Longitude: {latitude}, {longitude}

            Once approved, it will be listed on our platform.

            If you have any questions, feel free to contact us at {settings.EMAIL_HOST_USER}.

            Best regards,
            The PangasinanExpo Team
            """
            recipient = request.user.email

            # Send email
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [recipient],
                fail_silently=False,
            )

            return JsonResponse({'status': 'success', 'message': 'Accommodation details was saved and is now under review.'}, status=201)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)



def accommodation_details(request, pk):
    accomodation = Accommodation.objects.get(id=pk)
    rooms = Room.objects.filter(accommodation=accomodation)
    context = {
        'accomodation': accomodation,
        'rooms': rooms
    }
    return render(request, 'home/accommodation/accommodation_details.html', context)


def room_details(request, pk):
    room = Room.objects.get(id=pk)
    context = {
        'room': room
    }
    return render(request, 'home/accommodation/room_details.html', context)


@csrf_exempt
def check_availability(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        room_type = data.get('room_type')
        check_in_date = datetime.strptime(data.get('check_in_date'), '%Y-%m-%d').date()
        check_out_date = datetime.strptime(data.get('check_out_date'), '%Y-%m-%d').date()
        
        # Get all rooms of the selected type
        rooms_of_type = Room.objects.filter(room_type=room_type)
        
        # Check for overlapping bookings on any of these rooms
        overlapping_bookings = Booking.objects.filter(
            room__in=rooms_of_type,
            status='Confirmed',
            check_in_date__lt=check_out_date,
            check_out_date__gt=check_in_date
        ).count()
        
        # If the number of overlapping bookings is less than the available rooms, we have availability
        available = overlapping_bookings < rooms_of_type.count()
        
        return JsonResponse({'available': available})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

# USER FUNCTIONS


def user_profile(request):
    
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'home/user/profile.html', context)

def user_dashboard(request):
    
    return render(request, 'home/user/dashboard.html')

def user_accomodation(request):
    accommodation = Accommodation.objects.get(manager = request.user)

    # Get all rooms associated with this accommodation
    rooms = Room.objects.filter(accommodation=accommodation)
    
    # Get all bookings for the rooms in this accommodation
    bookings = Booking.objects.filter(room__in=rooms).select_related('guest', 'room')

    context = {
        'accommodation': accommodation,
        'rooms': rooms,
        'bookings': bookings,  # Pass the bookings to the template
    }

    return render(request, 'home/user/accommodation.html', context)

def add_review(request):
    if request.method == 'POST':
        spot = TouristSpot.objects.get(id=request.POST.get('spot_id'))
        rating = request.POST.get('rating')
        month_visited = request.POST.get('month_visited')
        visited_with = request.POST.get('visited_with')
        review_title = request.POST.get('review_title')
        review_content = request.POST.get('review_content')
        image = request.FILES.get('image')

        testimonial = Testimonial.objects.create(
            user=request.user,
            tourist_spot=spot,
            rating=rating,
            month_visited=month_visited,
            visited_with=visited_with,
            review_title=review_title,
            review_content=review_content,
   
        )

        testimonial.save()

        if image:
            TestimonialImage.objects.create(testimonial=testimonial, image=image)




        return redirect('place-details', pk = spot.id)
    

def book_room(request):
    if request.method == 'POST':
        # Parse POST data
        try:
            room_id = request.POST.get('room_id')
            check_in_date = datetime.strptime(request.POST.get('check_in'), '%Y-%m-%d').date()
            check_out_date = datetime.strptime(request.POST.get('check_out'), '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid date format'}, status=400)

        # Validate check-in and check-out dates
        if check_in_date >= check_out_date:
            return JsonResponse({'error': 'Check-out date must be after check-in date'}, status=400)

        room_type = request.POST.get('room_type')
        room = get_object_or_404(Room, id=room_id)
        guest = request.user

        # Check if room type has availability
        rooms_of_type = Room.objects.filter(room_type=room_type)
        overlapping_bookings = Booking.objects.filter(
            room__in=rooms_of_type,
            status='Confirmed',  # Assuming "Confirmed" status means approved bookings
            check_in_date__lt=check_out_date,  # Overlaps if check-in is before check-out
            check_out_date__gt=check_in_date   # Overlaps if check-out is after check-in
        ).count()

        if overlapping_bookings >= rooms_of_type.count():
            return JsonResponse({'available': False, 'error': 'No available rooms for the selected type and dates'}, status=400)

        # Create booking with status "Pending Approval"
        booking = Booking.objects.create(
            guest=guest,
            room=room,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
        )
        booking.save()

        # Send email notification
        subject = 'Room Booking Request Received'
        message = f"""
        Dear {guest.first_name},

        Thank you for your booking request! Your booking is currently under review and awaiting approval. Here are the details of your request:

        Room: {booking.guest}
        Room Type: {room_type}
        Check-In Date: {check_in_date}
        Check-Out Date: {check_out_date}
        Length of Stay: {booking.length_of_stay} days
        Total Price: {booking.total_price}

        You will receive an email confirmation once your booking is approved. If you have any questions or need assistance, feel free to contact us.

        Best regards,
        Your Hotel Team
        """
        recipient_email = guest.email  # Assumes the User model has an `email` field

        try:
            send_mail(
                subject,
                message,
                'PangasinanExpo@email.com',  # Replace with your email (EMAIL_HOST_USER)
                [recipient_email],
                fail_silently=False,
            )
        except Exception as e:
            return JsonResponse({'available': True, 'message': 'Booking request submitted, but email notification failed.', 'error': str(e)}, status=500)

        return JsonResponse({'available': True, 'message': 'Booking request submitted and awaiting approval. Email notification sent.'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Confirmed'
    booking.save()
    return redirect('bookings')

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Cancelled'
    booking.save()
    return redirect('bookings')


def send_booking_confirmation_email(booking):
    subject = f"Booking Confirmed: {booking.room.room_type}"
    message = f"""
    Dear {booking.guest.first_name} {booking.guest.last_name},

    Your booking has been confirmed. Here are the details of your booking:

    Room: {booking.room.room_type}
    Check-in Date: {booking.check_in_date}
    Check-out Date: {booking.check_out_date}
    Length of Stay: {booking.length_of_stay} days
    Total Price: ${booking.total_price}

    We look forward to hosting you. Please contact us if you need any further information.

    Best regards,
    PangasinanExpo
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [booking.guest.email]
    send_mail(subject, message, from_email, recipient_list)

def send_booking_cancellation_email(booking):
    subject = f"Booking Cancelled: {booking.room.room_type}"
    message = f"""
    Dear {booking.guest.first_name} {booking.guest.last_name},

    We regret to inform you that your booking has been cancelled. Below are the details:

    Room: {booking.room.room_type}
    Check-in Date: {booking.check_in_date}
    Check-out Date: {booking.check_out_date}
    Length of Stay: {booking.length_of_stay} days
    Total Price: ${booking.total_price}

    We apologize for any inconvenience caused. Please feel free to reach out if you have any questions.

    Best regards,
    PangasinanExpo
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [booking.guest.email]
    send_mail(subject, message, from_email, recipient_list)

def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Confirmed'
    booking.save()

    # Send email notification for booking confirmation
    send_booking_confirmation_email(booking)

    messages.success(request, 'Booking approved successfully.')
    return redirect('user_accomodation')

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Cancelled'
    booking.save()

    # Send email notification for booking cancellation
    send_booking_cancellation_email(booking)

    messages.success(request, 'Booking denied successfully.')
    return redirect('user_accomodation')








## MANAGE ACCOMMODATION

def add_room_accommodation(request):
    if request.method == 'POST':
        accommodation_id = request.POST.get('accommodation')
        accommodation = Accommodation.objects.get(id=accommodation_id)
        room_type = request.POST.get('room_type')
        capacity = request.POST.get('capacity')
        price = request.POST.get('price_per_night')
        amenities = request.POST.get('amenities')
        images = request.FILES.getlist('images')  # Correctly get multiple images

        room = Room.objects.create(
            accommodation=accommodation,
            room_type=room_type,
            capacity=capacity,
            price_per_night=price,
            amenities=amenities
        )

        # Save each image for the created room
        for image in images:
            RoomImage.objects.create(room=room, image=image)

        return redirect('user_accomodation')  # Ensure this URL exists in your project


@login_required
@csrf_exempt
def toggle_favorite(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tourist_spot_id = data.get('tourist_spot_id')
        action = data.get('action')

        try:
            tourist_spot = TouristSpot.objects.get(id=tourist_spot_id)
            if action == 'add':
                Favorites.objects.get_or_create(user=request.user, tourist_spot=tourist_spot)
                is_favorite = True
            elif action == 'remove':
                Favorites.objects.filter(user=request.user, tourist_spot=tourist_spot).delete()
                is_favorite = False

            return JsonResponse({'success': True, 'is_favorite': is_favorite})
        except TouristSpot.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Tourist spot not found.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})