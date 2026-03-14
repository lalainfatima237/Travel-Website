from rest_framework import generics
from django.shortcuts import render,redirect
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.contrib.auth import authenticate, login



def home(request):
    destinations = Destination.objects.all()[:3]   
    tours = Tour.objects.all()[:6]                
    blogs = Blog.objects.all()[:3]                 
    reviews = Review.objects.all()[:3]         

    return render(request, "main/home.html", {
        "destinations": destinations,
        "tours": tours,
        "blogs": blogs,
        "reviews": reviews,
    })
def register(request):
    return render(request, 'register.html')
def contact_view(request):
    return render(request, 'contact.html')
def packages_view(request):
    return render(request, 'packages.html')
def explore(request):
    return render(request, 'explore.html')
def Login(request):
    if request.method == "POST":
        u_email = request.POST.get('email')
        u_pass = request.POST.get('password')
        
        # 1. Check karein ke data aa raha hai
        print(f"Attempting login for: {u_email}") 

        # 2. Authenticate (Email ko username ke taur par pass karein)
        user = authenticate(request, username=u_email, password=u_pass)
        
        if user is not None:
            login(request, user)
            print("Login Successful!")
            # 'next' parameter handle karein (profile edit par jane ke liye)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
        else:
            print("Login Failed: Invalid credentials")
            return render(request, 'login.html', {'error': 'Invalid Email or Password'})
            
    return render(request, 'login.html')


def dashboard(request):
    bookings_list = Booking.objects.all().order_by('id') 
    total_bookings = bookings_list.count()
    total_revenue = total_bookings * 500
    
    total_users = total_bookings 
    total_locations = Booking.objects.values('location').distinct().count()

    context = {
        'bookings': bookings_list,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'total_users': total_users,
        'total_locations': total_locations,
    }
    return render(request, 'dashboard.html', context)

def booking(request):
    if request.method == "POST":
        name = request.POST.get('customer_name')
        loc = request.POST.get('location')
        cin = request.POST.get('check_in')
        cout = request.POST.get('check_out')
        gst = request.POST.get('guests')

        if name and loc and cin and cout:
            Booking.objects.create(
                customer_name=name,
                location=loc,
                check_in=cin,
                check_out=cout,
                guests=gst
            )
            messages.success(request, 'Your booking has been done successfully!')
            return redirect('booking') 
    
    return render(request, 'Booking.html')

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    if request.method == "POST":
        # Admin ki information update karna
        request.user.first_name = request.POST.get('first_name')
        request.user.email = request.POST.get('email')
        
        # Agar image upload ki hai toh
        if request.FILES.get('profile_pix'):
            request.user.profile_pix = request.FILES.get('profile_pix')
            
        request.user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('dashboard')

    return render(request, 'profile.html')



#----------------------------API--------------------------------------------#
# -------- Users --------
class UserAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------- Destinations --------
class DestinationListCreateView(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DestinationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer


# -------- Tours --------
class TourListCreateView(generics.ListCreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

class TourDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer


# -------- Bookings --------
class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


# -------- Reviews --------
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# -------- Blogs --------
class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


