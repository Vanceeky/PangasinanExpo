from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *

from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

def index(request):
    return render(request, 'index.html')


def place_details(request, pk):
    tourist_spot = TouristSpot.objects.get(id=pk)
    images = tourist_spot.images.all()

    context = {
        'spot': tourist_spot,
        'images': images,
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

def user_dashboard(request):
    
    return render(request, 'home/user/dashboard.html')


