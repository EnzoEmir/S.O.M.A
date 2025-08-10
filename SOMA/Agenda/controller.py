def voltar_main(current_window):
    from SOMA.inicial.ui import MainWindow
    
    current_window.main = MainWindow()
    current_window.main.show()
    
    current_window.close()