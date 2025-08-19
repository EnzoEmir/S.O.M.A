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
        
        self.title = QLabel("Assistente Pessoal")
        self.title.setObjectName("mainTitle") # ID para o QSS
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.subtitle = QLabel("O que você gostaria de fazer hoje?")
        self.subtitle.setObjectName("subTitle")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_agenda = QPushButton("Ver Agenda")
        self.btn_gerenciar = QPushButton("Gerenciar Atividades")
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
        """
        Centraliza todo o estilo (QSS) em um único lugar.
        Esta é a forma mais organizada e fácil de manter o visual da aplicação.
        """
        style_sheet = """
            /* Estilo geral da janela e fonte padrão */
            QMainWindow {
                background-color: #EDE7F6;
                font-family: Poppins, sans-serif; /* Fallback para fonte padrão */
            }

            /* Estilo do Título Principal */
            #mainTitle {
                font-size: 26px;
                font-weight: 600; /* SemiBold */
                color: #424242;
            }
            
            /* Estilo do Subtítulo */
            #subTitle {
                font-size: 14px;
                color: #757575;
            }
            
            /* Estilo geral para botões de ação */
            QPushButton {
                background-color: #7E57C2;
                color: white;
                font-size: 14px;
                font-weight: 500; /* Medium */
                border: none;
                padding: 12px;
                border-radius: 8px;
            }
            
            QPushButton:hover {
                background-color: #9575CD;
            }
            
            QPushButton:pressed {
                background-color: #673AB7;
            }
            
            /* Estilo específico para o botão de sair */
            #exitButton {
                background-color: transparent;
                color: #757575;
                border: 1px solid #C5CAE9;
            }
            
            #exitButton:hover {
                background-color: #C5CAE9;
                color: #424242;
            }
        """
        self.setStyleSheet(style_sheet)

    def conectar_signals(self):
        self.btn_agenda.clicked.connect(lambda: controller.handle_view_agenda(self))
        self.btn_gerenciar.clicked.connect(lambda: controller.handle_gerenciar_atividade(self))
        self.btn_exit.clicked.connect(self.close)