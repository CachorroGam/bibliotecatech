from django.contrib.auth.models import User
from django.core.management import call_command

call_command('createsuperuser', '--no-input', username='admin', email='franklinpop03azul@gmail.com', password='fisn853nmf')
