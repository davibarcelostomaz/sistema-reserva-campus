from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_espacos, name='listar_espacos'),
    path('cadastrar/', views.cadastrar_espaco, name='cadastrar_espaco'),
    path('editar/<int:id>/', views.editar_espaco, name='editar_espaco'),
    path('excluir/<int:id>/', views.excluir_espaco, name='excluir_espaco'),
]