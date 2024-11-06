import numpy as np
from typing import List, Optional, Union

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

class Gate:
    def __init__(self, 
                 gate_type: str, 
                 name: str, 
                 position: Union[List[float], np.ndarray], 
                 rpy: Union[List[float], np.ndarray], 
                 width: float, 
                 height: float, 
                 margin: float, 
                 length: float, 
                 midpoints: int, 
                 stationary: bool):
        self.gate_type = gate_type
        self.name = name
        self.position = position
        self.rpy = rpy
        self.width = width
        self.height = height
        self.margin = margin
        self.length = length
        self.midpoints = midpoints
        self.stationary = stationary

    def to_dict(self):
        return {
            'type': self.gate_type,
            'name': self.name,
            'position': self.position,
            'rpy': self.rpy,
            'width': self.width,
            'height': self.height,
            'margin': self.margin,
            'length': self.length,
            'midpoints': self.midpoints,
            'stationary': self.stationary
        }

# init_state = State(
#     pos=[-5.0, 4.5, 1.2],
#     vel=[0.0, 0.0, 0.0],
#     acc=[0.0, 0.0, 0.0],
#     jer=[0.0, 0.0, 0.0],
#     rot=[1.0, 0.0, 0.0, 0.0],
#     cthrustmass=9.8066,
#     euler=[0.0, 0.0, 0.0]
# )

# end_state = State(
#     pos=[4.75, -0.9, 1.2],
#     vel=[0.0, 0.0, 0.0],
#     acc=[0.0, 0.0, 0.0],
#     jer=[0.0, 0.0, 0.0],
#     rot=[1.0, 0.0, 0.0, 0.0],
#     cthrustmass=9.8066,
#     euler=[0.0, 0.0, 0.0]
# )

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