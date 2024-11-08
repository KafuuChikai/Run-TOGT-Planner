import numpy as np
from typing import List, Optional, Union, Type
from utils.RaceGenerator.GateShape import BaseShape, SingleBall, TrianglePrisma, RectanglePrisma, PentagonPrisma, HexagonPrisma
from utils.RaceGenerator.RaceClass import State, Gate

def create_state(state_kwargs: dict) -> State:
    missing_pos = True if 'pos' not in state_kwargs else False
    if missing_pos:
        raise ValueError("Missing parameters for State: pos")
    
    return State(**state_kwargs)

def create_gate(gate_type: Type[BaseShape],
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

    gate_type_name = gate_type.__name__

    missing_params = [param for param in shape_params[gate_type_name] if param not in shape_kwargs]
    if missing_params:
        raise ValueError(f"Missing parameters for {gate_type_name}: {', '.join(missing_params)}")

    return Gate(gate_shape=gate_type(**shape_kwargs), 
                position=position, 
                stationary=stationary, 
                name=name)

# def create_racetrack(init_state: State, end_state: State, gates: List[Gate]) -> dict:
#     data = {
#         'initState': init_state.to_dict(),
#         'endState': end_state.to_dict(),
#         'orders': [gate.name for gate in gates],
#         **{gate.name: gate.to_dict() for gate in gates}
#     }

#     return data

# gate1 = Gate(
#     gate_type='TrianglePrisma',
#     name='vicon_gate',
#     position=[-1.1, -1.6, 3.6],
#     rpy=[0.0, -90, 0.0],
#     width=2.4,
#     height=2.4,
#     margin=0.0,
#     length=0.0,
#     midpoints=0,
#     stationary=True
# )

# data = {
#     'initState': init_state.to_dict(),
#     'endState': end_state.to_dict(),
#     'orders': ['Gate1', 'Gate2', 'Gate3', 'Gate4', 'Gate5', 'Gate6', 'Gate7'],
#     'Gate1': gate1.to_dict()
# }

# with open('race_uzh_7g_multiprisma.yaml', 'w') as file:
#     yaml.dump(data, file, default_flow_style=False)