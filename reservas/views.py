from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import NoReverseMatch, reverse

from datetime import date, timedelta
from espacos.models import Espaco

from .forms import SolicitacaoReservaForm
from .models import Reserva
from usuarios.views import perfis_permitidos


def _pagina_de_volta():
    # Volta para "Minhas reservas" quando ela existir
    try:
        return reverse('minhas_reservas')
    except NoReverseMatch:
        return reverse('inicio')


@login_required
def cancelar_reserva(request, id):
    """SCRUM-35: o próprio usuário cancela uma reserva pendente ou aprovada."""
    reserva = get_object_or_404(Reserva, id=id, usuario=request.user)

    if reserva.status == Reserva.Status.CANCELADA:
        messages.info(request, 'Esta reserva já estava cancelada.')
        return redirect(_pagina_de_volta())

    if reserva.status not in (Reserva.Status.PENDENTE, Reserva.Status.APROVADA):
        messages.error(
            request,
            'Somente reservas pendentes ou aprovadas podem ser canceladas.'
        )
        return redirect(_pagina_de_volta())

    if request.method == 'POST':
        reserva.status = Reserva.Status.CANCELADA
        reserva.save()
        messages.success(request, 'Reserva cancelada com sucesso.')
        return redirect(_pagina_de_volta())

    return render(request, 'reservas/cancelar.html', {'reserva': reserva})


@login_required
def solicitar_reserva(request):
    """SCRUM-30: permite que um usuário autenticado solicite uma reserva."""

    if request.method == 'POST':
        form = SolicitacaoReservaForm(request.POST)

        if form.is_valid():
            reserva = form.save(commit=False)

            # Associa a reserva ao usuário autenticado.
            reserva.usuario = request.user

            # O status inicial é PENDENTE.
            # O signal do SCRUM-32 confirma automaticamente professores.
            reserva.status = Reserva.Status.PENDENTE

            reserva.save()

            messages.success(
                request,
                'Solicitação de reserva realizada com sucesso!'
            )

            return redirect('inicio')

    else:
        form = SolicitacaoReservaForm()

    return render(
        request,
        'reservas/solicitar.html',
        {'form': form}
    )


@login_required
def minhas_reservas(request):
    reservas = Reserva.objects.filter(
        usuario=request.user
    ).select_related('espaco')

    return render(
        request,
        'reservas/minhas_reservas.html',
        {'reservas': reservas}
    )


@login_required
@perfis_permitidos('ADMINISTRADOR')
def reservas_pendentes(request):
    reservas = Reserva.objects.filter(
        status=Reserva.Status.PENDENTE
    ).select_related('usuario', 'espaco').order_by('data', 'hora_inicio')

    return render(
        request,
        'reservas/pendentes.html',
        {'reservas': reservas}
    )


@login_required
@perfis_permitidos('ADMINISTRADOR')
def aprovar_reserva(request, id):
    if request.method != 'POST':
        return redirect('reservas_pendentes')

    reserva = get_object_or_404(
        Reserva,
        id=id,
        status=Reserva.Status.PENDENTE
    )

    reserva.status = Reserva.Status.APROVADA
    reserva.save()

    messages.success(request, 'Reserva aprovada com sucesso!')
    return redirect('reservas_pendentes')


@login_required
@perfis_permitidos('ADMINISTRADOR')
def recusar_reserva(request, id):
    if request.method != 'POST':
        return redirect('reservas_pendentes')

    reserva = get_object_or_404(
        Reserva,
        id=id,
        status=Reserva.Status.PENDENTE
    )

    reserva.status = Reserva.Status.RECUSADA
    reserva.save()

    messages.success(request, 'Reserva recusada com sucesso!')
    return redirect('reservas_pendentes')


@login_required
def reservas_do_espaco(request, espaco_id):
    espaco = get_object_or_404(Espaco, id=espaco_id)

    # Identifica a data de referência
    data_referencia = request.GET.get('semana')

    if data_referencia:
        try:
            data_referencia = date.fromisoformat(data_referencia)
        except ValueError:
            data_referencia = date.today()
    else:
        data_referencia = date.today()

    # Descobre o início e o fim da semana
    inicio_semana = data_referencia - timedelta(
        days=data_referencia.weekday()
    )

    fim_semana = inicio_semana + timedelta(days=6)

    # Busca as reservas daquele espaço na semana
    reservas = Reserva.objects.filter(
        espaco=espaco,
        data__range=[inicio_semana, fim_semana],
        status__in=[
            Reserva.Status.PENDENTE,
            Reserva.Status.APROVADA
        ]
    ).select_related('usuario').order_by('data', 'hora_inicio')

    # Calcula as semanas anterior e próxima
    semana_anterior = inicio_semana - timedelta(days=7)
    proxima_semana = inicio_semana + timedelta(days=7)

    return render(request, 'reservas/semana_espaco.html', {
        'espaco': espaco,
        'reservas': reservas,
        'inicio_semana': inicio_semana,
        'fim_semana': fim_semana,
        'semana_anterior': semana_anterior,
        'proxima_semana': proxima_semana,
    })
