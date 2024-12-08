from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def index(request):
    return render(request, 'index.html')

def dash_usuario(request):
    return render(request, 'dash_usuario.html')
def dash_empleado(request):
    return render(request, 'dash_empleado.html')
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
        
        return redirect('/login')  # Redirigir a la página de login después de registrarse
    
    return render(request, '/register')



