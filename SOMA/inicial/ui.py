from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy
from PySide6.QtCore import Qt
from SOMA.inicial import controller

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setup_ui()
        self.setup_styles()
        self.conectar_signals()

        # Referência para a próxima janela
        self.agenda_window = None

    def setup_ui(self):
        self.setWindowTitle("Assistente Pessoal")
        self.resize(380, 450)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30) 
        main_layout.setSpacing(20)

        # Widgets 
        
        self.title = QLabel("S.O.M.A")
        self.title.setObjectName("mainTitle") # ID para o QSS
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.subtitle = QLabel("O que você gostaria de fazer hoje?")
        self.subtitle.setObjectName("subTitle")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_agenda = QPushButton("Ver Agenda")
        self.btn_agenda.setObjectName("agendaButton")
        
        self.btn_gerenciar = QPushButton("Gerenciar Atividades")
        self.btn_gerenciar.setObjectName("managerButton")
        
        self.btn_exit = QPushButton("Sair")
        self.btn_exit.setObjectName("exitButton")

        # Usar QSizePolicy para  os botões expandirem horizontalmente
        self.btn_agenda.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_gerenciar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_exit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Layout 
        
        main_layout.addStretch(1) 
        main_layout.addWidget(self.title)
        main_layout.addWidget(self.subtitle)
        main_layout.addSpacing(20) 
        
        main_layout.addWidget(self.btn_agenda)
        main_layout.addWidget(self.btn_gerenciar)
        
        main_layout.addStretch(2) 
        main_layout.addWidget(self.btn_exit)

    def setup_styles(self):
        style_sheet = """
            /* Estilo geral da janela e fonte padrão */
            QMainWindow {
                background-color: #2B2D31;
                font-family: Poppins, sans-serif;
            }

            /* Estilo do Título Principal */
            #mainTitle {
                font-size: 26px;
                font-weight: 600;
                color: #ECECEC;
            }
            
            /* Estilo do Subtítulo */
            #subTitle {
                font-size: 14px;
                color: #B9BBBE;
            }
            
            /* Estilo geral para botões de ação */
            QPushButton {
                color: #0F141A;
                font-size: 14px;
                font-weight: 500;
                border: none;
                padding: 12px;
                border-radius: 10px;
                background-color: #A0C4FF;
            }
            
            QPushButton:hover {
                background-color: #90B9FF;
            }
            
            QPushButton:pressed {
                background-color: #7FAEFF;
            }
            
            /* Botão Agenda (primário) - Azul bebê pastel */
            #agendaButton {
                background-color: #A0C4FF;
                color: #0F141A;
            }
            
            #agendaButton:hover {
                background-color: #90B9FF;
            }
            
            #agendaButton:pressed {
                background-color: #7FAEFF;
            }
            
            /* Botão Gerenciar (secundário) - Lavanda pastel */
            #managerButton {
                background-color: #CDB4DB;
                color: #1A101C;
            }
            
            #managerButton:hover {
                background-color: #C4A7D6;
            }
            
            #managerButton:pressed {
                background-color: #BA9BD0;
            }
            
            /* Estilo específico para o botão de sair */
            #exitButton {
                background-color: transparent;
                color: #B9BBBE;
                border: 1px solid #474A51;
            }
            
            #exitButton:hover {
                background-color: #3A3D44;
                color: #ECECEC;
                border-color: #5A5E67;
            }
            
            #exitButton:pressed {
                background-color: #33363C;
            }
        """
        self.setStyleSheet(style_sheet)

    def conectar_signals(self):
        self.btn_agenda.clicked.connect(lambda: controller.handle_view_agenda(self))
        self.btn_gerenciar.clicked.connect(lambda: controller.handle_gerenciar_atividade(self))
        self.btn_exit.clicked.connect(self.close)