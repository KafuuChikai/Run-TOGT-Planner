from typing import List, Optional, Union
from run_togt_planner.RaceGenerator.BaseRaceClass import BaseRaceClass, State, Gate
from run_togt_planner.RaceGenerator.GenerationTools import create_state, create_gate, quote_specific_keys
import os

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.width = 4096
yaml.default_flow_style = False

class RaceTrack(BaseRaceClass):
    def __init__(self,
                 init_state: State,
                 end_state: State,
                 race_name: Optional[str] = None):
        self.initState = init_state
        self.endState = end_state
        self.race_name = race_name
        self.orders = []
        self.gate_sequence = []
        self.gate_num = 0

    def add_gate(self,
                 gate: Gate,
                 gate_name: Optional[str] = None):
        if gate_name is None:
            self.gate_num += 1
            gate_name = 'Gate' + str(self.gate_num)
        self.orders.append(gate_name)
        self.gate_sequence.append([gate_name, gate])

    def clear_gates(self):
        self.orders = []
        self.gate_sequence = []
        self.gate_num = 0

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
            'orders' : self.orders,
            **self.get_gate_dict()
        }
        return data
    
    def to_ordered_dict(self) -> CommentedMap:
        data = CommentedMap()
        data['initState'] = self.initState.to_ordered_dict()
        data['endState'] = self.endState.to_ordered_dict()
        Seq_orders = CommentedSeq(self.orders)
        Seq_orders.fa.set_flow_style()
        data['orders'] = Seq_orders
        ordered_gate_dict = self.get_gate_dict(ordered=True)
        for gate_name in self.orders:
            data[gate_name] = ordered_gate_dict[gate_name]
        return data

    def save_to_yaml(self,
                     save_dir: Optional[Union[os.PathLike, str]] = None,
                     overwrite: bool = False,
                     standard: bool = True,
                     save_output: bool = True,) -> bool:
        if self.gate_sequence == []:
            Warning("No gate has been added! The race track will not be saved.")
            return False

        if save_dir is None:
            save_path = os.path.join(os.getcwd(), 'resources/racetrack')
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

        if standard:
            save_data = self.to_ordered_dict()
            quote_specific_keys(save_data)
            try:
                with open(file=save_file, mode="w") as f:
                    pass
                with open(file=save_file, mode="a") as f:
                    for key in save_data.keys():
                        yaml.dump({key : save_data[key]}, f)
                        f.write('\n')
                if save_output:
                    print(f"Success to save to: {save_file}")
                return True
            except Exception as e:
                if save_output:
                    print(f"Error saving to YAML: {e}")
                return False
        else:
            save_data = self.to_dict()
            try:
                with open(file=save_file, mode="w") as f:
                    yaml.dump(save_data, f)
                if save_output:
                    print(f"Success to save to: {save_file}")
                return True
            except Exception as e:
                if save_output:
                    print(f"Error saving to YAML: {e}")
                return False
            
    def load_from_yaml(self,
                       load_dir: Optional[Union[os.PathLike, str]]):
        gate_param_list = ['type', 'name', 'position', 'stationary']
        load_dir = os.fspath(load_dir)
        self.race_name = os.path.splitext(os.path.basename(load_dir))[0]

        with open(file=load_dir, mode="r") as f:
            data = yaml.load(f)

        self.initState = create_state(data['initState'])
        self.endState = create_state(data['endState'])
        
        self.clear_gates()
        for gate_name in data['orders']:
            gate_params = data[gate_name]
            shape_kwarg = {k: v for k, v in gate_params.items() if k not in gate_param_list}
            gate_kwarg = {'gate_type': gate_params['type'],
                          'position': gate_params['position'],
                          'stationary': gate_params['stationary'],
                          'shape_kwargs': shape_kwarg,
                          'name': gate_params.get('name', None)}
            gate = create_gate(**gate_kwarg)
            self.add_gate(gate, gate_name)