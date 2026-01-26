from django.urls import path
from .views import * 
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('register/', views.register, name='register'),
    path('contact/', views.contact_view, name='contact'),
    path('packages/', views.packages_view, name='packages'),
    path('explore/', views.explore, name='explore'),

    # Users
    path("users/", UserListCreateView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),

    # Destinations
    path("destinations/", DestinationListCreateView.as_view(), name="destination-list"),
    path("destinations/<int:pk>/", DestinationDetailView.as_view(), name="destination-detail"),

    # Tours
    path("tours/", TourListCreateView.as_view(), name="tour-list"),
    path("tours/<int:pk>/", TourDetailView.as_view(), name="tour-detail"),

    # Bookings
    path("bookings/", BookingListCreateView.as_view(), name="booking-list"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),

    # Reviews
    path("reviews/", ReviewListCreateView.as_view(), name="review-list"),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="review-detail"),

    # Blogs
    path("blogs/", BlogListCreateView.as_view(), name="blog-list"),
    path("blogs/<int:pk>/", BlogDetailView.as_view(), name="blog-detail"),
]
