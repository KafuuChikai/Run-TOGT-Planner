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

# input parameters
track_path = os.fspath("../resources/racetrack")
traj_path = os.fspath("../resources/trajectory")
wpt_path = os.fspath("../resources/trajectory")
fig_path = os.fspath("../resources/figure")

track_path = os.path.join(BASEPATH, track_path, 'race_uzh_19wp.yaml')
traj_path = os.path.join(BASEPATH, traj_path, 'race_uzh_19wp.csv')
wpt_path = os.path.join(BASEPATH, wpt_path, 'race_uzh_19wp.yaml')
fig_path = os.path.join(BASEPATH, fig_path)

togt_plotter = RacePlotter(traj_path, track_path)
togt_plotter.plot(cmap=plt.cm.autumn.reversed(),
                    save_fig=True, 
                    fig_name="race_uzh_19wp", 
                    save_path=fig_path)
