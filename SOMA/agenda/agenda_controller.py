import json
from PySide6.QtGui import QColor, QTextCharFormat, QFont
from PySide6.QtCore import QDate

class Controller:
    def __init__(self, view):
        self.view = view
        
        self.tarefas = []
        self.filtro_atual = "all"

        self.formato_dias_importantes = QTextCharFormat()
        self.formato_dias_importantes.setBackground(QColor("#a4bcdd"))
        self.formato_dias_importantes.setFontWeight(QFont.Bold)
        
        self.carregar_tarefas_json()
        self.atualizar_grifados()

    def carregar_tarefas_json(self):
        try:
            with open("SOMA/minhas_datas.json", "r", encoding="utf-8") as f:
                self.tarefas = json.load(f)
        except FileNotFoundError:
            self.tarefas = []
            print("AVISO: Arquivo 'minhas_datas.json' não encontrado.")
    
    def atualizar_grifados(self):
        tipo_filtro = self.filtro_atual
        self.view.calendario.setDateTextFormat(QDate(), QTextCharFormat()) 
        self.aplicar_formatacao(tipo_filtro)

    def atualizar_filtro(self, tipo_filtro):
        self.filtro_atual = tipo_filtro
        self.atualizar_grifados()

    def aplicar_formatacao(self, tipo_filtro="all"):
        ano = self.view.calendario.yearShown()
        mes = self.view.calendario.monthShown()

        for tarefa in self.tarefas:
            tipo_tarefa = tarefa["type"]

            if tipo_filtro != "all" and tipo_tarefa != tipo_filtro:
                continue

            data_original = QDate.fromString(tarefa["date"], "dd-MM-yyyy")

            if tipo_tarefa == "single":
                if data_original.year() == ano and data_original.month() == mes:
                    self.view.calendario.setDateTextFormat(data_original, self.formato_dias_importantes)

            elif tipo_tarefa == "daily":
                dias_no_mes = QDate(ano, mes, 1).daysInMonth()
                for dia in range(1, dias_no_mes + 1):
                    self.view.calendario.setDateTextFormat(QDate(ano, mes, dia), self.formato_dias_importantes)

            elif tipo_tarefa == "weekly":
                dia_semana = data_original.dayOfWeek()
                dias_no_mes = QDate(ano, mes, 1).daysInMonth()
                for dia in range(1, dias_no_mes + 1):
                    data_atual = QDate(ano, mes, dia)
                    if data_atual.dayOfWeek() == dia_semana:
                        self.view.calendario.setDateTextFormat(data_atual, self.formato_dias_importantes)

    def abrir_janela_adicionar(self):
        from SOMA.agenda.adicionar_tarefa_ui import AdicionarTarefaWindow 

        data_selecionada = self.view.calendario.selectedDate()
        self.janela_adicionar = AdicionarTarefaWindow(self.view, data_selecionada)
        self.janela_adicionar.show()


def voltar_main(current_window):
    from SOMA.inicial.ui import MainWindow
    
    current_window.main = MainWindow()
    current_window.main.show()
    
    current_window.close()