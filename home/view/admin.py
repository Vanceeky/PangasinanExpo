
from django.shortcuts import render, redirect, reverse
from home.models import TouristSpot, Accommodation, Testimonial, TouristSpotImage
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group


def dashboard(request):
    tourist_spots = TouristSpot.objects.all()
    users = User.objects.all().exclude(is_superuser=True).exclude(is_staff=True)
    accommodations = Accommodation.objects.all()
    testimonials = Testimonial.objects.all()

    context = {
        'tourist_spots': tourist_spots,
        'users': users,
        'accommodations': accommodations,
        'reviews': testimonials
    }
    return render(request, 'home/admin/dashboard.html', context)


def tourist_spots(request):
    spots = TouristSpot.objects.all()
    context = {
        'spots': spots
    }
    return render(request, 'home/admin/tourist_spots.html', context)

def tourist_spot(request, pk):
    spot = TouristSpot.objects.get(id=pk)

    
    context = {
        'spot': spot,
    }
    return render(request, 'home/admin/tourist_spot.html', context)

def add_tourist_spot(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        address = request.POST.get('address')
        city_or_town = request.POST.get('city_or_town')
        category = request.POST.get('category')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        image = request.FILES.get('image')

        try:
            # Create the tourist spot
            tourist_spot = TouristSpot.objects.create(
                name=name,
                address=address,
                city_or_town=city_or_town,
                description=description,
                category=category,
                latitude=latitude,
                longitude=longitude,
            )

            # Handle multiple file uploads
            new_images = request.FILES.getlist('new_images[]')
            for image in new_images:
                TouristSpotImage.objects.create(tourist_spot=tourist_spot, image=image)

            # Add success message
            messages.success(request, "Tourist spot added successfully!")
            # Redirect to the tourist-spot-admin page
            return redirect('tourist-spot-admin', pk=tourist_spot.pk) # Redirect to the same page or another page
        except Exception as e:
            # Add error message
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'home/admin/add_tourist_spot.html')







# ACCOMODATIONS

def accommodations(request):
    accommodations = Accommodation.objects.all()
    context = {
        'accommodations': accommodations
    }
    return render(request, 'home/admin/accomodations.html', context)

def accomodation_details(request, pk):
    accomodation = Accommodation.objects.get(id=pk)
    context = {
        'accommodation': accomodation
    }
    return render(request, 'home/admin/accommodation_details.html', context)


@csrf_exempt
def accommodation_action(request, accommodation_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')  # Either "approve" or "deny"
            
            # Get the accommodation instance
            accommodation = Accommodation.objects.get(id=accommodation_id)

            if action == 'approve':
                accommodation.status = 'Approved'
                accommodation.save()

                # Check if the user is already in the "manager" group
                manager_group, created = Group.objects.get_or_create(name='manager')
                if not accommodation.manager.groups.filter(name='manager').exists():
                    accommodation.manager.groups.add(manager_group)

                # Notify the user
                subject = "Accommodation Approved"
                message = f"""
                Dear {accommodation.manager.first_name},

                Congratulations! Your accommodation "{accommodation.name}" has been approved and is now live on our platform.

                Thank you for being part of our community.

                Best regards,
                The EventMaster Team
                """
            elif action == 'deny':
                accommodation.status = 'Denied'
                accommodation.save()
                # Notify the user
                subject = "Accommodation Denied"
                message = f"""
                Dear {accommodation.manager.first_name},

                We regret to inform you that your accommodation "{accommodation.name}" has been denied. 
                
                If you have any questions or need further assistance, please contact us at {settings.EMAIL_HOST_USER}.

                Best regards,
                The PangasinanExpo Team
                """
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid action.'}, status=400)
            
            # Send email notification
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [accommodation.manager.email],
                fail_silently=False,
            )

            # Redirect after success
            return JsonResponse({
                'status': 'success',
                'message': f'Accommodation has been {action}ed successfully.',
                'redirect_url': reverse('accommodations-admin')
            }, status=200)

        except Accommodation.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Accommodation not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

# USERS 

def users(request):
    users = User.objects.all().exclude(is_superuser=True).exclude(is_staff=True)
    context = {
        'users': users
    }
    return render(request, 'home/admin/users.html', context)

def user_details(request, pk):
    user = User.objects.get(id=pk)
    context = {
        'user': user
    }
    return render(request, 'home/admin/user_details.html', context)


# Testomonials

def testimonials(request):
    testimonials = Testimonial.objects.all()
    context = {
        'testimonials': testimonials
    }
    return render(request, 'home/admin/testimonials.html', context)


def testimonial_details(request, pk):
    return render(request, 'home/admin/testimonial_details.html')