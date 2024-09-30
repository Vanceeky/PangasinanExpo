from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.auth_page, name="auth-page"),
    path('logout/', views.custom_logout, name='custom_logout'),
]
