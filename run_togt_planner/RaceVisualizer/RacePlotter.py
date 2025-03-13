import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import Colormap, ListedColormap
import matplotlib.ticker as ticker
from run_togt_planner.RaceVisualizer.track import plot_track, plot_track_3d
from typing import Union, Optional, Tuple
import yaml

import os
import warnings

ROOTPATH = os.path.abspath(__file__).split("Run-TOGT-Planner/", 1)[0]

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
        v0, v1 = (np.amin(vs) + 2 * np.amax(vs)) / 3, np.amax(vs)
        vt = np.minimum(np.maximum(vs, v0), v1)

        self.ts = ts
        self.ps = ps
        self.vs = vs
        self.vt = vt

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
             width: Optional[float] = None,
             height: Optional[float] = None,
             margin: Optional[float] = None,
             draw_tube: bool = False,
             sig_tube: bool = False,
             tube_color: Optional[str] = None,
             alpha: float = 0.01,
             tube_rate: float = 6):
        fig = plt.figure(figsize=(8, 6))
        ax = plt.gca()
        self.ax_2d = ax

        ps = self.ps
        vt = self.vt

        if draw_tube:
            if not sig_tube:
                self.plot_tube(sig_tube=sig_tube, tube_color=tube_color, alpha=alpha, tube_radius=radius)
            else:
                self.plot_tube(sig_tube=sig_tube, tube_color=tube_color, alpha=alpha, bias=1.5*radius, inner_radius=radius/2, outer_radius=1.5*radius, rate=tube_rate)

        plt.scatter(ps[:, 0], ps[:, 1], s=5,
                    c=vt, cmap=cmap)
        plt.colorbar(pad=0.01).ax.set_ylabel('Speed [m/s]')

        plot_track(plt.gca(), self.track_file, set_radius=radius, set_width=width, set_height=height, set_margin=margin)

        plt.xlabel('x [m]')
        plt.ylabel('y [m]')
        plt.axis('equal')
        plt.grid()

        if save_fig:
            save_path = os.fspath(save_path) if save_path is not None else os.path.join(ROOTPATH, "Run-TOGT-Planner/resources/figure/")
            os.makedirs(save_path, exist_ok=True)
            fig_name = (fig_name + '.png') if fig_name is not None else 'togt_traj.png'
            plt.savefig(os.path.join(save_path, fig_name), bbox_inches='tight')

    def plot_tube(self,
                  scale: float = 1.0,
                  sig_tube: bool = False,
                  tube_color: Optional[str] = None,
                  alpha: float = 0.01,
                  tube_edge_color: Optional[str] = None,
                  tube_radius: float = 1.0,
                  bias: float = 1.0,
                  inner_radius: float = 0.5,
                  outer_radius: float = 2.0,
                  rate: float = 6):

        ax = self.ax_2d
        ts = self.ts
        ps = self.ps

        # set tube color
        if tube_color is None:
            tube_color = 'purple'
        if tube_edge_color is None:
            tube_edge_color = tube_color

        # compute tube coordinates
        if not sig_tube:
            tube_x, tube_y, tube_z = self.get_line_tube(ps, tube_radius)
        else:
            tube_x, tube_y, tube_z = self.get_sig_tube(ts, ps, bias=bias, inner_radius=inner_radius, outer_radius=outer_radius, rate=rate, scale=scale)

        # plot tube
        single_color_map = ListedColormap([tube_color])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            ax.pcolormesh(tube_x, tube_y, tube_z, cmap=single_color_map, shading='auto', color=tube_color, edgecolor='none', alpha=alpha, antialiased=True)

    def plot3d(self,
               cmap: Colormap = plt.cm.winter.reversed(),
               save_fig: bool = False,
               save_path: Union[os.PathLike, str] = None,
               fig_name: Optional[str] = None,
               radius: Optional[float] = None,
               width: Optional[float] = None,
               height: Optional[float] = None,
               margin: Optional[float] = None,
               draw_tube: bool = False,
               sig_tube: bool = False,
               gate_color: Optional[str] = None,
               tube_color: Optional[str] = None,
               alpha: float = 0.01,
               tube_rate: float = 6,
               shade: bool = True):
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_axes([0, 0, 1, 1], projection='3d')

        # set aspect ratio
        x_range = self.ps[:, 0].max() - self.ps[:, 0].min()
        y_range = self.ps[:, 1].max() - self.ps[:, 1].min()
        z_range = self.ps[:, 2].max() - self.ps[:, 2].min()
        max_range = max(x_range, y_range, z_range)
        min_range_factor = 0.33
        x_range = max(x_range, max_range * min_range_factor)
        y_range = max(y_range, max_range * min_range_factor)
        z_range = max(z_range, max_range * min_range_factor)
        ax.set_box_aspect((x_range, y_range, z_range))

        # compute ticks
        x_ticks_count = max(min(int(x_range), 5), 3)
        y_ticks_count = max(min(int(y_range), 5), 3)
        z_ticks_count = max(min(int(z_range), 5), 3)

        # set ticks
        self.set_nice_ticks(ax, x_range, x_ticks_count, 'x')
        self.set_nice_ticks(ax, y_range, y_ticks_count, 'y')
        self.set_nice_ticks(ax, z_range, z_ticks_count, 'z')

        self.ax_3d = ax

        ps = self.ps
        vt = self.vt

        # draw tube
        if draw_tube:
            if not sig_tube:
                self.plot3d_tube(sig_tube=sig_tube, tube_color=tube_color, alpha=alpha, tube_radius=radius, shade=shade)
            else:
                self.plot3d_tube(sig_tube=sig_tube, tube_color=tube_color, alpha=alpha, bias=1.5*radius, inner_radius=radius/2, outer_radius=1.5*radius, rate=tube_rate, shade=shade)

        # plot trajectory
        sc = ax.scatter(ps[:, 0], ps[:, 1], ps[:, 2], s=5, c=vt, cmap=cmap)
        shrink_factor = min(0.8, max(0.6, 0.6 * y_range / x_range))
        colorbar_aspect = 20 * shrink_factor
        cbar = plt.colorbar(sc, shrink=shrink_factor, aspect=colorbar_aspect, pad=0.1)
        cbar.ax.set_ylabel('Speed [m/s]')

        plot_track_3d(plt.gca(), self.track_file, set_radius=radius, set_width=width, set_height=height, set_margin=margin, color=gate_color)

        ax.set_xlabel('x [m]', labelpad=30*(x_range/max_range))
        ax.set_ylabel('y [m]', labelpad=30*(y_range/max_range))
        ax.set_zlabel('z [m]', labelpad=30*(z_range/max_range)) 
        plt.axis('equal')
        plt.grid()

        if save_fig:
            save_path = os.fspath(save_path) if save_path is not None else os.path.join(ROOTPATH, "Run-TOGT-Planner/resources/figure/")
            os.makedirs(save_path, exist_ok=True)
            fig_name = (fig_name + '.png') if fig_name is not None else 'togt_traj.png'
            plt.savefig(os.path.join(save_path, fig_name), bbox_inches='tight')

    def plot3d_tube(self,
                    scale: float = 1.0,
                    sig_tube: bool = False,
                    tube_color: Optional[str] = None,
                    alpha: float = 0.01,
                    tube_edge_color: Optional[str] = None,
                    tube_radius: float = 1.0,
                    bias: float = 1.0,
                    inner_radius: float = 0.5,
                    outer_radius: float = 2.0,
                    rate: float = 6,
                    shade: bool = True):

        ax = self.ax_3d
        ts = self.ts
        ps = self.ps

        # set tube color
        if tube_color is None:
            tube_color = 'purple'
        if tube_edge_color is None:
            tube_edge_color = tube_color

        # compute tube coordinates
        if not sig_tube:
            tube_x, tube_y, tube_z = self.get_line_tube(ps, tube_radius)
        else:
            tube_x, tube_y, tube_z = self.get_sig_tube(ts, ps, bias=bias, inner_radius=inner_radius, outer_radius=outer_radius, rate=rate, scale=scale)

        # plot tube
        ax.plot_surface(tube_x, tube_y, tube_z, color=tube_color, alpha=alpha, edgecolor=tube_edge_color, shade=shade, antialiased=True)

    def set_nice_ticks(self, ax, range_val, ticks_count, axis='x'):
        ticks_interval = range_val / (ticks_count - 1)

        # select base value for major ticks
        if range_val <= 1:
            base = round(ticks_interval / 0.1) * 0.1
        elif range_val <= 5:
            base = round(ticks_interval / 0.5) * 0.5
        elif range_val <= 10:
            base = round(ticks_interval / 1.0) * 1.0
        else:
            base = int(max(1.0, round(range_val / 5)))
        
        # set locator
        locator = ticker.MultipleLocator(base)
        
        # apply locator
        if axis == 'x':
            ax.xaxis.set_major_locator(locator)
        elif axis == 'y':
            ax.yaxis.set_major_locator(locator)
        else:  # 'z'
            ax.zaxis.set_major_locator(locator)