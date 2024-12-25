import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
import keybinder

def main():
    keybinder.setup_hook()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    window.load_keybinds_from_config('config.json')

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
