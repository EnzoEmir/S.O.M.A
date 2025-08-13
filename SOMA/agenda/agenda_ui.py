from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QCalendarWidget
from SOMA.agenda import agenda_controller

class AgendaWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agenda")
        self.resize(360, 420)

        self.calendario = QCalendarWidget()

        self.btn_todos = QPushButton("Ver Todos")
        self.btn_diarios = QPushButton("Diários")
        self.btn_semanais = QPushButton("Semanais")
        self.btn_unicos = QPushButton("Evento Único")
        self.btn_adicionar = QPushButton("➕ Adicionar Tarefa")
        self.btn_voltar = QPushButton("❌ Voltar")

        layout = QVBoxLayout(self) 
        
        layout.addWidget(self.calendario)
        layout.addWidget(self.btn_todos)
        layout.addWidget(self.btn_diarios)
        layout.addWidget(self.btn_semanais)
        layout.addWidget(self.btn_unicos)
        layout.addWidget(self.btn_adicionar)
        layout.addWidget(self.btn_voltar)
        
        self.controller = agenda_controller.Controller(self)

        self.btn_todos.clicked.connect(lambda: self.controller.atualizar_filtro("all"))
        self.btn_diarios.clicked.connect(lambda: self.controller.atualizar_filtro("daily"))
        self.btn_semanais.clicked.connect(lambda: self.controller.atualizar_filtro("weekly"))
        self.btn_unicos.clicked.connect(lambda: self.controller.atualizar_filtro("single"))
        self.btn_adicionar.clicked.connect(self.controller.abrir_janela_adicionar)
        
        self.btn_voltar.clicked.connect(lambda: agenda_controller.voltar_main(self))

        self.calendario.currentPageChanged.connect(self.controller.atualizar_grifados)

        self.main = None