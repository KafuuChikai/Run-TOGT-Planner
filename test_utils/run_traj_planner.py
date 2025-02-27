import subprocess
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from run_togt_planner.RaceVisualizer.RacePlotter import RacePlotter

ROOTPATH = os.path.abspath(__file__).split("Run-TOGT-Planner/", 1)[0]

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

if __name__ == "__main__":
    # input parameters
    BASEPATH = os.path.abspath(__file__).split("Run-TOGT-Planner/", 1)[0]
    config_path = os.fspath("parameters/cpc")
    quad_name = "cpc"
    track_path = os.fspath("Run-TOGT-Planner/resources/racetrack")
    traj_path = os.fspath("Run-TOGT-Planner/resources/trajectory")
    wpt_path = os.fspath("Run-TOGT-Planner/resources/trajectory")

    os.makedirs(os.path.join(ROOTPATH, traj_path), exist_ok=True)
    os.makedirs(os.path.join(ROOTPATH, wpt_path), exist_ok=True)

    config_path = os.path.join(ROOTPATH, config_path)
    track_path = os.path.join(ROOTPATH, track_path, 'example.yaml')
    traj_path = os.path.join(ROOTPATH, traj_path, 'example.csv')
    wpt_path = os.path.join(ROOTPATH, wpt_path, 'example.yaml')

    # use c++ to generate trajectory
    run_traj_planner(config_path, quad_name, track_path, traj_path, wpt_path)

    togt_plotter = RacePlotter(traj_path, track_path)
    togt_plotter.plot(save_fig=True, fig_name="example", save_path=os.path.join(ROOTPATH, "Run-TOGT-Planner/resources/figure/"))