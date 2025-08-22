from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QDateEdit, QGroupBox, QHeaderView, QMessageBox, QProgressBar, QSizePolicy
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QColor
from .atividades_controller import AtividadesController

class HistoricoAtividadesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = AtividadesController()
        
        self.setup_ui()
        self.setup_styles()
        self.conectar_signals()
        self.carregar_historico_mes_atual()

    def setup_ui(self):
        self.setWindowTitle("Histórico de Atividades")
        self.setGeometry(200, 200, 1000, 600)
        self.setMinimumSize(900, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        layout_header = QHBoxLayout()
        
        self.title = QLabel("Histórico de Atividades")
        self.title.setObjectName("mainTitle")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_header.addWidget(self.title)
        
        layout.addLayout(layout_header)
        
        group_filtros = QGroupBox("Filtros")
        group_filtros.setObjectName("filterGroup")
        layout_filtros = QHBoxLayout(group_filtros)
        layout_filtros.setSpacing(10)
        
        label_inicio = QLabel("Data Início:")
        label_inicio.setObjectName("fieldLabel")
        layout_filtros.addWidget(label_inicio)
        
        self.data_inicio = QDateEdit()
        self.data_inicio.setObjectName("dateInput")
        self.data_inicio.setDate(QDate.currentDate().addDays(-30))
        self.data_inicio.setCalendarPopup(True)
        layout_filtros.addWidget(self.data_inicio)
        
        label_fim = QLabel("Data Fim:")
        label_fim.setObjectName("fieldLabel")
        layout_filtros.addWidget(label_fim)
        
        self.data_fim = QDateEdit()
        self.data_fim.setObjectName("dateInput")
        self.data_fim.setDate(QDate.currentDate())
        self.data_fim.setCalendarPopup(True)
        layout_filtros.addWidget(self.data_fim)
        
        self.btn_filtrar = QPushButton("Filtrar")
        self.btn_filtrar.setObjectName("neutralButton")
        
        self.btn_mes_atual = QPushButton("Mês Atual")
        self.btn_mes_atual.setObjectName("confirmButton")
        
        for btn in [self.btn_filtrar, self.btn_mes_atual]:
            btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        
        layout_filtros.addWidget(self.btn_filtrar)
        layout_filtros.addWidget(self.btn_mes_atual)
        layout_filtros.addStretch()
        
        layout.addWidget(group_filtros)
        
        group_resumo = QGroupBox("Resumo do Período")
        group_resumo.setObjectName("summaryGroup")
        layout_resumo = QVBoxLayout(group_resumo)
        layout_resumo.setSpacing(10)
        
        self.label_resumo = QLabel()
        self.label_resumo.setObjectName("summaryLabel")
        self.label_resumo.setWordWrap(True)
        layout_resumo.addWidget(self.label_resumo)
        
        self.progresso_geral = QProgressBar()
        self.progresso_geral.setObjectName("mainProgressBar")
        layout_resumo.addWidget(self.progresso_geral)
        
        layout.addWidget(group_resumo)
        
        tabela_group = QGroupBox("Detalhamento por Dia")
        tabela_group.setObjectName("tableGroup")
        layout_tabela = QVBoxLayout(tabela_group)
        
        self.tabela = QTableWidget()
        self.tabela.setObjectName("historyTable")
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
        
        self.btn_voltar = QPushButton("Voltar")
        self.btn_voltar.setObjectName("cancelButton")
        self.btn_voltar.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout_botoes.addWidget(self.btn_voltar)
        layout_botoes.addStretch()
        
        layout.addLayout(layout_botoes)

    def setup_styles(self):
        style_sheet = """
            /* Estilo geral da janela */
            QMainWindow {
                background-color: #2B2D31;
                font-family: Poppins, sans-serif;
                color: #ECECEC;
            }
            
            QWidget {
                background-color: #2B2D31;
                color: #ECECEC;
            }

            /* Título principal */
            #mainTitle {
                font-size: 20px;
                font-weight: 600;
                color: #A0C4FF;
                padding: 15px;
                background-color: #383B42;
                border-radius: 8px;
                border: 1px solid #474A51;
                margin-bottom: 10px;
            }

            /* Grupos */
            QGroupBox {
                font-size: 14px;
                font-weight: 600;
                color: #ECECEC;
                border: 2px solid #474A51;
                border-radius: 8px;
                padding: 10px;
                margin-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background-color: #2B2D31;
            }

            /* Labels dos campos */
            #fieldLabel {
                font-size: 13px;
                font-weight: 500;
                color: #ECECEC;
                padding: 5px;
            }

            /* Campos de data */
            #dateInput {
                background-color: #383B42;
                border: 1px solid #474A51;
                border-radius: 6px;
                padding: 8px 10px;
                font-size: 13px;
                color: #ECECEC;
                min-height: 20px;
                min-width: 120px;
            }
            
            #dateInput:focus {
                border-color: #A0C4FF;
                outline: none;
            }
            
            #dateInput::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #474A51;
                background-color: #474A51;
                border-radius: 0 6px 6px 0;
            }
            
            #dateInput::down-arrow {
                width: 10px;
                height: 10px;
            }
            
            /* Calendário popup */
            QCalendarWidget {
                background-color: #383B42;
                color: #ECECEC;
                border: 1px solid #474A51;
                border-radius: 8px;
            }
            
            QCalendarWidget QWidget {
                background-color: #383B42;
                color: #ECECEC;
            }
            
            QCalendarWidget QAbstractItemView {
                background-color: #383B42;
                color: #ECECEC;
                selection-background-color: #A0C4FF;
                selection-color: #0F141A;
                outline: 0;
                gridline-color: #474A51;
            }
            
            QCalendarWidget QToolButton {
                color: #ECECEC;
                background-color: transparent;
                border: none;
                padding: 5px;
            }
            
            QCalendarWidget QToolButton:hover {
                background-color: #474A51;
                border-radius: 4px;
            }
            
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #474A51;
                border-bottom: 1px solid #5A5E67;
            }

            /* Label de resumo */
            #summaryLabel {
                font-size: 13px;
                color: #ECECEC;
                line-height: 1.5;
                background-color: #383B42;
                padding: 15px;
                border-radius: 6px;
                border-left: 4px solid #A0C4FF;
            }

            /* Barra de progresso principal */
            #mainProgressBar {
                border: 1px solid #474A51;
                border-radius: 6px;
                background-color: #383B42;
                text-align: center;
                color: #ECECEC;
                font-weight: 500;
                height: 25px;
            }
            
            #mainProgressBar::chunk {
                background-color: #A0C4FF;
                border-radius: 5px;
            }

            /* Tabela */
            #historyTable {
                background-color: #383B42;
                border: 1px solid #474A51;
                border-radius: 8px;
                selection-background-color: #5A6B7D;
                selection-color: #ECECEC;
                gridline-color: #474A51;
                color: #ECECEC;
            }
            
            #historyTable::item {
                background-color: #383B42;
                border: none;
                padding: 8px;
            }
            
            #historyTable::item:selected {
                background-color: #5A6B7D;
                color: #ECECEC;
            }
            
            #historyTable::item:hover {
                background-color: #474A51;
            }
            
            QHeaderView::section {
                background-color: #474A51;
                color: #ECECEC;
                padding: 10px;
                border: 1px solid #5A5E67;
                font-weight: 600;
                font-size: 12px;
            }
            
            QHeaderView::section:hover {
                background-color: #5A5E67;
            }
            
            /* Corrigir quadrado branco */
            QTableWidget::item:first-child {
                background-color: #383B42;
            }
            
            QTableCornerButton::section {
                background-color: #474A51;
                border: 1px solid #5A5E67;
            }

            /* Scroll Bars */
            QScrollBar:vertical {
                background-color: #474A51;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #A0C4FF;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #90B9FF;
            }
            
            QScrollBar:horizontal {
                background-color: #474A51;
                height: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:horizontal {
                background-color: #A0C4FF;
                border-radius: 6px;
                min-width: 20px;
            }

            /* Botões */
            QPushButton {
                background-color: #A0C4FF;
                color: #0F141A;
                font-size: 13px;
                font-weight: 500;
                border: none;
                padding: 10px 15px;
                border-radius: 8px;
                min-height: 20px;
                min-width: 80px;
            }
            
            QPushButton:hover {
                background-color: #90B9FF;
            }
            
            QPushButton:pressed {
                background-color: #7FAEFF;
            }

            /* Botão de Confirmação */
            #confirmButton {
                background-color: #A0C4FF;
                color: #0F141A;
                font-weight: bold;
            }
            
            #confirmButton:hover {
                background-color: #90B9FF;
            }
            
            #confirmButton:pressed {
                background-color: #7FAEFF;
            }

            /* Botão Neutro */
            #neutralButton {
                background-color: #CDB4DB;
                color: #1A101C;
            }
            
            #neutralButton:hover {
                background-color: #C4A7D6;
            }
            
            #neutralButton:pressed {
                background-color: #BA9BD0;
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
        self.btn_filtrar.clicked.connect(self.filtrar_periodo)
        self.btn_mes_atual.clicked.connect(self.carregar_historico_mes_atual)
        self.btn_voltar.clicked.connect(self.close)
    
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
                    chunk_color = "#4CAF50"  
                elif progresso >= 70:
                    chunk_color = "#A0C4FF"  
                elif progresso >= 40:
                    chunk_color = "#F6E58D"  
                else:
                    chunk_color = "#E57373"  
                
                widget_progresso.setStyleSheet(f"""
                    QProgressBar {{
                        border: 1px solid #474A51;
                        border-radius: 4px;
                        background-color: #383B42;
                        text-align: center;
                        color: #ECECEC;
                        font-size: 11px;
                        font-weight: 500;
                        height: 18px;
                    }}
                    QProgressBar::chunk {{
                        background-color: {chunk_color};
                        border-radius: 3px;
                    }}
                """)
                
                self.tabela.setCellWidget(row, 3, widget_progresso)
                
                if progresso == 100:
                    status = "✅ Completo"
                    cor = QColor("#4CAF50")
                elif progresso >= 70:
                    status = "🔄 Parcial"
                    cor = QColor("#A0C4FF")
                elif progresso >= 40:
                    status = "⚠️ Baixo"
                    cor = QColor("#F6E58D")
                else:
                    status = "❌ Incompleto"
                    cor = QColor("#E57373")
                
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
        
        if stats['taxa_conclusao'] >= 90:
            chunk_color = "#4CAF50"  
        elif stats['taxa_conclusao'] >= 70:
            chunk_color = "#A0C4FF"  
        elif stats['taxa_conclusao'] >= 50:
            chunk_color = "#F6E58D"  
        else:
            chunk_color = "#E57373" 
        
        self.progresso_geral.setStyleSheet(f"""
            #mainProgressBar {{
                border: 1px solid #474A51;
                border-radius: 6px;
                background-color: #383B42;
                text-align: center;
                color: #0F141A;
                font-weight: 600;
                height: 25px;
            }}
            #mainProgressBar::chunk {{
                background-color: {chunk_color};
                border-radius: 5px;
            }}
        """)
    

