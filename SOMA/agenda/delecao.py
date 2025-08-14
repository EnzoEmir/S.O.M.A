from PySide6.QtWidgets import QMessageBox

def remover_tarefa(indice, parent_widget, agenda_window, gerenciador_tarefas):
    resposta = QMessageBox.question(parent_widget, "Confirmar Remoção", "Tem certeza que deseja remover esta tarefa?", QMessageBox.Yes | QMessageBox.No)
    
    if resposta == QMessageBox.Yes:
        tarefas = gerenciador_tarefas.carregar()
        if 0 <= indice < len(tarefas):
            tarefas.pop(indice)
            
            if gerenciador_tarefas.salvar(tarefas):
                QMessageBox.information(parent_widget, "Sucesso", "Tarefa removida com sucesso!")
                agenda_window.controller.carregar_tarefas_json()
                agenda_window.controller.atualizar_grifados()
                return True
            else:
                QMessageBox.critical(parent_widget, "Erro", "Não foi possível salvar as alterações.")
        else:
            QMessageBox.critical(parent_widget, "Erro", "Índice da tarefa inválido. Não foi possível remover.")
    
    return False