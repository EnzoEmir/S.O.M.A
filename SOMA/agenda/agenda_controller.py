import json
from PySide6.QtGui import QTextCharFormat
from PySide6.QtCore import QDate
from collections import defaultdict

class Controller:
    def __init__(self, view):
        self.view = view
        
        self.tarefas = []
        self.filtro_atual = "all"
        
        self.view.calendario.activated.connect(self.abrir_tarefas_do_dia)         # duplo clique no calendário 

        self.carregar_tarefas_json()
        self.atualizar_grifados()

    def carregar_tarefas_json(self):
        try:
            with open("SOMA/minhas_datas.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                self.tarefas = dados.get("tarefas", [])
                
            self.limpar_atividades_orfas_automatico()
                    
        except FileNotFoundError:
            self.tarefas = []
            print("AVISO: Arquivo 'minhas_datas.json' não encontrado.")
    
    def limpar_atividades_orfas_automatico(self):
        try:
            from SOMA.atividades.atividades_controller import AtividadesController
            atividades_controller = AtividadesController()
            atividades_controller.limpar_atividades_orfas()
        except Exception as e:
            print(f"Erro na limpeza automática: {e}")
    
    def atualizar_grifados(self):
        tipo_filtro = self.filtro_atual
        self.view.calendario.setDateTextFormat(QDate(), QTextCharFormat()) 
        self.aplicar_formatacao_com_barras(tipo_filtro)

    def aplicar_formatacao_com_barras(self, tipo_filtro="all"):
        ano = self.view.calendario.yearShown()
        mes = self.view.calendario.monthShown()  
        tarefas_por_data = defaultdict(set)
        tarefas_importantes_por_data = defaultdict(bool)
        
        for tarefa in self.tarefas:
            tipo_tarefa = tarefa["type"]

            if tipo_filtro != "all" and tipo_tarefa != tipo_filtro:
                continue

            data_original = QDate.fromString(tarefa["date"], "dd-MM-yyyy")
            eh_importante = tarefa.get("importante", False)
            
            if tipo_tarefa == "single":
                if data_original.year() == ano and data_original.month() == mes:
                    if eh_importante:
                        tarefas_importantes_por_data[data_original] = True
                    tarefas_por_data[data_original].add("single")            
            elif tipo_tarefa == "daily":
                dias_no_mes = QDate(ano, mes, 1).daysInMonth()
                for dia in range(1, dias_no_mes + 1):
                    data_atual = QDate(ano, mes, dia)
                    if data_atual >= data_original:
                        if eh_importante:
                            tarefas_importantes_por_data[data_atual] = True
                        tarefas_por_data[data_atual].add("daily")
                            
            elif tipo_tarefa == "weekly":
                dia_semana = data_original.dayOfWeek()
                dias_no_mes = QDate(ano, mes, 1).daysInMonth()
                for dia in range(1, dias_no_mes + 1):
                    data_atual = QDate(ano, mes, dia)
                    if data_atual.dayOfWeek() == dia_semana and data_atual >= data_original:
                        if eh_importante:
                            tarefas_importantes_por_data[data_atual] = True
                        tarefas_por_data[data_atual].add("weekly")
        
        self.view.calendario.atualizar_tarefas_data(tarefas_por_data, tarefas_importantes_por_data)

    def atualizar_filtro(self, tipo_filtro):
        self.filtro_atual = tipo_filtro
        self.atualizar_grifados()

    def abrir_janela_adicionar(self):
        from SOMA.agenda.adicionar_tarefa_ui import AdicionarTarefaWindow 

        data_selecionada = self.view.calendario.selectedDate()
        self.janela_adicionar = AdicionarTarefaWindow(self.view, data_selecionada)
        self.janela_adicionar.show()

    def abrir_tarefas_do_dia(self):
        from SOMA.agenda.tarefas_do_dia_ui import TarefasDoDiaWindow

        data_selecionada = self.view.calendario.selectedDate()
        self.janela_tarefas = TarefasDoDiaWindow(self.view, data_selecionada)
        self.janela_tarefas.show()