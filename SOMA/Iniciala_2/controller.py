from SOMA.agenda.agenda_ui import AgendaWindow 
from SOMA.atividades.atividades_ui import AtividadesWindow

def handle_view_agenda(main_window): 
    main_window.agenda_window = AgendaWindow()
    main_window.agenda_window.show()
    main_window.close() 

def handle_gerenciar_atividade(main_window):
    main_window.atividades_window = AtividadesWindow()
    main_window.atividades_window.show()
    main_window.close()
