import os
from run_togt_planner.RaceVisualizer.RacePlotter import RacePlotter
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import yaml

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

def main():
    # input parameters
    track_path = os.fspath("Run-TOGT-Planner/resources/racetrack")
    traj_path = os.fspath("Run-TOGT-Planner/resources/trajectory")
    wpt_path = os.fspath("Run-TOGT-Planner/resources/trajectory")
    fig_path = os.fspath("Run-TOGT-Planner/resources/figure")

    os.makedirs(os.path.join(ROOTPATH, traj_path), exist_ok=True)
    os.makedirs(os.path.join(ROOTPATH, wpt_path), exist_ok=True)

    config_path = os.path.join(ROOTPATH, "parameters/cpc")
    quad_name = "cpc"

    track_path = os.path.join(ROOTPATH, track_path, 'figure8.yaml')
    traj_path = os.path.join(ROOTPATH, traj_path, 'figure8.csv')
    wpt_path = os.path.join(ROOTPATH, wpt_path, 'figure8.yaml')
    fig_path = os.path.join(ROOTPATH, fig_path)

    run_traj_planner(config_path, quad_name, track_path, traj_path, wpt_path)

    radius = 0.25
    alpha = 0.01
    tube_rate = 10

    togt_plotter = RacePlotter(traj_path, track_path, wpt_path)
    togt_plotter.plot(cmap=plt.cm.autumn.reversed(),
                      save_fig=False, 
                      fig_name="figure8_2d", 
                      save_path=fig_path,
                      radius=radius,
                      width=2*radius,
                      height=2*radius,
                      margin=0.0,
                      draw_tube=False,
                      tube_color='purple', 
                      sig_tube=True,
                      alpha=alpha,
                      tube_rate=tube_rate)
    togt_plotter.plot3d(cmap=plt.cm.autumn.reversed(),
                        save_fig=False, 
                        fig_name="figure8_3d", 
                        save_path=fig_path,
                        radius=radius,
                        width=2*radius,
                        height=2*radius,
                        margin=0.0,
                        gate_color='r',
                        draw_tube=False,
                        tube_color='purple',
                        sig_tube=True,
                        alpha=alpha,
                        tube_rate=tube_rate)
    togt_plotter.plot_tube(scale=0.7,
                           sig_tube=True,
                           tube_color=[1.0, 0, 0], 
                           bias=2*radius, 
                           inner_radius=radius/2, 
                           outer_radius=radius*2,
                           alpha=0.008,
                           rate=tube_rate)
    togt_plotter.plot3d_tube(scale=0.7, 
                             sig_tube=True,
                             tube_color=[1.0, 0, 0], 
                             bias=2*radius, 
                             inner_radius=radius/2, 
                             outer_radius=radius*2,
                             alpha=0.008,
                             rate=tube_rate)
    # save the figure
    togt_plotter.save_2d_fig(fig_name="figure8_2d", save_path=fig_path)
    togt_plotter.save_3d_fig(fig_name="figure8_3d", save_path=fig_path)
    # togt_plotter.save_3d_fig(fig_name="figure8_3d", save_path=fig_path, hide_background=True, hide_ground=True)

    ###### Next track ######

    # input parameters
    track_path = os.fspath("Run-TOGT-Planner/resources/racetrack")
    traj_path = os.fspath("Run-TOGT-Planner/resources/trajectory")
    wpt_path = os.fspath("Run-TOGT-Planner/resources/trajectory")
    fig_path = os.fspath("Run-TOGT-Planner/resources/figure")

    os.makedirs(os.path.join(ROOTPATH, traj_path), exist_ok=True)
    os.makedirs(os.path.join(ROOTPATH, wpt_path), exist_ok=True)

    config_path = os.path.join(ROOTPATH, "parameters/cpc")
    quad_name = "cpc"

    track_path = os.path.join(ROOTPATH, track_path, 'race_uzh_19g.yaml')
    traj_path = os.path.join(ROOTPATH, traj_path, 'race_uzh_19g.csv')
    wpt_path = os.path.join(ROOTPATH, wpt_path, 'race_uzh_19g.yaml')
    fig_path = os.path.join(ROOTPATH, fig_path)

    run_traj_planner(config_path, quad_name, track_path, traj_path, wpt_path)

    radius = 1.0
    alpha = 0.04
    tube_rate = 4

    togt_plotter = RacePlotter(traj_path, track_path, wpt_path)
    togt_plotter.plot(cmap=plt.cm.cool_r,
                      save_fig=False, 
                      fig_name="race_uzh_19g_2d", 
                      save_path=fig_path,
                      radius=radius,
                      width=2*radius,
                      height=2*radius,
                      margin=0.0,
                      draw_tube=False,
                      tube_color='purple', 
                      sig_tube=True,
                      alpha=alpha,
                      tube_rate=tube_rate)
    togt_plotter.plot3d(cmap=plt.cm.cool_r,
                        save_fig=False, 
                        fig_name="race_uzh_19g_3d", 
                        save_path=fig_path,
                        radius=radius,
                        width=2*radius,
                        height=2*radius,
                        margin=0.0,
                        gate_color='r',
                        draw_tube=False,
                        tube_color='purple',
                        sig_tube=True,
                        alpha=alpha,
                        tube_rate=tube_rate)
    togt_plotter.plot_tube(scale=0.7,
                           sig_tube=True,
                           tube_color=[0, 0, 0.6], 
                           bias=2*radius, 
                           inner_radius=radius/2, 
                           outer_radius=radius*2,
                           alpha=0.03,
                           rate=tube_rate)
    togt_plotter.plot3d_tube(scale=0.7, 
                             sig_tube=True,
                             tube_color=[0, 0, 0.6], 
                             bias=2*radius, 
                             inner_radius=radius/2, 
                             outer_radius=radius*2,
                             alpha=0.03,
                             rate=tube_rate)
    # save the figure
    togt_plotter.save_2d_fig(fig_name='race_uzh_19g_2d', save_path=fig_path)
    togt_plotter.save_3d_fig(fig_name='race_uzh_19g_3d', save_path=fig_path)
    # togt_plotter.save_3d_fig(fig_name='race_uzh_19g_3d', save_path=fig_path, hide_background=True, hide_ground=True)

    togt_plotter.plot_show()

if __name__ == "__main__":
    main()