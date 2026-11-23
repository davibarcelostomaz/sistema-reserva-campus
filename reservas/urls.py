from django.urls import path

from . import views

urlpatterns = [
    path('<int:id>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
]
