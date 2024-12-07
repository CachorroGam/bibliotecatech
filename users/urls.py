from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dash_usuario', views.dash_usuario, name='dash_usuario'),
    path('dash_empleado', views.dash_empleado, name='dash_empleado'),
    path('dash_jefe', views.dash_jefe, name='dash_jefe'),
    path('dash_admin', views.dash_admin, name='dash_admin'),
    
]
