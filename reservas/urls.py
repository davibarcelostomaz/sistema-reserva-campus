from django.urls import path
from . import views

urlpatterns = [
    path('solicitar/', views.solicitar_reserva, name='solicitar_reserva'),

    path('minhas-reservas/', views.minhas_reservas, name='minhas_reservas'),

    path('pendentes/', views.reservas_pendentes, name='reservas_pendentes'),

    path('<int:id>/aprovar/', views.aprovar_reserva, name='aprovar_reserva'),

    path('<int:id>/recusar/', views.recusar_reserva, name='recusar_reserva'),

    path('<int:id>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
]