from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QMessageBox
from PySide6.QtCore import QDate
from SOMA.agenda.delecao import remover_tarefa
from SOMA.agenda.adicionar_tarefa_ui import AdicionarTarefaWindow
import json
import os


class GerenciadorTarefas:
    def __init__(self, caminho_arquivo="SOMA/minhas_datas.json"):
        self.caminho_arquivo = caminho_arquivo

    def carregar(self):
        if not os.path.exists(self.caminho_arquivo):
            return []
        try:
            with open(self.caminho_arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def salvar(self, tarefas):
        try:
            with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
                json.dump(tarefas, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar tarefas: {e}")
            return False

class TarefasDoDiaWindow(QWidget):
    def __init__(self, agenda_window, data_selecionada):
        super().__init__()
        self.agenda_window = agenda_window
        self.data_selecionada = data_selecionada
        self.gerenciador_tarefas = GerenciadorTarefas()

        
        self.setWindowTitle("Tarefas do Dia")
        self.resize(450, 400)

        self.label_data = QLabel(f"Tarefas para: {self.data_selecionada.toString('dd/MM/yyyy')}")
        self.label_data.setStyleSheet("font-weight: bold; color: #2c5282; font-size: 14px;")

        self.lista_tarefas = QListWidget()
        self.lista_tarefas.setStyleSheet("QListWidget::item { padding: 8px; border-bottom: 1px solid #ddd; }")

        self.btn_remover = QPushButton("🗑️ Remover Tarefa")
        self.btn_remover.setStyleSheet("background-color: #e53e3e; color: white; font-weight: bold;")
        
        self.btn_adicionar = QPushButton("➕ Adicionar Tarefa")
        self.btn_adicionar.setStyleSheet("background-color: #38a169; color: white; font-weight: bold;")

        self.btn_fechar = QPushButton("❌ Fechar")

        self.btn_remover.clicked.connect(self.remover_tarefa_selecionada)
        self.btn_adicionar.clicked.connect(self.abrir_janela_adicionar)
        self.btn_fechar.clicked.connect(self.close)
        
        self.carregar_tarefas_do_dia()


        layout = QVBoxLayout(self)
        btn_layout = QHBoxLayout()
        
        btn_layout.addWidget(self.btn_remover)
        btn_layout.addWidget(self.btn_adicionar)

        layout.addWidget(self.label_data)
        layout.addWidget(self.lista_tarefas)
        layout.addLayout(btn_layout)
        layout.addWidget(self.btn_fechar)

    def carregar_tarefas_do_dia(self):
        self.lista_tarefas.clear()
        todas_tarefas = self.gerenciador_tarefas.carregar()
        tarefas_do_dia = self._filtrar_tarefas_do_dia(todas_tarefas)

        if not tarefas_do_dia:
            self.lista_tarefas.addItem("Nenhuma tarefa para este dia.")
            self.btn_remover.setEnabled(False)
        else:
            self.btn_remover.setEnabled(True)
            for tarefa_info in tarefas_do_dia:
                tipo_map = {"single": "Evento Único", "daily": "Diário", "weekly": "Semanal"}
                tipo_texto = tipo_map.get(tarefa_info["type"], "Desconhecido")
                
                item_text = f"{tarefa_info['description']} ({tipo_texto})"
                item = QListWidgetItem(item_text)
                item.setData(32, tarefa_info["index"])  
                self.lista_tarefas.addItem(item)

    def _filtrar_tarefas_do_dia(self, tarefas):
        tarefas_filtradas = []
        for i, tarefa in enumerate(tarefas):
            tipo = tarefa.get("type")
            data_tarefa = QDate.fromString(tarefa.get("date", ""), "dd-MM-yyyy")
            
            is_today = (tipo == "single" and data_tarefa == self.data_selecionada) or \
                       (tipo == "daily") or \
                       (tipo == "weekly" and data_tarefa.dayOfWeek() == self.data_selecionada.dayOfWeek())
            
            if is_today:
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