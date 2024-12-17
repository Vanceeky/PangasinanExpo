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

    path('nearby-tourist-spots/', views.nearby_tourist_spot, name="nearby-tourist-spots"),
    path('nearby-accommdations/', views.nearby_accommodation, name="nearby-accommodations"),




    path('accommodations/', views.accommodations, name="accommodations"),
    path('add-accommodation/', views.add_accommodation_page, name="add-accommodation-page"),
    path('add-accommodation-listing/', views.add_accommodation, name="add_accommodation"),
    path('accommodation-details/<int:pk>/', views.accommodation_details, name="accommodation-details"),
    path('accommodation/room/<int:pk>/', views.room_details, name="room-details"),
    path('check-availability/', views.check_availability, name='check_availability'),



    # USER URLS
    path('user-profile/', views.user_profile, name="user_profile"),
    path('user-dashboard/', views.user_dashboard, name="user_dashboard"),
    path('add-review/', views.add_review, name="add_review"),

    path('book-room/', views.book_room, name="book_room"),
    path('favorites/toggle/', views.toggle_favorite, name='toggle-favorite'),

    path('manage/accommodation/', views.user_accomodation, name="user_accomodation"),
    path('add-room/', views.add_room_accommodation, name="add_room_accommodation"),


    path('approve-booking/<int:booking_id>/', views.approve_booking, name="approve-booking"),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name="cancel-booking"),



    #ADMIN DASHBOARD

    path('dashboard/', dashboard, name="dashboard"),
    path('tourist-spots/admin/', tourist_spots, name="tourist-spots-admin"),
    path('tourist-spot/<int:pk>/admin/', tourist_spot, name="tourist-spot-admin"),
    path('add-tourist-spot/', add_tourist_spot, name="add-tourist-spot"),


    # ADMIN ACCOMODATION URLS
    path('accommodations/admin/', accommodations, name="accommodations-admin"),
    path('accommodation/<int:pk>/admin/', accomodation_details, name="accommodation-admin"),
    path('accommodation/action/<int:accommodation_id>/', accommodation_action, name='accommodation_action'),

    # ADMIN USER URLS
    path('users/admin/', users, name="users-admin"),
    path('user/<int:pk>/admin/', user_details, name="user-admin"),

    # ADMIN TESTIMONIAL URLS
    path('testimonials/admin/', testimonials, name="testimonials-admin"),
    path('testimonial/<int:pk>/admin/', testimonial_details, name="testimonial-admin"),

]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)