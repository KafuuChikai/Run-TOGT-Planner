import numpy as np
from typing import List, Optional, Union
from utils.RaceGenerator.GateShape import BaseShape

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
        return vars(self)

class Gate:
    def __init__(self, 
                 gate_shape: BaseShape, 
                 position: Union[List[float], np.ndarray], 
                 stationary: bool, 
                 name: Optional[str]):
        self.shape = gate_shape
        self.name = name
        self.position = position if isinstance(position, list) else position.tolist()
        self.stationary = stationary

    def to_dict(self) -> dict:
        data = {
            **self.shape.get_shape_info(),
            'position': self.position,
            'stationary': self.stationary
        }
        if self.name is not None:
            data['name'] = self.name
        return data