import numpy as np
from typing import List, Optional, Union, Type
from run_togt_planner.RaceGenerator.GateShape import BaseShape, SingleBall, TrianglePrisma, RectanglePrisma, PentagonPrisma, HexagonPrisma
from run_togt_planner.RaceGenerator.BaseRaceClass import State, Gate
from ruamel.yaml.scalarstring import SingleQuotedScalarString

KEYS_TO_QUOTE = ['type', 'name']

def quote_specific_keys(data: Union[dict, List[dict], str], 
                        keys_to_quote: List[str] = KEYS_TO_QUOTE):
    if isinstance(data, dict):
        for key, value in data.items():
            if key in keys_to_quote and isinstance(value, str):
                data[key] = SingleQuotedScalarString(value)
            elif isinstance(value, (dict, list)):
                quote_specific_keys(value, keys_to_quote)
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            if isinstance(item, str):
                data[idx] = SingleQuotedScalarString(item)
            elif isinstance(item, (dict, list)):
                quote_specific_keys(item, keys_to_quote)
    return data

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