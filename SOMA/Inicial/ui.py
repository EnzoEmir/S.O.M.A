from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt
from SOMA.inicial import controller

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistente Pessoal")
        self.resize(360, 420)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Assistente Pessoal")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        btn_agenda = QPushButton("Ver agenda")
        btn_add = QPushButton("Adicionar tarefa")
        btn_exit = QPushButton("❌ Sair")

        for btn in (btn_agenda, btn_add, btn_exit):
            btn.setMinimumHeight(40)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            layout.addWidget(btn)

        central_widget.setLayout(layout)

        btn_agenda.clicked.connect(lambda: controller.handle_view_agenda(self))
        btn_add.clicked.connect(controller.handle_add_tarefa) # Não precisa de lambda pois não passa args
        btn_exit.clicked.connect(self.close)

        # referência para a próxima janela
        self.agenda_window = None