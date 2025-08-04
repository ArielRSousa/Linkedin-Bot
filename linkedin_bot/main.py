import sys
import os
import pyfiglet
import threading
from colorama import Fore, Style
from dotenv import load_dotenv
from .config_manager import AutomationManager, agendar_bot
from .linkedin_bot import LinkedinBot
from PyQt6.QtWidgets import QApplication
from .gui import MainWindow

def iniciar_automacao_em_thread(manager):
    """Executa a automação em uma thread separada para não bloquear o menu."""
    automacao_thread = threading.Thread(target=agendar_bot, args=(manager,), daemon=True)
    automacao_thread.start()

def executar_bot_manual():
    """Executa o bot manualmente."""
    username = os.getenv("LINKEDIN_USERNAME")
    password = os.getenv("LINKEDIN_PASSWORD")
    bot = LinkedinBot(username, password)

    if not bot.verificar_login():
        bot.fazer_login()
    
    termo_busca = input(Fore.CYAN + "Digite o termo de busca (ex.: Desenvolvedor de Software): ")
    localizacao = input(Fore.CYAN + "Digite a localização desejada ou pressione Enter para ignorar: ")
    mensagem_personalizada = input(Fore.CYAN + "Digite a mensagem personalizada ou pressione Enter para ignorar: ")
    
    # Tratamento para entrada vazia no número de páginas
    max_pages_input = input(Fore.CYAN + "Digite o número máximo de páginas para visitar (ou Enter para padrão=10): ")
    max_pages = int(max_pages_input) if max_pages_input.strip() else 10
    
    bot.pesquisar_pessoas(termo_busca, localizacao if localizacao else None)
    bot.enviar_pedidos_conexao(mensagem_personalizada if mensagem_personalizada else None, max_pages)
    bot.fechar()

def mostrar_menu():
    """Exibe o menu principal para ativação/desativação da automação."""
    manager = AutomationManager()

    # Se a automação estiver ativada, iniciamos em segundo plano
    if manager.config["automation_enabled"]:
        iniciar_automacao_em_thread(manager)

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        titulo = pyfiglet.figlet_format("Linkedin Bot")
        print(Fore.BLUE + titulo)
        print(Style.BRIGHT + Fore.YELLOW + "Automação de conexões no LinkedIn\n")
        print(Fore.CYAN + "1. Ativar automação (Roda toda segunda-feira)")
        print(Fore.RED + "2. Desativar automação")
        print(Fore.GREEN + "3. Alterar parâmetros da automação")
        print(Fore.BLUE + "4. Iniciar manualmente agora")
        print(Fore.WHITE + "5. Sair\n")

        opcao = input(Fore.YELLOW + "Escolha uma opção: ")

        if opcao == "1":
            manager.enable_automation()
            iniciar_automacao_em_thread(manager)  
        elif opcao == "2":
            manager.disable_automation()
            print(Fore.RED + "Automação desativada. Reinicie o programa para interromper processos em execução.")
        elif opcao == "3":
            termo = input(Fore.CYAN + "Digite o novo termo de busca: ")
            localizacao = input(Fore.CYAN + "Digite a nova localização (ou pressione Enter para ignorar): ")
            mensagem = input(Fore.CYAN + "Digite a nova mensagem personalizada: ")
            max_pages = int(input(Fore.CYAN + "Digite o número máximo de páginas para visitar: "))

            manager.set_parameters(termo, localizacao, mensagem, max_pages)

        elif opcao == "4":
            executar_bot_manual()
        elif opcao == "5":
            print(Fore.GREEN + "Encerrando o programa. Até logo!")
            break
        else:
            print(Fore.RED + "Opção inválida! Tente novamente.")

        input(Fore.CYAN + "\nPressione Enter para continuar...")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        mostrar_menu()
    else:
        try:
            app = QApplication(sys.argv)
            window = MainWindow()
            window.show()
            return app.exec()
        except ImportError as e:
            print(f"Erro: {str(e)}")
            print("Instalando dependências...")
            os.system("pip install -r requirements.txt")
            print("Dependências instaladas. Reinicie o programa.")
            return 1
        except Exception as e:
            print(f"Erro ao iniciar a interface gráfica: {str(e)}")
            return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nBot interrompido pelo usuário. Até a próxima!")
