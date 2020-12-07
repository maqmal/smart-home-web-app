from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'camera'

urlpatterns = [
    path('user_login/', views.user_login, name='user_login'),
    path('register/', views.register, name ='register'),
    # path('', views.get_user, name ='get_user'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)