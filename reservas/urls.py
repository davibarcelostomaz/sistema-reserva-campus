from django.urls import path

from . import views

urlpatterns = [
    path('solicitar/', views.solicitar_reserva, name='solicitar_reserva'),
    path('<int:id>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
]
