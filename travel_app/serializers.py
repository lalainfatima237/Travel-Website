from rest_framework import serializers
from .models import User, Destination, Tour, Booking, Review, Blog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone']

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'

class TourSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer(read_only=True)
    destination_id = serializers.PrimaryKeyRelatedField(
        queryset=Destination.objects.all(), source="destination", write_only=True
    )

    class Meta:
        model = Tour
        fields = ['id', 'title', 'price', 'duration', 'description', 'image', 'destination', 'destination_id']

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )
    tour = TourSerializer(read_only=True)
    tour_id = serializers.PrimaryKeyRelatedField(
        queryset=Tour.objects.all(), source="tour", write_only=True
    )

    class Meta:
        model = Booking
        fields = ['id', 'user', 'user_id', 'tour', 'tour_id', 'booking_date', 'status']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tour = TourSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )
    tour_id = serializers.PrimaryKeyRelatedField(
        queryset=Tour.objects.all(), source="tour", write_only=True
    )

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_id', 'tour', 'tour_id', 'rating', 'comment', 'created_at']

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
