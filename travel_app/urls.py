from django.urls import path
from .views import * 
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path('login/', views.Login, name='login'),      
    path('register/', views.register, name='register'),
    path('contact/', views.contact_view, name='contact'),
    path('contact_submit/', views.contact_submit, name='contact_submit'),
    path('newsletter_subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('packages/', views.packages_view, name='packages'),
    path('explore/', views.explore, name='explore'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("booking/", views.booking, name="booking"),
    path("my_bookings/", views.my_bookings, name="my_bookings"),
    path('profile/edit/', views.profile, name='profile'),
    path('update_booking_status/<int:pk>/', views.update_booking_status, name='update_booking_status'),





#------------------------- APIs urls------------------------------------#
    # Users
   path('signup/', UserAPIView.as_view(), name='api_signup'),
   

    # Destinations
    path("destinations/", DestinationListCreateView.as_view(), name="destination-list"),
    path("destinations/<int:pk>/", DestinationDetailView.as_view(), name="destination-detail"),

    # Tours
    path("tours/", TourListCreateView.as_view(), name="tour-list"),
    path("tours/<int:pk>/", TourDetailView.as_view(), name="tour-detail"),

    # Bookings
    path('bookings/', BookingListCreateView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    # Reviews
    path("reviews/", ReviewListCreateView.as_view(), name="review-list"),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="review-detail"),

    # Blogs
    path("blogs/", BlogListCreateView.as_view(), name="blog-list"),
    path("blogs/<int:pk>/", BlogDetailView.as_view(), name="blog-detail"),
]
