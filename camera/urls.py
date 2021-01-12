from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'camera'

urlpatterns = [
    path('register/', views.register, name ='register'),
    # path('', views.create_room_view, name ='create_room_view'),
    path('create_device/', views.create_device_view, name ='create_device_view'),
    path('create_camera/', views.create_camera_view, name ='create_camera_view'),

    path('del/<slug:delname>', views.delete, name='delete_room'),
    path('del_cam/<slug:delname>', views.delete_cam, name='delete_cam'),
    path('del_device/<slug:delname>', views.delete_device, name='delete_device'),

    path('face_detect/<int:cam_id>',views.face_detect, name='face_detect'),
    path('', views.get_data, name ='get_data'),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)