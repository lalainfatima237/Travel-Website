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

def contact_submit(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name', '')
        mobile_no = request.POST.get('mobile_no')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if first_name and mobile_no and email and message:
            Message.objects.create(
                first_name=first_name,
                last_name=last_name,
                mobile_no=mobile_no,
                email=email,
                message=message
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('contact')
    return redirect('contact')

def newsletter_subscribe(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            # Create or get to avoid unique constraint errors
            NewsletterSubscriber.objects.get_or_create(email=email)
            messages.success(request, 'Thank you for subscribing to our newsletter!')
        else:
            messages.error(request, 'Please provide a valid email address.')
    # Redirect back to the referring page, or home if not available
    return redirect(request.META.get('HTTP_REFERER', 'home'))
def packages_view(request):
    return render(request, 'packages.html')
def explore(request):
    destinations = Destination.objects.all()
    return render(request, 'explore.html', {'destinations': destinations})
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


from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

import json
from django.db.models.functions import TruncDay
from django.db.models import Count

@login_required
@staff_member_required
def dashboard(request):
    bookings_list = Booking.objects.all().order_by('id') 
    total_bookings = bookings_list.count()
    total_revenue = total_bookings * 500
    
    total_users = total_bookings 
    total_locations = Booking.objects.values('location').distinct().count()

    # Chart data
    bar_labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    bar_data = [6, 2, 3, 1, 4, 5, 7] # Fallback data logic
    
    ongoing = bookings_list.filter(status='Ongoing').count()
    confirmed = bookings_list.filter(status='Confirmed').count()
    canceled = bookings_list.filter(status='Canceled').count()
    pending = bookings_list.filter(status='Pending').count()
    
    doughnut_labels = ['Pending/Ongoing', 'Confirmed', 'Canceled']
    doughnut_data = [ongoing + pending, confirmed, canceled]

    chart_data = {
        'bar_labels': bar_labels,
        'bar_data': bar_data,
        'doughnut_labels': doughnut_labels,
        'doughnut_data': doughnut_data,
    }

    context = {
        'bookings': bookings_list,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'total_users': total_users,
        'total_locations': total_locations,
        'chart_data': json.dumps(chart_data)
    }
    return render(request, 'dashboard.html', context)

def booking(request):
    if request.method == "POST":
        name = request.POST.get('customer_name')
        loc = request.POST.get('location')
        pkg = request.POST.get('package')
        cin = request.POST.get('check_in')
        cout = request.POST.get('check_out')
        gst = request.POST.get('guests')

        if name and loc and cin and cout:
            Booking.objects.create(
                user=request.user if request.user.is_authenticated else None,
                customer_name=name,
                location=loc,
                package=pkg,
                check_in=cin,
                check_out=cout,
                guests=gst
            )
            messages.success(request, 'Your booking has been done successfully!')
            return redirect('booking') 
    
    selected_package = request.GET.get('package', '')
    return render(request, 'Booking.html', {'selected_package': selected_package})

@login_required
def my_bookings(request):
    if request.method == "POST":
        booking_id = request.POST.get('cancel_booking_id')
        if booking_id:
            try:
                b = Booking.objects.get(id=booking_id, user=request.user)
                b.status = 'Canceled'
                b.save()
                messages.success(request, 'Booking canceled successfully.')
            except Booking.DoesNotExist:
                pass
        return redirect('my_bookings')
        
    user_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_bookings.html', {'bookings': user_bookings})

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


@login_required
@staff_member_required
def update_booking_status(request, pk):
    if request.method == "POST":
        status_val = request.POST.get('status')
        try:
            booking = Booking.objects.get(pk=pk)
            booking.status = status_val
            booking.save()
            messages.success(request, f'Booking #{pk} status updated to {status_val}.')
        except Booking.DoesNotExist:
            messages.error(request, 'Booking not found.')
    return redirect('dashboard')




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


