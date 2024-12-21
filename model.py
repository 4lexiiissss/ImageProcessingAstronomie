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
import numpy as np

# ------------------------------------------------------------------------------------------
# --- class FITSModel-------------------------------------------------------
# ------------------------------------------------------------------------------------------
class FITSModel:
    
    # methods
    # -------------------------------------------------- 
    def __init__(self):
        self.rgb_image = None 

    # -------------------------------------------------- 
    def set_rgb_image(self, image: np.ndarray):
        self.rgb_image = image

    # -------------------------------------------------- 
    def get_rgb_image(self) -> np.ndarray:
        return self.rgb_image