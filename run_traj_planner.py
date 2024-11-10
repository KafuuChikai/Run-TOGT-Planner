import subprocess
import os

def run_traj_planner(config_path, quad_name, track_path, traj_path, wpt_path):
    # get the path to c++ program
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    cpp_program_path = os.path.join(base_dir, 'build', 'planners')

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
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    config_path = os.fspath("parameters/cpc")
    quad_name = "cpc"
    track_path = os.fspath("Run-TOGT-Planner/resources/racetrack")
    traj_path = os.fspath("Run-TOGT-Planner/resources/planner/traj")
    wpt_path = os.fspath("Run-TOGT-Planner/resources/planner/wpt")
    os.makedirs(os.path.join(base_dir, traj_path), exist_ok=True)
    os.makedirs(os.path.join(base_dir, wpt_path), exist_ok=True)

    config_path = os.path.join(base_dir, config_path)
    track_path = os.path.join(base_dir, track_path, 'test.yaml')
    traj_path = os.path.join(base_dir, traj_path, 'togt_traj.csv')
    wpt_path = os.path.join(base_dir, wpt_path, 'togt_wpt.yaml')

    # use c++ to generate trajectory
    run_traj_planner(config_path, quad_name, track_path, traj_path, wpt_path)