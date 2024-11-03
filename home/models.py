from django.db import models
from django.contrib.auth.models import User

def get_city_town_choices():
    return [
        ('Agno', 'Agno'),
        ('Aguilar', 'Aguilar'),
        ('Alcala', 'Alcala'),
        ('Anda', 'Anda'),
        ('Asingan', 'Asingan'),
        ('Balungao', 'Balungao'),
        ('Bani', 'Bani'),
        ('Basista', 'Basista'),
        ('Bautista', 'Bautista'),
        ('Bayambang', 'Bayambang'),
        ('Binalonan', 'Binalonan'),
        ('Binmaley', 'Binmaley'),
        ('Bolinao', 'Bolinao'),
        ('Bugallon', 'Bugallon'),
        ('Burgos', 'Burgos'),
        ('Calasiao', 'Calasiao'),
        ('Dasol', 'Dasol'),
        ('Infanta', 'Infanta'),
        ('Labrador', 'Labrador'),
        ('Laoac', 'Laoac'),
        ('Lingayen', 'Lingayen'),
        ('Mabini', 'Mabini'),
        ('Malasiqui', 'Malasiqui'),
        ('Manaoag', 'Manaoag'),
        ('Mangaldan', 'Mangaldan'),
        ('Mangatarem', 'Mangatarem'),
        ('Mapandan', 'Mapandan'),
        ('Natividad', 'Natividad'),
        ('Pozorrubio', 'Pozorrubio'),
        ('Rosales', 'Rosales'),
        ('San Fabian', 'San Fabian'),
        ('San Jacinto', 'San Jacinto'),
        ('San Manuel', 'San Manuel'),
        ('San Nicolas', 'San Nicolas'),
        ('San Quintin', 'San Quintin'),
        ('Santa Barbara', 'Santa Barbara'),
        ('Santa Maria', 'Santa Maria'),
        ('Santo Tomas', 'Santo Tomas'),
        ('Sison', 'Sison'),
        ('Sual', 'Sual'),
        ('Tayug', 'Tayug'),
        ('Umingan', 'Umingan'),
        ('Urbiztondo', 'Urbiztondo'),
        ('Villasis', 'Villasis'),
        ('Alaminos', 'Alaminos'),   # City
        ('Dagupan', 'Dagupan'),     # City
        ('San Carlos', 'San Carlos'),  # City
        ('Urdaneta', 'Urdaneta'),   # City
    ]


def get_categories():
    return [
        ('Beach', 'Beach'),
        ('Mountains', 'Mountains'),
        ('Falls', 'Falls'),
        ('Rivers', 'Rivers'),
        ('Churches', 'Churches'),
        ('Others', 'Others'),
    ]

# Define the model
class TouristSpot(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=100)
    city_or_town = models.CharField(
        max_length=100,
        choices=get_city_town_choices()
    )
    category = models.CharField(max_length = 100, choices = get_categories, null=True, blank = True)
    
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)

    def __str__(self):
        
        return self.name

# Model for Tourist Spot Images
class TouristSpotImage(models.Model):
    tourist_spot = models.ForeignKey(TouristSpot, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='tourist_spot_images/')

    def __str__(self):
        return f"{self.tourist_spot.name} Image"
    


class Accommodation(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    description = models.TextField()
    city_town = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)

    status = models.CharField(max_length=10, default='Pending', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied')])

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name
    
class AccomodationImage(models.Model):
    accomodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='accomodation_images/')

    def __str__(self):
        return f"{self.accomodation.name} Image"
    
class Room(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=100)  # e.g., Single, Double, Suite
    capacity = models.PositiveIntegerField()       # Number of guests the room can accommodate
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)  # Room price
    description = models.TextField(blank=True, null=True)  # Optional room description
    amenities = models.TextField(blank=True, null=True)  # Comma-separated amenities
    
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_type} in {self.accommodation.name}"

    def get_amenities_list(self):
        """Returns a list of amenities."""
        if self.amenities:
            return [amenity.strip() for amenity in self.amenities.split(',')]
        return []
    
class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='accomodations_images/')

    def __st__(self):
        return f"{self.room.name} Image"


class Booking(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled')
    ], default='Pending')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.guest.username} for {self.room} from {self.check_in_date} to {self.check_out_date}"

    def save(self, *args, **kwargs):
        # Calculate total price based on room price and duration of stay
        if self.check_in_date and self.check_out_date:
            nights = (self.check_out_date - self.check_in_date).days
            self.total_price = self.room.price_per_night * nights
        super().save(*args, **kwargs)

    def is_available(self):
        """Check if the room is available for the requested dates."""
        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            status='Confirmed',
            check_in_date__lt=self.check_out_date,
            check_out_date__gt=self.check_in_date
        ).exists()
        return not overlapping_bookings
    
    def is_room_type_available(self):
        """Check availability across rooms of the same type for the selected dates."""
        # Get all rooms of the specified type
        available_rooms = Room.objects.filter(room_type=self.room.room_type)    

        # Filter out rooms that are already booked for overlapping dates
        unavailable_rooms = Booking.objects.filter(
            room__in=available_rooms,
            status='Confirmed',
            check_in_date__lt=self.check_out_date,
            check_out_date__gt=self.check_in_date
        ).values_list('room_id', flat=True)

        # Check if there are any rooms left that are not in the unavailable list
        available_count = available_rooms.exclude(id__in=unavailable_rooms).count()
        return available_count > 0
    

