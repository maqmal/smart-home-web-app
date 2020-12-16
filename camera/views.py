from django.shortcuts import render, redirect
from camera.forms import UserForm, RoomForm, DeviceForm, CameraForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from camera.models import UserProfileInfo, Camera, Device, Room

def index(request):
    return render(request,'camera/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    if request.method == 'POST':
        login_failed = False
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
            login_failed = True
            return render(request, 'camera/login.html', {'login_failed': login_failed})
    else:
        return render(request, 'camera/login.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        #profile_form = UserProfileInfoForm(data=request.POST) =>> ini di if  and profile_form.is_valid()
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            #profile = profile_form.save(commit=False)
            #profile.user = user
            # if 'profile_pic' in request.FILES:
            #     print('found it')
            #     profile.profile_pic = request.FILES['profile_pic']
            #profile.save()
            registered = True
        # else:
            #print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        #profile_form = UserProfileInfoForm()  =>> ini ke render 'profile_form':profile_form,
    return render(request,'camera/register.html', {'user_form':user_form, 'registered':registered})


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

@login_required
def create_camera_view(request):
    user = request.user
    upload = CameraForm(user)
    if request.method == 'POST':
        upload = CameraForm(request.user, data = request.POST)
        if upload.is_valid():
            upload.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url 'camera:create_camera_view' }}">reload</a>""")
    else:
        return render(request, 'camera/create_camera.html', {'upload_form':upload})



@login_required
def get_data(request):
    ambil_room = Room.objects.filter(user=request.user).values_list('name',flat=True)

    ambil_device = Device.objects.filter(room__user=request.user)
    nama_room_device = ambil_device.values_list('room__name',flat=True)
    nama_device = ambil_device.values_list('name',flat=True)
    sub_device = ambil_device.values_list('sub',flat=True)

    ambil_camera = Camera.objects.filter(room__user=request.user)
    nama_room_camera = ambil_camera.values_list('room__name',flat=True)
    nama_camera = ambil_camera.values_list('name',flat=True)
    url_camera = ambil_camera.values_list('cam_url',flat=True)

    data = {}
    for i in range(len(ambil_room)):
        j = 0
        data[ambil_room[i]]={}
        data[ambil_room[i]]['device'] = []
        data[ambil_room[i]]['camera'] = []
        for device in nama_device:
            if (nama_room_device[j]==ambil_room[i]):
                data[ambil_room[i]]['device'].append(device)
            j+=1
        k = 0
        for camera in nama_camera:
            if (nama_room_camera[k]==ambil_room[i]):
                data[ambil_room[i]]['camera'].append(camera)
            k+=1
    print(data) 
    context = {'data':data }
    return render(request,'camera/index.html',context)