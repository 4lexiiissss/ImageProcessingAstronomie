python 
import sys
from PyQt6.QtWidgets import QApplication
from model import FITSModel
from view import FITSView
from controller import FITSController


def main():
    app = QApplication(sys.argv)

    # Création du modèle
    model = FITSModel()

    # Création de la vue et du contrôleur
    controller = FITSController(model, None)
    view = FITSView(controller)
    controller.view = view  # Relie le contrôleur à la vue

    # Affiche la vue
    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()