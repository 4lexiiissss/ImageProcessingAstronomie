import sys
from PyQt6.QtWidgets import QApplication
from model import FITSModel
from view import FITSView
from controller import FITSController

def main():
    app = QApplication(sys.argv)

    model = FITSModel()

    controller = FITSController(model, None)
    view = FITSView(controller)
    controller.view = view  

    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()