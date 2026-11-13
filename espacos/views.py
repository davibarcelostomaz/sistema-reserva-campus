from django.shortcuts import render, redirect
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
