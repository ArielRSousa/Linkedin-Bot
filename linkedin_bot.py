import undetected_chromedriver as uc
import time
import os
import pyfiglet
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from dotenv import load_dotenv
from colorama import Fore, Style, init

init(autoreset=True)

if not os.path.exists(".env"):
    with open(".env", "w") as f:
        f.write("LINKEDIN_USERNAME=\n")
        f.write("LINKEDIN_PASSWORD=\n")
    print(Fore.YELLOW + "Arquivo .env criado. Preencha com suas credenciais do LinkedIn.")

load_dotenv()

class LinkedinBot:
    def __init__(self, username, password, conter_nota=False):
        self.username = username
        self.password = password
        self.conter_nota = conter_nota
        self.driver = self.iniciar_driver()
        self.wait = WebDriverWait(self.driver, 10)  # Tempo de espera dinâmico

    def iniciar_driver(self):
        try:
            options = uc.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--user-data-dir=./session")
            return uc.Chrome(options=options)
        except Exception as e:
            print(Fore.RED + f"Erro ao iniciar o driver: {e}")
            exit(1)

    def verificar_login(self):
        try:
            self.driver.get("https://www.linkedin.com/feed")
            time.sleep(5)
            return "session_redirect" not in self.driver.current_url
        except Exception as e:
            print(Fore.RED + f"Erro ao verificar login: {e}")
            return False

    def fazer_login(self):
        try:
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(2)
            self.driver.find_element(By.ID, "username").send_keys(self.username)
            self.driver.find_element(By.ID, "password").send_keys(self.password)
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(5)
        except NoSuchElementException:
            print(Fore.RED + "Erro: Elementos de login não encontrados.")
        except Exception as e:
            print(Fore.RED + f"Erro ao fazer login: {e}")

    def pesquisar_pessoas(self, termo_busca, localizacao=None):
        self.termo_busca = termo_busca
        self.localizacao = localizacao if localizacao else ""
        print(Fore.CYAN + f"Pesquisando: {termo_busca} em {localizacao if localizacao else 'qualquer lugar'}")

        url = f"https://www.linkedin.com/search/results/people/?keywords={termo_busca.replace(' ', '%20')}"
        if localizacao:
            url += f"%20em%20{localizacao.replace(' ', '%20')}"
        print(Fore.YELLOW + f"URL gerada: {url}")

        try:
            self.driver.get(url)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except Exception as e:
            print(Fore.RED + f"Erro ao carregar página de pesquisa: {e}")

    def enviar_pedidos_conexao(self, mensagem, max_pages=10):
        print(Fore.YELLOW + "Enviando pedidos de conexão...")
        conexoes_enviadas = 0
        pagina_atual = 1

        while pagina_atual <= max_pages:
            print(Fore.CYAN + f"Visitando página {pagina_atual}")
            url = f"https://www.linkedin.com/search/results/people/?keywords={self.termo_busca.replace(' ', '%20')}%20em%20{self.localizacao.replace(' ', '%20')}&page={pagina_atual}"
            
            try:
                self.driver.get(url)
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                time.sleep(3)  # Pequena pausa extra para garantir carregamento
            except Exception as e:
                print(Fore.RED + f"Erro ao carregar página {pagina_atual}: {e}")
                break

            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'se conectar')]")))
            except TimeoutException:
                print(Fore.YELLOW + "Nenhum botão encontrado rapidamente. Esperando mais tempo...")
                time.sleep(3)

            botoes_conectar = self.driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'se conectar')]")
            print(f"Total de botões de conectar na página {pagina_atual}: {len(botoes_conectar)}")

            if not botoes_conectar:
                print(Fore.YELLOW + "Nenhum botão de conectar encontrado nesta página. Indo para a próxima.")
                pagina_atual += 1
                continue

            for botao in botoes_conectar:
                try:
                    botao.click()
                    time.sleep(1)

                    if self.conter_nota and mensagem:
                        adicionar_nota = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Adicionar nota')]")))
                        adicionar_nota.click()
                        campo_mensagem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@name='message']")))
                        campo_mensagem.send_keys(mensagem)
                        self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Enviar')]"))).click()
                    else:
                        self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Enviar sem nota')]"))).click()

                    conexoes_enviadas += 1
                    print(Fore.GREEN + f"Conexão enviada. Total: {conexoes_enviadas}")
                    time.sleep(1)
                except Exception as e:
                    print(Fore.RED + f"Erro ao enviar pedido: {e}")
            
            pagina_atual += 1
        print(Fore.CYAN + f"Total de conexões enviadas: {conexoes_enviadas}")

    def fechar(self):
        self.driver.quit()

def mostrar_menu():
    titulo = pyfiglet.figlet_format("Linkedin Bot")
    print(Fore.BLUE + titulo)
    print(Style.BRIGHT + Fore.YELLOW + "Criado por: @ArielRSousa\n")
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
            localizacao = input(Fore.CYAN + "Digite a localização desejada ou pressione Enter para ignorar: ")
            mensagem_personalizada = input(Fore.CYAN + "Digite a mensagem personalizada ou pressione Enter para ignorar: ")
            max_pages = int(input(Fore.CYAN + "Digite o número máximo de páginas para visitar: "))
            bot.pesquisar_pessoas(termo_busca, localizacao if localizacao else None)
            bot.enviar_pedidos_conexao(mensagem_personalizada if mensagem_personalizada else None, max_pages)
        elif opcao == "3":
            print(Fore.GREEN + "Encerrando o bot. Até a próxima!")
            bot.fechar()
            break
        else:
            print(Fore.RED + "Opção inválida. Tente novamente.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\nBot interrompido pelo usuário. Até a próxima!")