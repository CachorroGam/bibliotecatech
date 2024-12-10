from django.urls import path
from . import views
from .views import profile_view, settings_view, delete_account, logout_view, settings_usuario_view, contacto_users, profile_empleado_view, settings_empleado_view
from django.conf import settings
from django.conf.urls.static import static
from .views import profile_users_view, settings_view_jefe, profile_view_jefe

from users.forms import LoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dash_usuario', views.dash_usuario, name='dash_usuario'),
    path('dash_empleado', views.dash_empleado, name='dash_empleado'),
    path('dash_jefe', views.dash_jefe, name='dash_jefe'),
    path('dash_admin', views.dash_admin, name='dash_admin'),
    path('logout/', logout_view, name='logout'),
    path('contacto/', views.contacto, name='contacto'),
    path('contacto_users/', contacto_users, name='contacto_users'),

    path('settings/', settings_view, name='settings'),
    path('settings_jefe/', settings_view_jefe, name='settings_jefe'),
    path('settings_empleado/', settings_empleado_view, name='settings_empleado'),
    path('profile/', profile_view, name='profile'),

    path('profile_jefe/', profile_view_jefe, name='profile_jefe'),
    path('profile_empleado/', profile_empleado_view, name='profile_empleado'),
    path('settings_usuario/', settings_usuario_view, name='settings_usuario'),
    path('delete_account/', delete_account, name='delete_account'), 
    path('libros/', views.listar_libros, name='libros'),

    path('libros_jefe/', views.listar_libros_jefe, name='libros_jefe'),
    path('libros_empleado/', views.listar_libros_empleado, name='libros_empleado'),
    path('editar_libro/<int:id>/', views.editar_libro, name='editar_libro'),
    path('editar_libro_jefe/<int:id>/', views.editar_libro_jefe, name='editar_libro_jefe'),
    path('register_libro_new/', views.registrar_libro, name='register_libro_new'),
    path('register_libro_new_jefe/', views.registrar_libro_jefe, name='register_libro_new_jefe'),
    path('register_libro_new_empleado/', views.registrar_libro_empleado, name='register_libro_new_empleado'),
    path('eliminar_libro/<int:id>/', views.eliminar_libro, name='eliminar_libro'),
    path('users/', views.users, name='users'),
    path('users_jefe/', views.users_jefe, name='users_jefe'),
    path('eliminar_usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('editar_usuario/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('editar_usuario_jefe/<int:id>/', views.editar_usuario_jefe, name='editar_usuario_jefe'),
    path('editar_usuario_empleado/<int:id>/', views.editar_usuario_empleado, name='editar_usuario_empleado'),
    path('libros_users/', views.listar_libros_users, name='libros_users'),
    path('libro/', views.listar_libro, name='libro'),
    path('contacto/', views.contacto, name='contacto'),
    path('contacto_users/', contacto_users, name='contacto_users'),
    path('detalles_libro/<int:id>/', views.detalles_libro, name='detalles_libro'),
    path('detalles_libro_pre/<int:id>/', views.detalles_libro_pre, name='detalles_libro_pre'),
    path('reservar_libro/<int:libro_id>/', views.reservar_libro, name='reservar_libro'),
    path('cancelar_reserva/<int:libro_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('reservas/', views.reservas_view, name='reservas'),  
    path('reservas_jefe/', views.reservas_view_jefe, name='reservas_jefe'),  
    path('reservas/eliminar/<int:id>/', views.eliminar_reserva, name='eliminar_reserva'),
    path('libro/<int:libro_id>/realizar_prestamo/', views.realizar_prestamo, name='realizar_prestamo'),
    path('libro/<int:libro_id>/realizar_prestamo_jefe/', views.realizar_prestamo_jefe, name='realizar_prestamo_jefe'),
    path('devolver_libro/<int:libro_id>/', views.devolver_libro, name='devolver_libro'),

    

    path('historial/', views.historial_prestamos, name='historial_prestamos'),
    path('historial_jefe/', views.historial_prestamos_jefe, name='historial_prestamos_jefe'),

    path('mis_prestamos/', views.mis_prestamos, name='mis_prestamos'),
    path('profile_users/', profile_users_view, name='profile_users'),







    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
