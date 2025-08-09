from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt

from SOMA.Agenda import controller

class AgendaWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agenda")
        self.resize(360, 420)

        layout = QVBoxLayout()
        self.setLayout(layout)

        btn_Voltar = QPushButton("❌ Voltar")
        layout.addWidget(btn_Voltar) 

        btn_Voltar.clicked.connect(lambda: controller.voltar_main(self))

        self.main = None