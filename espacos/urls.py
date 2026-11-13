from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_espaco, name='cadastrar_espaco'),
    path('', views.listar_espacos, name='listar_espacos'),
]