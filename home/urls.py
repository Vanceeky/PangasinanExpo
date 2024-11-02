from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.index, name="index"),
    path('categories/<str:category>/', views.categories, name="categories"),
    path('place-details/<int:pk>/', views.place_details, name="place-details"),
    path('map-direction/<int:pk>/', views.map_direction, name="map-direction"),




    path('accommodations/', views.accommodations, name="accommodations"),
    path('add-accommodation/', views.add_accommodation_page, name="add-accommodation-page"),
    path('add-accommodation-listing/', views.add_accommodation, name="add_accommodation"),
    path('accommodation-details/<int:pk>/', views.accommodation_details, name="accommodation-details"),




    # USER URLS
    path('dashboard/', views.user_dashboard, name="user_dashboard"),
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)