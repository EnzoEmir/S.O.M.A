from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt
from SOMA.agenda import agenda_controller
from SOMA.agenda.calendario_customizado import CalendarioCustomizado

class AgendaWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setup_ui()
        self.setup_styles()
        
        self.controller = agenda_controller.Controller(self)
        self.conectar_signals()

        self.main = None

    def setup_ui(self):
        self.setWindowTitle("Agenda de Atividades")
        self.resize(420, 550)
        self.setMinimumSize(380, 500)  # Tamanho mínimo para evitar quebras

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        self.calendario = CalendarioCustomizado()
        self.calendario.setObjectName("mainCalendar")
        
        # Tornar o calendário responsivo
        self.calendario.setMinimumSize(300, 200)
        
        # Remove as semanas 
        self.calendario.setVerticalHeaderFormat(self.calendario.VerticalHeaderFormat.NoVerticalHeader)

        legenda_container = QWidget()
        legenda_layout = QHBoxLayout(legenda_container)
        legenda_layout.setContentsMargins(0, 5, 0, 5)

        legenda_titulo = QLabel("Legendas:")
        legenda_titulo.setObjectName("legendTitle")
        
        self.legenda_diario = QLabel("■ Diário")
        self.legenda_diario.setObjectName("legendaDiario")
        
        self.legenda_semanal = QLabel("■ Semanal")
        self.legenda_semanal.setObjectName("legendaSemanal")
        
        self.legenda_unico = QLabel("■ Único")
        self.legenda_unico.setObjectName("legendaUnico")
        
        self.legenda_importante = QLabel("■ Importante")
        self.legenda_importante.setObjectName("legendaImportante")
        
        legenda_layout.addWidget(legenda_titulo)
        legenda_layout.addSpacing(10)
        legenda_layout.addWidget(self.legenda_diario)
        legenda_layout.addWidget(self.legenda_semanal)
        legenda_layout.addWidget(self.legenda_unico)
        legenda_layout.addWidget(self.legenda_importante)
        legenda_layout.addStretch()

        botoes_filtro_layout = QHBoxLayout()
        botoes_filtro_layout.setSpacing(10)
        
        self.btn_todos = QPushButton("Ver Todos")
        self.btn_diarios = QPushButton("Diários")
        self.btn_semanais = QPushButton("Semanais")
        self.btn_unicos = QPushButton("Evento Único")
        
        # Botões se expandem igualmente
        for btn in [self.btn_todos, self.btn_diarios, self.btn_semanais, self.btn_unicos]:
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        botoes_filtro_layout.addWidget(self.btn_todos)
        botoes_filtro_layout.addWidget(self.btn_diarios)
        botoes_filtro_layout.addWidget(self.btn_semanais)
        botoes_filtro_layout.addWidget(self.btn_unicos)

        self.btn_ver_tarefas = QPushButton("Ver Tarefas do Dia")
        self.btn_adicionar = QPushButton("Adicionar Tarefa")
        self.btn_voltar = QPushButton("Voltar")
        
        self.btn_adicionar.setObjectName("confirmButton")
        self.btn_voltar.setObjectName("cancelButton")

        for btn in [self.btn_ver_tarefas, self.btn_adicionar, self.btn_voltar]:
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        main_layout.addWidget(self.calendario, 1) 
        main_layout.addWidget(legenda_container)
        main_layout.addLayout(botoes_filtro_layout)
        main_layout.addWidget(self.btn_ver_tarefas)
        main_layout.addStretch(0)  
        main_layout.addWidget(self.btn_adicionar)
        main_layout.addWidget(self.btn_voltar)

    def setup_styles(self):
        style_sheet = """
            /* Estilo geral da janela e fonte */
            QWidget {
                background-color: #2B2D31;
                font-family: Poppins, sans-serif;
                color: #ECECEC; 
            }

            #mainCalendar {
                background-color: #383B42;
                border: none;
                border-radius: 8px;
                min-height: 200px;
                /* Permitir que o calendário cresça */
            }
            
            /* Forçar fundo escuro em  nos elementos do calendário */
            #mainCalendar * {
                background-color: #383B42;
            }
            
            /* Visão dos dias do mês */
            #mainCalendar QAbstractItemView {
                background-color: #383B42;
                color: #ECECEC;
                selection-background-color: #5A6B7D; /* AZUL MUITO MAIS SUAVE */
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
            #qt_calendar_prevmonth::after {
                content: '◄';
            }
            #qt_calendar_nextmonth::before {
                content: '►';
            }
            
            /* Estilizando os dias da semana (Seg, Ter, Qua...) */
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

            /* --- ESTILO DAS LEGENDAS --- */
            #legendTitle { font-weight: 500; }
            #legendaDiario { color: #B5EAD7; font-weight: bold; }
            #legendaSemanal { color: #CDB4DB; font-weight: bold; }
            #legendaUnico { color: #A0C4FF; font-weight: bold; }
            #legendaImportante { color: #F6E58D; font-weight: bold; }
            
            /* --- ESTILO DOS BOTÕES --- */
            /* Botão Neutro/Secundário (Azul Pastel) - Padrão */
            QPushButton {
                background-color: #A0C4FF;
                color: #0F141A;
                font-size: 13px;
                font-weight: 500;
                border: none;
                padding: 10px 15px;
                border-radius: 8px;
                min-height: 20px;
                /* Permitir que os botões se adaptem ao tamanho da janela */
            }
            QPushButton:hover {
                background-color: #90B9FF;
            }
            QPushButton:pressed {
                background-color: #7FAEFF;
            }

            /* Botão de Ação/Confirmar (Verde) */
            #confirmButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 20px;
                min-height: 25px;
            }
            #confirmButton:hover { background-color: #45a049; }
            #confirmButton:pressed { background-color: #3e8e41; }

            /* Botão de Cancelar/Remover (Vermelho Pastel) */
            #cancelButton {
                background-color: #E57373;
                color: white;
                padding: 12px 20px;
                min-height: 25px;
            }
            #cancelButton:hover { background-color: #e56363; }
            #cancelButton:pressed { background-color: #e55353; }
        """
        self.setStyleSheet(style_sheet)

    def conectar_signals(self):
        self.btn_todos.clicked.connect(lambda: self.controller.atualizar_filtro("all"))
        self.btn_diarios.clicked.connect(lambda: self.controller.atualizar_filtro("daily"))
        self.btn_semanais.clicked.connect(lambda: self.controller.atualizar_filtro("weekly"))
        self.btn_unicos.clicked.connect(lambda: self.controller.atualizar_filtro("single"))
        
        self.btn_adicionar.clicked.connect(self.controller.abrir_janela_adicionar)
        self.btn_ver_tarefas.clicked.connect(self.controller.abrir_tarefas_do_dia)
        self.btn_voltar.clicked.connect(lambda: agenda_controller.voltar_main(self))

        # Sinal do calendário
        self.calendario.currentPageChanged.connect(self.controller.atualizar_grifados)