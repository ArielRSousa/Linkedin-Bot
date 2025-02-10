import undetected_chromedriver as uc
import time
import os
import pyfiglet
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from colorama import Fore, Style, init

init(autoreset=True)
load_dotenv()

class LinkedinBot:
    def __init__(self, username, password, conter_nota=False):
        self.username = username
        self.password = password
        self.conter_nota = conter_nota
        self.driver = self.iniciar_driver()

    def iniciar_driver(self):
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--user-data-dir=./session")
        return uc.Chrome(options=options)

    def verificar_login(self):
        self.driver.get("https://www.linkedin.com/feed")
        time.sleep(5)
        if "session_redirect" in self.driver.current_url:
            print(Fore.RED + "O usuário não está logado.")
            return False
        else:
            print(Fore.GREEN + "O usuário já está logado.")
            return True

    def fazer_login(self):
        self.driver.get("https://www.linkedin.com/login")
        time.sleep(2)
        self.driver.find_element(By.ID, "username").send_keys(self.username)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)
        if "feed" in self.driver.current_url:
            print(Fore.GREEN + "Login bem-sucedido.")
        else:
            print(Fore.RED + "Erro no login. Verifique suas credenciais.")

    def pesquisar_pessoas(self, termo_busca):
        self.termo_busca = termo_busca
        print(Fore.CYAN + f"Pesquisando: {termo_busca}")
        self.driver.get(f"https://www.linkedin.com/search/results/people/?keywords={termo_busca}")
        time.sleep(5)


    def enviar_pedidos_conexao(self, mensagem, max_pages=10):
        print(Fore.YELLOW + "Enviando pedidos de conexão...")
        conexoes_enviadas = 0
        pagina_atual = 1

        while pagina_atual <= max_pages:
            print(Fore.CYAN + f"Visitando página {pagina_atual}")
            self.driver.get(f"https://www.linkedin.com/search/results/people/?keywords={self.termo_busca}&page={pagina_atual}")
            time.sleep(5)

            botoes_conectar = self.driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'se conectar')]")
            print(f"Total de botões de conectar na página {pagina_atual}: {len(botoes_conectar)}")

            if not botoes_conectar:
                print(Fore.YELLOW + "Nenhum botão de conectar encontrado nesta página. Indo para a próxima.")
                pagina_atual += 1
                continue

            for botao in botoes_conectar:
                try:
                    botao.click()
                    time.sleep(2)

                    if self.conter_nota:
                        adicionar_nota = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Adicionar nota')]")
                        adicionar_nota.click()
                        campo_mensagem = self.driver.find_element(By.XPATH, "//textarea[@name='message']")
                        campo_mensagem.send_keys(mensagem)
                        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Enviar')]").click()
                        conexoes_enviadas += 1
                        print(Fore.GREEN + f"Conexão enviada com mensagem. Total: {conexoes_enviadas}")
                        time.sleep(2)
                    else:
                        self.driver.find_element(By.XPATH, "//button[contains(., 'Enviar sem nota')]").click()
                        conexoes_enviadas += 1
                        print(Fore.GREEN + f"Conexão enviada sem mensagem. Total: {conexoes_enviadas}")
                        time.sleep(2)

                except Exception as e:
                    print(Fore.RED + f"Erro ao enviar pedido: {e}")

            pagina_atual += 1

        print(Fore.CYAN + f"Total de conexões enviadas: {conexoes_enviadas}")


    def fechar(self):
        self.driver.quit()

def mostrar_menu():
    titulo = pyfiglet.figlet_format("Linkedin Bot")
    print(Fore.BLUE + titulo)
    print(Style.BRIGHT + Fore.YELLOW + "Automatize suas conexões no LinkedIn rapidamente.\n")
    print(Fore.CYAN + "Escolha uma opção:")
    print("1. Login no LinkedIn")
    print("2. Pesquisar e enviar pedidos de conexão")
    print("3. Sair\n")

def main():
    username = os.getenv("LINKEDIN_USERNAME")
    password = os.getenv("LINKEDIN_PASSWORD")
    bot = LinkedinBot(username, password)

    while True:
        mostrar_menu()
        opcao = input(Fore.YELLOW + "Digite a opção desejada: ")

        if opcao == "1":
            if not bot.verificar_login():
                bot.fazer_login()
        elif opcao == "2":
            if not bot.verificar_login():
                print(Fore.RED + "Você precisa fazer login antes de continuar.")
                continue

            termo_busca = input(Fore.CYAN + "Digite o termo de busca (ex.: Desenvolvedor de Software): ")
            mensagem_personalizada = input(Fore.CYAN + "Digite a mensagem personalizada: ")
            max_pages = int(input(Fore.CYAN + "Digite o número máximo de páginas para visitar: "))
            bot.pesquisar_pessoas(termo_busca)
            bot.enviar_pedidos_conexao(mensagem_personalizada, max_pages)

        elif opcao == "3":
            print(Fore.GREEN + "Encerrando o bot. Até a próxima!")
            bot.fechar()
            break
        else:
            print(Fore.RED + "Opção inválida. Tente novamente.\n")

if __name__ == "__main__":
    main()
