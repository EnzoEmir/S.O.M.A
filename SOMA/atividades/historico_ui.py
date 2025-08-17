from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QDateEdit, QGroupBox, QHeaderView, QMessageBox, QProgressBar
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QColor
from .atividades_controller import AtividadesController

class HistoricoAtividadesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = AtividadesController()
        self.setup_ui()
        self.carregar_historico_mes_atual()
    
    def setup_ui(self):
        self.setWindowTitle("Histórico de Atividades")
        self.setGeometry(200, 200, 1000, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        layout_header = QHBoxLayout()
        
        title = QLabel("Histórico de Atividades")
        title.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        title.setFont(font)
        layout_header.addWidget(title)
        
        layout.addLayout(layout_header)
        
        group_filtros = QGroupBox("Filtros")
        layout_filtros = QHBoxLayout(group_filtros)
        
        layout_filtros.addWidget(QLabel("Data Início:"))
        self.data_inicio = QDateEdit()
        self.data_inicio.setDate(QDate.currentDate().addDays(-30))
        self.data_inicio.setCalendarPopup(True)
        layout_filtros.addWidget(self.data_inicio)
        
        layout_filtros.addWidget(QLabel("Data Fim:"))
        self.data_fim = QDateEdit()
        self.data_fim.setDate(QDate.currentDate())
        self.data_fim.setCalendarPopup(True)
        layout_filtros.addWidget(self.data_fim)
        
        btn_filtrar = QPushButton("Filtrar")
        btn_filtrar.clicked.connect(self.filtrar_periodo)
        layout_filtros.addWidget(btn_filtrar)
        
        btn_mes_atual = QPushButton("Mês Atual")
        btn_mes_atual.clicked.connect(self.carregar_historico_mes_atual)
        layout_filtros.addWidget(btn_mes_atual)
        
        layout_filtros.addStretch()
        
        layout.addWidget(group_filtros)
        
        group_resumo = QGroupBox("Resumo do Período")
        layout_resumo = QVBoxLayout(group_resumo)
        
        self.label_resumo = QLabel()
        self.label_resumo.setWordWrap(True)
        layout_resumo.addWidget(self.label_resumo)
        
        self.progresso_geral = QProgressBar()
        layout_resumo.addWidget(self.progresso_geral)
        
        layout.addWidget(group_resumo)
        
        tabela_group = QGroupBox("Detalhamento por Dia")
        layout_tabela = QVBoxLayout(tabela_group)
        
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels([
            "Data", "Total Tarefas", "Concluídas", "Progresso", "Status"
        ])
        
        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        layout_tabela.addWidget(self.tabela)
        layout.addWidget(tabela_group)
        
        layout_botoes = QHBoxLayout()
                
        layout_botoes.addStretch()
        
        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.close)
        layout_botoes.addWidget(btn_voltar)
        
        layout.addLayout(layout_botoes)
    
    def carregar_historico_mes_atual(self):
        hoje = QDate.currentDate()
        inicio_mes = QDate(hoje.year(), hoje.month(), 1)
        fim_mes = QDate(hoje.year(), hoje.month(), hoje.daysInMonth())
        
        self.data_inicio.setDate(inicio_mes)
        self.data_fim.setDate(fim_mes)
        self.filtrar_periodo()
    
    def filtrar_periodo(self):
        data_inicio = self.data_inicio.date()
        data_fim = self.data_fim.date()
        
        if data_inicio > data_fim:
            QMessageBox.warning(self, "Erro", "Data de início deve ser anterior à data de fim!")
            return
        
        self.carregar_dados_periodo(data_inicio, data_fim)
    
    def carregar_dados_periodo(self, data_inicio, data_fim):
        # Limpar tabela
        self.tabela.setRowCount(0)
        
        stats = self.controller.obter_estatisticas_periodo(data_inicio, data_fim)
        
        self.atualizar_resumo(stats, data_inicio, data_fim)
        
        data_atual = data_inicio
        row = 0
        
        while data_atual <= data_fim:
            tarefas_do_dia = self.controller.obter_tarefas_do_dia(data_atual)
            
            if tarefas_do_dia:  
                self.tabela.insertRow(row)
                
                item_data = QTableWidgetItem(data_atual.toString("dd/MM/yyyy"))
                item_data.setTextAlignment(Qt.AlignCenter)
                self.tabela.setItem(row, 0, item_data)
                
                total_tarefas = len(tarefas_do_dia)
                item_total = QTableWidgetItem(str(total_tarefas))
                item_total.setTextAlignment(Qt.AlignCenter)
                self.tabela.setItem(row, 1, item_total)
                
                concluidas, _, progresso = self.controller.obter_progresso_do_dia(data_atual)
                item_concluidas = QTableWidgetItem(str(concluidas))
                item_concluidas.setTextAlignment(Qt.AlignCenter)
                self.tabela.setItem(row, 2, item_concluidas)
                
                widget_progresso = QProgressBar()
                widget_progresso.setMinimum(0)
                widget_progresso.setMaximum(100)
                widget_progresso.setValue(int(progresso))
                widget_progresso.setFormat(f"{progresso:.1f}%")
                
                if progresso == 100:
                    widget_progresso.setStyleSheet("QProgressBar::chunk { background-color: #4CAF50; }")
                elif progresso >= 50:
                    widget_progresso.setStyleSheet("QProgressBar::chunk { background-color: #FF9800; }")
                else:
                    widget_progresso.setStyleSheet("QProgressBar::chunk { background-color: #F44336; }")
                
                self.tabela.setCellWidget(row, 3, widget_progresso)
                
                if progresso == 100:
                    status = "✅ Completo"
                    cor = QColor(76, 175, 80)  
                elif progresso >= 50:
                    status = "Parcial"
                    cor = QColor(255, 152, 0)  
                else:
                    status = "Incompleto"
                    cor = QColor(244, 67, 54)  
                
                item_status = QTableWidgetItem(status)
                item_status.setTextAlignment(Qt.AlignCenter)
                item_status.setForeground(cor)
                self.tabela.setItem(row, 4, item_status)
                
                row += 1
            
            data_atual = data_atual.addDays(1)
        
        self.tabela.resizeRowsToContents()
    
    def atualizar_resumo(self, stats, data_inicio, data_fim):
        periodo = f"{data_inicio.toString('dd/MM/yyyy')} a {data_fim.toString('dd/MM/yyyy')}"
        
        texto_resumo = f"""Período: {periodo}
Taxa de conclusão: {stats['taxa_conclusao']:.1f}%
Streak de dias perfeitos: {stats['streak_dias_perfeitos']} dias
Total de tarefas concluídas: {stats['total_tarefas_concluidas']}"""
        
        self.label_resumo.setText(texto_resumo)
        
        self.progresso_geral.setValue(int(stats['taxa_conclusao']))
        self.progresso_geral.setFormat(f"Taxa de Conclusão: {stats['taxa_conclusao']:.1f}%")
        
        if stats['taxa_conclusao'] >= 80:
            self.progresso_geral.setStyleSheet("QProgressBar::chunk { background-color: #4CAF50; }")
        elif stats['taxa_conclusao'] >= 60:
            self.progresso_geral.setStyleSheet("QProgressBar::chunk { background-color: #FF9800; }")
        else:
            self.progresso_geral.setStyleSheet("QProgressBar::chunk { background-color: #F44336; }")
    

