import os
from utils.RaceGenerator.GenerationTools import create_state, create_gate
from utils.RaceGenerator.GateShape import SingleBall, TrianglePrisma, RectanglePrisma, PentagonPrisma, HexagonPrisma
from utils.RaceGenerator.RaceTrack import RaceTrack
from utils.RaceVisualizer.RacePlotter import RacePlotter
import subprocess

ROOTPATH = os.path.abspath(__file__).split("Run-TOGT-Planner/", 1)[0]
BASEPATH = os.path.dirname(os.path.abspath(__file__))

def create_racetrack():
    # Define gate parameters
    ball_kwargs = {
        'radius': 0.5,
        'margin': 0.0
    }

    tri_kwargs = {
        'rpy': [0.0, -90, 0.0],
        'width': 2.4,
        'height': 2.4,
        'margin': 0.0,
        'length': 0.0,
        'midpoints': 0
    }

    rec_kwargs = {
        'rpy': [0.0, -90, 0.0],
        'width': 2.4,
        'height': 2.4,
        'marginW': 0.0,
        'marginH': 0.0,
        'length': 0.0,
        'midpoints': 0
    }

    pen_kwargs = {
        'rpy': [0.0, -90, 0.0],
        'radius': 2.4,
        'margin': 0.0,
        'length': 16.0,
        'midpoints': 0
    }

    hex_kwargs = {
        'rpy': [0.0, -90, 0.0],
        'side': 1.5,
        'margin': 0.0,
        'length': 0.0,
        'midpoints': 0
    }

    state_kwargs = {
        'pos' : [0.0, 0.0, 0.0]
    }

    # Generate race track & save to yaml
    init_state = create_state(state_kwargs)
    end_state = create_state(state_kwargs)
    ball_gate = create_gate(SingleBall, [3.0, 0.0, 0.0], True, ball_kwargs, 'ball_gate')
    tri_gate = create_gate(TrianglePrisma, [0.0, 5.0, 0.0], True, tri_kwargs, 'tri_gate')
    rec_gate = create_gate(RectanglePrisma, [0.0, 8.0, 0.0], True, rec_kwargs, 'rec_gate')
    pen_gate = create_gate(PentagonPrisma, [0.0, 9.0, 0.0], True, pen_kwargs, 'pen_gate')
    hex_gate = create_gate(HexagonPrisma, [0.0, 18.0, 0.0], True, hex_kwargs, 'hex_gate')

    test_race = RaceTrack(init_state=init_state,
                        end_state=end_state,
                        race_name='example')
    test_race.add_gate(ball_gate)
    test_race.add_gate(tri_gate)
    test_race.add_gate(rec_gate)
    test_race.add_gate(pen_gate)
    test_race.add_gate(hex_gate)

    test_race.save_to_yaml(save_dir=os.path.join(BASEPATH, "resources/racetrack"),
                        overwrite=True, 
                        standard=True, 
                        save_output=True)

def read_racetrack():
    state_kwargs = {
        'pos' : [0.0, 0.0, 0.0]
    }
    init_state = create_state(state_kwargs)
    end_state = create_state(state_kwargs)

    # read from yaml
    read_race = RaceTrack(init_state=init_state,
                        end_state=end_state,
                        race_name='example')
    read_race.load_from_yaml(load_dir=os.path.join(BASEPATH, "resources/racetrack/example.yaml"))
    return read_race

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

def plot_traj(traj_path, track_path):
    togt_plotter = RacePlotter(traj_path, track_path)
    togt_plotter.plot(save_fig=True, fig_name="example", save_path=os.path.join(BASEPATH, "resources/figure/"))

if __name__ == "__main__":
    # input parameters
    config_path = os.fspath("../parameters/cpc")
    quad_name = "cpc"
    track_path = os.fspath("resources/racetrack")
    traj_path = os.fspath("resources/trajectory")
    wpt_path = os.fspath("resources/trajectory")

    os.makedirs(os.path.join(BASEPATH, traj_path), exist_ok=True)
    os.makedirs(os.path.join(BASEPATH, wpt_path), exist_ok=True)

    config_path = os.path.join(BASEPATH, config_path)
    track_path = os.path.join(BASEPATH, track_path, 'example.yaml')
    traj_path = os.path.join(BASEPATH, traj_path, 'example.csv')
    wpt_path = os.path.join(BASEPATH, wpt_path, 'example.yaml')

    # Step 1: Create a racetrack
    create_racetrack()

    # Step 2: Read the racetrack
    examplt_racetrack = read_racetrack()
    print(examplt_racetrack.to_dict())  # output the racetrack

    # Step 3: Run the trajectory planner
    run_traj_planner(config_path, quad_name, track_path, traj_path, wpt_path)

    # Step 4: Plot the trajectory
    plot_traj(traj_path, track_path)