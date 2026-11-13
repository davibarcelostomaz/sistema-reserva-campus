from functools import wraps

from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden

from .forms import CadastroUsuarioForm


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)

        if form.is_valid():
            usuario = form.save()
            login(request, usuario)

            messages.success(
                request,
                'Cadastro realizado com sucesso!'
            )

            return redirect('inicio')
    else:
        form = CadastroUsuarioForm()

    return render(
        request,
        'usuarios/cadastro.html',
        {'form': form}
    )

@login_required
def inicio(request):
    return render(
        request,
        'usuarios/inicio.html'
    )

def perfis_permitidos(*perfis):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if request.user.perfil not in perfis:
                return HttpResponseForbidden(
                    'Você não tem permissão para acessar esta página.'
                )

            return view_func(request, *args, **kwargs)

        return login_required(wrapper)

    return decorator

@perfis_permitidos('ADMINISTRADOR')
def teste_administrador(request):
    return HttpResponse("Acesso permitido! Você é administrador.")
