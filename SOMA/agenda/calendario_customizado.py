from PySide6.QtWidgets import QCalendarWidget
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import QRect, QDate
from collections import defaultdict

class CalendarioCustomizado(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tarefas_por_data = defaultdict(set)
        self.tarefas_importantes_por_data = defaultdict(bool)
        
    def atualizar_tarefas_data(self, tarefas_por_data, importantes_por_data):
        self.tarefas_por_data = tarefas_por_data
        self.tarefas_importantes_por_data = importantes_por_data
        self.update()  
        
    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)
        
        tipos_tarefas = self.tarefas_por_data.get(date, set())
        eh_importante = self.tarefas_importantes_por_data.get(date, False)
        
        if tipos_tarefas or eh_importante:
            self.desenhar_barras_tipos(painter, rect, tipos_tarefas, eh_importante)
    
    def desenhar_barras_tipos(self, painter, rect, tipos_tarefas, eh_importante):
        painter.save()
        
        altura_barra = 4
        largura_total = rect.width() - 4
        margem_horizontal = 2
        y_base = rect.bottom() - altura_barra - 1
        
        if eh_importante:
            painter.fillRect(
                rect.left() + margem_horizontal,
                rect.top() + 2,
                largura_total,
                altura_barra,
                QColor("#F6E58D")  
            )
        
        if tipos_tarefas:
            ordem_tipos = ["daily", "weekly", "single"]
            tipos_ordenados = [tipo for tipo in ordem_tipos if tipo in tipos_tarefas]
            
            num_tipos = len(tipos_ordenados)
            if num_tipos > 0:
                largura_barra = max(1, largura_total // num_tipos)
                
                cores_tipos = {
                    "daily": QColor("#B5EAD7"),   
                    "weekly": QColor("#CDB4DB"),   
                    "single": QColor("#A0C4FF")    
                }
                
                for i, tipo in enumerate(tipos_ordenados):
                    x_inicio = rect.left() + margem_horizontal + (i * largura_barra)
                    if i == num_tipos - 1:
                        largura_atual = largura_total - (i * largura_barra)
                    else:
                        largura_atual = largura_barra
                    
                    cor = cores_tipos.get(tipo, QColor("#CCCCCC"))
                    
                    painter.fillRect(
                        x_inicio,
                        y_base,
                        largura_atual,
                        altura_barra,
                        cor
                    )
        
        painter.restore()
