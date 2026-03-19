from django.contrib import admin
from .models import RoomCategory, Room, RoomBooking, FoodItem, PartyBooking, SystemSetting, FoodOrder

admin.site.register(RoomCategory)
admin.site.register(Room)
admin.site.register(RoomBooking)
admin.site.register(FoodItem)
admin.site.register(PartyBooking)
admin.site.register(SystemSetting)
admin.site.register(FoodOrder)
