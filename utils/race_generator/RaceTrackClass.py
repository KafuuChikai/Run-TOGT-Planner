import numpy as np
from typing import List, Optional, Union
from GateShape import SingleBall, TrianglePrisma, RectanglePrisma, PentagonPrisma, HexagonPrisma

class State:
    def __init__(self, 
                 pos: Optional[Union[List[float], np.ndarray]],   # (3,) - position [x, y, z]
                 vel: Optional[Union[List[float], np.ndarray]],   # (3,) - velocity [vx, vy, vz]
                 acc: Optional[Union[List[float], np.ndarray]],   # (3,) - acceleration [ax, ay, az]
                 jer: Optional[Union[List[float], np.ndarray]],   # (3,) - jerk [jx, jy, jz]
                 rot: Optional[Union[List[float], np.ndarray]],   # (4,) - quaternion [w, x, y, z]
                 cthrustmass: Optional[float],                    # (1,) - collective thrust
                 euler: Optional[Union[List[float], np.ndarray]]  # (3,) - euler angles [roll, pitch, yaw]
                 ):
        self.pos = [0.0, 0.0, 0.0] if pos is None else (pos if isinstance(pos, list) else pos.tolist())
        self.vel = [0.0, 0.0, 0.0] if vel is None else (vel if isinstance(vel, list) else vel.tolist())
        self.acc = [0.0, 0.0, 0.0] if acc is None else (acc if isinstance(acc, list) else acc.tolist())
        self.jer = [0.0, 0.0, 0.0] if jer is None else (jer if isinstance(jer, list) else jer.tolist())
        self.rot = [0.0, 0.0, 0.0, 0.0] if rot is None else (rot if isinstance(rot, list) else rot.tolist())
        self.cthrustmass = 9.8066 if cthrustmass is None else cthrustmass
        self.euler = [0.0, 0.0, 0.0] if euler is None else (euler if isinstance(euler, list) else euler.tolist())

    def to_dict(self):
        return {
            'pos': self.pos,
            'vel': self.vel,
            'acc': self.acc,
            'jer': self.jer,
            'rot': self.rot,
            'cthrustmass': self.cthrustmass,
            'euler': self.euler
        }

# class Gate:
#     def __init__(self, 
#                  gate_shape: GateShape, 
#                  position: Union[List[float], np.ndarray], 
#                  stationary: bool, 
#                  name: Optional[str]):
#         self.gate_type = gate_shape
#         self.name = name
#         self.position = position if isinstance(position, list) else position.tolist()
#         self.stationary = stationary

#     def to_dict(self) -> dict:
#         data = {
#             'type': self.gate_type.get_shape_info(),
#             'position': self.position,
#             'stationary': self.stationary
#         }
#         if self.name is not None:
#             data['name'] = self.name
#         return data

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