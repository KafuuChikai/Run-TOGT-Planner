import subprocess
import os

def run_traj_planner(quad_name, track_name, traj_name, wpt_name):
    # get the path to c++ program
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    cpp_program_path = os.path.join(base_dir, 'build', 'planners')

    # make sure the path exists
    if not os.path.isfile(cpp_program_path):
        print(f"Error: {cpp_program_path} does not exist.")
        return

    # construct the command
    command = [
        cpp_program_path,  # path to the C++ program
        quad_name,
        track_name,
        traj_name,
        wpt_name
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
    quad_name = "cpc"
    track_name = "race_uzh_7g_multiprisma.yaml"
    traj_name = "togt_traj.csv"
    wpt_name = "togt_wpt.yaml"

    # use c++ to generate trajectory
    run_traj_planner(quad_name, track_name, traj_name, wpt_name)