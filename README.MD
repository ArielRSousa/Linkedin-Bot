# 💼 Linkedin Bot - Automatizador de Conexões no LinkedIn 🚀

Este projeto é um bot de automação no LinkedIn, que permite realizar login, pesquisar por usuários em uma área específica e enviar solicitações de conexão personalizadas automaticamente.

---

## 🔧 **Requisitos**
- **Python 3.8+**
- Ambiente virtual configurado (recomendado)
- **Google Chrome** instalado
- **Chromedriver** gerenciado automaticamente pelo `undetected-chromedriver`

---

## 🛆 **Instalação**
1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/linkedin-bot.git
   cd linkedin-bot
   ```

2. Crie e ative o ambiente virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Crie o arquivo `.env` com as suas credenciais:
   ```plaintext
   LINKEDIN_USERNAME=seu_email@exemplo.com
   LINKEDIN_PASSWORD=sua_senha_segura
   ```

---

## 🛠️ **Como usar**
1. Execute o bot:
   ```bash
   python main.py
   ```

2. Escolha uma das opções no menu interativo:
   - **1**: Fazer login no LinkedIn
   - **2**: Pesquisar e enviar pedidos de conexão
   - **3**: Sair

---

## 🌟 **Funcionalidades**
- Login automático com reutilização de sessão
- Pesquisa personalizada por usuários no LinkedIn
- Envio de solicitações de conexão com ou sem mensagens personalizadas

---

## 🖂 **Estrutura do Projeto**
```
/linkedin-bot
    ├── .venv/              # Ambiente virtual
    ├── session/            # Dados de sessão (cookies) do LinkedIn
    ├── .env                # Credenciais do LinkedIn
    ├── .gitignore          # Arquivos ignorados pelo Git
    ├── main.py             # Código principal do bot
    ├── requirements.txt    # Dependências do projeto
    └── README.md           # Documentação
```

---

## 🔒 **Segurança**
- As credenciais estão armazenadas no arquivo `.env`, que é ignorado pelo Git.
- Não compartilhe o arquivo `.env` ou dados da sessão com outras pessoas.

---

## ⚠️ **Aviso**
Este projeto é para fins educacionais. O uso excessivo pode violar os termos de serviço do LinkedIn, resultando no bloqueio da sua conta. Use com responsabilidade.

---

## 📜 **Licença**
MIT License © 2025 - Ariel Sousa