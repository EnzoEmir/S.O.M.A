from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget

class NavigationStack(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("S.O.M.A")
        self.setGeometry(200, 200, 1000, 700)
        self.setMinimumSize(800, 600)
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        self.pages = {}
        
        self.historico_navegacao = []
        
        self.setup_estilos_globais()
        
    def setup_estilos_globais(self):
        estilo_global = """
            QMainWindow {
                background-color: #2B2D31;
                font-family: Poppins, sans-serif;
                color: #ECECEC;
            }
            
            QStackedWidget {
                background-color: #2B2D31;
            }
        """
        self.setStyleSheet(estilo_global)
    
    def adicionar_pagina(self, name, widget):
        self.pages[name] = widget
        self.stack.addWidget(widget)
        
        if hasattr(widget, 'definir_navigation_stack'):
            widget.definir_navigation_stack(self)
    
    def navegar_para(self, page_name, add_to_history=True):
        if page_name in self.pages:
            current_index = self.stack.currentIndex()
            
            if add_to_history and current_index != -1:
                current_page_name = self.obter_nome_pagina_atual()
                if current_page_name and current_page_name != page_name:
                    self.historico_navegacao.append(current_page_name)
            
            widget = self.pages[page_name]
            self.stack.setCurrentWidget(widget)
            
            if hasattr(widget, 'on_page_activated'):
                widget.on_page_activated()
                
    def voltar(self):
        if self.historico_navegacao:
            previous_page = self.historico_navegacao.pop()
            self.navegar_para(previous_page, add_to_history=False)
            return True
        return False
    
    def obter_nome_pagina_atual(self):
        current_widget = self.stack.currentWidget()
        for name, widget in self.pages.items():
            if widget == current_widget:
                return name
        return None


class NavigableWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.navigation_stack = None
    
    def definir_navigation_stack(self, navigation_stack):
        self.navigation_stack = navigation_stack
    
    def navegar_para(self, page_name):
        if self.navigation_stack:
            self.navigation_stack.navegar_para(page_name)
    
    def voltar(self):
        if self.navigation_stack:
            return self.navigation_stack.voltar()
        return False
    
    def on_page_activated(self):
        pass