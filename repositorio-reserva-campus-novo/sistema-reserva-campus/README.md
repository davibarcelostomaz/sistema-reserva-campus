# Sistema de Reserva de Salas e Laboratórios do Campus

Aplicação web acadêmica para consultar a disponibilidade e solicitar reservas de salas, laboratórios e outros espaços do campus.

## Objetivo

Substituir o controle manual por planilhas, e-mails e solicitações presenciais por um sistema centralizado, reduzindo conflitos de horários e aumentando a visibilidade dos espaços disponíveis.

## Tecnologias previstas

- **Backend:** Python e Django (orientado a objetos)
- **Frontend:** HTML, CSS e JavaScript
- **Banco de dados:** PostgreSQL
- **Versionamento:** Git e GitHub
- **Metodologia:** Scrum

## Perfis de usuário

- **Alunos e professores:** consultar disponibilidade, solicitar reservas, acompanhar solicitações e cancelar reservas próprias.
- **Administradores:** cadastrar e editar espaços, aprovar ou recusar solicitações e bloquear horários indisponíveis.

## Funcionalidades planejadas

1. Autenticação e autorização por perfil.
2. Cadastro de espaços com capacidade, recursos e localização.
3. Consulta de disponibilidade em calendário.
4. Solicitação, acompanhamento e cancelamento de reservas.
5. Aprovação e recusa de solicitações pelo administrador.
6. Bloqueio administrativo de períodos indisponíveis.
7. Prevenção de conflitos de horário.

## Estrutura do repositório

```text
sistema-reserva-campus/
├── README.md
├── docs/
│   ├── requisitos.md
│   ├── historias-usuario.md
│   ├── regras-negocio.md
│   └── scrum.md
├── backend/
├── frontend/
│   ├── css/
│   └── js/
├── database/
├── tests/
└── .gitignore
```

## Metodologia Scrum

O trabalho será dividido em Sprints. As tarefas poderão ser registradas em GitHub Issues e acompanhadas por um quadro no GitHub Projects. Veja [o planejamento inicial](docs/scrum.md).

## Status

**Planejamento e documentação inicial.** O sistema ainda não está implementado; a estrutura foi criada para organizar o desenvolvimento futuro.

## Equipe

- Adicionar os nomes dos integrantes aqui.

## Contexto

Projeto acadêmico de desenvolvimento de software.
