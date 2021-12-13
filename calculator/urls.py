from django.urls import path

from . import views     # it means - 'from all import views'

urlpatterns = [
    path('',views.index, name='index'),
    path('add',views.addition, name='add'),
    path('sub',views.subtraction, name='sub'),
    path('multi',views.multiplication, name='multi'),
    path('div',views.division, name='div'),
    path('entDeg',views.degrau, name='entDeg'),
    path('ent',views.ent, name = 'ent'),
    path('csd',views.csd, name = 'csd'),
    path('cc',views.cc, name = 'cc'),
    path('cpid',views.cpid, name = 'cpid')
]

# whenever 'localhost:8000' will be called, function named 'index' will be called that is present in 'views.py' file
# This will happen for all other routes as well