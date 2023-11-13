from datetime import datetime

from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Turf(models.Model):
    owner_name = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='turf_images/', default='default.jpg')#for avatar of turf
    price = models.IntegerField(default=0)
    info = models.TextField(default="")
    connect = models.CharField(max_length=1000, default="")
    owner_email = models.EmailField(max_length=100, blank=True, null=True, default="")

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            total_ratings = sum(review.rating for review in reviews)
            return total_ratings / len(reviews)
        else:
            return 0

    @property
    def avg_rating(self):
        return round(self.average_rating(), 2)


    def __str__(self):
        return self.name


class TurfImage(models.Model):
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='turf_images/', default='default.jpg')#another photos of turf

    def __str__(self):
        return f"Image for {self.turf.name}"

class TimeSlot(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK, default="")
    start_time = models.TimeField(default=datetime.now)
    end_time = models.TimeField(default=datetime.now)
    available = models.BooleanField(default=True)
    selected = models.BooleanField(default=False)
    booked = models.BooleanField(default=False)

    def __str__(self):
        start_time = self.start_time.strftime('%H:%M') if self.start_time else "Unspecified"
        end_time = self.end_time.strftime('%H:%M') if self.end_time else "Unspecified"
        return f"{self.turf.name} - {self.get_day_of_week_display()} - {start_time} to {end_time}"


class Booking(models.Model):
    user_name = models.CharField(max_length=100, default="")
    user_email = models.EmailField(max_length=100, default="")
    turf_owner_email = models.EmailField(max_length=100, blank=True, null=True, default="")
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    booking_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.user_name} on {self.booking_date} - Time Slot: {self.time_slot}"


class Facilities(models.Model):
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    facilities = models.CharField(max_length=100, default="")

    def __str__(self):
        return f"Facilities for {self.turf.name}"

class Sports(models.Model):
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    sports = models.CharField(max_length=100)

    def __str__(self):
        return f"Sports for {self.turf.name}"

class TurfReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.turf.name}"