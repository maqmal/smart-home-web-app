from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    def __str__(self):
        return self.user.username

class Room(models.Model):
    name = models.CharField(max_length = 50)
    created_at = models.DateField()
    def __str__(self):
        return self.name

class Device(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    created_at = models.DateField() 
    def __str__(self):
        return self.name

class Camera(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    cam_url = models.CharField(max_length = 200)
    created_at = models.DateField() 
    def __str__(self):
        return self.name