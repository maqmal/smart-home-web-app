from camera.cv import FaceDetect
from django.shortcuts import render, redirect
from camera.forms import UserForm, RoomForm, DeviceForm, CameraForm
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.urls import reverse
from camera.models import UserProfileInfo, Camera, Device, Room
from django.contrib.auth.models import User
from django.views.decorators import gzip
import numpy as np
import cv2
from datetime import datetime
from datetime import date
import time
from notifications.signals import notify
from json import dumps 

def generator(camera, logged_in, url_cam):
    user = User.objects.get(username=logged_in)
    trigger = False
    notifSent = False
    writer = None
    iterate = 0

    ambil_room = Room.objects.filter(user=user).values_list('name',flat=True)

    ambil_camera = Camera.objects.filter(room__user=user)
    
    url_camera = ambil_camera.values_list('cam_url',flat=True)
    nama_room_camera = ambil_camera.values_list('room__name',flat=True)
    while True:
        data = {}
        data['location'] = {}
        data['date'] = {}
        data['time'] = {}
        data['duration'] = {}
        for i in range(len(ambil_room)):
            k = 0
            for camera_iterate in url_camera:
                if (str(url_camera[k])==str(url_cam)):
                    data['location'] = nama_room_camera[k]
                k+=1

        frame, detected = camera.get_frame()
        triggerPrev = trigger
        if detected:
            trigger = True
        else:
            trigger = False

        if (trigger and not triggerPrev):
            startTime = datetime.now()
            
            # fourcc = cv2.VideoWriter_fourcc(*'XVID')
            # filename = "video/{}_{}.avi".format(startTime.strftime('%A'),iterate)
            # writer = cv2.VideoWriter(filename,fourcc,20,(640,480))
        elif triggerPrev:
            timeDiff = (datetime.now() - startTime).seconds
            if trigger and timeDiff > 20:
                if not notifSent:
                    # writer.release()
                    # writer = None
				
                    notifSent = True
            if not trigger:
                # if a notification has already been sent, then just set 
                # the notifSent to false for the next iteration
                if notifSent:
                    notifSent = False
                else:
                    # record the end time and calculate the total time in
                    # seconds
                    endTime = datetime.now()
                    totalSeconds = (endTime - startTime).seconds
                    dateOpened = date.today().strftime("%A, %B %d %Y")
                    # build the message and send a notification
                    if totalSeconds>=3:
                        data['date'] = dateOpened
                        data['time'] = startTime.strftime("%I:%M%p")
                        data['duration'] = totalSeconds

                        iterate += 1
                        # writer.release()
                        # writer = None
                        dataJSON = dumps(data) 
                        string = 'Someone was in ' + data['location'] + ' at ' + str(data['time'])+ ' for ' + str(data['duration'])+ ' seconds'
                        notify.send(user, recipient=user, verb=string, level='warning')
                        print(dataJSON) 

        # frame_decode = cv2.imdecode(np.fromstring(frame, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        # if writer is not None:
        #     writer.write(frame_decode)

        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
    # if writer is not None:
    #     writer.release()

@gzip.gzip_page
def face_detect(request, cam_id):
    logged_in = request.user
    camera = Camera.objects.filter(pk=cam_id).values_list('cam_url',flat=True)
    for cam in camera:
        print("==>>", cam)
        if cam == "0":
            cam = int(cam)
        url_cam = cam
    return StreamingHttpResponse(generator(FaceDetect(url_cam),logged_in,url_cam),content_type="multipart/x-mixed-replace;boundary=frame")