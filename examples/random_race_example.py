import os
from run_togt_planner.RaceGenerator.GenerationTools import create_state, create_gate
from run_togt_planner.RaceGenerator.GateShape import SingleBall, TrianglePrisma, RectanglePrisma, PentagonPrisma, HexagonPrisma
from run_togt_planner.RaceGenerator.RaceTrack import RaceTrack
from run_togt_planner.RaceVisualizer.RacePlotter import RacePlotter
import subprocess
import random
from typing import Optional
import matplotlib.pyplot as plt

ROOTPATH = os.path.abspath(__file__).split("Run-TOGT-Planner/", 1)[0]
BASEPATH = os.path.dirname(os.path.abspath(__file__))

def create_random_racetrack_wp(gate_num: int,
                               shape_kwargs: dict,
                               name: Optional[str] = None) -> RaceTrack:    
    if gate_num <= 0:
        raise ValueError("gate_num must be a positive integer.")
    
    # Define initial and end states
    position = [
        random.uniform(-16.0, 16.0),  # x-coordinate
        random.uniform(-16.0, 16.0),  # y-coordinate
        random.uniform(0.0, 5.0)       # z-coordinate
    ]
    init_state = create_state({
        'pos': position,
    })
    position = [
        random.uniform(-16.0, 16.0),  # x-coordinate
        random.uniform(-16.0, 16.0),  # y-coordinate
        random.uniform(0.0, 5.0)       # z-coordinate
    ]
    end_state = create_state({
        'pos': position,
    })
    
    # Create the RaceTrack object
    race_track = RaceTrack(
        init_state=init_state,
        end_state=end_state,
        race_name=name or "RandomRace",
    )
    
    for i in range(gate_num):        
        # Generate random position within a predefined range
        position = [
            random.uniform(-16.0, 16.0),  # x-coordinate
            random.uniform(-16.0, 16.0),  # y-coordinate
            random.uniform(0.0, 5.0)       # z-coordinate
        ]
        
        # Randomly decide if the gate is stationary
        stationary = True
        
        # Create the gate
        gate = create_gate(
            gate_type='SingleBall',
            position=position,
            stationary=stationary,
            shape_kwargs=shape_kwargs,
            name=f"{name}_Gate_{i+1}" if name else f"Gate_{i+1}"
        )
        
        race_track.add_gate(gate, gate.name)

    return race_track

def run_traj_planner(config_path, quad_name, track_path, traj_path, wpt_path):
    # get the path to c++ program    
    cpp_program_path = os.path.join(ROOTPATH, 'build', 'planners')

    # make sure the path exists
    if not os.path.isfile(cpp_program_path):
        print(f"Error: {cpp_program_path} does not exist.")
        return

    # construct the command
    command = [
        cpp_program_path,  # path to the C++ program
        config_path,
        quad_name,
        track_path,
        traj_path,
        wpt_path
    ]

    # run the command
    result = subprocess.run(command, capture_output=True, text=True)

    # check if the command was successful
    if result.returncode != 0:
        print(f"Error running traj_planner_togt: {result.stderr}")
    else:
        print(f"{result.stdout}")

def plot_traj(traj_path, track_path, fig_path):
    togt_plotter = RacePlotter(traj_path, track_path)
    togt_plotter.plot(cmap=plt.cm.autumn.reversed(),
                      save_fig=True, 
                      fig_name="random_example", 
                      save_path=fig_path)

if __name__ == "__main__":
    # input parameters
    config_path = os.path.join(ROOTPATH, "parameters/cpc")
    quad_name = "cpc"
    track_path = os.fspath("../resources/racetrack")
    traj_path = os.fspath("../resources/trajectory")
    wpt_path = os.fspath("../resources/trajectory")
    fig_path = os.fspath("../resources/figure")

    os.makedirs(os.path.join(BASEPATH, traj_path), exist_ok=True)
    os.makedirs(os.path.join(BASEPATH, wpt_path), exist_ok=True)

    config_path = os.path.join(BASEPATH, config_path)
    track_path = os.path.join(BASEPATH, track_path)
    track_file_name = os.path.join(track_path, 'random_example.yaml')
    traj_path = os.path.join(BASEPATH, traj_path, 'random_example.csv')
    wpt_path = os.path.join(BASEPATH, wpt_path, 'random_example.yaml')
    fig_path = os.path.join(BASEPATH, fig_path)

    ball_shape_kwargs = {
        'radius': 1.0,
        'margin': 0.0
    }

    # Step 1: Create a racetrack
    random_race = create_random_racetrack_wp(gate_num=10, 
                                             shape_kwargs=ball_shape_kwargs, 
                                             name='random_example')
    random_race.save_to_yaml(save_dir=track_path,
                             overwrite=True, 
                             standard=True, 
                             save_output=True)

    # Step 2: Run the trajectory planner
    run_traj_planner(config_path, quad_name, track_file_name, traj_path, wpt_path)

    # Step 3: Plot the trajectory
    plot_traj(traj_path, track_file_name, fig_path)