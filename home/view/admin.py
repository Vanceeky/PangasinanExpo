
from django.shortcuts import render
from home.models import TouristSpot



def dashboard(request):
    return render(request, 'home/admin/dashboard.html')


def tourist_spots(request):
    spots = TouristSpot.objects.all()
    context = {
        'spots': spots
    }
    return render(request, 'home/admin/tourist_spots.html', context)

def tourist_spot(request, pk):
    spot = TouristSpot.objects.get(id=pk)
    context = {
        'spot': spot
    }
    return render(request, 'home/admin/tourist_spot.html', context)