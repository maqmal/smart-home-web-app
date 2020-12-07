from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Device(models.Model):
    name = models.CharField(max_length = 50)
    sub = models.CharField(max_length = 50)
    created_at = models.DateField(auto_now_add=True, blank=True) 
    def __str__(self):
        return self.name

class Camera(models.Model):
    name = models.CharField(max_length = 50)
    cam_url = models.CharField(max_length = 200)
    created_at = models.DateField(auto_now_add=True, blank=True) 
    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length = 50)
    camera = models.ManyToManyField(Camera, blank=True)
    device = models.ManyToManyField(Device, blank=True)
    created_at = models.DateField(auto_now_add=True, blank=True)
    def __str__(self):
        return self.name

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    room = models.ManyToManyField(Room)
    def __str__(self):
        return self.user.username