import subprocess
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.RaceVisualizer.RacePlotter import RacePlotter

def run_traj_planner(config_path, quad_name, track_path, traj_path, wpt_path):
    # get the path to c++ program
    ROOTPATH = os.path.abspath(__file__).split("Run-TOGT-Planner/", 1)[0]
    
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

if __name__ == "__main__":
    # input parameters
    BASEPATH = ROOTPATH = os.path.abspath(__file__).split("Run-TOGT-Planner/", 1)[0]
    config_path = os.fspath("parameters/cpc")
    quad_name = "cpc"
    track_path = os.fspath("Run-TOGT-Planner/resources/racetrack")
    traj_path = os.fspath("Run-TOGT-Planner/resources/trajectory")
    wpt_path = os.fspath("Run-TOGT-Planner/resources/trajectory")

    os.makedirs(os.path.join(BASEPATH, traj_path), exist_ok=True)
    os.makedirs(os.path.join(BASEPATH, wpt_path), exist_ok=True)

    config_path = os.path.join(BASEPATH, config_path)
    track_path = os.path.join(BASEPATH, track_path, 'test.yaml')
    traj_path = os.path.join(BASEPATH, traj_path, 'togt_traj.csv')
    wpt_path = os.path.join(BASEPATH, wpt_path, 'togt_wpt.yaml')

    # use c++ to generate trajectory
    run_traj_planner(config_path, quad_name, track_path, traj_path, wpt_path)

    togt_plotter = RacePlotter(traj_path, track_path)
    togt_plotter.plot(save_fig=True, fig_name="togt_traj", save_path=os.path.join(BASEPATH, "resources/figure/"))