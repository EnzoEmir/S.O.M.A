from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QMessageBox, QSizePolicy
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QColor
from SOMA.agenda.delecao import remover_tarefa
from SOMA.agenda.adicionar_tarefa_ui import AdicionarTarefaWindow
import json
import os


class GerenciadorTarefas:
    def __init__(self, caminho_arquivo="SOMA/minhas_datas.json"):
        self.caminho_arquivo = caminho_arquivo

    def carregar(self):
        if not os.path.exists(self.caminho_arquivo):
            return {"tarefas": [], "atividades_concluidas": {}}
        try:
            with open(self.caminho_arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                
                if "tarefas" not in dados:
                    dados["tarefas"] = []
                if "atividades_concluidas" not in dados:
                    dados["atividades_concluidas"] = {}
                return dados
                    
        except (json.JSONDecodeError, FileNotFoundError):
            return {"tarefas": [], "atividades_concluidas": {}}

    def salvar(self, dados):
        try:
            with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            return False

class TarefasDoDiaWindow(QWidget):
    def __init__(self, agenda_window, data_selecionada):
        super().__init__()
        self.agenda_window = agenda_window
        self.data_selecionada = data_selecionada
        self.gerenciador_tarefas = GerenciadorTarefas()

        self.setup_ui()
        self.setup_styles()
        self.conectar_signals()
        
        self.carregar_tarefas_do_dia()

    def setup_ui(self):
        self.setWindowTitle("Tarefas do Dia")
        self.resize(450, 500)
        self.setMinimumSize(400, 450)  

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        
        self.label_data = QLabel(f"Tarefas para: {self.data_selecionada.toString('dd/MM/yyyy')}")
        self.label_data.setObjectName("dataTitle")
        self.label_data.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lista_tarefas = QListWidget()
        self.lista_tarefas.setObjectName("taskList")

        self.btn_adicionar = QPushButton("Adicionar Tarefa")
        self.btn_adicionar.setObjectName("confirmButton")
        
        self.btn_remover = QPushButton("Remover Tarefa")
        self.btn_remover.setObjectName("cancelButton")
        
        self.btn_fechar = QPushButton("Fechar")
        self.btn_fechar.setObjectName("neutralButton")

        for btn in [self.btn_adicionar, self.btn_remover, self.btn_fechar]:
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.setMinimumHeight(40)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addWidget(self.btn_remover)
        btn_layout.addWidget(self.btn_adicionar)

        main_layout.addWidget(self.label_data)
        main_layout.addWidget(self.lista_tarefas, 1)  
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.btn_fechar)

    def setup_styles(self):
        style_sheet = """
            /* Estilo geral da janela e fonte */
            QWidget {
                background-color: #2B2D31;
                font-family: Poppins, sans-serif;
                color: #ECECEC; 
            }

            /* Título da data */
            #dataTitle {
                font-size: 16px;
                font-weight: 600;
                color: #ECECEC;
                background-color: #383B42;
                padding: 12px;
                border-radius: 8px;
                border: 1px solid #474A51;
            }

            /* Lista de tarefas */
            #taskList {
                background-color: #383B42;
                border: 1px solid #474A51;
                border-radius: 8px;
                padding: 5px;
                color: #ECECEC;
                font-size: 13px;
            }

            #taskList::item {
                padding: 10px;
                border-bottom: 1px solid #474A51;
                border-radius: 4px;
                margin: 2px 0px;
            }

            #taskList::item:selected {
                background-color: #5A6B7D;
                color: #ECECEC;
            }

            #taskList::item:hover {
                background-color: #474A51;
            }

            /* --- ESTILO DOS BOTÕES --- */
            
            /* Botão Neutro/Padrão  */
            QPushButton {
                background-color: #A0C4FF;
                color: #0F141A;
                font-size: 13px;
                font-weight: 500;
                border: none;
                padding: 12px 15px;
                border-radius: 8px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #90B9FF;
            }
            QPushButton:pressed {
                background-color: #7FAEFF;
            }

            /* Botão de Ação/Confirmar (Verde) */
            #confirmButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
            #confirmButton:hover { 
                background-color: #45a049; 
            }
            #confirmButton:pressed { 
                background-color: #3e8e41; 
            }

            /* Botão de Cancelar/Remover  */
            #cancelButton {
                background-color: #E57373;
                color: white;
                font-weight: bold;
            }
            #cancelButton:hover { 
                background-color: #e56363; 
            }
            #cancelButton:pressed { 
                background-color: #e55353; 
            }

            /* Botão Neutro/Secundário */
            #neutralButton {
                background-color: #A0C4FF;
                color: #0F141A;
            }
            #neutralButton:hover {
                background-color: #90B9FF;
            }
            #neutralButton:pressed {
                background-color: #7FAEFF;
            }
        """
        self.setStyleSheet(style_sheet)

    def conectar_signals(self):
        self.btn_remover.clicked.connect(self.remover_tarefa_selecionada)
        self.btn_adicionar.clicked.connect(self.abrir_janela_adicionar)
        self.btn_fechar.clicked.connect(self.close)

    def carregar_tarefas_do_dia(self):
        self.lista_tarefas.clear()
        dados = self.gerenciador_tarefas.carregar()
        tarefas_do_dia = self._filtrar_tarefas_do_dia(dados["tarefas"])

        if not tarefas_do_dia:
            item = QListWidgetItem("Nenhuma tarefa para este dia.")
            item.setForeground(QColor("#B9BBBE"))  
            self.lista_tarefas.addItem(item)
            self.btn_remover.setEnabled(False)
        else:
            self.btn_remover.setEnabled(True)
            for tarefa_info in tarefas_do_dia:
                tipo_map = {"single": "Evento Único", "daily": "Diário", "weekly": "Semanal"}
                tipo_texto = tipo_map.get(tarefa_info["type"], "Desconhecido")
                
                eh_importante = tarefa_info.get("importante", False)
                if eh_importante:
                    tipo_texto = "IMPORTANTE"
                    item_text = f"{tarefa_info['description']} ({tipo_texto})"
                else:
                    item_text = f"{tarefa_info['description']} ({tipo_texto})"
                
                item = QListWidgetItem(item_text)
                item.setData(32, tarefa_info["index"])  
                
                if eh_importante:
                    item.setForeground(QColor("#F6E58D"))
                    item.setBackground(QColor("#4A4832"))  
                elif tarefa_info["type"] == "daily":
                    item.setForeground(QColor("#B5EAD7"))
                elif tarefa_info["type"] == "weekly":
                    item.setForeground(QColor("#CDB4DB"))
                elif tarefa_info["type"] == "single":
                    item.setForeground(QColor("#A0C4FF"))
                
                self.lista_tarefas.addItem(item)

    def _filtrar_tarefas_do_dia(self, tarefas):
        tarefas_filtradas = []
        for i, tarefa in enumerate(tarefas):
            tipo = tarefa.get("type")
            data_tarefa = QDate.fromString(tarefa.get("date", ""), "dd-MM-yyyy")
            
            atualmente = False
            
            if tipo == "single":
                atualmente = data_tarefa == self.data_selecionada
            elif tipo == "daily":
                atualmente = self.data_selecionada >= data_tarefa
            elif tipo == "weekly":
                atualmente = (data_tarefa.dayOfWeek() == self.data_selecionada.dayOfWeek() and 
                           self.data_selecionada >= data_tarefa)
            
            if atualmente:
                tarefas_filtradas.append({"index": i, **tarefa})
        
        return tarefas_filtradas

    def remover_tarefa_selecionada(self):
        item_selecionado = self.lista_tarefas.currentItem()
        if not item_selecionado:
            QMessageBox.warning(self, "Atenção", "Por favor, selecione uma tarefa para remover.")
            return

        indice_para_remover = item_selecionado.data(32)
        
        if remover_tarefa(indice_para_remover, self, self.agenda_window, self.gerenciador_tarefas):
            self.carregar_tarefas_do_dia()

    def abrir_janela_adicionar(self):     

        self.janela_adicionar = AdicionarTarefaWindow(self.agenda_window, self.data_selecionada)
        self.janela_adicionar.tarefa_adicionada = self.carregar_tarefas_do_dia
        self.janela_adicionar.show()