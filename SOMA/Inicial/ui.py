from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt
from SOMA.Inicial.controller import handle_view_agenda, handle_add_tarefa


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistente Pessoal")
        self.setFixedSize(300, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Assistente Pessoal")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        # Botões
        btn_agenda = QPushButton("Ver agenda")
        btn_add = QPushButton("Adicionar tarefa")
        btn_exit = QPushButton("❌ Sair")

        for btn in (btn_agenda, btn_add, btn_exit):
            btn.setMinimumHeight(40)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            layout.addWidget(btn)

        central_widget.setLayout(layout)

        # Conectar sinais aos slots
        btn_agenda.clicked.connect(handle_view_agenda)
        btn_add.clicked.connect(handle_add_tarefa)
        btn_exit.clicked.connect(self.close)
