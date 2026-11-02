# Histórias de usuário (Product Backlog inicial)

| ID | História de usuário | Prioridade |
| --- | --- | --- |
| HU01 | Como aluno ou professor, quero consultar os espaços disponíveis para escolher onde realizar uma atividade. | Alta |
| HU02 | Como aluno ou professor, quero solicitar uma reserva para utilizar um espaço em determinado horário. | Alta |
| HU03 | Como aluno ou professor, quero acompanhar o status da minha solicitação para saber se foi aprovada. | Alta |
| HU04 | Como aluno ou professor, quero cancelar uma solicitação para liberar o horário. | Média |
| HU05 | Como administrador, quero cadastrar espaços com capacidade, recursos e localização para manter o catálogo atualizado. | Alta |
| HU06 | Como administrador, quero aprovar ou recusar solicitações para controlar o uso dos espaços. | Alta |
| HU07 | Como administrador, quero bloquear horários indisponíveis para evitar solicitações indevidas. | Alta |
| HU08 | Como usuário, quero visualizar reservas em um calendário para planejar minhas atividades. | Alta |

## Critério de aceite ilustrativo (HU02)

- Usuário autenticado seleciona um espaço, uma data e um intervalo de horário.
- Sistema valida dados e informa conflitos ou bloqueios.
- Solicitação válida é registrada com status **pendente**.
- Usuário consegue visualizar a solicitação registrada.
