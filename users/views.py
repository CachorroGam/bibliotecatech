from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from .models import Profile
from django.db.models import Max
from django.db.models import Count
from .models import Prestamo, Libro
from .models import UserProfile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .models import Libro
from django.shortcuts import render, get_object_or_404
from .forms import LibroForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Group
from .forms import UserForm  
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Libro, Prestamo
from django.utils import timezone
from users.models import Prestamo
from .forms import EditarPrestamoForm
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout
from django.utils.decorators import decorator_from_middleware
from django.middleware.cache import CacheMiddleware


def index(request):
    libros = Libro.objects.all()
    return render(request, 'index.html', {'libros': libros})

def dash_usuario(request):
    libros = Libro.objects.all()
    return render(request, 'dash_usuario.html', {'libros': libros})


def dash_empleado(request):
    total_libros = Libro.objects.count()
    libros_disponibles = Libro.objects.filter(disponible=True).count()
    total_prestamos = Prestamo.objects.count()
    prestamos_activos = Prestamo.objects.filter(estado='prestado').count()

    libros_mas_prestados = Prestamo.objects.values('libro__titulo') \
        .annotate(total=Count('libro')) \
        .order_by('-total')[:5]

    context = {
        'total_libros': total_libros,
        'libros_disponibles': libros_disponibles,
        'total_prestamos': total_prestamos,
        'prestamos_activos': prestamos_activos,
        'libros_mas_prestados': libros_mas_prestados
    }

    return render(request, 'dash_empleado.html', context)

def dash_jefe(request):
    return render(request, 'dash_jefe.html')
def dash_admin(request):
    return render(request, 'dash_admin.html')




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Verificar el grupo al que pertenece el usuario
            if user.groups.filter(name='admin').exists():
                return redirect('dash_admin')  # Redirigir a la página de admin
            elif user.groups.filter(name='jefe').exists():
                return redirect('dash_jefe')  # Redirigir a la página de jefe
            elif user.groups.filter(name='empleado').exists():
                return redirect('dash_empleado')  # Redirigir a la página de empleado
            else:
                return redirect('dash_usuario')  # Redirigir a la página de usuario común
        else:
            # Mostrar mensaje de error si el usuario no es autenticado
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        return render(request, 'login.html')





from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = User.objects.create_user(username=username, password=password)
        
        # Asigna el grupo 'usuario' directamente al registrar
        group = Group.objects.get(name='usuario')
        user.groups.add(group)
        
        return redirect('login')  # Redirigir a la página de login después de registrarse
    
    return render(request, 'register.html')



def contacto(request):
    return render(request, 'contacto.html')



def contacto_users(request):

    context = {}
    response = render(request, 'contacto_users.html', context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response



def logout_view(request):
    logout(request) 
    return redirect('login') 





def settings_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        notifications = request.POST.get('notifications') == 'on'
        profile_picture = request.FILES.get('profile_pictures') 

        request.user.username = username
        request.user.email = email
        request.user.notifications = notifications 
        request.user.save()

        if new_password and new_password == confirm_password:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, '¡La contraseña se ha actualizado correctamente!')
        elif new_password:
            messages.error(request, 'Las contraseñas no coinciden.')

        # Manejo de la foto de perfil
        if profile_picture:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.profile_picture = profile_picture 
            user_profile.save()
            messages.success(request, '¡La foto de perfil se ha actualizado correctamente!')

        messages.success(request, '¡La configuración se ha actualizado correctamente!')
        return redirect('settings')

    return render(request, 'settings.html')


def settings_empleado_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        notifications = request.POST.get('notifications') == 'on'
        profile_picture = request.FILES.get('profile_picture')  


        request.user.username = username
        request.user.email = email
        request.user.notifications = notifications
        request.user.save()

        if new_password and new_password == confirm_password:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, '¡La contraseña se ha actualizado correctamente!')
        elif new_password:
            messages.error(request, 'Las contraseñas no coinciden.')

        if profile_picture:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.profile_picture = profile_picture 
            user_profile.save()
            messages.success(request, '¡La foto de perfil se ha actualizado correctamente!')

        messages.success(request, '¡La configuración se ha actualizado correctamente!')
        return redirect('settings_empleado')

    return render(request, 'settings_empleado.html')



