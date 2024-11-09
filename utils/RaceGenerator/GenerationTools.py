import numpy as np
from typing import List, Optional, Union, Type
from utils.RaceGenerator.GateShape import BaseShape, SingleBall, TrianglePrisma, RectanglePrisma, PentagonPrisma, HexagonPrisma
from utils.RaceGenerator.BaseRaceClass import State, Gate

def get_shape_class(gate_shape: str) -> BaseShape:
    shape_classes = {
        'SingleBall': SingleBall,
        'TrianglePrisma': TrianglePrisma,
        'RectanglePrisma': RectanglePrisma,
        'PentagonPrisma': PentagonPrisma,
        'HexagonPrisma': HexagonPrisma
    }
    return shape_classes[gate_shape]

def create_state(state_kwargs: dict) -> State:
    missing_pos = True if 'pos' not in state_kwargs else False
    if missing_pos:
        raise ValueError("Missing parameters for State: pos")
    
    return State(**state_kwargs)

def create_gate(gate_type: Union[Type[BaseShape], str],
                position: Union[List[float], np.ndarray],
                stationary: bool,
                shape_kwargs: dict,
                name: Optional[str] = None) -> Gate:
    shape_params = {
        'SingleBall': ['radius', 'margin'],
        'TrianglePrisma': ['rpy', 'length', 'midpoints', 'width', 'height', 'margin'],
        'RectanglePrisma': ['rpy', 'length', 'midpoints', 'width', 'height', 'marginW', 'marginH'],
        'PentagonPrisma': ['rpy', 'length', 'midpoints', 'radius', 'margin'],
        'HexagonPrisma': ['rpy', 'length', 'midpoints', 'side', 'margin']
    }

    if isinstance(gate_type, str):
        gate_type = get_shape_class(gate_type)
    gate_type_name = gate_type.__name__

    missing_params = [param for param in shape_params[gate_type_name] if param not in shape_kwargs]
    if missing_params:
        raise ValueError(f"Missing parameters for {gate_type_name}: {', '.join(missing_params)}")

    return Gate(gate_shape=gate_type(**shape_kwargs), 
                position=position, 
                stationary=stationary, 
                name=name)