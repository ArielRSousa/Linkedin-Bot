import json
import os
import schedule
import time
from datetime import datetime
from colorama import Fore
from .linkedin_bot import LinkedinBot

CONFIG_FILE = os.path.join("config", "config.json")

class AutomationManager:
    def __init__(self):
        self.config = self.load_config()

    def set_parameters(self, termo, localizacao, mensagem, max_pages):
        """Modifica os parâmetros da automação e os salva no JSON."""
        self.config["termo_busca"] = termo
        self.config["localizacao"] = localizacao
        self.config["mensagem_personalizada"] = mensagem
        self.config["max_pages"] = max_pages
        self.save_config(self.config)
        print(Fore.GREEN + "Parâmetros da automação atualizados com sucesso.")


    def load_config(self):
        """Carrega ou cria a configuração da automação."""
        if not os.path.exists(CONFIG_FILE):
            default_config = {
                "automation_enabled": False,
                "last_execution": None,
                "schedules": [],  
                "termo_busca": "Desenvolvedor",
                "localizacao": "Brasil",
                "mensagem_personalizada": "Olá, gostaria de me conectar!",
                "max_pages": 5
            }
            self.save_config(default_config)
            return default_config
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)

    def save_config(self, config):
        """Salva as configurações no JSON."""
        os.makedirs("config", exist_ok=True)
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)

    def enable_automation(self):
        """Ativa a automação e salva no JSON."""
        self.config["automation_enabled"] = True
        self.save_config(self.config)
        print(Fore.GREEN + "Automação ativada. O bot rodará toda segunda-feira.")

    def disable_automation(self):
        """Desativa a automação e salva no JSON."""
        self.config["automation_enabled"] = False
        self.save_config(self.config)
        print(Fore.RED + "Automação desativada.")

    def get_parameters(self):
        """Retorna os parâmetros atuais da automação."""
        return (
            self.config["termo_busca"],
            self.config["localizacao"],
            self.config["mensagem_personalizada"],
            self.config["max_pages"]
        )

def executar_bot():
    """Executa o bot automaticamente toda segunda-feira."""
    manager = AutomationManager()
    if not manager.config["automation_enabled"]:
        print(Fore.RED + "Automação está desativada. Não executando.")
        return
    
    # Verifica se hoje é segunda-feira (0 = segunda, 6 = domingo)
    if datetime.today().weekday() != 0:
        print(Fore.YELLOW + "Hoje não é segunda-feira. O bot não será executado.")
        return

    print(Fore.GREEN + f"Executando automação do LinkedIn às {datetime.now().strftime('%H:%M:%S')}...")

    username = os.getenv("LINKEDIN_USERNAME")
    password = os.getenv("LINKEDIN_PASSWORD")
    
    bot = LinkedinBot(username, password)
    bot.fazer_login()
    
    termo_busca, localizacao, mensagem_personalizada, max_pages = manager.get_parameters()

    bot.pesquisar_pessoas(termo_busca, localizacao)
    bot.enviar_pedidos_conexao(mensagem_personalizada, max_pages)
    
    bot.fechar()

def agendar_bot(manager):
    """Configura o agendamento da automação para rodar toda segunda-feira."""
    if not manager.config["automation_enabled"]:
        print(Fore.RED + "Automação desativada. Ative para iniciar.")
        return

    # Agendar a execução toda segunda-feira às 08:00 (ou outro horário desejado)
    schedule.every().monday.at("08:00").do(executar_bot)
    print(Fore.CYAN + "Automação agendada para toda segunda-feira às 08:00.")

    print(Fore.YELLOW + "Automação rodando em segundo plano...\n")

    while True:
        schedule.run_pending()  # Verifica e executa as tarefas no horário correto
        time.sleep(30)  # Espera 30 segundos antes de verificar novamente

if __name__ == "__main__":
    manager = AutomationManager()

    if manager.config["automation_enabled"]:
        agendar_bot(manager)
