from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import EspacoForm
from .models import Espaco
from usuarios.views import perfis_permitidos

@perfis_permitidos('ADMINISTRADOR')
def cadastrar_espaco(request):

    if request.method == 'POST':
        form = EspacoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('listar_espacos')

    else:
        form = EspacoForm()

    return render(request, 'espacos/cadastrar.html', {'form': form})


@login_required
def listar_espacos(request):

    espacos = Espaco.objects.all()

    return render(request, 'espacos/listar.html', {
        'espacos': espacos
    })

@perfis_permitidos('ADMINISTRADOR')
def editar_espaco(request, id):

    espaco = get_object_or_404(Espaco, id=id)

    if request.method == 'POST':
        form = EspacoForm(request.POST, instance=espaco)

        if form.is_valid():
            form.save()
            return redirect('listar_espacos')

    else:
        form = EspacoForm(instance=espaco)

    return render(request, 'espacos/editar.html', {
        'form': form,
        'espaco': espaco
    })


@perfis_permitidos('ADMINISTRADOR')
def excluir_espaco(request, id):

    espaco = get_object_or_404(Espaco, id=id)

    if request.method == 'POST':
        espaco.delete()
        return redirect('listar_espacos')

    return render(request, 'espacos/excluir.html', {
        'espaco': espaco
    })