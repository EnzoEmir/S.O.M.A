from PySide6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt

class ConfirmacaoDelecao(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_styles()
        self.resultado = False

    def setup_ui(self):
        self.setWindowTitle("Confirmar Remoção")
        self.setFixedSize(350, 150)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        self.label_mensagem = QLabel("Tem certeza que deseja remover esta tarefa")
        self.label_mensagem.setObjectName("confirmMessage")
        self.label_mensagem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_mensagem.setWordWrap(True)

        botoes_layout = QHBoxLayout()
        botoes_layout.setSpacing(15)

        self.btn_sim = QPushButton("Sim")
        self.btn_sim.setObjectName("confirmYes")
        
        self.btn_nao = QPushButton("Não")
        self.btn_nao.setObjectName("confirmNo")

        for btn in [self.btn_sim, self.btn_nao]:
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        botoes_layout.addWidget(self.btn_sim)
        botoes_layout.addWidget(self.btn_nao)

        layout.addWidget(self.label_mensagem)
        layout.addLayout(botoes_layout)

        self.btn_sim.clicked.connect(self.aceitar)
        self.btn_nao.clicked.connect(self.rejeitar)

    def setup_styles(self):
        style_sheet = """
            /* Estilo geral da janela */
            QDialog {
                background-color: #2B2D31;
                font-family: Poppins, sans-serif;
            }

            /* Mensagem de confirmação */
            #confirmMessage {
                font-size: 14px;
                font-weight: 500;
                color: #ECECEC;
                background-color: #383B42;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #E57373;
            }

            /* Botões */
            QPushButton {
                font-size: 14px;
                font-weight: 600;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                min-height: 25px;
            }

            /* Botão Sim (Verde) */
            #confirmYes {
                background-color: #4CAF50;
                color: white;
            }
            
            #confirmYes:hover {
                background-color: #45a049;
            }
            
            #confirmYes:pressed {
                background-color: #3e8e41;
            }

            /* Botão Não (Vermelho) */
            #confirmNo {
                background-color: #E57373;
                color: white;
            }
            
            #confirmNo:hover {
                background-color: #e56363;
            }
            
            #confirmNo:pressed {
                background-color: #e55353;
            }
        """
        self.setStyleSheet(style_sheet)

    def aceitar(self):
        self.resultado = True
        self.accept()

    def rejeitar(self):
        self.resultado = False
        self.reject()

def remover_tarefa(indice, parent_widget, agenda_window, gerenciador_tarefas):
    dialog = ConfirmacaoDelecao(parent_widget)
    dialog.exec()
    
    if dialog.resultado:
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
                sucesso_dialog = QMessageBox(parent_widget)
                sucesso_dialog.setWindowTitle("Sucesso")
                sucesso_dialog.setText("Tarefa removida com sucesso!")
                sucesso_dialog.setIcon(QMessageBox.Icon.Information)
                sucesso_dialog.setStyleSheet("""
                    QMessageBox {
                        background-color: #2B2D31;
                        color: #ECECEC;
                        font-family: Poppins, sans-serif;
                    }
                    QMessageBox QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 6px;
                        font-weight: 500;
                        min-width: 60px;
                    }
                    QMessageBox QPushButton:hover {
                        background-color: #45a049;
                    }
                """)
                sucesso_dialog.exec()
                
                agenda_window.controller.carregar_tarefas_json()
                agenda_window.controller.atualizar_grifados()
                return True
            
        else:
            erro_dialog = QMessageBox(parent_widget)
            erro_dialog.setWindowTitle("Erro")
            erro_dialog.setText("Índice da tarefa inválido. Não foi possível remover.")
            erro_dialog.setIcon(QMessageBox.Icon.Critical)
            erro_dialog.setStyleSheet("""
                QMessageBox {
                    background-color: #2B2D31;
                    color: #ECECEC;
                    font-family: Poppins, sans-serif;
                }
                QMessageBox QPushButton {
                    background-color: #E57373;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-weight: 500;
                    min-width: 60px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #e56363;
                }
            """)
            erro_dialog.exec()
    
    return False