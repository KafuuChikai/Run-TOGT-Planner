import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import Colormap
from run_togt_planner.RaceVisualizer.track import plot_track
from typing import Union, Optional

import os

BASEPATH = os.path.abspath(__file__).split("utils/", 1)[0]

# plot settings
matplotlib.rc('font', **{'size': 26})
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

class RacePlotter:
    def __init__(self,
                 traj_file: Union[os.PathLike, str],
                 track_file: Union[os.PathLike, str]):
        self.traj_file = os.fspath(traj_file)
        self.track_file = os.fspath(track_file)

        data_ocp = np.genfromtxt(traj_file, dtype=float, delimiter=',', names=True)
        self.t = data_ocp['t']
        self.p_x = data_ocp['p_x']
        self.p_y = data_ocp['p_y']
        self.p_z = data_ocp['p_z']
        self.q_w = data_ocp['q_w']
        self.q_x = data_ocp['q_x']
        self.q_y = data_ocp['q_y']
        self.q_z = data_ocp['q_z']
        self.v_x = data_ocp['v_x']
        self.v_y = data_ocp['v_y']
        self.v_z = data_ocp['v_z']
        self.w_x = data_ocp['w_x']
        self.w_y = data_ocp['w_y']
        self.w_z = data_ocp['w_z']
        self.u_1 = data_ocp['u_1']
        self.u_2 = data_ocp['u_2']
        self.u_3 = data_ocp['u_3']
        self.u_4 = data_ocp['u_4']

    def plot(self,
             cmap: Colormap = plt.cm.winter.reversed(),
             save_fig: bool = False,
             save_path: Union[os.PathLike, str] = None,
             fig_name: Optional[str] = None):
        fig = plt.figure(figsize=(13, 7))

        ts = np.linspace(self.t[0], self.t[-1], 5000)
        ps = np.array([
            np.interp(ts, self.t, self.p_x),
            np.interp(ts, self.t, self.p_y),
            np.interp(ts, self.t, self.p_z)
        ]).T
        # print("TOGT length:", np.sum(np.linalg.norm(ps[1:]-ps[:-1], axis=1)))
        vs = np.array([
            np.interp(ts, self.t, self.v_x),
            np.interp(ts, self.t, self.v_y),
            np.interp(ts, self.t, self.v_z)
        ]).T
        vs = np.linalg.norm(vs, axis=1)
        v0, v1 = 6.0, np.amax(vs)
        vt = np.minimum(np.maximum(vs, v0), v1)
        #vt = (vt-v0) / (v1-v0)
        r = 1.0 * (1-vt) + 1.0 * vt
        g = 1.0 * (1-vt) + 0.0 * vt
        b = 0.0 * (1-vt) + 0.0 * vt
        rgb = np.array([r, g, b]).T

        plt.scatter(ps[:, 0], ps[:, 1], s=5,
                    c=vt, cmap=cmap)
        plt.colorbar(pad=0.01).ax.set_ylabel('Speed [m/s]')

        plot_track(plt.gca(), self.track_file)

        plt.xlabel('x [m]')
        plt.ylabel('y [m]')
        plt.axis('equal')
        plt.grid()

        if save_fig:
            save_path = os.fspath(save_path) if save_path is not None else (BASEPATH + "resources/figure/")
            os.makedirs(save_path, exist_ok=True)
            fig_name = (fig_name + '.png') if fig_name is not None else 'togt_traj.png'
            plt.savefig(os.path.join(save_path, fig_name), bbox_inches='tight')

        plt.show()
