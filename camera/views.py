from django.shortcuts import render, redirect
from camera.forms import UserForm,UserProfileInfoForm, RoomForm, DeviceForm, CameraForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from camera.models import UserProfileInfo, Camera, Device, Room

def index(request):
    return render(request,'camera/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'camera/login.html', {})

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'camera/register.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})


@login_required
def create_room_view(request):
    upload = RoomForm()
    if request.method == 'POST':
        upload = RoomForm(request.POST)
        if upload.is_valid():
            room_save = upload.save(commit = False)
            room_save.user = request.user
            room_save.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url 'camera:create_room_view' }}">reload</a>""")
    else:
        return render(request, 'camera/create_room.html', {'upload_form':upload})

@login_required
def create_device_view(request):
    user = request.user
    upload = DeviceForm(user)
    if request.method == 'POST':
        upload = DeviceForm(request.user, data = request.POST)
        if upload.is_valid():
            upload.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url 'camera:create_device_view' }}">reload</a>""")
    else:
        return render(request, 'camera/create_device.html', {'upload_form':upload})


