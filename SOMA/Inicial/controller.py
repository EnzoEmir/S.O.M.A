from PySide6.QtWidgets import QMessageBox
from SOMA.agenda.ui import AgendaWindow 

def handle_view_agenda(main_window): 
    main_window.agenda_window = AgendaWindow()
    main_window.agenda_window.show()
    main_window.close() 

def handle_add_tarefa():
    QMessageBox.information(None, "Nova Tarefa", "Função de adicionar tarefa ainda não implementada.")
