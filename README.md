# 📡 Dona Odete — Monitoramento Ativo de Servidores

Desenvolvi uma infraestrutura de bots para monitorar o funcionamento de determinados serviços dos servidores, disponibilidades de APIs da empresa e, em caso de falha, notificar a equipe por meio do MS Teams.  
Esta aplicação foi apelidada como Dona Odete e se comunica com a equipe de forma leve e gentil, apesar de comunicar falhas importantes na produção  
---

## 🧱 Estrutura do Projeto

### 🖥️ Aplicativo Standalone

- Funciona como um executável independente ou serviço instalado no Windows.
- Deve ser instalado diretamente na máquina a ser monitorada.
- Responsável por enviar alertas em caso de falhas ou instabilidades.
- Suporte a testes de conectividade via **Telnet** para monitoramento de APIs e serviços remotos.
- Pode se integrar a uma **API centralizadora**, permitindo o encaminhamento dos alertas de forma unificada para o Teams.

### 🌐 API Centralizadora

- Multiplas instâncias possíveis
- As APIs recebem e redirecionam mensagens de falha para webhooks previamente cadastrados.
- É possível registrar múltiplas webhooks e configurar os serviços para acionar uma ou mais delas.
