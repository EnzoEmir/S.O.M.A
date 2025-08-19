from PySide6.QtWidgets import QMessageBox

def remover_tarefa(indice, parent_widget, agenda_window, gerenciador_tarefas):
    resposta = QMessageBox.question(parent_widget, "Confirmar Remoção", "Tem certeza que deseja remover esta tarefa?", QMessageBox.Yes | QMessageBox.No)
    
    if resposta == QMessageBox.Yes:
        dados = gerenciador_tarefas.carregar()
        tarefas = dados["tarefas"]
        
        if 0 <= indice < len(tarefas):
            tarefa_removida = tarefas[indice]
            descricao_tarefa = tarefa_removida["description"]
            
            tarefas.pop(indice)
            
            atividades_concluidas = dados.get("atividades_concluidas", {})
            tarefas_para_remover = []
            
            for data, atividades_do_dia in atividades_concluidas.items():
                if descricao_tarefa in atividades_do_dia:
                    del atividades_do_dia[descricao_tarefa]
                    
                    if not atividades_do_dia:
                        tarefas_para_remover.append(data)
            
            for data in tarefas_para_remover:
                del atividades_concluidas[data]
            
            if gerenciador_tarefas.salvar(dados):
                QMessageBox.information(parent_widget, "Sucesso", "Tarefa removida com sucesso!")
                agenda_window.controller.carregar_tarefas_json()
                agenda_window.controller.atualizar_grifados()
                return True
            else:
                QMessageBox.critical(parent_widget, "Erro", "Não foi possível salvar as alterações.")
        else:
            QMessageBox.critical(parent_widget, "Erro", "Índice da tarefa inválido. Não foi possível remover.")
    
    return False