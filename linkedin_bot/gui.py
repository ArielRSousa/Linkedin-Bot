import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                            QTextEdit, QSpinBox, QMessageBox, QTabWidget,
                            QGroupBox, QFormLayout, QCheckBox, QMenuBar, QMenu,
                            QProgressBar, QStatusBar, QStyleFactory)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QAction, QPalette, QColor
from dotenv import load_dotenv
from .linkedin_bot import LinkedinBot
from .config_manager import AutomationManager
from .updater import check_and_update
from selenium.common.exceptions import WebDriverException

ENV_PATH = os.path.join("config", ".env")

class BotThread(QThread):
    update_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    progress_signal = pyqtSignal(int)
    status_signal = pyqtSignal(str)

    def __init__(self, bot, action, **kwargs):
        super().__init__()
        self.bot = bot
        self.action = action
        self.kwargs = kwargs
        self.is_running = True

    def stop(self):
        self.is_running = False
        if self.bot:
            try:
                self.bot.fechar()
            except:
                pass
        self.update_signal.emit("Operação cancelada pelo usuário.")
        self.status_signal.emit("Operação cancelada")

    def run(self):
        try:
            if self.action == "login":
                self.status_signal.emit("Realizando login...")
                if not self.bot.verificar_login():
                    self.bot.fazer_login()
                    self.update_signal.emit("Login realizado com sucesso!")
                    self.status_signal.emit("Login realizado com sucesso")
            elif self.action == "search":
                self.status_signal.emit("Iniciando busca...")
                try:
                    self.bot.pesquisar_pessoas(
                        self.kwargs.get('termo_busca'),
                        self.kwargs.get('localizacao')
                    )
                except Exception as e:
                    self.update_signal.emit(f"Erro de login: {str(e)}")
                    self.status_signal.emit("Erro de login")
                    return
                conexoes_enviadas = 0
                pagina_atual = 1
                max_pages = self.kwargs.get('max_pages', 10)

                while pagina_atual <= max_pages and self.is_running:
                    self.status_signal.emit(f"Processando página {pagina_atual} de {max_pages}")
                    self.update_signal.emit(f"Processando página {pagina_atual} de {max_pages}")
                    self.progress_signal.emit(int((pagina_atual / max_pages) * 100))
                    try:
                        self.bot.enviar_pedidos_conexao(
                            self.kwargs.get('mensagem'),
                            1
                        )
                        conexoes_enviadas += 1
                        self.update_signal.emit(f"Conexões enviadas nesta página: {conexoes_enviadas}")
                    except WebDriverException as wde:
                        if not self.is_running:
                            self.update_signal.emit("A operação foi cancelada e a conexão com o navegador foi encerrada.")
                            self.status_signal.emit("Operação cancelada")
                        else:
                            self.update_signal.emit("Erro de conexão com o navegador. Tente novamente.")
                            self.status_signal.emit("Erro de conexão")
                        break
                    except Exception as e:
                        self.update_signal.emit(f"Erro inesperado ao enviar conexões: {str(e)}")
                        self.status_signal.emit("Erro inesperado")
                        break
                    pagina_atual += 1

                if self.is_running:
                    self.update_signal.emit(f"Busca e envio de conexões concluídos! Total de conexões: {conexoes_enviadas}")
                    self.status_signal.emit("Operação concluída com sucesso")
                else:
                    self.update_signal.emit("Operação cancelada pelo usuário.")
                    self.status_signal.emit("Operação cancelada")
        except WebDriverException as wde:
            if not self.is_running:
                self.update_signal.emit("A operação foi cancelada e a conexão com o navegador foi encerrada.")
                self.status_signal.emit("Operação cancelada")
            else:
                self.update_signal.emit("Erro de conexão com o navegador. Tente novamente.")
                self.status_signal.emit("Erro de conexão")
        except Exception as e:
            if not self.is_running:
                self.update_signal.emit("A operação foi cancelada pelo usuário.")
                self.status_signal.emit("Operação cancelada")
            else:
                self.update_signal.emit(f"Erro inesperado: {str(e)}")
                self.status_signal.emit("Erro inesperado")
        finally:
            self.finished_signal.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LinkedIn Bot")
        self.setMinimumSize(1000, 700)
        self.bot = None
        self.current_thread = None
        
        # Configurar estilo
        self.setStyleSheet("""
            QMainWindow {
                background-color: #181818;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #333333;
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 10px;
                color: #e0e0e0;
                background-color: #232323;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 7px;
                padding: 0px 5px 0px 5px;
                color: #00bfff;
            }
            QPushButton {
                background-color: #0077b5;
                color: #fff;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005582;
            }
            QPushButton:disabled {
                background-color: #444444;
                color: #888888;
            }
            QLineEdit, QTextEdit {
                padding: 5px;
                border: 1px solid #333333;
                border-radius: 4px;
                background-color: #222222;
                color: #e0e0e0;
                selection-background-color: #0077b5;
                selection-color: #fff;
            }
            QCheckBox, QLabel, QSpinBox {
                color: #e0e0e0;
            }
            QTabWidget::pane {
                border: 1px solid #333333;
                background: #181818;
            }
            QTabBar::tab {
                background: #232323;
                color: #e0e0e0;
                padding: 8px 20px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background: #0077b5;
                color: #fff;
            }
            QProgressBar {
                border: 2px solid #333333;
                border-radius: 5px;
                text-align: center;
                background: #232323;
                color: #e0e0e0;
            }
            QProgressBar::chunk {
                background-color: #0077b5;
            }
            QTextEdit {
                background-color: #222222;
                color: #e0e0e0;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 5px;
            }
            QMenuBar {
                background-color: #181818;
                color: #e0e0e0;
            }
            QMenuBar::item:selected {
                background: #232323;
            }
            QMenu {
                background-color: #232323;
                color: #e0e0e0;
                border: 1px solid #333333;
            }
            QMenu::item:selected {
                background-color: #0077b5;
                color: #fff;
            }
            QStatusBar {
                background: #181818;
                color: #e0e0e0;
            }
        """)
        
        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()
        self.load_credentials()
        check_and_update(self)

    def setup_status_bar(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Pronto")

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Tabs
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # Tab de Login
        login_tab = QWidget()
        login_layout = QVBoxLayout(login_tab)
        login_layout.setSpacing(10)
        
        # Grupo de Credenciais
        cred_group = QGroupBox("Credenciais do LinkedIn")
        cred_layout = QFormLayout()
        cred_layout.setSpacing(10)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Digite seu email do LinkedIn")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Digite sua senha")
        
        cred_layout.addRow("Email:", self.email_input)
        cred_layout.addRow("Senha:", self.password_input)
        self.auto_login_checkbox = QCheckBox("Login automático")
        cred_layout.addRow(self.auto_login_checkbox)
        cred_group.setLayout(cred_layout)
        login_layout.addWidget(cred_group)

        # Botão de Login
        login_btn = QPushButton("Fazer Login")
        login_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_DialogOkButton))
        login_btn.clicked.connect(self.handle_login)
        login_layout.addWidget(login_btn)

        # Tab de Busca
        search_tab = QWidget()
        search_layout = QVBoxLayout(search_tab)
        search_layout.setSpacing(10)

        # Grupo de Busca
        search_group = QGroupBox("Parâmetros de Busca")
        search_form = QFormLayout()
        search_form.setSpacing(10)

        self.termo_busca = QLineEdit()
        self.termo_busca.setPlaceholderText("Ex: Desenvolvedor Python")
        self.localizacao = QLineEdit()
        self.localizacao.setPlaceholderText("Ex: São Paulo, Brasil")
        self.mensagem = QTextEdit()
        self.mensagem.setPlaceholderText("Digite sua mensagem personalizada aqui...")
        self.mensagem.setMaximumHeight(100)
        self.max_pages = QSpinBox()
        self.max_pages.setRange(1, 100)
        self.max_pages.setValue(10)
        self.conter_nota = QCheckBox("Incluir mensagem personalizada")

        search_form.addRow("Termo de Busca:", self.termo_busca)
        search_form.addRow("Localização:", self.localizacao)
        search_form.addRow("Mensagem:", self.mensagem)
        search_form.addRow("Máximo de Páginas:", self.max_pages)
        search_form.addRow(self.conter_nota)

        search_group.setLayout(search_form)
        search_layout.addWidget(search_group)

        # Barra de Progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        search_layout.addWidget(self.progress_bar)

        # Botões de Busca e Cancelar
        button_layout = QHBoxLayout()
        self.search_btn = QPushButton("Iniciar Busca e Envio de Conexões")
        self.search_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_MediaPlay))
        self.search_btn.clicked.connect(self.handle_search)
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_MediaStop))
        self.cancel_btn.clicked.connect(self.cancel_search)
        self.cancel_btn.setEnabled(False)
        
        button_layout.addWidget(self.search_btn)
        button_layout.addWidget(self.cancel_btn)
        search_layout.addLayout(button_layout)

        # Tab de Automação
        automation_tab = QWidget()
        automation_layout = QVBoxLayout(automation_tab)
        automation_layout.setSpacing(10)

        # Grupo de Automação
        auto_group = QGroupBox("Configurações de Automação")
        auto_form = QFormLayout()
        auto_form.setSpacing(10)

        self.auto_enabled = QCheckBox("Ativar Automação Semanal")
        self.auto_enabled.stateChanged.connect(self.toggle_automation)

        auto_form.addRow(self.auto_enabled)
        auto_group.setLayout(auto_form)
        automation_layout.addWidget(auto_group)

        # Adicionar tabs
        tabs.addTab(login_tab, "Login")
        tabs.addTab(search_tab, "Busca")
        tabs.addTab(automation_tab, "Automação")

        # Área de Log
        log_group = QGroupBox("Log de Operações")
        log_layout = QVBoxLayout()
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("""
            QTextEdit {
                background-color: #222222;
                color: #e0e0e0;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        log_layout.addWidget(self.log_area)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

    def setup_menu(self):
        menubar = self.menuBar()
        
        # Menu Arquivo
        file_menu = menubar.addMenu("Arquivo")
        
        # Ação de Verificar Atualizações
        check_update_action = QAction("Verificar Atualizações", self)
        check_update_action.triggered.connect(lambda: check_and_update(self))
        file_menu.addAction(check_update_action)
        
        # Separador
        file_menu.addSeparator()
        
        # Ação de Sair
        exit_action = QAction("Sair", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def load_credentials(self):
        load_dotenv(ENV_PATH)
        email = os.getenv("LINKEDIN_USERNAME")
        password = os.getenv("LINKEDIN_PASSWORD")
        auto_login = os.getenv("AUTO_LOGIN", "False")
        if email:
            self.email_input.setText(email)
        if password:
            self.password_input.setText(password)
        self.auto_login_checkbox.setChecked(auto_login == "True")
        # Login automático se opção marcada e credenciais presentes
        if self.auto_login_checkbox.isChecked() and email and password:
            self.handle_login(auto=True)

    def save_credentials(self):
        os.makedirs("config", exist_ok=True)
        with open(ENV_PATH, "w") as f:
            f.write(f"LINKEDIN_USERNAME={self.email_input.text()}\n")
            f.write(f"LINKEDIN_PASSWORD={self.password_input.text()}\n")
            f.write(f"AUTO_LOGIN={'True' if self.auto_login_checkbox.isChecked() else 'False'}\n")

    def log(self, message):
        self.log_area.append(message)

    def handle_login(self, auto=False):
        if not self.email_input.text() or not self.password_input.text():
            if not auto:
                QMessageBox.warning(self, "Erro", "Por favor, preencha email e senha.")
            return

        self.save_credentials()
        if self.bot:
            try:
                self.bot.fechar()
            except:
                pass
        
        self.bot = LinkedinBot(self.email_input.text(), self.password_input.text())
        
        if self.current_thread:
            self.current_thread.stop()
            self.current_thread.wait()
        
        self.current_thread = BotThread(self.bot, "login")
        self.current_thread.update_signal.connect(self.log)
        self.current_thread.status_signal.connect(self.update_status)
        self.current_thread.finished_signal.connect(lambda: self.log("Processo de login finalizado."))
        self.current_thread.start()

    def handle_search(self):
        if not self.bot:
            QMessageBox.warning(self, "Erro", "Por favor, faça login primeiro.")
            return

        if not self.termo_busca.text():
            QMessageBox.warning(self, "Erro", "Por favor, insira um termo de busca.")
            return

        try:
            kwargs = {
                'termo_busca': self.termo_busca.text(),
                'localizacao': self.localizacao.text() if self.localizacao.text() else None,
                'mensagem': self.mensagem.toPlainText() if self.conter_nota.isChecked() else None,
                'max_pages': self.max_pages.value()
            }

            if self.current_thread:
                self.current_thread.stop()
                self.current_thread.wait()

            self.current_thread = BotThread(self.bot, "search", **kwargs)
            self.current_thread.update_signal.connect(self.log)
            self.current_thread.progress_signal.connect(self.update_progress)
            self.current_thread.status_signal.connect(self.update_status)
            self.current_thread.finished_signal.connect(self.search_finished)
            
            self.search_btn.setEnabled(False)
            self.cancel_btn.setEnabled(True)
            self.current_thread.start()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao iniciar busca: {str(e)}")
            self.log(f"Erro ao iniciar busca: {str(e)}")
            self.update_status("Erro ao iniciar busca")
            self.search_btn.setEnabled(True)
            self.cancel_btn.setEnabled(False)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_status(self, message):
        self.statusBar.showMessage(message)

    def search_finished(self):
        try:
            self.search_btn.setEnabled(True)
            self.cancel_btn.setEnabled(False)
            self.progress_bar.setValue(0)
            # Não fechar o navegador aqui!
            # if self.bot:
            #     try:
            #         self.bot.fechar()
            #     except:
            #         pass
            # Verifica se houve erro na busca
            if "Erro" in self.statusBar.currentMessage():
                QMessageBox.warning(self, "Aviso", "A busca foi interrompida devido a um erro. Por favor, tente novamente.")
        except Exception as e:
            self.log(f"Erro ao finalizar busca: {str(e)}")
            self.update_status("Erro ao finalizar busca")

    def toggle_automation(self, state):
        if state == Qt.CheckState.Checked.value:
            manager = AutomationManager()
            manager.enable_automation()
            self.log("Automação semanal ativada.")
            self.update_status("Automação ativada")
        else:
            manager = AutomationManager()
            manager.disable_automation()
            self.log("Automação semanal desativada.")
            self.update_status("Automação desativada")

    def cancel_search(self):
        if self.current_thread and self.current_thread.isRunning():
            reply = QMessageBox.question(
                self,
                "Confirmar Cancelamento",
                "Tem certeza que deseja cancelar a operação atual?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    self.current_thread.stop()
                    self.cancel_btn.setEnabled(False)
                    self.search_btn.setEnabled(True)
                    self.progress_bar.setValue(0)
                    self.update_status("Operação cancelada")
                    self.log("Operação cancelada pelo usuário.")
                    # Só fecha o navegador se for cancelamento manual
                    if self.bot:
                        try:
                            self.bot.fechar()
                        except:
                            pass
                except Exception as e:
                    self.log(f"Erro ao cancelar operação: {str(e)}")
                    self.update_status("Erro ao cancelar operação")

    def closeEvent(self, event):
        if self.current_thread and self.current_thread.isRunning():
            reply = QMessageBox.question(
                self,
                "Confirmar Saída",
                "Há uma operação em andamento. Deseja realmente sair?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                if self.current_thread:
                    self.current_thread.stop()
                    self.current_thread.wait()
                if self.bot:
                    try:
                        self.bot.fechar()
                    except:
                        pass
                event.accept()
            else:
                event.ignore()
        else:
            if self.bot:
                try:
                    self.bot.fechar()
                except:
                    pass
            event.accept()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main()) 