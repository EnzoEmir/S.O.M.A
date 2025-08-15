from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QCheckBox, QMessageBox
import json
import os

class AdicionarTarefaWindow(QWidget):
    def __init__(self, agenda_window, data_selecionada):
        super().__init__()
        self.agenda_window = agenda_window
        self.data_selecionada = data_selecionada
        self.tarefa_adicionada = None 
        self.setWindowTitle("Adicionar Nova Tarefa")
        self.resize(400, 250)

        self.label_descricao = QLabel("Descrição da Tarefa:")
        self.input_descricao = QLineEdit()
        self.input_descricao.setPlaceholderText("Ex: Reunião importante, Exercícios...")


        self.label_tipo = QLabel("Tipo de Tarefa:")
        
        self.checkbox_unico = QCheckBox("Evento Único")
        self.checkbox_diario = QCheckBox("Diário")
        self.checkbox_semanal = QCheckBox("Semanal")
        
        self.checkbox_unico.setChecked(True)

        self.label_data = QLabel(f"Data selecionada: {self.data_selecionada.toString('dd/MM/yyyy')}")
        self.label_data.setStyleSheet("font-weight: bold; color: #2c5282;")

        self.label_info = QLabel()
        self.atualizar_info_tipo()

        self.btn_salvar = QPushButton("Salvar Tarefa")
        self.btn_cancelar = QPushButton("❌ Cancelar")

        layout = QVBoxLayout(self)
        
        layout.addWidget(self.label_data)
        layout.addWidget(self.label_descricao)
        layout.addWidget(self.input_descricao)
        
        layout.addWidget(self.label_tipo)
        layout.addWidget(self.checkbox_unico)
        layout.addWidget(self.checkbox_diario)
        layout.addWidget(self.checkbox_semanal)
        
        layout.addWidget(self.label_info)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_salvar)
        btn_layout.addWidget(self.btn_cancelar)
        layout.addLayout(btn_layout)

        self.checkbox_unico.toggled.connect(lambda checked: self.gerenciar_checkboxes(self.checkbox_unico, checked))
        self.checkbox_diario.toggled.connect(lambda checked: self.gerenciar_checkboxes(self.checkbox_diario, checked))
        self.checkbox_semanal.toggled.connect(lambda checked: self.gerenciar_checkboxes(self.checkbox_semanal, checked))
        self.btn_salvar.clicked.connect(self.salvar_tarefa)
        self.btn_cancelar.clicked.connect(self.close)

    def gerenciar_checkboxes(self, checkbox_ativa, checked):
        if checked:
            if checkbox_ativa != self.checkbox_unico:
                self.checkbox_unico.setChecked(False)
            if checkbox_ativa != self.checkbox_diario:
                self.checkbox_diario.setChecked(False)
            if checkbox_ativa != self.checkbox_semanal:
                self.checkbox_semanal.setChecked(False)
        
        self.atualizar_info_tipo()

    def atualizar_info_tipo(self):
        if self.checkbox_unico.isChecked():
            self.label_info.setText("Evento único: aparecerá apenas na data selecionada")
        elif self.checkbox_diario.isChecked():
            self.label_info.setText("Diário: aparecerá todos os dias do calendário")
        elif self.checkbox_semanal.isChecked():
            self.label_info.setText("Semanal: aparecerá no mesmo dia da semana da data selecionada")
        else:
            self.label_info.setText("Por favor, selecione um tipo de tarefa")

    def obter_tipo_selecionado(self):
        if self.checkbox_unico.isChecked():
            return "single"
        elif self.checkbox_diario.isChecked():
            return "daily"
        elif self.checkbox_semanal.isChecked():
            return "weekly"
        return None

    def salvar_tarefa(self):
        descricao = self.input_descricao.text().strip()
        
        if not descricao:
            QMessageBox.warning(self, "Erro", "Por favor, insira uma descrição para a tarefa!")
            return

        tipo = self.obter_tipo_selecionado()
        
        if not tipo:
            QMessageBox.warning(self, "Erro", "Por favor, selecione um tipo de tarefa!")
            return
        
        data = self.data_selecionada.toString("dd-MM-yyyy")

        nova_tarefa = {
            "description": descricao,
            "date": data,
            "type": tipo
        }

        caminho_arquivo = "SOMA/minhas_datas.json"
        dados = {"tarefas": [], "atividades_concluidas": {}}
        
        try:
            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                        
                    if "tarefas" not in dados:
                        dados["tarefas"] = []
                    if "atividades_concluidas" not in dados:
                        dados["atividades_concluidas"] = {}
                        
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar arquivo: {e}")
            return

        dados["tarefas"].append(nova_tarefa)

        try:
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            
            QMessageBox.information(self, "Sucesso", "Tarefa adicionada com sucesso!")
            
            self.agenda_window.controller.carregar_tarefas_json()
            self.agenda_window.controller.atualizar_grifados()
            
            if self.tarefa_adicionada:
                self.tarefa_adicionada()
            
            self.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar tarefa: {e}")
