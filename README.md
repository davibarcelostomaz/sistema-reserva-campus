# Reserva Campus

Sistema web para reserva de espaços do campus (salas, laboratórios, auditórios), feito em Django.

## Funcionalidades

- **Usuários:** cadastro e login. Os perfis são Aluno, Professor e Administrador.
- **Espaços:** o administrador cadastra, edita e exclui ambientes. Todos os usuários podem consultá-los.
- **Reservas:**
  - Qualquer usuário autenticado pode solicitar uma reserva.
  - O sistema bloqueia conflito de horário, data passada e horário de término anterior ao início.
  - Reservas de professores já entram **aprovadas**. As demais ficam **pendentes**.
- **Análise:** o administrador aprova ou recusa as reservas pendentes.
- **Cancelamento:** o usuário cancela as próprias reservas que estejam pendentes ou aprovadas.

## Como rodar

Requer Python 3.12 ou superior.

```bash
# 1. Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Criar o banco de dados
python manage.py migrate

# 4. Iniciar o servidor
python manage.py runserver
```

Depois, acesse http://localhost:8000.

## Usuários de teste

Para criar os usuários `admin`, `aluno` e `professor` (a senha está no próprio arquivo), rode:

```bash
python manage.py shell -c "exec(open('seed_dev.py', encoding='utf-8').read())"
```

Outra opção é criar um administrador com `python manage.py createsuperuser`. Ele já recebe o perfil Administrador.

## Testes

```bash
python manage.py test
```

## Estrutura

| App         | Responsabilidade                                      |
|-------------|-------------------------------------------------------|
| `usuarios`  | Modelo de usuário com perfil, cadastro, login e início |
| `espacos`   | Cadastro e listagem de ambientes                      |
| `reservas`  | Solicitação, análise e cancelamento de reservas       |

## Principais URLs

| URL                          | Descrição                        |
|------------------------------|----------------------------------|
| `/usuarios/login/`           | Login                            |
| `/usuarios/cadastro/`        | Cadastro de usuário              |
| `/usuarios/inicio/`          | Página inicial                   |
| `/espacos/`                  | Lista de espaços                 |
| `/espacos/cadastrar/`        | Cadastrar espaço (admin)         |
| `/reservas/solicitar/`       | Solicitar reserva                |
| `/reservas/minhas-reservas/` | Minhas reservas e cancelamento   |
| `/reservas/pendentes/`       | Analisar pendentes (admin)       |
| `/admin/`                    | Painel administrativo do Django  |
