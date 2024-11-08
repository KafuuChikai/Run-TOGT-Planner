import numpy as np
from typing import List, Optional, Union
from utils.RaceGenerator.GateShape import BaseShape
import yaml
import os

class FlowStyleDumper(yaml.SafeDumper):
    pass

def represent_list_flow(dumper, data):
    return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)

FlowStyleDumper.add_representer(list, represent_list_flow)

class State:
    def __init__(self, 
                 pos: Union[List[float], np.ndarray],                   # (3,) - position [x, y, z]
                 vel: Optional[Union[List[float], np.ndarray]] = None,  # (3,) - velocity [vx, vy, vz]
                 acc: Optional[Union[List[float], np.ndarray]] = None,  # (3,) - acceleration [ax, ay, az]
                 jer: Optional[Union[List[float], np.ndarray]] = None,  # (3,) - jerk [jx, jy, jz]
                 rot: Optional[Union[List[float], np.ndarray]] = None,  # (4,) - quaternion [w, x, y, z]
                 cthrustmass: Optional[float] = None,                   # (1,) - collective thrust
                 euler: Optional[Union[List[float], np.ndarray]] = None # (3,) - euler angles [roll, pitch, yaw]
                 ):
        self.pos = pos if isinstance(pos, list) else pos.tolist()
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
                 name: Optional[str] = None):
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
    
class RaceTrack:
    def __init__(self,
                 init_state: State,
                 end_state: State,
                 race_name: Optional[str] = None):
        self.initState = init_state
        self.endState = end_state
        self.race_name = race_name
        self.order = []
        self.gate_list = []
        self.gate_dict = {}
        self.gate_num = 0

    def add_gate(self,
                 gate: Gate,
                 gate_name: Optional[str] = None):
        if gate_name is None:
            self.gate_num += 1
            gate_name = 'Gate' + str(self.gate_num)
        self.order.append(gate_name)
        self.gate_list.append(gate)
        self.gate_dict[gate_name] = gate.to_dict()

    def to_dict(self) -> dict:
        data = {
            'initState' : self.initState.to_dict(),
            'endState' : self.endState.to_dict(),
            'Order' : self.order,
            **self.gate_dict
        }
        return data
    
    def save_to_yaml(self,
                     save_dir: Optional[Union[os.PathLike, str]] = None,
                     overwrite: bool = False) -> bool:
        if self.gate_list == []:
            Warning("No gate has been added! The race track will not be saved.")
            return False

        if save_dir is None:
            save_path = os.path.join(os.getcwd(), 'racetrack')
        else:
            save_path = os.fspath(save_dir)
        os.makedirs(save_path, exist_ok=True)

        file_name = self.race_name if self.race_name is not None else "racetrack"
        save_file = os.path.join(save_path, file_name + '.yaml')

        if not overwrite:
            base_name = file_name
            counter = 1
            while os.path.exists(save_file):
                file_name = f"{base_name}_{counter}"
                save_file = os.path.join(save_path, file_name + '.yaml')
                counter += 1

        save_data = self.to_dict()

        try:
            with open(file=save_file, mode="w") as f:
                yaml.dump(save_data, f, Dumper=FlowStyleDumper, default_flow_style=False)
            print(f"Success to save to: {save_file}")
            return True
        except Exception as e:
            print(f"Error saving to YAML: {e}")
            return False
            
        # No quote
        # with open(file=save_path, mode="r") as file:
        #     content = file.read()
        # content = re.sub(r'["\']', '', content)
        # with open(file=save_path, mode="w") as file:
        #     file.write(content)