def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    response = render(request, 'profile.html', {'user_profile': user_profile})
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def profile_empleado_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    response = render(request, 'profile_empleado.html', {'user_profile': user_profile})
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def settings_usuario_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        notifications = request.POST.get('notifications') == 'on'
        profile_picture = request.FILES.get('profile_picture') 

        if User.objects.filter(username=username).exclude(id=request.user.id).exists():
            messages.error(request, 'Este nombre de usuario ya está siendo utilizado.')
            return redirect('settings_usuario') 


        request.user.username = username
        request.user.email = email
        request.user.notifications = notifications 
        request.user.save()


        if new_password and new_password == confirm_password:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, '¡La contraseña se ha actualizado correctamente!')
        elif new_password:
            messages.error(request, 'Las contraseñas no coinciden.')

        if profile_picture:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.profile_picture = profile_picture 
            user_profile.save()
            messages.success(request, '¡La foto de perfil se ha actualizado correctamente!')

        messages.success(request, '¡La configuración se ha actualizado correctamente!')
        return redirect('settings_usuario')

    return render(request, 'settings_usuario.html')



def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Tu cuenta ha sido eliminada con éxito.')
        return redirect('index') 
    return redirect('settings')  






def listar_libros(request):
    libros = Libro.objects.all() 

    response = render(request, 'libros_list.html', {'libros': libros})

    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response

@login_required
def listar_libros_empleado(request):
    libros = Libro.objects.all() 

    response = render(request, 'libros_list_empleado.html', {'libros': libros})

    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response


def listar_libros_users(request):
    libros = Libro.objects.all() 

    response = render(request, 'listar_libros_users.html', {'libros': libros})

    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response


def listar_libro(request):
    libros = Libro.objects.all() 

    return render(request, 'listar_libro.html', {'libros': libros})

    # # Deshabilitar el almacenamiento en caché
    # response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    # response['Pragma'] = 'no-cache'
    # response['Expires'] = '0'

    # return response


def detalles_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    
    return render(request, 'detalles_libro.html', {'libro': libro})

def detalles_libro_pre(request, id):
    libro = get_object_or_404(Libro, id=id)
    
    return render(request, 'detalles_libro_pre.html', {'libro': libro})



def mis_prestamos(request):
    prestamos = Prestamo.objects.filter(usuario=request.user).select_related('libro')
    return render(request, 'mis_prestamos.html', {'prestamos': prestamos})





def registrar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('libros')
    else:
        form = LibroForm()
    
    return render(request, 'register_libro.html', {'form': form})


def registrar_libro_empleado(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('libros_empleado') 
    else:
        form = LibroForm()
    
    return render(request, 'register_libro_empleado.html', {'form': form})




def editar_libro(request, id):
    libro = get_object_or_404(Libro, id=id)

    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('dash_admin') 
    else:
        form = LibroForm(instance=libro)

    return render(request, 'editar_libro.html', {'form': form, 'libro': libro})



def eliminar_libro(request, id):
    libro = get_object_or_404(Libro, id=id)

    if request.method == 'POST':
        libro.delete()
        return redirect('dash_admin')

    return redirect('dash_admin')  

from django.shortcuts import render
from django.contrib.auth.models import User, Group

def users(request):
    usuarios = User.objects.all().select_related('profile')  # Cargar perfiles relacionados
    grupos = Group.objects.all()  # Obtener todos los grupos
    grouped_usuarios = {grupo.name: usuarios.filter(groups__name=grupo.name) for grupo in grupos}
    return render(request, 'users.html', {'grouped_usuarios': grouped_usuarios})



# def users(request):
#     all_users = User.objects.all()  
#     return render(request, 'users.html', {'all_users': all_users})


def users_empleado(request):
    all_users = User.objects.all() 
    return render(request, 'users_empleado.html', {'all_users': all_users})




def eliminar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('users')  


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from .forms import UserForm
from django.db import transaction  # Para manejar transacciones en la base de datos

def editar_usuario(request, id):
    user = get_object_or_404(User, id=id)

    tiene_admin = user.groups.filter(name="admin").exists()
    tiene_empleado = user.groups.filter(name="empleado").exists()
    tiene_jefe = user.groups.filter(name="jefe").exists()
    tiene_usuario = user.groups.filter(name="usuario").exists()
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        role = request.POST.get('role')  # Obtener el valor del rol del formulario
        password_form = PasswordChangeForm(user, request.POST)

        new_role = request.POST.get('role')  
        
        if password_form.is_valid():
            user.set_password(password_form.cleaned_data['new_password1'])
            user.save()
            messages.success(request, "Contraseña cambiada con éxito")
        
        if new_role:
            group = Group.objects.get(name=new_role)
            user.groups.clear() 
            user.groups.add(group)  
            
            messages.success(request, f"Rol cambiado a {new_role}")
        
    else:
        form = UserForm(instance=user)
        password_form = PasswordChangeForm(user)
    
    return render(request, 'editar_usuario.html', {
        'form': form,
        'password_form': password_form,
        'user': user,
        'tiene_admin': tiene_admin,
        'tiene_empleado': tiene_empleado,
        'tiene_jefe': tiene_jefe,
        'tiene_usuario': tiene_usuario,
    })




from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserForm

def editar_usuario_empleado(request, id):
    user = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user, request.POST)
        
        if password_form.is_valid():
            user.set_password(password_form.cleaned_data['new_password1'])
            user.save()
            messages.success(request, "Contraseña cambiada con éxito")
        
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente")
            return redirect('users')
    
    else:
        form = UserForm(instance=user)
        password_form = PasswordChangeForm(user)
    
    return render(request, 'editar_usuario_empleado.html', {
        'form': form,
        'password_form': password_form,
        'user': user,
    })




