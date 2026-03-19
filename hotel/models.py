from django.db import models
from django.contrib.auth.models import User

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)   # NEW

class OTP(models.Model):
    phone = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

# Room Category
class RoomCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    price = models.IntegerField()
    available = models.BooleanField(default=True)

# Room Booking
class RoomBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.room}"

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class PartyBooking(models.Model):
    PAYMENT_CHOICES = [
        ('advance', 'Advance'),
        ('full', 'Full Payment'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    people = models.PositiveIntegerField()
    date = models.DateField()

    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    confirmed = models.BooleanField(default=False)

    total_price = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date}"


class BookingItem(models.Model):
    booking = models.ForeignKey(PartyBooking, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def get_price(self):
        return self.food_item.price * self.quantity

    def __str__(self):
        return f"{self.food_item.name} x {self.quantity}"

class SystemSetting(models.Model):
    food_order_enabled = models.BooleanField(default=True)
    room_booking_enabled = models.BooleanField(default=True)
    payment_enabled = models.BooleanField(default=True)

    def __str__(self):
        return "System Settings"

class FoodOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField()
    paid = models.BooleanField(default=False)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1) 

class FoodOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    price = models.IntegerField()
