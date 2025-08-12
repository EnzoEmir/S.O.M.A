from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QCalendarWidget
from PySide6.QtGui import QColor, QTextCharFormat, QFont
from PySide6.QtCore import QDate
from SOMA.agenda import controller
import json

class AgendaWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agenda")
        self.resize(360, 420)

        self.calendario = QCalendarWidget()

        self.formato_dias_importantes = QTextCharFormat() 
        cor_de_fundo = QColor("#a4bcdd")
        self.formato_dias_importantes.setBackground(cor_de_fundo)
        self.formato_dias_importantes.setFontWeight(QFont.Bold)

        try: 
            with open("SOMA\minhas_datas.json", "r") as f:
                lista_de_tarefas = json.load(f)
        except FileNotFoundError: 
            lista_de_tarefas = [] 
            print("AVISO: Arquivo 'minhas_datas.json' não encontrado.")

        
        for tarefa in lista_de_tarefas:             
            q_date = QDate.fromString(tarefa["date"], "dd-MM-yyyy")

            self.calendario.setDateTextFormat(q_date, self.formato_dias_importantes)

        layout = QVBoxLayout()
        


        btn_todos = QPushButton("Ver Todos")
        btn_diarios = QPushButton("Diários")
        btn_semanais = QPushButton("Semanais")
        btn_unicos = QPushButton("Evento Único")
        btn_voltar = QPushButton("❌ Voltar")


        layout.addWidget(self.calendario)

        layout.addWidget(btn_todos)
        layout.addWidget(btn_diarios)
        layout.addWidget(btn_semanais)
        layout.addWidget(btn_unicos)
        layout.addWidget(btn_voltar)

        self.setLayout(layout)

        self.carregar_tarefas_json()

        self.filtro_atual = "all"

        self.atualizar_grifados() 

        btn_todos.clicked.connect(lambda: self.atualizar_filtro("all"))
        btn_diarios.clicked.connect(lambda: self.atualizar_filtro("daily"))
        btn_semanais.clicked.connect(lambda: self.atualizar_filtro("weekly"))
        btn_unicos.clicked.connect(lambda: self.atualizar_filtro("single"))
        btn_voltar.clicked.connect(lambda: controller.voltar_main(self))

        self.calendario.currentPageChanged.connect(lambda: self.atualizar_grifados(self.filtro_atual))


    def carregar_tarefas_json(self):
        try:
            with open("SOMA\minhas_datas.json", "r", encoding="utf-8") as f:
                self.tarefas = json.load(f)
        except FileNotFoundError:
            self.tarefas = []
            print("AVISO: Arquivo 'minhas_datas.json' não encontrado.")
    
    def atualizar_grifados(self, tipo_filtro="all"): 
        self.calendario.setDateTextFormat(QDate(), QTextCharFormat())
        self.aplicar_formatacao(tipo_filtro)

    def atualizar_filtro(self, tipo_filtro):
        self.filtro_atual = tipo_filtro
        self.atualizar_grifados(tipo_filtro)

    def aplicar_formatacao(self, tipo_filtro="all"):
        ano = self.calendario.yearShown()
        mes = self.calendario.monthShown()

        for tarefas in self.tarefas:
            tipo_tarefa = tarefas["type"]

            if tipo_filtro != "all" and tipo_tarefa != tipo_filtro:
                continue

            data_original = QDate.fromString(tarefas["date"], "dd-MM-yyyy")

            if tipo_tarefa == "single":
                if data_original.year() == ano and data_original.month() == mes:
                    self.calendario.setDateTextFormat(data_original, self.formato_dias_importantes)

            elif tipo_tarefa == "daily":
                dias_no_mes = QDate(ano, mes, 1).daysInMonth()
                for dia in range(1, dias_no_mes + 1):
                    self.calendario.setDateTextFormat(QDate(ano, mes, dia), self.formato_dias_importantes)

            elif tipo_tarefa == "weekly":
                dia_semana = data_original.dayOfWeek()
                dias_no_mes = QDate(ano, mes, 1).daysInMonth()
                for dia in range(1, dias_no_mes + 1):
                    data_atual = QDate(ano, mes, dia)
                    if data_atual.dayOfWeek() == dia_semana:
                        self.calendario.setDateTextFormat(data_atual, self.formato_dias_importantes)

    

        self.main = None