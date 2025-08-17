from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar, QCheckBox, QCalendarWidget, QGroupBox, QScrollArea, QFrame, QMessageBox
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
from .atividades_controller import AtividadesController

class AtividadesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = AtividadesController()
        self.data_selecionada = QDate.currentDate()
        self.setup_ui()
        self.conectar_signals()
        self.atualizar_interface()
    
    def setup_ui(self):
        self.setWindowTitle("Gerenciar Atividades do Dia")
        self.setGeometry(200, 200, 900, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        panel_esquerdo = QVBoxLayout()
        
        group_calendario = QGroupBox("Selecionar Data")
        layout_calendario = QVBoxLayout(group_calendario)
        
        self.calendario = QCalendarWidget()
        self.calendario.setSelectedDate(self.data_selecionada)
        layout_calendario.addWidget(self.calendario)
        
        panel_esquerdo.addWidget(group_calendario)
        
        group_processos = QGroupBox("Progresso do Dia")
        layout_progresso = QVBoxLayout(group_processos)
        
        self.label_data = QLabel()
        self.label_data.setAlignment(Qt.AlignCenter)
        font_data = QFont()
        font_data.setBold(True)
        font_data.setPointSize(12)
        self.label_data.setFont(font_data)
        layout_progresso.addWidget(self.label_data)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        layout_progresso.addWidget(self.progress_bar)
        
        self.label_progresso = QLabel()
        self.label_progresso.setAlignment(Qt.AlignCenter)
        layout_progresso.addWidget(self.label_progresso)
        
        panel_esquerdo.addWidget(group_processos)
        
        group_estatisticas = QGroupBox("Estatísticas da Semana")
        layout_estatisticas = QVBoxLayout(group_estatisticas)
        
        self.label_stats = QLabel()
        self.label_stats.setWordWrap(True)
        layout_estatisticas.addWidget(self.label_stats)
        
        panel_esquerdo.addWidget(group_estatisticas)
        
        bottom_buttons = QHBoxLayout()
        
        self.btn_historico = QPushButton("Ver Histórico")
        self.btn_historico.clicked.connect(self.abrir_historico)
        bottom_buttons.addWidget(self.btn_historico)
        
        self.btn_voltar = QPushButton("Voltar ao Menu Principal")
        self.btn_voltar.clicked.connect(self.voltar_menu_principal)
        bottom_buttons.addWidget(self.btn_voltar)
        
        panel_esquerdo.addLayout(bottom_buttons)
        
        panel_direito = QVBoxLayout()
        
        atividades_group = QGroupBox("Atividades do Dia")
        layout_atividades = QVBoxLayout(atividades_group)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.atividades_widget = QWidget()
        self.layout_atividades = QVBoxLayout(self.atividades_widget)
        self.layout_atividades.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(self.atividades_widget)
        layout_atividades.addWidget(scroll_area)
        
        layout_botoes = QHBoxLayout()
        
        self.btn_marcar_todas = QPushButton("Marcar Todas como Concluídas")
        self.btn_marcar_todas.clicked.connect(self.marcar_todas_concluidas)
        layout_botoes.addWidget(self.btn_marcar_todas)
        
        layout_atividades.addLayout(layout_botoes)
        
        panel_direito.addWidget(atividades_group)
        
        eventos_importantes_group = QGroupBox("Eventos Importantes - Próximos 30 Dias")
        layout_eventos = QVBoxLayout(eventos_importantes_group)
        
        scroll_area_eventos = QScrollArea()
        scroll_area_eventos.setWidgetResizable(True)
        scroll_area_eventos.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area_eventos.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area_eventos.setMaximumHeight(200)  
        
        self.eventos_widget = QWidget()
        self.layout_eventos = QVBoxLayout(self.eventos_widget)
        self.layout_eventos.setAlignment(Qt.AlignTop)
        
        scroll_area_eventos.setWidget(self.eventos_widget)
        layout_eventos.addWidget(scroll_area_eventos)
        
        panel_direito.addWidget(eventos_importantes_group)
        
        main_layout.addLayout(panel_esquerdo, 1)
        main_layout.addLayout(panel_direito, 2)
    
    def conectar_signals(self):
        self.calendario.clicked.connect(self.data_selecionada_mudou)
        
    def data_selecionada_mudou(self, data):
        self.data_selecionada = data
        self.atualizar_interface()
    
    def atualizar_interface(self):
        self.atualizar_label_data()
        self.atualizar_progresso()
        self.atualizar_lista_atividades()
        self.atualizar_eventos_importantes()
        self.atualizar_estatisticas()
    
    def atualizar_label_data(self):
        data_formatada = self.data_selecionada.toString("dddd, dd/MM/yyyy")
        self.label_data.setText(data_formatada)
    
    def atualizar_progresso(self):
        concluidas, total, progresso = self.controller.obter_progresso_do_dia(self.data_selecionada)
        
        self.progress_bar.setValue(int(progresso))
        self.label_progresso.setText(f"{concluidas} de {total} tarefas concluídas ({progresso:.1f}%)")
        
        if progresso == 100:
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #4CAF50; }")
        elif progresso >= 50:
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #FF9800; }")
        else:
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #F44336; }")
    
    def atualizar_lista_atividades(self):
        for i in reversed(range(self.layout_atividades.count())):
            child = self.layout_atividades.itemAt(i)
            if child and child.widget():
                child.widget().setParent(None)
        
        tarefas = self.controller.obter_tarefas_do_dia(self.data_selecionada)
        
        if not tarefas:
            label_vazio = QLabel("Nenhuma tarefa programada para este dia.")
            label_vazio.setAlignment(Qt.AlignCenter)
            label_vazio.setStyleSheet("color: gray; font-style: italic; padding: 20px;")
            self.layout_atividades.addWidget(label_vazio)
            return
        
        for tarefa in tarefas:
            self.criar_item_atividade(tarefa)
    
    def atualizar_eventos_importantes(self):
        for i in reversed(range(self.layout_eventos.count())):
            child = self.layout_eventos.itemAt(i)
            if child and child.widget():
                child.widget().setParent(None)
        
        eventos = self.controller.obter_eventos_importantes_proximos_30_dias()
        
        if not eventos:
            label_vazio = QLabel("Nenhum evento importante nos próximos 30 dias.")
            label_vazio.setAlignment(Qt.AlignCenter)
            label_vazio.setStyleSheet("color: gray; font-style: italic; padding: 10px;")
            self.layout_eventos.addWidget(label_vazio)
            return
        
        for evento in eventos:
            self.criar_item_evento_importante(evento)
    
    def criar_item_evento_importante(self, evento):
        frame = QFrame()
        frame.setFrameStyle(QFrame.Box)
        frame.setStyleSheet("""
            QFrame { 
                border: 2px solid #ff6b6b; 
                border-radius: 8px; 
                margin: 3px; 
                padding: 8px; 
                background-color: #fff5f5;
            }
        """)
        
        layout = QVBoxLayout(frame)
        
        # Linha principal com descrição e data
        linha_principal = QHBoxLayout()
        
        label_desc = QLabel(f"{evento['descricao']}")
        label_desc.setStyleSheet("font-weight: bold; color: #c53030; font-size: 12px;")
        label_desc.setWordWrap(True)
        linha_principal.addWidget(label_desc, 1)
        
        label_data = QLabel(evento['data_str'])
        label_data.setStyleSheet("color: #2d3748; font-weight: bold; font-size: 11px;")
        linha_principal.addWidget(label_data)
        
        layout.addLayout(linha_principal)
        
        if evento['dias_restantes'] == 0:
            texto_dias = "HOJE!!!"
            cor_dias = "#c53030"
        elif evento['dias_restantes'] == 1:
            texto_dias = "Amanhã!"
            cor_dias = "#e53e3e"
        else:
            texto_dias = f"Em {evento['dias_restantes']} dias"
            cor_dias = "#805ad5"
        
        label_dias = QLabel(texto_dias)
        label_dias.setStyleSheet(f"color: {cor_dias}; font-size: 10px; font-style: italic;")
        layout.addWidget(label_dias)
        
        self.layout_eventos.addWidget(frame)
    
    def criar_item_atividade(self, tarefa):
        frame = QFrame()
        frame.setFrameStyle(QFrame.Box)
        frame.setStyleSheet("QFrame { border: 1px solid #ddd; border-radius: 5px; margin: 2px; padding: 5px; }")
        
        layout = QHBoxLayout(frame)
        
        checkbox = QCheckBox()
        checkbox.setChecked(self.controller.tarefa_esta_concluida(self.data_selecionada, tarefa["description"]))
        
        def on_checkbox_toggled(checked, descricao=tarefa["description"], label=None):
            if label:
                if checked:
                    label.setStyleSheet("text-decoration: line-through; color: gray;")
                else:
                    label.setStyleSheet("")
            self.marcar_tarefa(descricao, checked)
        
        label_desc = QLabel(tarefa["description"])
        label_desc.setWordWrap(True)
        
        # Aplicar estilo se concluída
        if checkbox.isChecked():
            label_desc.setStyleSheet("text-decoration: line-through; color: gray;")
        
        checkbox.toggled.connect(lambda checked, desc=tarefa["description"], lbl=label_desc: 
                               on_checkbox_toggled(checked, desc, lbl))
        layout.addWidget(checkbox)
        
        layout.addWidget(label_desc, 1)
        
        label_tipo = QLabel(f"[{tarefa['type']}]")
        label_tipo.setStyleSheet("color: #666; font-size: 10px;")
        layout.addWidget(label_tipo)
        
        self.layout_atividades.addWidget(frame)
    
    def marcar_tarefa(self, descricao, concluida):
        self.controller.marcar_tarefa_concluida(self.data_selecionada, descricao, concluida)
        
        self.atualizar_progresso()
        self.atualizar_eventos_importantes()  
        self.atualizar_estatisticas()
        
        if concluida and self.controller.todas_tarefas_concluidas(self.data_selecionada):
            QMessageBox.information(self, "Parabéns!", 
                                  "Todas as tarefas do dia foram concluídas!")
    
    def marcar_todas_concluidas(self):
        tarefas = self.controller.obter_tarefas_do_dia(self.data_selecionada)
        
        if not tarefas:
            QMessageBox.information(self, "Aviso", 
                                  "Não há tarefas para marcar neste dia.")
            return
        
        for tarefa in tarefas:
            self.controller.marcar_tarefa_concluida(self.data_selecionada, tarefa["description"], True)
        
        self.atualizar_interface()
        
        QMessageBox.information(self, "Sucesso", 
                              f"Todas as {len(tarefas)} tarefas do dia foram marcadas como concluídas!")
    
    def atualizar_estatisticas(self):
        # (domingo a sábado)
        # dayOfWeek() retorna: 1=Segunda, 2=Terça, ..., 7=Domingo
        dia_semana = self.data_selecionada.dayOfWeek()
        
        if dia_semana == 7:  # Se é domingo
            dias_desde_domingo = 0
        else:  # Segunda a sábado
            dias_desde_domingo = dia_semana
        
        inicio_semana = self.data_selecionada.addDays(-dias_desde_domingo)
        fim_semana = inicio_semana.addDays(6)
        
        stats = self.controller.obter_estatisticas_periodo(inicio_semana, fim_semana)
        
        texto_stats = f"""Estatísticas da Semana:
• Taxa de conclusão: {stats['taxa_conclusao']:.1f}%
• Streak de dias perfeitos: {stats['streak_dias_perfeitos']} dias
• Total de tarefas concluídas: {stats['total_tarefas_concluidas']}"""
        
        self.label_stats.setText(texto_stats)
    
    def abrir_historico(self):
        from .historico_ui import HistoricoAtividadesWindow
        self.historico_window = HistoricoAtividadesWindow()
        self.historico_window.show()
    
    def voltar_menu_principal(self):
        from SOMA.inicial.ui import MainWindow
        
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
