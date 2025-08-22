from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar, QCheckBox, QCalendarWidget, QGroupBox, QScrollArea, QFrame, QMessageBox, QSizePolicy
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
from .atividades_controller import AtividadesController
from SOMA.agenda.calendario_customizado import CalendarioCustomizado

class AtividadesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = AtividadesController()
        self.data_selecionada = QDate.currentDate()
        
        self.setup_ui()
        self.setup_styles()
        self.conectar_signals()
        self.atualizar_interface()

    def setup_ui(self):
        self.setWindowTitle("Gerenciar Atividades do Dia")
        self.setGeometry(200, 200, 900, 700)
        self.setMinimumSize(800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        panel_esquerdo = QVBoxLayout()
        panel_esquerdo.setSpacing(15)
        
        group_calendario = QGroupBox("Selecionar Data")
        group_calendario.setObjectName("calendarGroup")
        layout_calendario = QVBoxLayout(group_calendario)
        
        self.calendario = CalendarioCustomizado()
        self.calendario.setObjectName("mainCalendar")
        self.calendario.setSelectedDate(self.data_selecionada)
        self.calendario.setVerticalHeaderFormat(self.calendario.VerticalHeaderFormat.NoVerticalHeader)
        layout_calendario.addWidget(self.calendario)
        
        panel_esquerdo.addWidget(group_calendario)
        
        group_progresso = QGroupBox("Progresso do Dia")
        group_progresso.setObjectName("progressGroup")
        layout_progresso = QVBoxLayout(group_progresso)
        layout_progresso.setSpacing(10)
        
        self.label_data = QLabel()
        self.label_data.setObjectName("selectedDateLabel")
        self.label_data.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_progresso.addWidget(self.label_data)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("mainProgressBar")
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        layout_progresso.addWidget(self.progress_bar)
        
        self.label_progresso = QLabel()
        self.label_progresso.setObjectName("progressLabel")
        self.label_progresso.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_progresso.addWidget(self.label_progresso)
        
        panel_esquerdo.addWidget(group_progresso)
        
        group_estatisticas = QGroupBox("Estatísticas:")
        group_estatisticas.setObjectName("statsGroup")
        layout_estatisticas = QVBoxLayout(group_estatisticas)
        
        self.label_stats = QLabel()
        self.label_stats.setObjectName("statsLabel")
        self.label_stats.setWordWrap(True)
        layout_estatisticas.addWidget(self.label_stats)
        
        panel_esquerdo.addWidget(group_estatisticas)
        
        bottom_buttons = QHBoxLayout()
        bottom_buttons.setSpacing(10)

        self.btn_voltar = QPushButton("Voltar ao Menu Principal")
        self.btn_voltar.setObjectName("cancelButton")
        
        self.btn_historico = QPushButton("Ver Histórico")
        self.btn_historico.setObjectName("neutralButton")
        
        for btn in [self.btn_voltar, self.btn_historico]:
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        bottom_buttons.addWidget(self.btn_voltar)
        bottom_buttons.addWidget(self.btn_historico)
        
        panel_esquerdo.addLayout(bottom_buttons)
        
        panel_direito = QVBoxLayout()
        panel_direito.setSpacing(15)
        
        atividades_group = QGroupBox("Atividades do Dia")
        atividades_group.setObjectName("activitiesGroup")
        layout_atividades = QVBoxLayout(atividades_group)
        layout_atividades.setSpacing(10)
        
        scroll_area = QScrollArea()
        scroll_area.setObjectName("activitiesScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        self.atividades_widget = QWidget()
        self.layout_atividades = QVBoxLayout(self.atividades_widget)
        self.layout_atividades.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_atividades.setSpacing(5)
        
        scroll_area.setWidget(self.atividades_widget)
        layout_atividades.addWidget(scroll_area)
        
        self.btn_marcar_todas = QPushButton("Marcar Todas como Concluídas")
        self.btn_marcar_todas.setObjectName("confirmButton")
        self.btn_marcar_todas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout_atividades.addWidget(self.btn_marcar_todas)
        
        panel_direito.addWidget(atividades_group)
        
        eventos_importantes_group = QGroupBox("Eventos Importantes - Próximos 30 Dias")
        eventos_importantes_group.setObjectName("importantEventsGroup")
        layout_eventos = QVBoxLayout(eventos_importantes_group)
        
        scroll_area_eventos = QScrollArea()
        scroll_area_eventos.setObjectName("eventsScrollArea")
        scroll_area_eventos.setWidgetResizable(True)
        scroll_area_eventos.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area_eventos.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area_eventos.setMaximumHeight(200)
        
        self.eventos_widget = QWidget()
        self.layout_eventos = QVBoxLayout(self.eventos_widget)
        self.layout_eventos.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_eventos.setSpacing(5)
        
        scroll_area_eventos.setWidget(self.eventos_widget)
        layout_eventos.addWidget(scroll_area_eventos)
        
        panel_direito.addWidget(eventos_importantes_group)
        
        main_layout.addLayout(panel_esquerdo, 1)
        main_layout.addLayout(panel_direito, 2)

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

            /* Calendário */
            #mainCalendar {
                background-color: #383B42;
                border: none;
                border-radius: 8px;
                min-height: 200px;
                /* Permitir que o calendário cresça */
            }
            
            /* Forçar fundo escuro em todos os elementos do calendário */
            #mainCalendar * {
                background-color: #383B42;
            }
            
            /* Visão dos dias do mês */
            #mainCalendar QAbstractItemView {
                background-color: #383B42;
                color: #ECECEC;
                selection-background-color: #5A6B7D; 
                selection-color: #ECECEC; /* Texto claro na seleção */
                outline: 0; /* Remove a borda pontilhada ao focar */
                gridline-color: #474A51; /* Linhas da grade mais suaves */
                /* Permitir que as células se expandam proporcionalmente */
                min-height: 25px;
            }
            
            /* Barra de navegação (onde fica Mês/Ano) */
            #qt_calendar_navigationbar {
                background-color: #383B42;
                border-bottom: 1px solid #474A51;
            }

            /* Botões de navegação (mês anterior/próximo e seleção de mês/ano) */
            #mainCalendar QToolButton {
                color: #ECECEC;
                background-color: transparent;
                border: none;
                padding: 10px;
                font-size: 14px;
            }
            
            #mainCalendar QToolButton:hover {
                background-color: #474A51;
                border-radius: 4px;
            }
            
            #mainCalendar QToolButton:pressed {
                background-color: #33363C;
            }

            /* Removendo os ícones padrão (setas verdes) */
            #qt_calendar_prevmonth, #qt_calendar_nextmonth {
                qproperty-icon: none; 
            }
            
            /* Adicionando nossos próprios ícones de seta via CSS */
            #qt_calendar_prevmonth {
                font-size: 16px;
            }
            
            #qt_calendar_nextmonth {
                font-size: 16px;
            }
            
            /* Estilizando os dias da semana (Seg, Ter, Qua) */
            QCalendarWidget QWidget {
                alternate-background-color: #474A51;
            }
            
            #qt_calendar_weekdaybar {
                background-color: #474A51; /* Fundo mais escuro */
                color: #ECECEC; /* Texto claro em vez de branco feio */
                font-size: 12px;
                font-weight: 500;
                border-bottom: 1px solid #5A5E67;
            }

            /* Células dos dias de outros meses (dias acinzentados) */
            #mainCalendar QAbstractItemView:disabled {
                color: #6B7280; /* Cinza mais suave */
            }

            /* Labels */
            #selectedDateLabel {
                font-size: 16px;
                font-weight: 600;
                color: #A0C4FF;
                background-color: #383B42;
                padding: 10px;
                border-radius: 6px;
                border: 1px solid #474A51;
            }
            
            #progressLabel {
                font-size: 13px;
                color: #ECECEC;
                font-weight: 500;
            }
            
            #statsLabel {
                font-size: 12px;
                color: #B9BBBE;
                line-height: 1.4;
                background-color: #383B42;
                padding: 12px;
                border-radius: 6px;
                border-left: 3px solid #CDB4DB;
            }

            /* Barra de progresso */
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
                background-color: #4CAF50;
                border-radius: 5px;
            }

            /* Scroll Areas */
            #activitiesScrollArea, #eventsScrollArea {
                border: 1px solid #474A51;
                border-radius: 6px;
                background-color: #383B42;
            }
            
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
                color: white;
                font-weight: bold;
                padding: 12px 20px;
                min-height: 25px;
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

            /* Frames das atividades */
            QFrame {
                background-color: #383B42;
                border: 1px solid #474A51;
                border-radius: 6px;
                margin: 2px;
                padding: 8px;
            }
            
            QFrame:hover {
                border-color: #A0C4FF;
            }

            /* Checkboxes */
            QCheckBox {
                color: #ECECEC;
                font-size: 13px;
                spacing: 8px;
                background: transparent;
            }
            
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 3px;
                border: 2px solid #474A51;
                background-color: #383B42;
            }
            
            QCheckBox::indicator:unchecked {
                background-color: #383B42;
                border-color: #474A51;
            }
            
            QCheckBox::indicator:checked {
                background-color: #A0C4FF;
                border-color: #A0C4FF;
                image: none;
            }
            
            QCheckBox::indicator:hover {
                border-color: #90B9FF;
            }
            
            QCheckBox::indicator:checked:hover {
                background-color: #90B9FF;
                border-color: #90B9FF;
            }
        """
        self.setStyleSheet(style_sheet)

    def conectar_signals(self):
        self.calendario.clicked.connect(self.data_selecionada_mudou)
        self.calendario.currentPageChanged.connect(self.atualizar_grifados)
        self.btn_marcar_todas.clicked.connect(self.marcar_todas_concluidas)
        self.btn_voltar.clicked.connect(self.voltar_menu_principal)
        self.btn_historico.clicked.connect(self.abrir_historico)

    def carregar_tarefas_json(self):
        import json
        import os
        from collections import defaultdict
        
        caminho_arquivo = "SOMA/minhas_datas.json"
        dados = {"tarefas": []}
        
        try:
            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    
                    if "tarefas" not in dados:
                        dados["tarefas"] = []
                        
        except Exception as e:
            print(f"Erro ao carregar tarefas: {e}")
            
        return dados["tarefas"]

    def atualizar_grifados(self):
        from collections import defaultdict
        
        tarefas = self.carregar_tarefas_json()
        
        tarefas_por_data = defaultdict(set)
        tarefas_importantes_por_data = defaultdict(bool)
        
        mes_atual = self.calendario.monthShown()
        ano_atual = self.calendario.yearShown()
        
        for tarefa in tarefas:
            try:
                data_tarefa = QDate.fromString(tarefa["date"], "dd-MM-yyyy")
                
                if tarefa["type"] == "single":
                    data_original = data_tarefa
                    if data_original.month() == mes_atual and data_original.year() == ano_atual:
                        tarefas_por_data[data_original].add("single")
                        
                        if tarefa.get("importante", False):
                            tarefas_importantes_por_data[data_original] = True
                            
                elif tarefa["type"] == "daily":
                    primeiro_dia_mes = QDate(ano_atual, mes_atual, 1)
                    ultimo_dia_mes = QDate(ano_atual, mes_atual, primeiro_dia_mes.daysInMonth())
                    
                    data_atual = max(data_tarefa, primeiro_dia_mes)
                    while data_atual <= ultimo_dia_mes:
                        tarefas_por_data[data_atual].add("daily")
                        data_atual = data_atual.addDays(1)
                        
                elif tarefa["type"] == "weekly":
                    primeiro_dia_mes = QDate(ano_atual, mes_atual, 1)
                    ultimo_dia_mes = QDate(ano_atual, mes_atual, primeiro_dia_mes.daysInMonth())
                    
                    data_atual = data_tarefa
                    while data_atual < primeiro_dia_mes:
                        data_atual = data_atual.addDays(7)
                    
                    while data_atual <= ultimo_dia_mes:
                        tarefas_por_data[data_atual].add("weekly")
                        data_atual = data_atual.addDays(7)
                        
            except Exception as e:
                print(f"Erro ao processar tarefa: {e}")
                
        self.calendario.atualizar_tarefas_data(tarefas_por_data, tarefas_importantes_por_data)
        
    def data_selecionada_mudou(self, data):
        self.data_selecionada = data
        self.atualizar_interface()
    
    def atualizar_interface(self):
        self.atualizar_label_data()
        self.atualizar_progresso()
        self.atualizar_lista_atividades()
        self.atualizar_eventos_importantes()
        self.atualizar_estatisticas()
        self.atualizar_grifados()
    
    def atualizar_label_data(self):
        dias_semana = {
            1: "Segunda-feira",
            2: "Terça-feira", 
            3: "Quarta-feira",
            4: "Quinta-feira",
            5: "Sexta-feira",
            6: "Sábado",
            7: "Domingo"
        }
        
        dia_semana_pt = dias_semana.get(self.data_selecionada.dayOfWeek(), "")
        data_formatada = f"{dia_semana_pt}, {self.data_selecionada.toString('dd/MM/yyyy')}"
        self.label_data.setText(data_formatada)
    
    def atualizar_progresso(self):
        concluidas, total, progresso = self.controller.obter_progresso_do_dia(self.data_selecionada)
        
        self.progress_bar.setValue(int(progresso))
        self.label_progresso.setText(f"{concluidas} de {total} tarefas concluídas ({progresso:.1f}%)")
        
        if progresso == 100:
            chunk_color = "#4CAF50"
        elif progresso >= 70:
            chunk_color = "#A0C4FF"
        elif progresso >= 40:
            chunk_color = "#F6E58D"
        else:
            chunk_color = "#E57373"
        
        self.progress_bar.setStyleSheet(f"""
            #mainProgressBar {{
                border: 1px solid #474A51;
                border-radius: 6px;
                background-color: #383B42;
                text-align: center;
                color: #ECECEC;
                font-weight: 500;
                height: 25px;
            }}
            #mainProgressBar::chunk {{
                background-color: {chunk_color};
                border-radius: 5px;
            }}
        """)
    
    def atualizar_lista_atividades(self):
        for i in reversed(range(self.layout_atividades.count())):
            child = self.layout_atividades.itemAt(i)
            if child and child.widget():
                child.widget().setParent(None)
        
        tarefas = self.controller.obter_tarefas_do_dia(self.data_selecionada)
        
        if not tarefas:
            label_vazio = QLabel("Nenhuma tarefa programada para este dia.")
            label_vazio.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_vazio.setStyleSheet("""
                color: #B9BBBE; 
                font-style: italic; 
                padding: 20px;
                font-size: 14px;
                background-color: #383B42;
                border-radius: 6px;
                border: 1px dashed #474A51;
            """)
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
            label_vazio.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_vazio.setStyleSheet("""
                color: #B9BBBE; 
                font-style: italic; 
                padding: 15px;
                font-size: 12px;
                background-color: #383B42;
                border-radius: 6px;
                border: 1px dashed #474A51;
            """)
            self.layout_eventos.addWidget(label_vazio)
            return
        
        for evento in eventos:
            self.criar_item_evento_importante(evento)
    
    def criar_item_evento_importante(self, evento):
        frame = QFrame()
        frame.setObjectName("importantEventFrame")
        frame.setStyleSheet("""
            #importantEventFrame { 
                border: 2px solid #F6E58D; 
                border-radius: 8px; 
                margin: 3px; 
                padding: 8px; 
                background-color: #4A4628;
            }
            #importantEventFrame:hover {
                border-color: #F6E58D;
                background-color: #52492A;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(5)
        
        linha_principal = QHBoxLayout()
        
        label_desc = QLabel(f"{evento['descricao']}")
        label_desc.setStyleSheet("font-weight: bold; color: #F6E58D; font-size: 12px;")
        label_desc.setWordWrap(True)
        linha_principal.addWidget(label_desc, 1)
        
        label_data = QLabel(evento['data_str'])
        label_data.setStyleSheet("color: #ECECEC; font-weight: bold; font-size: 11px;")
        linha_principal.addWidget(label_data)
        
        layout.addLayout(linha_principal)
        
        if evento['dias_restantes'] == 0:
            texto_dias = "HOJE!!!"
            cor_dias = "#F6E58D"
        elif evento['dias_restantes'] == 1:
            texto_dias = "Amanhã!"
            cor_dias = "#F6E58D"
        else:
            texto_dias = f"Em {evento['dias_restantes']} dias"
            cor_dias = "#B9BBBE"
        
        label_dias = QLabel(texto_dias)
        label_dias.setStyleSheet(f"color: {cor_dias}; font-size: 10px; font-style: italic; font-weight: 500;")
        layout.addWidget(label_dias)
        
        self.layout_eventos.addWidget(frame)
    
    def criar_item_atividade(self, tarefa):
        frame = QFrame()
        frame.setObjectName("activityFrame")
        
        layout = QHBoxLayout(frame)
        layout.setSpacing(10)
        
        checkbox = QCheckBox()
        checkbox.setChecked(self.controller.tarefa_esta_concluida(self.data_selecionada, tarefa["description"]))
        
        def on_checkbox_toggled(checked, descricao=tarefa["description"], label=None):
            if label:
                if checked:
                    label.setStyleSheet("text-decoration: line-through; color: #6B7280; font-style: italic;")
                else:
                    label.setStyleSheet("color: #ECECEC;")
            self.marcar_tarefa(descricao, checked)
        
        label_desc = QLabel(tarefa["description"])
        label_desc.setWordWrap(True)
        label_desc.setStyleSheet("color: #ECECEC; font-size: 13px;")
        
        if checkbox.isChecked():
            label_desc.setStyleSheet("text-decoration: line-through; color: #6B7280; font-style: italic; font-size: 13px;")
        
        checkbox.toggled.connect(lambda checked, desc=tarefa["description"], lbl=label_desc: 
                               on_checkbox_toggled(checked, desc, lbl))
        layout.addWidget(checkbox)
        
        layout.addWidget(label_desc, 1)
        
        tipo_cores = {
            "daily": "#B5EAD7",
            "weekly": "#CDB4DB", 
            "single": "#A0C4FF"
        }
        
        cor_tipo = tipo_cores.get(tarefa['type'], "#B9BBBE")
        
        label_tipo = QLabel(f"[{tarefa['type']}]")
        label_tipo.setStyleSheet(f"color: {cor_tipo}; font-size: 10px; font-weight: 500;")
        layout.addWidget(label_tipo)
        
        self.layout_atividades.addWidget(frame)
    
    def marcar_tarefa(self, descricao, concluida):
        self.controller.marcar_tarefa_concluida(self.data_selecionada, descricao, concluida)
        
        self.atualizar_progresso()
        self.atualizar_eventos_importantes()  
        self.atualizar_estatisticas()
        self.atualizar_grifados()
        
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
    
    def calcular_streak_atual(self):
        try:
            streak = 0
            data_atual = QDate.currentDate()
            max_dias = 30  
            
            for _ in range(max_dias):
                try:
                    tarefas_do_dia = self.controller.obter_tarefas_do_dia(data_atual)
                    
                    # Se não há tarefas no dia, pular para o dia anterior
                    if not tarefas_do_dia:
                        data_atual = data_atual.addDays(-1)
                        continue
                    
                    # Verificar se todas as tarefas do dia estão concluídas
                    concluidas, total, progresso = self.controller.obter_progresso_do_dia(data_atual)
                    
                    if total > 0 and progresso == 100.0:  # Dia perfeito
                        streak += 1
                    else:
                        break  # Quebrou a streak
                        
                    data_atual = data_atual.addDays(-1)
                    
                except Exception:
                    break  # Se der erro, parar o loop
            
            return streak
            
        except Exception:
            return 0  # Retornar 0 se der qualquer erro

    def atualizar_estatisticas(self):
        try:
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
            
            streak_atual = self.calcular_streak_atual()
            
            texto_stats = f"""Estatísticas da Semana:
• Taxa de conclusão: {stats['taxa_conclusao']:.1f}%
• Total de tarefas concluídas: {stats['total_tarefas_concluidas']}

Streak Atual:
• Dias perfeitos consecutivos: {streak_atual} dias"""
            
            self.label_stats.setText(texto_stats)
            
        except Exception as e:
            self.label_stats.setText("Estatísticas indisponíveis no momento.")
    
    def abrir_historico(self):
        from .historico_ui import HistoricoAtividadesWindow
        self.historico_window = HistoricoAtividadesWindow()
        self.historico_window.show()
    
    def voltar_menu_principal(self):
        from SOMA.inicial.ui import MainWindow
        
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
