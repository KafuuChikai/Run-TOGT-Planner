import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import Colormap
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from run_togt_planner.RaceVisualizer.track import plot_track, plot_track_3d
from typing import Union, Optional, Tuple
import yaml
from scipy.spatial.distance import cdist

import os

BASEPATH = os.path.abspath(__file__).split("utils/", 1)[0]

# plot settings
matplotlib.rc('font', **{'size': 26})
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

class RacePlotter:
    def __init__(self,
                 traj_file: Union[os.PathLike, str],
                 track_file: Union[os.PathLike, str],
                 wpt_path: Optional[Union[os.PathLike, str]] = None):
        self.traj_file = os.fspath(traj_file)
        self.track_file = os.fspath(track_file)
        if wpt_path is not None:
            self.wpt_path = os.fspath(wpt_path)

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

    def estimate_tangents(self, 
                          ps : np.ndarray) -> np.ndarray:
        # compute tangents
        dp_x = np.gradient(ps[:, 0])
        dp_y = np.gradient(ps[:, 1])
        dp_z = np.gradient(ps[:, 2])
        tangents = np.vstack((dp_x, dp_y, dp_z)).T
        # normalize tangents
        tangents /= np.linalg.norm(tangents, axis=1).reshape(-1, 1)
        return tangents
    
    def sigmoid(self, 
                x : np.ndarray, 
                bias : float, 
                inner_radius : float,
                outer_radius : float,
                rate : float) -> np.ndarray:
        # return 1 + max_scale*(-1/(1 + np.exp(bias)) + 1/(1 + np.exp(-(x - bias))))/(1 - 1/(1 + np.exp(bias)))
        return inner_radius + outer_radius * (1 / (1 + np.exp(- rate * (x - bias))))
    
    def plot_show(self):
        plt.show()

    def get_line_tube(self, 
                      ps : np.ndarray, 
                      tube_radius : float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        # create tube parameters
        num_points = len(ps)
        theta = np.linspace(0, 2 * np.pi, 20)
        circle_x = tube_radius * np.cos(theta)
        circle_y = tube_radius * np.sin(theta)
        tangent = self.estimate_tangents(ps)

        # initialize tube coordinates array
        tube_x = np.zeros((num_points, len(theta)))
        tube_y = np.zeros((num_points, len(theta)))
        tube_z = np.zeros((num_points, len(theta)))

        # compute tangents and normals for building tube cross-section
        for i in range(num_points):
            # choose an arbitrary vector not parallel to the tangent
            arbitrary_vector = np.array([1, 0, 0]) if not np.allclose(tangent[i], [1, 0, 0]) else np.array([0, 1, 0])

            normal = np.cross(tangent[i], arbitrary_vector)
            normal /= np.linalg.norm(normal)
            binormal = np.cross(tangent[i], normal)

            # construct orthogonal basis matrix
            TNB = np.column_stack((normal, binormal, tangent[i]))

            # for each cross-section, compute points on the circle
            for j in range(len(theta)):
                local_point = np.array([circle_x[j], circle_y[j], 0])
                global_point = ps[i] + TNB @ local_point
                tube_x[i, j] = global_point[0]
                tube_y[i, j] = global_point[1]
                tube_z[i, j] = global_point[2]
        
        return tube_x, tube_y, tube_z
    
    def get_sig_tube(self, 
                     ts : np.ndarray,
                     ps : np.ndarray, 
                     bias : float,
                     inner_radius : float,
                     outer_radius : float,
                     rate : float,
                     scale: float = 1.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        if self.wpt_path is None:
            raise ValueError("wpt_path is not provided.")
        with open(self.wpt_path, 'r') as file:
            wpt_data = yaml.safe_load(file)
        with open(self.track_file, 'r') as file:
            track_data = yaml.safe_load(file)
        
        wps = np.array([wpt_data['waypoints']]).reshape(-1, 3)
        wps_t = np.array([wpt_data['timestamps']]).flatten()

        # search for the next waypoints
        indices = np.searchsorted(wps_t[:-1], ts, side='right').astype(int)
        dist1 = np.linalg.norm(ps - wps[indices - 1], axis=1)
        dist2 = np.linalg.norm(ps - wps[indices], axis=1)
        min_distances = np.minimum(dist1, dist2)

        tube_size = self.sigmoid(min_distances, bias, inner_radius, outer_radius, rate)  # 根据距离计算 tube 半径
        tube_size = tube_size * scale  # 缩放 tube 半径
        
        theta = np.linspace(0, 2 * np.pi, 20)
        tangent = self.estimate_tangents(ps)

        # initialize tube coordinates array
        num_points = len(ps)
        tube_x = np.zeros((num_points, len(theta)))
        tube_y = np.zeros((num_points, len(theta)))
        tube_z = np.zeros((num_points, len(theta)))

        # compute tangents and normals for building tube cross-section
        for i in range(num_points):
            # compute circle points
            circle_x = tube_size[i] * np.cos(theta)
            circle_y = tube_size[i] * np.sin(theta)
            # choose an arbitrary vector not parallel to the tangent
            arbitrary_vector = np.array([1, 0, 0]) if not np.allclose(tangent[i], [1, 0, 0]) else np.array([0, 1, 0])

            normal = np.cross(tangent[i], arbitrary_vector)
            normal /= np.linalg.norm(normal)
            binormal = np.cross(tangent[i], normal)

            # construct orthogonal basis matrix
            TNB = np.column_stack((normal, binormal, tangent[i]))

            # for each cross-section, compute points on the circle
            for j in range(len(theta)):
                local_point = np.array([circle_x[j], circle_y[j], 0])
                global_point = ps[i] + TNB @ local_point
                tube_x[i, j] = global_point[0]
                tube_y[i, j] = global_point[1]
                tube_z[i, j] = global_point[2]
        
        return tube_x, tube_y, tube_z

    def plot(self,
             cmap: Colormap = plt.cm.winter.reversed(),
             save_fig: bool = False,
             save_path: Union[os.PathLike, str] = None,
             fig_name: Optional[str] = None,
             radius: Optional[float] = None,
             margin: Optional[float] = None,
             draw_tube: bool = False,
             sig_tube: bool = False,
             tube_color: Optional[str] = None):
        fig = plt.figure(figsize=(13, 7))

        ts = np.linspace(self.t[0], self.t[-1], 5000)
        ps = np.array([
            np.interp(ts, self.t, self.p_x),
            np.interp(ts, self.t, self.p_y),
            np.interp(ts, self.t, self.p_z)
        ]).T
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

        if draw_tube:
            path_data = []
            codes = []
            for i, p in enumerate(ps):
                if i % 10 == 0:
                    circle = plt.Circle((p[0], p[1]), 1.0, edgecolor='none', facecolor='none')
                    vertices = circle.get_path().transformed(circle.get_transform()).vertices
                    path_data.extend(vertices)
                    codes.extend([Path.MOVETO] + [Path.LINETO] * (len(vertices) - 2) + [Path.CLOSEPOLY])

            path_data = np.array(path_data)
            path = Path(path_data, codes)

            if tube_color is None:
                tube_color = 'purple'
            patch = PathPatch(path, facecolor=tube_color, edgecolor=tube_color, alpha=0.15)
            plt.gca().add_patch(patch)

        plt.scatter(ps[:, 0], ps[:, 1], s=5,
                    c=vt, cmap=cmap)
        plt.colorbar(pad=0.01).ax.set_ylabel('Speed [m/s]')

        plot_track(plt.gca(), self.track_file, radius=radius, margin=margin)

        plt.xlabel('x [m]')
        plt.ylabel('y [m]')
        plt.axis('equal')
        plt.grid()

        if save_fig:
            save_path = os.fspath(save_path) if save_path is not None else (BASEPATH + "resources/figure/")
            os.makedirs(save_path, exist_ok=True)
            fig_name = (fig_name + '.png') if fig_name is not None else 'togt_traj.png'
            plt.savefig(os.path.join(save_path, fig_name), bbox_inches='tight')

    def plot3d(self,
               cmap: Colormap = plt.cm.winter.reversed(),
               save_fig: bool = False,
               save_path: Union[os.PathLike, str] = None,
               fig_name: Optional[str] = None,
               radius: Optional[float] = None,
               margin: Optional[float] = None,
               draw_tube: bool = False,
               sig_tube: bool = False,
               gate_color: Optional[str] = None,
               tube_color: Optional[str] = None):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ts = np.linspace(self.t[0], self.t[-1], 5000)
        ps = np.array([
            np.interp(ts, self.t, self.p_x),
            np.interp(ts, self.t, self.p_y),
            np.interp(ts, self.t, self.p_z)
        ]).T
        vs = np.array([
            np.interp(ts, self.t, self.v_x),
            np.interp(ts, self.t, self.v_y),
            np.interp(ts, self.t, self.v_z)
        ]).T
        vs = np.linalg.norm(vs, axis=1)
        v0, v1 = 6.0, np.amax(vs)
        vt = np.minimum(np.maximum(vs, v0), v1)
        
        # draw tube
        if draw_tube:
            tube_radius = 1.0
            if tube_color is None:
                tube_color = 'purple'
                # tube_color_ = 'green'
            if not sig_tube:
                tube_x, tube_y, tube_z = self.get_line_tube(ps, tube_radius)
            else:
                # tube_x, tube_y, tube_z = self.get_sig_tube(ts, ps, bias=1.0, inner_radius=0.5, outer_radius=2.0, rate=3)
                # race_mini_uzh_19g
                tube_x, tube_y, tube_z = self.get_sig_tube(ts, ps, bias=0.5, inner_radius=0.125, outer_radius=0.5, rate=6)
                tube_x_, tube_y_, tube_z_ = self.get_sig_tube(ts, ps, bias=0.5, inner_radius=0.125, outer_radius=0.5, rate=6, scale=0.5)
            ax.plot_surface(tube_x, tube_y, tube_z, color=tube_color, alpha=0.05, edgecolor=tube_color)
            ax.plot_surface(tube_x_, tube_y_, tube_z_, color='green', alpha=0.05, edgecolor='green')

        # plot trajectory
        sc = ax.scatter(ps[:, 0], ps[:, 1], ps[:, 2], s=5, c=vt, cmap=cmap)
        plt.colorbar(sc).ax.set_ylabel('Speed [m/s]')

        plot_track_3d(plt.gca(), self.track_file, radius=radius, margin=margin, color=gate_color)

        plt.xlabel('x [m]')
        plt.ylabel('y [m]')
        # plt.axis('equal')
        self.set_axes_equal(ax)
        plt.grid()
        ax.view_init(elev=90, azim=-90)

        if save_fig:
            save_path = os.fspath(save_path) if save_path is not None else (BASEPATH + "resources/figure/")
            os.makedirs(save_path, exist_ok=True)
            fig_name = (fig_name + '.png') if fig_name is not None else 'togt_traj.png'
            plt.savefig(os.path.join(save_path, fig_name), bbox_inches='tight')

    
    def set_axes_equal(self, ax):
        """Set 3D plot axes to equal scale."""
        x_limits = ax.get_xlim3d()
        y_limits = ax.get_ylim3d()
        z_limits = ax.get_zlim3d()

        x_range = abs(x_limits[1] - x_limits[0])
        y_range = abs(y_limits[1] - y_limits[0])
        z_range = abs(z_limits[1] - z_limits[0])

        max_range = max(x_range, y_range, z_range)

        mid_x = np.mean(x_limits)
        mid_y = np.mean(y_limits)
        mid_z = np.mean(z_limits)

        ax.set_xlim3d([mid_x - max_range / 2, mid_x + max_range / 2])
        ax.set_ylim3d([mid_y - max_range / 2, mid_y + max_range / 2])
        ax.set_zlim3d([mid_z - max_range / 2, mid_z + max_range / 2])