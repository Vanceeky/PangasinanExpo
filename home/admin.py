from django.contrib import admin
from .models import *

# Register your models here.
# Inline model for Tourist Spot Images

admin.site.register(Tourist)
class TouristSpotImageInline(admin.TabularInline):
    model = TouristSpotImage
    extra = 1

# Tourist Spot Admin configuration with inline images
@admin.register(TouristSpot)
class TouristSpotAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'city_or_town', 'latitude', 'longitude')
    inlines = [TouristSpotImageInline]


class AccomodationImageInline(admin.TabularInline):  # You can also use `admin.StackedInline`
    model = AccomodationImage
    extra = 1  # Number of empty image slots to show by default

# Register the Accomodation model with the inline
@admin.register(Accommodation)
class AccomodationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'city_town', 'manager')  # Display fields in list view
    inlines = [AccomodationImageInline]

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1  # Number of empty forms to display for adding new images

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomImageInline]  # Add the inline to the Room admin



admin.site.register(Booking)


class TestimonialImageInline(admin.TabularInline):
    model = TestimonialImage
    extra = 1  # Number of empty forms to display for adding new images

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'tourist_spot', 'month_visited', 'visited_with', 'rating', 'review_title')
    inlines = [TestimonialImageInline]

admin.site.register(Favorites)