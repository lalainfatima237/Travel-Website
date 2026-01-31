from django.contrib import admin
from .models import User, Destination, Tour, Booking, Review, Blog

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'phone')

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'price', 'duration')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'status', 'booking_date')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'rating', 'created_at')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
