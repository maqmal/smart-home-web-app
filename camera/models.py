from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    def __str__(self):
        return self.user.username

class Room(models.Model):
    name = models.CharField(max_length = 50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, blank=True)
    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length = 50)
    topic = models.CharField(max_length = 50, unique=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    QOS_CHOICE = [
        ('0','QoS 0'),
        ('1','QoS 1'),
        ('2','QoS 2'),
    ]
    qos = models.CharField(
        max_length=5,
        choices=QOS_CHOICE,
        default='0',
    )
    created_at = models.DateField(auto_now_add=True, blank=True) 
    def __str__(self):
        return self.name

class Camera(models.Model):
    name = models.CharField(max_length = 50)
    cam_url = models.CharField(max_length = 200, unique=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, blank=True) 
    WARNING_CHOICE = [
        ('0',"Don't use warning system"),
        ('1','Warning system 1'),
        ('2','Warning system 2'),
    ]
    warning_system = models.CharField(
        max_length=100,
        choices=WARNING_CHOICE,
        default='0',
    )
    ai_enable = models.BooleanField(default=True)
    def __str__(self):
        return self.name

