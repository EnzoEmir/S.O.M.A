from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QCalendarWidget
from PySide6.QtGui import QColor, QTextCharFormat
from PySide6.QtCore import QDate
from SOMA.agenda import controller
import json

class AgendaWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agenda")
        self.resize(360, 420)

        self.calendario = QCalendarWidget()
    
        formato_dias_importantes = QTextCharFormat() 
        cor_de_fundo = QColor("#a4bcdd")
        formato_dias_importantes.setBackground(cor_de_fundo)

        try: 
            with open("SOMA\minhas_datas.json", "r") as f:
                lista_de_tarefas = json.load(f)
        except FileNotFoundError: 
            lista_de_tarefas = [] 
            print("AVISO: Arquivo 'minhas_datas.json' não encontrado.")

        
        for tarefa in lista_de_tarefas:             
            q_date = QDate.fromString(tarefa["date"], "dd-MM-yyyy")
            
            self.calendario.setDateTextFormat(q_date, formato_dias_importantes)
        
        layout = QVBoxLayout()
        layout.addWidget(self.calendario)
        self.setLayout(layout)

        btn_Voltar = QPushButton("❌ Voltar")
        layout.addWidget(btn_Voltar) 

        btn_Voltar.clicked.connect(lambda: controller.voltar_main(self))

        self.main = None