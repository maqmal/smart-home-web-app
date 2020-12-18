import cv2
from imutils.io import TempFile
from datetime import datetime
from datetime import date
import imutils
import time
import os
from django.conf import settings
from azure.storage.blob import ContainerClient
from azure.storage.blob import BlobClient


class FaceDetect(object):
    def __init__(self, url):
        self.capture = cv2.VideoCapture(url)
        self.faceDetect = cv2.CascadeClassifier(os.path.join(settings.BASE_DIR,'haarcascade/haarcascade_frontalface_default.xml'))

    def __del__(self):
        self.capture.release()
    
    def get_frame(self):        
        _,frame = self.capture.read()
        resize_frame = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_LINEAR)  

        gray = cv2.cvtColor(resize_frame,cv2.COLOR_BGR2GRAY)
        
        faces = self.faceDetect.detectMultiScale(gray,1.3,5)

        if faces == ():
            detected = False
        else:
            detected = True

        for (x,y,w,h) in faces:
            cv2.rectangle(resize_frame,(x,y), (x+w,y+h),(0,255,0),2)

        _,jpeg = cv2.imencode('.jpg',resize_frame)
        return jpeg.tobytes(), detected
    
    def upload_video(self):
        if self.iterate!=0:
            file_list = os.listdir('video/')
            for i in range(len(file_list)):
                input_file_path = 'video/{}'.format(file_list[i])
                output_blob_name = file_list[i]
                blob = BlobClient.from_connection_string(conn_str=CONNECT_STR, container_name=CONTAINER_NAME, blob_name=output_blob_name)
                exists = blob.exists()
                if exists:
                    print("File already exist!")
                else:
                    with open(input_file_path, "rb") as data:
                        container_client.upload_blob(name=output_blob_name, data=data)
                    print("Upload file",i,",Succsess")

