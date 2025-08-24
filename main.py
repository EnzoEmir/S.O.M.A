from PySide6.QtWidgets import QApplication
from SOMA.navegacao.stack import NavigationStack
from SOMA.inicial.ui import MainWindow
from SOMA.agenda.agenda_ui import AgendaWindow
from SOMA.atividades.atividades_ui import AtividadesWindow
import sys

def main():
    app = QApplication(sys.argv)
    
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
