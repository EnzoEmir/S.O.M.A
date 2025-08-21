from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QCheckBox, QMessageBox, QSizePolicy
from PySide6.QtCore import QDate, Qt
import json
import os

class AdicionarTarefaWindow(QWidget):
    def __init__(self, agenda_window, data_selecionada):
        super().__init__()
        self.agenda_window = agenda_window
        self.data_selecionada = data_selecionada
        self.tarefa_adicionada = None 
        
        self.setup_ui()
        self.setup_styles()
        self.conectar_signals()

        self.adjustSize()
        self.show()

    def setup_ui(self):
        self.setWindowTitle("Adicionar Nova Tarefa")
        self.resize(450, 400)
        self.setMinimumSize(450, 400)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        self.label_data = QLabel(f"Data selecionada: {self.data_selecionada.toString('dd/MM/yyyy')}")
        self.label_data.setObjectName("selectedDate")
        self.label_data.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_descricao = QLabel("Descrição da Tarefa:")
        self.label_descricao.setObjectName("fieldLabel")
        
        self.input_descricao = QLineEdit()
        self.input_descricao.setPlaceholderText("Ex: Reunião importante, Exercícios...")
        self.input_descricao.setObjectName("inputField")

        self.label_tipo = QLabel("Tipo de Tarefa:")
        self.label_tipo.setObjectName("fieldLabel")
        
        self.checkbox_unico = QCheckBox("Evento Único")
        self.checkbox_unico.setObjectName("typeCheckbox")
        self.checkbox_unico.setChecked(True)
        
        self.checkbox_diario = QCheckBox("Diário")
        self.checkbox_diario.setObjectName("typeCheckbox")
        
        self.checkbox_semanal = QCheckBox("Semanal")
        self.checkbox_semanal.setObjectName("typeCheckbox")
        
        self.checkbox_importante = QCheckBox("Marcar como Importante (evento especial)")
        self.checkbox_importante.setObjectName("importantCheckbox")
        self.checkbox_importante.setEnabled(True)

        self.label_info = QLabel()
        self.label_info.setObjectName("infoLabel")
        self.label_info.setWordWrap(True)
        self.atualizar_info_tipo()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.btn_salvar = QPushButton("Salvar Tarefa")
        self.btn_salvar.setObjectName("confirmButton")
        
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setObjectName("cancelButton")

        for btn in [self.btn_salvar, self.btn_cancelar]:
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        btn_layout.addWidget(self.btn_salvar)
        btn_layout.addWidget(self.btn_cancelar)

        main_layout.addWidget(self.label_data)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.label_descricao)
        main_layout.addWidget(self.input_descricao)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.label_tipo)
        main_layout.addWidget(self.checkbox_unico)
        main_layout.addWidget(self.checkbox_diario)
        main_layout.addWidget(self.checkbox_semanal)
        main_layout.addSpacing(5)
        main_layout.addWidget(self.checkbox_importante)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.label_info)
        main_layout.addStretch(1)
        main_layout.addLayout(btn_layout)

    def setup_styles(self):
        style_sheet = """
            /* Estilo geral da janela e fonte */
            QWidget {
                background-color: #2B2D31;
                font-family: Poppins, sans-serif;
                color: #ECECEC;
            }

            /* Data selecionada */
            #selectedDate {
                font-size: 16px;
                font-weight: 600;
                color: #A0C4FF;
                background-color: #383B42;
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #474A51;
            }

            /* Labels dos campos */
            #fieldLabel {
                font-size: 14px;
                font-weight: 500;
                color: #ECECEC;
                margin-bottom: 5px;
            }

            /* Campo de entrada */
            #inputField {
                background-color: #383B42;
                border: 1px solid #474A51;
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 14px;
                color: #ECECEC;
                min-height: 20px;
            }
            
            #inputField:focus {
                border-color: #A0C4FF;
                outline: none;
            }
            
            #inputField::placeholder {
                color: #B9BBBE;
            }

            /* Checkboxes de tipo */
            #typeCheckbox {
                font-size: 14px;
                color: #ECECEC;
                spacing: 8px;
                padding: 5px;
            }
            
            #typeCheckbox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 3px;
                border: 2px solid #474A51;
                background-color: #383B42;
            }
            
            #typeCheckbox::indicator:checked {
                background-color: #A0C4FF;
                border-color: #A0C4FF;
            }
            
            #typeCheckbox::indicator:hover {
                border-color: #90B9FF;
            }

            /* Checkbox importante */
            #importantCheckbox {
                font-size: 13px;
                font-weight: 500;
                color: #F6E58D;
                spacing: 8px;
                padding: 8px;
                margin-left: 15px;
            }
            
            #importantCheckbox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 3px;
                border: 2px solid #F6E58D;
                background-color: #383B42;
            }
            
            #importantCheckbox::indicator:checked {
                background-color: #F6E58D;
                border-color: #F6E58D;
            }
            
            #importantCheckbox::indicator:disabled {
                border-color: #5A5E67;
                background-color: #33363C;
            }

            /* Label de informação */
            #infoLabel {
                font-size: 12px;
                color: #B9BBBE;
                background-color: #383B42;
                padding: 10px;
                border-radius: 6px;
                border-left: 3px solid #A0C4FF;
                font-style: italic;
            }

            /* Botões */
            QPushButton {
                background-color: #A0C4FF;
                color: #0F141A;
                font-size: 14px;
                font-weight: 500;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                min-height: 25px;
            }
            
            QPushButton:hover {
                background-color: #90B9FF;
            }
            
            QPushButton:pressed {
                background-color: #7FAEFF;
            }

            /* Botão de Confirmar (Verde) */
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

            /* Botão de Cancelar */
            #cancelButton {
                background-color: #E57373;
                color: white;
            }
            
            #cancelButton:hover {
                background-color: #e56363;
            }
            
            #cancelButton:pressed {
                background-color: #e55353;
            }
        """
        self.setStyleSheet(style_sheet)

    def conectar_signals(self):
        self.checkbox_unico.toggled.connect(lambda checked: self.gerenciar_checkboxes(self.checkbox_unico, checked))
        self.checkbox_diario.toggled.connect(lambda checked: self.gerenciar_checkboxes(self.checkbox_diario, checked))
        self.checkbox_semanal.toggled.connect(lambda checked: self.gerenciar_checkboxes(self.checkbox_semanal, checked))
        self.checkbox_importante.toggled.connect(self.atualizar_info_tipo)
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
        
        # Só é importante se Evento Único estiver marcado
        if self.checkbox_unico.isChecked():
            self.checkbox_importante.setEnabled(True)
        else:
            self.checkbox_importante.setEnabled(False)
            self.checkbox_importante.setChecked(False)  
        
        self.atualizar_info_tipo()

    def atualizar_info_tipo(self):
        if self.checkbox_unico.isChecked():
            if self.checkbox_importante.isChecked():
                self.label_info.setText("Evento único IMPORTANTE: aparecerá na data selecionada destacado")
            else:
                self.label_info.setText("Evento único: aparecerá apenas na data selecionada")
        elif self.checkbox_diario.isChecked():
            self.label_info.setText("Diário: aparecerá todos os dias do calendário")
        elif self.checkbox_semanal.isChecked():
            self.label_info.setText("Semanal: aparecerá no mesmo dia da semana da data selecionada")
        else:
            self.label_info.setText("Por favor, selecione um tipo de tarefa")

    def verificar_tarefa_duplicada(self, descricao, data_selecionada, dados):
        
        data_qdate = QDate.fromString(data_selecionada, "dd-MM-yyyy")
        
        for tarefa_existente in dados["tarefas"]:
            if tarefa_existente["description"].lower() == descricao.lower():
                data_tarefa_existente = QDate.fromString(tarefa_existente["date"], "dd-MM-yyyy")
                tipo_existente = tarefa_existente["type"]
                
                tarefa_aparece_na_data = False
                
                if tipo_existente == "single":
                    tarefa_aparece_na_data = (data_tarefa_existente == data_qdate)
                    
                elif tipo_existente == "daily":
                    tarefa_aparece_na_data = (data_qdate >= data_tarefa_existente)
                    
                elif tipo_existente == "weekly":
                    tarefa_aparece_na_data = (data_qdate >= data_tarefa_existente and data_qdate.dayOfWeek() == data_tarefa_existente.dayOfWeek())
                
                if tarefa_aparece_na_data:
                    return True, tipo_existente
        
        return False, None

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
            "type": tipo,
            "importante": self.checkbox_importante.isChecked() if tipo == "single" else False
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

        tem_duplicata, tipo_existente = self.verificar_tarefa_duplicada(descricao, data, dados)
        
        if tem_duplicata:
            
            QMessageBox.warning(self, "Tarefa Duplicada", 
                              f"Já existe uma tarefa '{descricao}' em {self.data_selecionada.toString('dd/MM/yyyy')}!\n"
                              "Por favor, escolha outro nome para evitar conflitos.")
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
