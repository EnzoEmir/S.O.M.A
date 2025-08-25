from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from SOMA.navegacao.stack import NavigationStack
from SOMA.inicial.ui import MainWindow
from SOMA.agenda.agenda_ui import AgendaWindow
from SOMA.atividades.atividades_ui import AtividadesWindow
import sys
import os

def main():
    app = QApplication(sys.argv)
    
    # Define o ícone da aplicação
    icon_path = os.path.join(os.path.dirname(__file__), "main.ico")
    if os.path.exists(icon_path):
        icon = QIcon(icon_path)
        app.setWindowIcon(icon)
        print(f"Ícone carregado: {icon_path}")
    else:
        print(f"Ícone não encontrado: {icon_path}")
    
    # Força o ícone na barra de tarefas no Windows
    try:
        from ctypes import windll
        windll.shell32.SetCurrentProcessExplicitAppUserModelID("S.O.M.A.1.0")
    except:
        pass  # Ignora se não estiver no Windows
    
    navigation = NavigationStack()
    
    main_page = MainWindow()
    agenda_page = AgendaWindow()
    atividades_page = AtividadesWindow()
    
    navigation.adicionar_pagina("main", main_page)
    navigation.adicionar_pagina("agenda", agenda_page)
    navigation.adicionar_pagina("atividades", atividades_page)
    
    navigation.navegar_para("main", add_to_history=False)
    
    navigation.showMaximized()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
