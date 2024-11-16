from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from home.view.admin import *





urlpatterns = [
    path('', views.index, name="index"),
    path('categories/<str:category>/', views.categories, name="categories"),
    path('place-details/<int:pk>/', views.place_details, name="place-details"),
    path('map-direction/<int:pk>/', views.map_direction, name="map-direction"),




    path('accommodations/', views.accommodations, name="accommodations"),
    path('add-accommodation/', views.add_accommodation_page, name="add-accommodation-page"),
    path('add-accommodation-listing/', views.add_accommodation, name="add_accommodation"),
    path('accommodation-details/<int:pk>/', views.accommodation_details, name="accommodation-details"),
    path('accommodation/room/<int:pk>/', views.room_details, name="room-details"),
    path('check-availability/', views.check_availability, name='check_availability'),



    # USER URLS
    path('user-dashboard/', views.user_dashboard, name="user_dashboard"),



    #ADMIN DASHBOARD

    path('dashboard/', dashboard, name="dashboard"),
    path('tourist-spots/admin/', tourist_spots, name="tourist-spots-admin"),
    path('tourist-spot/<int:pk>/admin/', tourist_spot, name="tourist-spot-admin"),


]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)