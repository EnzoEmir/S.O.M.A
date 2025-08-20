from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from SOMA.agenda import agenda_controller
from SOMA.agenda.calendario_customizado import CalendarioCustomizado

class AgendaWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agenda")
        self.resize(400, 480)

        self.calendario = CalendarioCustomizado()

        self.btn_todos = QPushButton("Ver Todos")
        self.btn_diarios = QPushButton("Diários")
        self.btn_semanais = QPushButton("Semanais")
        self.btn_unicos = QPushButton("Evento Único")
        self.btn_ver_tarefas = QPushButton("Ver Tarefas do Dia")
        self.btn_adicionar = QPushButton("➕ Adicionar Tarefa")
        self.btn_voltar = QPushButton("❌ Voltar")

        layout = QVBoxLayout(self) 
        
        layout.addWidget(self.calendario)
        
        legenda_layout = QHBoxLayout()
        legenda_layout.addWidget(QLabel("Legendas:"))
        
        legenda_diario = QLabel("■ Diário")
        legenda_diario.setStyleSheet("color: #B5EAD7; font-weight: bold;")
        
        legenda_semanal = QLabel("■ Semanal") 
        legenda_semanal.setStyleSheet("color: #CDB4DB; font-weight: bold;")
        
        legenda_unico = QLabel("■ Único")
        legenda_unico.setStyleSheet("color: #A0C4FF; font-weight: bold;")
        
        legenda_importante = QLabel("■ Importante")
        legenda_importante.setStyleSheet("color: #F6E58D; font-weight: bold;")
        
        legenda_layout.addWidget(legenda_diario)
        legenda_layout.addWidget(legenda_semanal)
        legenda_layout.addWidget(legenda_unico)
        legenda_layout.addWidget(legenda_importante)
        legenda_layout.addStretch()
        
        layout.addLayout(legenda_layout)
        
        layout.addWidget(self.btn_todos)
        layout.addWidget(self.btn_diarios)
        layout.addWidget(self.btn_semanais)
        layout.addWidget(self.btn_unicos)
        layout.addWidget(self.btn_ver_tarefas)
        layout.addWidget(self.btn_adicionar)
        layout.addWidget(self.btn_voltar)
        
        self.controller = agenda_controller.Controller(self)

        self.btn_todos.clicked.connect(lambda: self.controller.atualizar_filtro("all"))
        self.btn_diarios.clicked.connect(lambda: self.controller.atualizar_filtro("daily"))
        self.btn_semanais.clicked.connect(lambda: self.controller.atualizar_filtro("weekly"))
        self.btn_unicos.clicked.connect(lambda: self.controller.atualizar_filtro("single"))
        self.btn_adicionar.clicked.connect(self.controller.abrir_janela_adicionar)
        self.btn_ver_tarefas.clicked.connect(self.controller.abrir_tarefas_do_dia)
        
        self.btn_voltar.clicked.connect(lambda: agenda_controller.voltar_main(self))

        self.calendario.currentPageChanged.connect(self.controller.atualizar_grifados)

        self.main = None