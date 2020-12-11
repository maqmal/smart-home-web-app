from django import forms
from camera.models import UserProfileInfo, Camera, Device, Room
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')

# class UserProfileInfoForm(forms.ModelForm):
#      class Meta():
#          model = UserProfileInfo
#          fields = ('profile_pic',)

class RoomForm(forms.ModelForm):
    class Meta():
        model = Room
        fields = ('name',)
        exclude = ["user"]

class DeviceForm(forms.ModelForm):
    room = forms.ModelChoiceField(queryset = Room.objects.filter(user_id=1))
    def __init__(self, user, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.filter(user=user)
    class Meta():
        model = Device
        fields = ('name','sub','room',)
        exclude = ["user"]

class CameraForm(forms.ModelForm):
    room = forms.ModelChoiceField(queryset = Room.objects.filter(user_id=1))
    def __init__(self, user, *args, **kwargs):
        super(CameraForm, self).__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.filter(user=user)
    class Meta():
        model = Camera
        fields = ('name', 'cam_url','room',)
        exclude = ["user"]