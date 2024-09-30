from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('place-details/', views.place_details, name="place-details"),
]