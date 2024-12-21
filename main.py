#   Copyright (C) 2024  Alexis Demol - Lucas Debruyne  
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
# ImageProcessingAstronomie project 2024
# author: 
# Alexis Demol (4lexiiissss) | alexisdemol.europe@gmail.com 
# Lucas Debruyne (lucas210905) | lucas.debruyne2109@gmail.com

# import 
# -----------------------------------------------------------------------------
import sys
from PyQt6.QtWidgets import QApplication
from model import FITSModel
from view import FITSView
from controller import FITSController

# ------------------------------------------------------------------------------------------
# --- Main-------------------------------------------------------
# ------------------------------------------------------------------------------------------
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