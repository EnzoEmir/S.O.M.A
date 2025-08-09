def voltar_main(current_window):
    from SOMA.Inicial.ui import MainWindow
    
    current_window.main = MainWindow()
    current_window.main.show()
    
    current_window.close()