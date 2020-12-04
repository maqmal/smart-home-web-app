from django.contrib import admin
from camera.models import UserProfileInfo, User, Camera, Room, Device
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Room)
admin.site.register(Device)
admin.site.register(Camera)