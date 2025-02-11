import os
from run_togt_planner.RaceVisualizer.RacePlotter import RacePlotter
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import yaml

ROOTPATH = os.path.abspath(__file__).split("Run-TOGT-Planner/", 1)[0]
BASEPATH = os.path.dirname(os.path.abspath(__file__))

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

def main():
    # input parameters
    track_path = os.fspath("resources/racetrack")
    traj_path = os.fspath("../resources/trajectory")
    wpt_path = os.fspath("../resources/trajectory")
    fig_path = os.fspath("../resources/figure")

    os.makedirs(os.path.join(BASEPATH, traj_path), exist_ok=True)
    os.makedirs(os.path.join(BASEPATH, wpt_path), exist_ok=True)

    config_path = os.path.join(ROOTPATH, "parameters/cpc")
    quad_name = "cpc"
    track_path = os.path.join(ROOTPATH, track_path, 'race_uzh_19wp.yaml')
    traj_path = os.path.join(BASEPATH, traj_path, 'race_uzh_19wp.csv')
    wpt_path = os.path.join(BASEPATH, wpt_path, 'race_uzh_19wp.yaml')
    fig_path = os.path.join(BASEPATH, fig_path)

    run_traj_planner(config_path, quad_name, track_path, traj_path, wpt_path)

    togt_plotter = RacePlotter(traj_path, track_path, wpt_path)
    togt_plotter.plot(cmap=plt.cm.autumn.reversed(),
                    save_fig=True, 
                    fig_name="race_uzh_19wp_2d", 
                    save_path=fig_path,
                    radius=1.0,
                    margin=0.0,
                    draw_tube=True,
                    tube_color='purple')
    togt_plotter.plot3d(cmap=plt.cm.autumn.reversed(),
                        save_fig=True, 
                        fig_name="race_uzh_19wp_3d", 
                        save_path=fig_path,
                        radius=1.0,
                        margin=0.0,
                        gate_color='r',
                        draw_tube=True,
                        tube_color='purple',
                        sig_tube=True)
    togt_plotter.plot_show()

if __name__ == "__main__":
    main()