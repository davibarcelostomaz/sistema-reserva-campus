# Requisitos do sistema (proposta inicial)

## Requisitos funcionais

- **RF01:** O sistema deve permitir autenticação de usuários.
- **RF02:** O administrador deve poder cadastrar, editar e consultar espaços com nome, capacidade, recursos e localização.
- **RF03:** O usuário deve poder visualizar disponibilidade de espaços em um calendário.
- **RF04:** O usuário deve poder solicitar uma reserva para um espaço e intervalo de tempo.
- **RF05:** O usuário deve poder consultar o status de suas solicitações.
- **RF06:** O usuário deve poder cancelar suas próprias solicitações, conforme regras estabelecidas.
- **RF07:** O administrador deve poder aprovar ou recusar solicitações.
- **RF08:** O administrador deve poder bloquear horários de espaços.
- **RF09:** O sistema deve impedir a confirmação de reservas com horários conflitantes para o mesmo espaço.

## Requisitos não funcionais

- **RNF01:** Interface web acessível por navegadores modernos.
- **RNF02:** Backend desenvolvido em Python/Django com organização orientada a objetos.
- **RNF03:** Persistência de dados em PostgreSQL.
- **RNF04:** Controle de acesso conforme perfil do usuário.
- **RNF05:** Proteção de credenciais e dados sensíveis por configuração de ambiente.

> Requisitos preliminares sujeitos a validação pela equipe e pelo professor.
