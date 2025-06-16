# Linkedin Bot - Automatizador de Conexões no LinkedIn

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Automation-orange)](https://www.linkedin.com/)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)](https://github.com/seuusuario/linkedin-bot)
[![Chrome](https://img.shields.io/badge/Chrome-Required-red)](https://www.google.com/chrome/)

[![LinkedIn Bot](https://img.shields.io/badge/LinkedIn%20Bot-Automation%20Tool-yellow)](https://github.com/seuusuario/linkedin-bot)
[![Automation](https://img.shields.io/badge/Automation-Scheduled-blueviolet)](https://github.com/seuusuario/linkedin-bot)
[![Security](https://img.shields.io/badge/Security-Safe-brightgreen)](https://github.com/seuusuario/linkedin-bot)

Este projeto é um **bot de automação para o LinkedIn**, que permite realizar login, pesquisar usuários de uma área específica e enviar solicitações de conexão personalizadas **automaticamente**. Agora, conta também com um **sistema de automação programada**, que executa as conexões toda **segunda-feira** e pode ser configurado para **iniciar automaticamente com o sistema**.

## 📋 Índice
- [Requisitos](#️-requisitos)
- [Instalação](#-instalação)
- [Como usar](#️-como-usar)
  - [Interface Gráfica](#interface-gráfica)
  - [Linha de Comando](#linha-de-comando)
- [Automação e Agendamento](#-automação-e-agendamento)
- [Funcionalidades](#-funcionalidades)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Segurança](#-segurança)
- [Contribuindo](#-contribuindo)
- [Aviso](#️-aviso)
- [Licença](#-licença)

## 🛠️ **Requisitos**

- **Python 3.8+**
- Ambiente virtual configurado (recomendado)
- **Google Chrome** instalado
- **Chromedriver** gerenciado automaticamente pelo `undetected-chromedriver`

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

4. **Crie o arquivo `.env` com suas credenciais**:

   ```plaintext
   LINKEDIN_USERNAME=seu_email@exemplo.com
   LINKEDIN_PASSWORD=sua_senha_segura
   ```

## 🕹️ **Como usar**

### Interface Gráfica

Para iniciar o bot com a interface gráfica, simplesmente execute:

```bash
python main.py
```

A interface gráfica oferece três abas principais:

1. **Login**: Configure suas credenciais do LinkedIn
2. **Busca**: Configure os parâmetros de busca e envio de conexões
3. **Automação**: Ative ou desative a automação semanal

### Linha de Comando

Para usar o bot via linha de comando, execute:

```bash
python main.py --cli
```

O menu interativo oferece as seguintes opções:

- **1**: Fazer login no LinkedIn
- **2**: Pesquisar e enviar pedidos de conexão
- **3**: Sair

## ⏰ **Automação e Agendamento**

O bot pode **rodar automaticamente toda segunda-feira** para evitar bloqueios do LinkedIn devido ao limite semanal de conexões. O agendamento pode ser ativado ou desativado tanto pela interface gráfica quanto pela linha de comando.

## 🌟 **Funcionalidades**

✅ **Interface gráfica moderna e intuitiva**\
✅ **Login automático** (reutilização de sessão)\
✅ **Pesquisa personalizada** por usuários no LinkedIn\
✅ **Envio automático de conexões**, com ou sem mensagem personalizada\
✅ **Execução programada toda segunda-feira** para evitar bloqueios\
✅ **Possibilidade de alterar os parâmetros de automação**\
✅ **Opção de iniciar automaticamente com o sistema**\
✅ **Suporte a modo CLI para usuários avançados**

## 📂 **Estrutura do Projeto**

```
/linkedin-bot
    ├── .venv/              # Ambiente virtual
    ├── session/            # Dados de sessão (cookies) do LinkedIn
    ├── .env                # Credenciais do LinkedIn
    ├── .gitignore          # Arquivos ignorados pelo Git
    ├── main.py             # Ponto de entrada do programa
    ├── gui.py              # Interface gráfica
    ├── config_manager.py   # Sistema de automação e agendamentos
    ├── linkedin_bot.py     # Código principal do bot do LinkedIn
    ├── requirements.txt    # Dependências do projeto
    └── README.md           # Documentação
```

## 🔒 **Segurança**

- As credenciais do LinkedIn estão armazenadas no arquivo `.env`, que **não deve ser compartilhado**.
- O projeto **não armazena** suas credenciais de forma insegura.
- O uso excessivo do bot pode resultar em restrições da conta do LinkedIn.

## 🤝 **Contribuindo**

Contribuições são sempre bem-vindas! Se você tem alguma ideia para melhorar o projeto, sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'feat: add some amazing feature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

### 📝 Padrões de Commit

Este projeto segue o padrão [Conventional Commits](https://www.conventionalcommits.org/). Por favor, use os seguintes prefixos nos seus commits:

- `feat:` para novas funcionalidades
- `fix:` para correções de bugs
- `docs:` para alterações na documentação
- `style:` para alterações de formatação
- `refactor:` para refatorações de código
- `test:` para adição ou modificação de testes
- `chore:` para atualizações de dependências ou configurações

### 🐛 Reportando Bugs

Se você encontrar algum bug, por favor, abra uma issue com:
- Descrição detalhada do problema
- Passos para reproduzir
- Comportamento esperado
- Screenshots (se aplicável)
- Ambiente (sistema operacional, versão do Python, etc.)

## ⚠️ **Aviso**

Este projeto foi desenvolvido **para fins educacionais**. O uso abusivo pode violar os **termos de serviço do LinkedIn**, resultando no bloqueio da sua conta. Use com responsabilidade.

## 🐜 **Licença**

MIT License © 2025 - Ariel Sousa
