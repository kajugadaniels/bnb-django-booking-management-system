import os
import random
from django.db import models
from django.db.models import Avg
from django.utils import timezone
from django.utils.text import slugify
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField

class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"

def room_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return f'rooms/room_{slugify(instance.name)}_{instance.created_at}{file_extension}'

class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.IntegerField(null=True, blank=True)
    capacity = models.IntegerField()
    size = models.CharField(max_length=255, null=True, blank=True)
    image = ProcessedImageField(
        upload_to='room_images/',
        # processors=[ResizeToFill(1340, 894)],
        format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True,
    )
    amenities = models.ManyToManyField('Amenity', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        base_slug = slugify(self.name)
        unique_slug = base_slug
        num = 1
        while Room.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{num}"
            num += 1
        return unique_slug

    # Method to retrieve review data (total reviews and average ratings)
    def get_review_data(self):
        reviews = self.roomreview_set.filter(status=True)  # Filter reviews with status=True
        total_reviews = reviews.count()
        
        # Aggregate average ratings
        avg_ratings = reviews.aggregate(
            avg_location=Avg('location'),
            avg_staff=Avg('staff'),
            avg_cleanliness=Avg('cleanliness'),
            avg_value_for_money=Avg('value_for_money'),
            avg_comfort=Avg('comfort'),
            avg_facilities=Avg('facilities'),
            avg_free_wifi=Avg('free_wifi')
        )

        # Calculate overall rating
        if total_reviews > 0:
            overall_rating = (
                avg_ratings['avg_location'] +
                avg_ratings['avg_staff'] +
                avg_ratings['avg_cleanliness'] +
                avg_ratings['avg_value_for_money'] +
                avg_ratings['avg_comfort'] +
                avg_ratings['avg_facilities'] +
                avg_ratings['avg_free_wifi']
            ) / 7
        else:
            overall_rating = 0  # Default to 0 if no reviews

        return {
            'total_reviews': total_reviews,
            'overall_rating': round(overall_rating, 2) if overall_rating else 0
        }

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Rooms"

def room_add_on_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    random_number = random.randint(1000, 9999)
    return f'rooms/add_on/{random_number}_{instance.created_at}{file_extension}'

class RoomImage(models.Model):
    room = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE)
    image = ProcessedImageField(
        upload_to=room_add_on_image_path,
        # processors=[ResizeToFill(1340, 894)],
        format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.room.name} - {self.created_at}"

    class Meta:
        verbose_name_plural = "Room Images"

class RoomReview(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    location = models.IntegerField(default=5, null=True, blank=True)
    staff = models.IntegerField(default=5, null=True, blank=True)
    cleanliness = models.IntegerField(default=5, null=True, blank=True)
    value_for_money = models.IntegerField(default=5, null=True, blank=True)
    comfort = models.IntegerField(default=5, null=True, blank=True)
    facilities = models.IntegerField(default=5, null=True, blank=True)
    free_wifi = models.IntegerField(default=5, null=True, blank=True)
    status = models.BooleanField(default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.name} for {self.room.name}"

    class Meta:
        verbose_name_plural = "Room Reviews"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    checkInDate = models.DateField(null=True, blank=True)
    checkOutDate = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    special_request = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, null=True, blank=True)
    transactionId = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Booking for {self.room} by {self.name}"

def team_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return f'team/member_{slugify(instance.name)}_{instance.created_at}{file_extension}'

class Team(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    image = ProcessedImageField(
        upload_to=team_image_path,
        processors=[ResizeToFill(234, 300)],
        format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Team Members"

def testimony_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return f'testimony/person_{slugify(instance.name)}_{instance.created_at}{file_extension}'

class Testimony(models.Model):
    STAR_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]

    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    rating = models.IntegerField(choices=STAR_CHOICES)
    image = ProcessedImageField(
        upload_to=testimony_image_path,
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True,
    )
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Testimonies"

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Message from {self.name} - {self.subject}'

class Setting(models.Model):
    email = models.CharField(max_length=255, null=True, blank=True)
    second_email = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    instagram = models.URLField(max_length=255, null=True, blank=True)
    twitter = models.URLField(max_length=255, null=True, blank=True)
    facebook = models.URLField(max_length=255, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Ensure only one instance of settings can exist
        if not self.pk and Setting.objects.exists():
            raise ValueError("You can only create one instance of the settings.")
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Website Settings"

    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"