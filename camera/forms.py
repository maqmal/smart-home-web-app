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
        fields = ('name','topic','room',)
        exclude = ["user"]

class CameraForm(forms.ModelForm):
    room = forms.ModelChoiceField(queryset = Room.objects.filter(user_id=1))
    def __init__(self, user, *args, **kwargs):
        super(CameraForm, self).__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.filter(user=user)
    class Meta():
        model = Camera
        fields = ('name', 'cam_url','room','warning_system',)
        exclude = ["user",]

class DeviceUpdateForm(forms.ModelForm):
    room = forms.ModelChoiceField(queryset = Room.objects.filter(user_id=1))
    def __init__(self, user, *args, **kwargs):
        super(DeviceUpdateForm, self).__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.filter(user=user)
    class Meta():
        model = Device
        fields = ('name','room','qos')
        exclude = ["user"]

class CameraUpdateForm(forms.ModelForm):
    room = forms.ModelChoiceField(queryset = Room.objects.filter(user_id=1))
    def __init__(self, user, *args, **kwargs):
        super(CameraUpdateForm, self).__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.filter(user=user)
    class Meta():
        model = Camera
        fields = ('name', 'room','warning_system','ai_enable')
        exclude = ["user",]

