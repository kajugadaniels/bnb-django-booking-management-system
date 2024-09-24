from home.models import *
from django.contrib import admin

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'capacity', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('amenities',)
    inlines = [RoomImageInline]

@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ('room', 'created_at')
    search_fields = ('room__name',)

@admin.register(RoomReview)
class RoomReviewAdmin(admin.ModelAdmin):
    list_display = ['room', 'name', 'email', 'location', 'staff', 'cleanliness', 'value_for_money', 'comfort', 'facilities', 'free_wifi', 'status', 'created_at']
    list_filter = ['room', 'status', 'created_at']
    search_fields = ['name', 'email', 'room__name']
    ordering = ['created_at']
    readonly_fields = ['created_at']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'name', 'email', 'phone', 'checkInDate', 'checkOutDate', 'status', 'payment_status')
    list_filter = ('status', 'payment_status', 'checkInDate', 'checkOutDate')
    search_fields = ('name', 'email', 'phone', 'transactionId')