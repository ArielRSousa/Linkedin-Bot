import os
import sys
import json
import requests
import subprocess
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox, QProgressDialog
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class Updater(QThread):
    update_available = pyqtSignal(bool, str)
    update_progress = pyqtSignal(int)
    update_finished = pyqtSignal(bool, str)

    def __init__(self, current_version):
        super().__init__()
        self.current_version = current_version
        self.github_repo = "seuusuario/linkedin-bot"  # Substitua pelo seu repositório
        self.github_api = f"https://api.github.com/repos/{self.github_repo}/releases/latest"

    def check_for_updates(self):
        try:
            response = requests.get(self.github_api)
            if response.status_code == 200:
                latest_release = response.json()
                latest_version = latest_release["tag_name"]
                
                if self.compare_versions(latest_version, self.current_version):
                    self.update_available.emit(True, latest_version)
                    return True, latest_version
                else:
                    self.update_available.emit(False, latest_version)
                    return False, latest_version
            else:
                return False, None
        except Exception as e:
            print(f"Erro ao verificar atualizações: {e}")
            return False, None

    def compare_versions(self, latest, current):
        """Compara versões no formato x.y.z"""
        latest_parts = [int(x) for x in latest.split('.')]
        current_parts = [int(x) for x in current.split('.')]
        
        for i in range(max(len(latest_parts), len(current_parts))):
            latest_part = latest_parts[i] if i < len(latest_parts) else 0
            current_part = current_parts[i] if i < len(current_parts) else 0
            
            if latest_part > current_part:
                return True
            elif latest_part < current_part:
                return False
        return False

    def update_system(self):
        try:
            # Atualiza o repositório
            self.update_progress.emit(10)
            subprocess.run(["git", "fetch", "origin"], check=True)
            self.update_progress.emit(30)
            
            # Reseta para a última versão
            subprocess.run(["git", "reset", "--hard", "origin/main"], check=True)
            self.update_progress.emit(60)
            
            # Atualiza as dependências
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            self.update_progress.emit(90)
            
            # Atualiza a versão no arquivo de configuração
            self.update_version_file()
            self.update_progress.emit(100)
            
            self.update_finished.emit(True, "Sistema atualizado com sucesso!")
            return True
        except Exception as e:
            self.update_finished.emit(False, f"Erro ao atualizar: {str(e)}")
            return False

    def update_version_file(self):
        """Atualiza o arquivo de versão"""
        version_file = "version.json"
        version_data = {
            "version": self.current_version,
            "last_update": datetime.now().isoformat()
        }
        with open(version_file, "w") as f:
            json.dump(version_data, f, indent=4)

def check_and_update(parent=None):
    """Função principal para verificar e atualizar o sistema"""
    # Carrega a versão atual
    try:
        with open("version.json", "r") as f:
            version_data = json.load(f)
            current_version = version_data.get("version", "1.0.0")
    except FileNotFoundError:
        current_version = "1.0.0"
        with open("version.json", "w") as f:
            json.dump({"version": current_version, "last_update": datetime.now().isoformat()}, f, indent=4)

    updater = Updater(current_version)
    
    # Verifica atualizações
    has_update, latest_version = updater.check_for_updates()
    
    if has_update and parent:
        reply = QMessageBox.question(
            parent,
            "Atualização Disponível",
            f"Uma nova versão ({latest_version}) está disponível. Deseja atualizar agora?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            progress = QProgressDialog("Atualizando o sistema...", "Cancelar", 0, 100, parent)
            progress.setWindowModality(Qt.WindowModality.WindowModal)
            progress.setWindowTitle("Atualização")
            progress.setAutoClose(True)
            
            updater.update_progress.connect(progress.setValue)
            updater.update_finished.connect(lambda success, msg: show_update_result(success, msg, parent))
            
            updater.update_system()
            progress.exec()

def show_update_result(success, message, parent=None):
    """Mostra o resultado da atualização"""
    if parent:
        if success:
            QMessageBox.information(parent, "Atualização", message)
        else:
            QMessageBox.warning(parent, "Erro na Atualização", message)
    else:
        print(message) 