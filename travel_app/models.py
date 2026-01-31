from django.db import models
from django.contrib.auth.models import AbstractUser

# -----------------------------
# USER MODEL
# -----------------------------
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('agent', 'Agent'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=20, blank=True, null=True)
    # is_active is already inherited from AbstractUser
    # created_at and updated_at timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


# -----------------------------
# DESTINATION MODEL
# -----------------------------
class Destination(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Destinations"

    def __str__(self):
        return f"{self.name} - {self.country}"


# -----------------------------
# TOUR MODEL
# -----------------------------
class Tour(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='tours')
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50)  # e.g., "5 Days / 4 Nights"
    description = models.TextField()
    image = models.ImageField(upload_to='tours/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  # Admin can deactivate tours

    def __str__(self):
        return f"{self.title} ({self.destination.name})"


# -----------------------------
# BOOKING MODEL
# -----------------------------
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.tour.title} ({self.status})"


# -----------------------------
# REVIEW MODEL
# -----------------------------
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()  # 1 to 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'tour')  # One review per tour per user

    def __str__(self):
        return f"Review by {self.user.username} for {self.tour.title}"


# -----------------------------
# BLOG MODEL
# -----------------------------
class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)  # Admin can unpublish

    def __str__(self):
        return self.title
