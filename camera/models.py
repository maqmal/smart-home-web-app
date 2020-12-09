from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    def __str__(self):
        return self.user.username

class Room(models.Model):
    name = models.CharField(max_length = 50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, blank=True)
    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length = 50)
    sub = models.CharField(max_length = 50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, blank=True) 
    def __str__(self):
        return self.name

class Camera(models.Model):
    name = models.CharField(max_length = 50)
    cam_url = models.CharField(max_length = 200)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, blank=True) 
    def __str__(self):
        return self.name

