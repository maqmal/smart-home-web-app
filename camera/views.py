from django.shortcuts import render, redirect
from camera.forms import UserForm, RoomForm, DeviceForm, CameraForm, DeviceUpdateForm, CameraUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from camera.models import UserProfileInfo, Camera, Device, Room
from json import dumps 
from asgiref.sync import sync_to_async
from django.http import JsonResponse
from django.contrib import messages
from django.template import loader

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

def delete(request, room_id):
    if request.method == 'POST':
        del_name = Room.objects.get(id = room_id)
        del_name.delete()
        messages.success(request, 'Room deleted successfully.')
    return HttpResponseRedirect(reverse('index'))

def delete_cam(request, cam_id):
    if request.method == 'POST':
        del_name = Camera.objects.get(id = cam_id)
        del_name.delete()
        messages.success(request, 'Camera deleted successfully.')
    return HttpResponseRedirect(reverse('index'))

def delete_device(request, device_id):
    if request.method == 'POST':
        del_name = Device.objects.get(id = device_id)
        del_name.delete()
        messages.success(request, 'Device deleted successfully.')
    return HttpResponseRedirect(reverse('index'))

@login_required
def create_device_view(request):
    user = request.user
    created=None
    if request.method == 'POST':
        upload = DeviceForm(user, data = request.POST)
        if upload.is_valid():
            upload.save()
            created = '1'
        else:
            created = '0'
    else:
        upload = DeviceForm(user)
    t = loader.get_template('camera/create_device.html')
    c = {'created': created,'upload_form':upload}
    return HttpResponse(t.render(c, request))

@login_required
def create_camera_view(request):
    user = request.user
    created = None
    if request.method == 'POST':
        upload = CameraForm(user, data = request.POST)
        if upload.is_valid():
            upload.save()
            created = "1"
        else:
            created = "0"
    else:
        upload = CameraForm(user)
    t = loader.get_template('camera/create_camera.html')
    c = {'created': created,'upload_form':upload}
    return HttpResponse(t.render(c, request))

def read_notif(request):
    user =  request.user
    user.notifications.mark_all_as_read()
    data = {'msg':'Notification Marked as Read'}
    return JsonResponse(data)

def update_room(request, room_id):
    room_field = Room.objects.get(id = room_id)
    upload = RoomForm(request.POST, instance=room_field)
    if upload.is_valid():
        messages.success(request, 'Room updated.')
        upload.save()
    return HttpResponseRedirect(reverse('index'))

def update_device(request, device_id):
    device_field = Device.objects.get(id = device_id)
    data = {'name':device_field.name, 'room':device_field.room, 'qos':device_field.qos}
    upload = DeviceUpdateForm(request.user, request.POST,instance=device_field, initial=data)
    if upload.is_valid():
        messages.success(request, 'Device updated.')
        upload.save()
    return HttpResponseRedirect(reverse('index'))
    
def update_cam(request, cam_id):
    camera_field = Camera.objects.get(id = cam_id)
    data = {'name':camera_field.name, 'room':camera_field.room,'warning_system':camera_field.warning_system,'ai_enable':camera_field.ai_enable}
    upload = CameraUpdateForm(request.user, request.POST, instance=camera_field, initial=data)
    if upload.is_valid():
        messages.success(request, 'Camera updated.')
        upload.save()
    return HttpResponseRedirect(reverse('index'))


@login_required
def get_data(request):
    created = None
    raw_data = []
    dataJSON = None
    update_device = DeviceUpdateForm(request.user)
    update_cam = CameraUpdateForm(request.user)
    if request.method == 'POST':
        upload = RoomForm(request.POST)
        if upload.is_valid():
            room_save = upload.save(commit = False)
            room_save.user = request.user
            room_save.save()
            messages.success(request, 'Room created successfully.')
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'Room name already used.')
            return HttpResponseRedirect(reverse('index'))
    else:
        upload = RoomForm()

        ambil_room = Room.objects.filter(user=request.user).values_list('name',flat=True)
        ambil_room_id = ambil_room.values_list('id',flat=True)

        ambil_device = Device.objects.filter(room__user=request.user)
        ambil_device_id = ambil_device.values_list('id',flat=True)
        nama_room_device = ambil_device.values_list('room__name',flat=True)
        nama_device = ambil_device.values_list('name',flat=True)
        topic = ambil_device.values_list('topic',flat=True)

        ambil_camera = Camera.objects.filter(room__user=request.user)
        ambil_camera_id = ambil_camera.values_list('id',flat=True)
        url_camera = ambil_camera.values_list('cam_url',flat=True)
        nama_room_camera = ambil_camera.values_list('room__name',flat=True)
        nama_camera = ambil_camera.values_list('name',flat=True)
        warning = ambil_camera.values_list('warning_system',flat=True)

        for i in range(len(ambil_room)):
            data = {}
            data['room']={}
            data['room']['id'] = ambil_room_id[i]
            data['room']['nama'] = ambil_room[i]

            data['room']['device'] = {}
            data['room']['device']['id'] = []
            data['room']['device']['nama'] = []
            data['room']['device']['topic'] = []

            data['room']['camera'] = {}
            data['room']['camera']['id'] = []
            data['room']['camera']['nama'] = []
            data['room']['camera']['warning'] = []
            
            j = 0
            for device in nama_device:
                if (nama_room_device[j]==ambil_room[i]):
                    data['room']['device']['nama'].append(device)
                    data['room']['device']['id'].append(ambil_device_id[j])
                    data['room']['device']['topic'].append(topic[j])
                j+=1
                
            k = 0
            for camera in nama_camera:
                if (nama_room_camera[k]==ambil_room[i]):
                    data['room']['camera']['nama'].append(camera)
                    data['room']['camera']['id'].append(ambil_camera_id[k])
                    data['room']['camera']['warning'].append(warning[k])
                k+=1
            raw_data.append(data)
        dataJSON = dumps(raw_data) 
        print(raw_data)
        return render(request,'camera/index.html', {'data':raw_data,'dataJSON':dataJSON, 'upload_form':upload, 'update_device':update_device,'update_cam':update_cam})


