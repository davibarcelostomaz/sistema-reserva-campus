"""Cria usuários de teste para desenvolvimento local.

Uso: .venv/Scripts/python manage.py shell -c "exec(open('seed_dev.py', encoding='utf-8').read())"
Senha de todos: teste12345
"""
from usuarios.models import Usuario

for username, perfil in [('admin', 'ADMINISTRADOR'), ('aluno', 'ALUNO'), ('professor', 'PROFESSOR')]:
    u, _ = Usuario.objects.get_or_create(username=username, defaults={'perfil': perfil, 'first_name': username.title()})
    u.perfil = perfil
    u.set_password('teste12345')
    u.save()
    print('ok', username, perfil)
