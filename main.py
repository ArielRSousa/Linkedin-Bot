import os
import pyfiglet
import threading
from colorama import Fore, Style
from config_manager import AutomationManager, agendar_bot
from linkedin_bot import main as linkedin_main

def iniciar_automacao_em_thread(manager):
    """Executa a automação em uma thread separada para não bloquear o menu."""
    automacao_thread = threading.Thread(target=agendar_bot, args=(manager,), daemon=True)
    automacao_thread.start()

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
            linkedin_main()  
        elif opcao == "5":
            print(Fore.GREEN + "Encerrando o programa. Até logo!")
            break
        else:
            print(Fore.RED + "Opção inválida! Tente novamente.")

        input(Fore.CYAN + "\nPressione Enter para continuar...")

if __name__ == "__main__":
    try:
        mostrar_menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\nPrograma encerrado pelo usuário.")