@login_required
def reservar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if libro.reservado:
        if libro.reservado_por == request.user:
            libro.reservado = False
            libro.reservado_por = None
            libro.save()
            messages.success(request, f'Has cancelado tu reserva del libro: {libro.titulo}')
        else:
            messages.error(request, f'Este libro ya está reservado por otro usuario.')
    else:
        libro.reservado = True
        libro.reservado_por = request.user  # Aquí asignamos el usuario autenticado
        libro.save()
        messages.success(request, f'Has reservado el libro: {libro.titulo}')

    return redirect('detalles_libro', id=libro.id)





@login_required
def cancelar_reserva(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id, reservado_por=request.user)

    libro.reservado = False
    libro.reservado_por = None
    libro.save()
    messages.success(request, f'Has cancelado la reserva del libro "{libro.titulo}".')

    return redirect('detalles_libro', id=libro_id)




def reservas_view(request):
    reservas = Libro.objects.filter(reservado=True) 
    context = {
        'reservas': reservas
    }
    return render(request, 'reservas.html', context)




def eliminar_reserva(request, id):
    libro = get_object_or_404(Libro, id=id)

    if libro.reservado:
        libro.reservado = False 
        libro.reservado_por = None  
        libro.save()  

        messages.success(request, f'La reserva del libro "{libro.titulo}" ha sido eliminada exitosamente.')
    else:
        messages.error(request, 'Este libro no tiene una reserva activa.')

    return redirect('reservas')




from django.shortcuts import render, redirect, get_object_or_404
from .models import Prestamo, Libro
from .forms import PrestamoForm
from django.utils import timezone

def realizar_prestamo(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    
    if not libro.disponible:
        # Si el libro ya no está disponible, redirigir a la página de reservas o alguna otra acción
        return redirect('reservas')
    
    if request.method == 'POST':
        form = PrestamoForm(request.POST, user=request.user)
        if form.is_valid():
            prestamo = form.save()
            libro.disponible = False  # Marcar el libro como no disponible
            libro.save()
            return redirect('reservas')
    else:
        form = PrestamoForm(user=request.user)

    return render(request, 'realizar_prestamo.html', {'form': form})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone  # Asegúrate de importar esto
from .models import Prestamo

def devolver_libro(request, libro_id):
    # Busca el préstamo relacionado con el libro
    prestamo = get_object_or_404(Prestamo, libro_id=libro_id, estado='prestado')  # Verifica que 'estado' sea el campo correcto en tu modelo

    # Verifica si el libro no ha sido devuelto ya
    if prestamo.estado != 'devuelto':
        prestamo.estado = 'devuelto'  # Cambia el estado a 'devuelto'
        prestamo.fecha_devolucion = timezone.now()  # Registra la fecha de devolución
        prestamo.libro.disponible = True  # Marca el libro como disponible
        prestamo.libro.save()  # Guarda los cambios en el libro
        prestamo.save()  # Guarda los cambios en el préstamo

        messages.success(request, "El libro ha sido devuelto exitosamente.")
    else:
        messages.warning(request, "El libro ya había sido devuelto anteriormente.")
    
    # Redirige al usuario a su página de préstamos
    return redirect('reservas')  # Cambia esta ruta según tu aplicación









@login_required
def profile_users_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    response = render(request, 'profile_users.html', {'user_profile': user_profile})
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response