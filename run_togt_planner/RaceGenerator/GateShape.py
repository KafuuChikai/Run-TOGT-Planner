import numpy as np
from typing import List, Union

########################################
###### BASE CLASS FOR GATE SHAPES ######
########################################

class BaseShape:
    def __init__(self, 
                 gate_type: str):
        self.type = gate_type

    def get_shape_info(self) -> dict:
        return vars(self)
    
class BasePrisma(BaseShape):
    def __init__(self, 
                 gate_type: str, 
                 rpy: Union[List[float], np.ndarray], 
                 length: float, 
                 midpoints: int):
        super().__init__(gate_type)
        self.rpy = rpy if isinstance(rpy, list) else rpy.tolist()
        self.length = length
        self.midpoints = midpoints
    
########################################
###### GATE SHAPES IMPLEMENTATION ######
########################################

class SingleBall(BaseShape):
    def __init__(self, 
                 radius: float, 
                 margin: float):
        super().__init__('SingleBall')
        self.radius = radius
        self.margin = margin

class TrianglePrisma(BasePrisma):
    def __init__(self, 
                 rpy: Union[List[float], np.ndarray], 
                 length: float, 
                 midpoints: int, 
                 width: float, 
                 height: float, 
                 margin: float):
        super().__init__('TrianglePrisma', rpy, length, midpoints)
        self.width = width
        self.height = height
        self.margin = margin
    
class RectanglePrisma(BasePrisma):
    def __init__(self, 
                 rpy: Union[List[float], np.ndarray], 
                 length: float, 
                 midpoints: int,
                 width: float, 
                 height: float, 
                 marginW: float, 
                 marginH: float):
        super().__init__('RectanglePrisma', rpy, length, midpoints)
        self.width = width
        self.height = height
        self.marginW = marginW
        self.marginH = marginH

class PentagonPrisma(BasePrisma):
    def __init__(self, 
                 rpy: Union[List[float], np.ndarray], 
                 length: float, 
                 midpoints: int,
                 radius: float, 
                 margin: float):
        super().__init__('PentagonPrisma', rpy, length, midpoints)
        self.radius = radius
        self.margin = margin

class HexagonPrisma(BasePrisma):
    def __init__(self, 
                 rpy: Union[List[float], np.ndarray], 
                 length: float, 
                 midpoints: int,
                 side: float, 
                 margin: float):
        super().__init__('HexagonPrisma', rpy, length, midpoints)
        self.side = side
        self.margin = margin