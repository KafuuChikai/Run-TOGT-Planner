import numpy as np
from typing import List, Optional, Union
from utils.RaceGenerator.GateShape import BaseShape
import os

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.default_flow_style = False

class BaseRaceClass:
    def __init__(self):
        pass

    def to_ordered_dict(self,
                        ordered_keys: List[str],
                        dict: dict) -> CommentedMap:
        data = CommentedMap()
        for key in ordered_keys:
            # data[key] = dict[key]
            value = dict[key]
            if isinstance(dict[key], list):
                commented_seq = CommentedSeq(value)
                commented_seq.fa.set_flow_style()
                data[key] = commented_seq
            else:
                data[key] = value
        return data

class State(BaseRaceClass):
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
    
    def to_ordered_dict(self) -> CommentedMap:
        ordered_keys = ['pos', 'vel', 'acc', 'jer', 'rot', 'cthrustmass', 'euler']
        return super().to_ordered_dict(ordered_keys = ordered_keys,
                                       dict = self.to_dict())

class Gate(BaseRaceClass):
    def __init__(self, 
                 gate_shape: BaseShape, 
                 position: Union[List[float], np.ndarray], 
                 stationary: bool, 
                 name: Optional[str] = None):
        self.shape = gate_shape
        self.name = name
        self.position = position if isinstance(position, list) else position.tolist()
        self.stationary = stationary
        self.SHAPE_ORDER_KEYS = {
            'SingleBall': ['type', 'name', 'position', 'radius', 'margin', 'stationary'],
            'TrianglePrisma': ['type', 'name', 'position', 'rpy', 'width', 'height', 'margin', 'length', 'midpoints', 'stationary'],
            'RectanglePrisma': ['type', 'name', 'position', 'rpy', 'width', 'height', 'marginW', 'marginH', 'length', 'midpoints', 'stationary'],
            'PentagonPrisma': ['type', 'name', 'position', 'rpy', 'radius', 'margin', 'length', 'midpoints', 'stationary'],
            'HexagonPrisma': ['type', 'name', 'position', 'rpy', 'side', 'margin', 'length', 'midpoints', 'stationary'],
        }

    def to_dict(self) -> dict:
        data = {
            **self.shape.get_shape_info(),
            'position': self.position,
            'stationary': self.stationary
        }
        if self.name is not None:
            data['name'] = self.name
        return data

    def to_ordered_dict(self) -> CommentedMap:
        ordered_keys = self.SHAPE_ORDER_KEYS[self.shape.type]
        if self.name is None:
            ordered_keys.remove('name')
        return super().to_ordered_dict(ordered_keys = ordered_keys, 
                                       dict = self.to_dict())
    
class RaceTrack(BaseRaceClass):
    def __init__(self,
                 init_state: State,
                 end_state: State,
                 race_name: Optional[str] = None):
        self.initState = init_state
        self.endState = end_state
        self.race_name = race_name
        self.order = []
        self.gate_sequence = []
        self.gate_num = 0

    def add_gate(self,
                 gate: Gate,
                 gate_name: Optional[str] = None):
        if gate_name is None:
            self.gate_num += 1
            gate_name = 'Gate' + str(self.gate_num)
        self.order.append(gate_name)
        self.gate_sequence.append([gate_name, gate])

    def get_gate_dict(self,
                      ordered: bool = False) -> Union[dict, CommentedMap]:
        gate_dict = CommentedMap() if ordered else {}
        for gate_info in self.gate_sequence:
            if ordered:
                gate_dict[gate_info[0]] = gate_info[1].to_ordered_dict()
            else:
                gate_dict[gate_info[0]] = gate_info[1].to_dict()
        return gate_dict

    def to_dict(self) -> dict:
        data = {
            'initState' : self.initState.to_dict(),
            'endState' : self.endState.to_dict(),
            'Order' : self.order,
            **self.get_gate_dict()
        }
        return data
    
    def to_ordered_dict(self) -> CommentedMap:
        data = CommentedMap()
        data['initState'] = self.initState.to_ordered_dict()
        data['endState'] = self.endState.to_ordered_dict()
        Seq_order = CommentedSeq(self.order)
        Seq_order.fa.set_flow_style()
        data['Order'] = Seq_order
        ordered_gate_dict = self.get_gate_dict(ordered=True)
        for gate_name in self.order:
            data[gate_name] = ordered_gate_dict[gate_name]
        return data
    
    def save_to_yaml_standard(self,
                              save_dir: Optional[Union[os.PathLike, str]] = None,
                              overwrite: bool = False) -> bool:
        if self.gate_sequence == []:
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

        save_data = self.to_ordered_dict()

        try:
            with open(file=save_file, mode="w") as f:
                pass
            with open(file=save_file, mode="a") as f:
                for key in save_data.keys():
                    yaml.dump({key : save_data[key]}, f)
                    f.write('\n')
            print(f"Success to save to: {save_file}")
            return True
        except Exception as e:
            print(f"Error saving to YAML: {e}")
            return False