# Linkedin Bot - Automatizador de Conexões no LinkedIn

Este projeto é um **bot de automação para o LinkedIn**, que permite realizar login, pesquisar usuários de uma área específica e enviar solicitações de conexão personalizadas **automaticamente**. Agora, conta também com um **sistema de automação programada**, que executa as conexões toda **segunda-feira** e pode ser configurado para **iniciar automaticamente com o sistema**.

---

## 🛠️ **Requisitos**

- **Python 3.8+**
- Ambiente virtual configurado (recomendado)
- **Google Chrome** instalado
- **Chromedriver** gerenciado automaticamente pelo `undetected-chromedriver`

---

## 🔦 **Instalação**

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/seuusuario/linkedin-bot.git
   cd linkedin-bot
   ```

2. **Crie e ative o ambiente virtual**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   ```

3. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Crie o arquivo ********************`.env`******************** com suas credenciais**:

   ```plaintext
   LINKEDIN_USERNAME=seu_email@exemplo.com
   LINKEDIN_PASSWORD=sua_senha_segura
   ```

---

## 🕹️ **Como usar**

1. **Execute o bot**:

   ```bash
   python main.py
   ```

2. **Escolha uma opção no menu interativo**:

   - **1**: **Ativar automação** (O bot rodará automaticamente toda segunda-feira)
   - **2**: **Desativar automação** (O bot não será executado automaticamente)
   - **3**: **Alterar parâmetros da automação** (termo de busca, localização, mensagem personalizada, número de páginas)
   - **4**: **Iniciar manualmente** (Executa a automação imediatamente)
   - **5**: **Sair**

---

## ⏰ **Automação e Agendamento**

Agora, o bot pode **rodar automaticamente toda segunda-feira** para evitar bloqueios do LinkedIn devido ao limite semanal de conexões. O agendamento pode ser ativado ou desativado pelo próprio menu.

Caso o sistema seja desligado e religado, a automação **ainda será executada na próxima segunda-feira**.

---

## 🌟 **Funcionalidades**

✅ **Login automático** (reutilização de sessão)\
✅ **Pesquisa personalizada** por usuários no LinkedIn\
✅ **Envio automático de conexões**, com ou sem mensagem personalizada\
✅ **Execução programada toda segunda-feira** para evitar bloqueios\
✅ **Possibilidade de alterar os parâmetros de automação pelo menu**\
✅ **Opção de iniciar automaticamente com o sistema**

---

## 📂 **Estrutura do Projeto**

```
/linkedin-bot
    ├── .venv/              # Ambiente virtual
    ├── session/            # Dados de sessão (cookies) do LinkedIn
    ├── .env                # Credenciais do LinkedIn
    ├── .gitignore          # Arquivos ignorados pelo Git
    ├── main.py             # Código principal do bot e menu interativo
    ├── config_manager.py   # Sistema de automação e agendamentos
    ├── linkedin_bot.py     # Código principal do bot do LinkedIn
    ├── requirements.txt    # Dependências do projeto
    └── README.md           # Documentação
```

---

## 🔒 **Segurança**

- As credenciais do LinkedIn estão armazenadas no arquivo `.env`, que **não deve ser compartilhado**.
- O projeto **não armazena** suas credenciais de forma insegura.
- O uso excessivo do bot pode resultar em restrições da conta do LinkedIn.

---

## ⚠️ **Aviso**

Este projeto foi desenvolvido **para fins educacionais**. O uso abusivo pode violar os **termos de serviço do LinkedIn**, resultando no bloqueio da sua conta. Use com responsabilidade.

---

## 🐜 **Licença**

MIT License © 2025 - Ariel Sousa
