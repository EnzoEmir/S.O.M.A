from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QCalendarWidget
from PySide6.QtGui import QColor, QTextCharFormat
from PySide6.QtCore import QDate
from SOMA.Agenda import controller

class AgendaWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agenda")
        self.resize(360, 420)

        self.calendario = QCalendarWidget()
    
        teste = QDate(2024, 1, 1)
        hoje = QDate.currentDate()
        formato_dia_especial = QTextCharFormat() 
        cor_de_fundo = QColor("#a4bcdd")
        formato_dia_especial.setBackground(cor_de_fundo)
        self.calendario.setDateTextFormat(hoje, formato_dia_especial)
        self.calendario.setDateTextFormat(teste, formato_dia_especial)

        layout = QVBoxLayout()
        layout.addWidget(self.calendario)
        self.setLayout(layout)

        btn_Voltar = QPushButton("❌ Voltar")
        layout.addWidget(btn_Voltar) 

        btn_Voltar.clicked.connect(lambda: controller.voltar_main(self))

        self.main = None