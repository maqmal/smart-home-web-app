from django import forms
from camera.models import UserProfileInfo, Camera, Device, Room
from django.contrib.auth.models import User
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')

class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = UserProfileInfo
         fields = ('profile_pic',)

class RoomForm(forms.ModelForm):
    class Meta():
        model = Room
        fields = ('name','camera','device')

class DeviceForm(forms.ModelForm):
    class Meta():
        model = Device
        fields = ('name','sub')

class CameraForm(forms.ModelForm):
    class Meta():
        model = Camera
        fields = ('name', 'cam_url',)