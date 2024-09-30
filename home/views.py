from django.shortcuts import render


# Create your views here.





def index(request):
    return render(request, 'index.html')


def place_details(request):
    return render(request, 'home/place_details.html')