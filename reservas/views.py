from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import NoReverseMatch, reverse

from .models import Reserva


def _pagina_de_volta():
    # Volta para "Minhas reservas" quando ela existir
    try:
        return reverse('minhas_reservas')
    except NoReverseMatch:
        return reverse('inicio')


@login_required
def cancelar_reserva(request, id):
    """SCRUM-35: o próprio usuário cancela uma reserva pendente ou confirmada."""
    reserva = get_object_or_404(Reserva, id=id, usuario=request.user)

    if reserva.status == Reserva.Status.CANCELADA:
        messages.info(request, 'Esta reserva já estava cancelada.')
        return redirect(_pagina_de_volta())

    if request.method == 'POST':
        reserva.status = Reserva.Status.CANCELADA
        reserva.save()
        messages.success(request, 'Reserva cancelada com sucesso.')
        return redirect(_pagina_de_volta())

    return render(request, 'reservas/cancelar.html', {'reserva': reserva})
