from django.urls import path
from . import views, cam_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'camera'

urlpatterns = [
    path('register/', views.register, name ='register'),

    path('create_device/', views.create_device_view, name ='create_device_view'),
    path('create_camera/', views.create_camera_view, name ='create_camera_view'),

    path('del/<int:room_id>', views.delete, name='delete_room'),
    path('del_cam/<int:cam_id>', views.delete_cam, name='delete_cam'),
    path('del_device/<int:device_id>', views.delete_device, name='delete_device'),

    path('update_room/<int:room_id>', views.update_room, name='update_room'),
    path('update_device/<int:device_id>', views.update_device, name='update_device'),
    path('update_cam/<int:cam_id>', views.update_cam, name='update_cam'),

    path('face_detect/<int:cam_id>',cam_views.face_detect, name='face_detect'),
    path('off_cam/<int:cam_id>',cam_views.off_cam, name='off_cam'),

    path('device_view/', views.get_data_device, name ='device_view'),
    path('cam_view/', views.get_data_cam, name ='cam_view'),
    path('', views.get_data, name ='get_data'),
    path('read_notif/', views.read_notif, name ='read_notif'),

    path('device_view/del/<int:room_id>', views.delete, name='delete_room_device_view'),
    path('device_view/update_room/<int:room_id>', views.update_room, name='update_room_device_view'),
    path('device_view/del_device/<int:device_id>', views.delete_device, name='delete_device_view'),
    path('device_view/update_device/<int:device_id>', views.update_device, name='update_device_view'),

    path('cam_view/del/<int:room_id>', views.delete, name='delete_room_cam_view'),
    path('cam_view/update_room/<int:room_id>', views.update_room, name='update_room_cam_view'),
    path('cam_view/del_cam/<int:cam_id>', views.delete_cam, name='delete_cam_view'),
    path('cam_view/update_cam/<int:cam_id>', views.update_cam, name='update_cam_view'),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)