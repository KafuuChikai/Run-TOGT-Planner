import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import Colormap
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from mpl_toolkits.mplot3d.art3d import PathPatch3D
from scipy.spatial import ConvexHull
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
        ax = fig.add_subplot(111, projection='3d')

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

        # tangents = self.estimate_tangents()
        # plt.quiver(ps[:, 0], ps[:, 1], tangents[:, 0], tangents[:, 1], color='r', scale=10)
        # for i, p in enumerate(ps):
        #     if i % 10 == 0:
        #         circle = plt.Circle((p[0], p[1]), 1.0, color='gray', alpha=0.02)
        #         plt.gca().add_patch(circle)

        # path_data = []
        # codes = []
        # for i, p in enumerate(ps):
        #     if i % 10 == 0:
        #         circle = plt.Circle((p[0], p[1], p[2]), 1.0, edgecolor='none', facecolor='none')
        #         vertices = circle.get_path().transformed(circle.get_transform()).vertices
        #         path_data.extend(vertices)
        #         codes.extend([Path.MOVETO] + [Path.LINETO] * (len(vertices) - 2) + [Path.CLOSEPOLY])

        # path_data = np.array(path_data)
        # path = Path(path_data, codes)
        # patch = PathPatch3D(path, facecolor='purple', edgecolor='gray', alpha=0.3)
        # plt.gca().add_patch(patch)

        # 创建包含所有球体的路径
        # u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        # sphere_radius = 1.0
        # sphere_x = sphere_radius * np.cos(u) * np.sin(v)
        # sphere_y = sphere_radius * np.sin(u) * np.sin(v)
        # sphere_z = sphere_radius * np.cos(v)

        # for i, p in enumerate(ps):
        #     if i % 10 == 0:
        #         x = p[0] + sphere_x
        #         y = p[1] + sphere_y
        #         z = p[2] + sphere_z
        #         ax.plot_surface(x, y, z, color='purple', alpha=0.3, edgecolor='gray')
        # 收集所有球体的顶点
        # all_vertices = []
        # for i, p in enumerate(ps):
        #     if i % 10 == 0:
        #         x = p[0] + sphere_x
        #         y = p[1] + sphere_y
        #         z = p[2] + sphere_z
        #         all_vertices.append(np.vstack((x.flatten(), y.flatten(), z.flatten())).T)

        # all_vertices = np.vstack(all_vertices)
        
        # # 确保有足够的唯一点来计算包络面
        # if len(np.unique(all_vertices, axis=0)) >= 3:
        #     # 计算包络面
        #     hull = ConvexHull(all_vertices)
        #     # 使用所有顶点和三角形一次性绘制包络面
        #     ax.plot_trisurf(all_vertices[:, 0], all_vertices[:, 1], all_vertices[:, 2],
        #                     triangles=hull.simplices, color='purple', alpha=0.3, edgecolor='none')
        
        tube_radius = 1.0
        # 创建管道的参数化
        num_points = len(ps)
        theta = np.linspace(0, 2 * np.pi, 20)
        circle_x = tube_radius * np.cos(theta)
        circle_y = tube_radius * np.sin(theta)

        # 初始化管道的坐标数组
        tube_x = np.zeros((num_points, len(theta)))
        tube_y = np.zeros((num_points, len(theta)))
        tube_z = np.zeros((num_points, len(theta)))

        # 计算切线和法线，用于构建管道截面
        for i in range(num_points):
            if i < num_points - 1:
                tangent = ps[i + 1] - ps[i]
            else:
                tangent = ps[i] - ps[i - 1]
            tangent /= np.linalg.norm(tangent)

            # 选择一个任意向量，不与切线平行
            arbitrary_vector = np.array([1, 0, 0]) if not np.allclose(tangent, [1, 0, 0]) else np.array([0, 1, 0])

            normal = np.cross(tangent, arbitrary_vector)
            normal /= np.linalg.norm(normal)
            binormal = np.cross(tangent, normal)

            # 组成正交基矩阵
            TNB = np.column_stack((normal, binormal, tangent))

            # 对于每个截面，计算圆周上的点
            for j in range(len(theta)):
                local_point = np.array([circle_x[j], circle_y[j], 0])
                global_point = ps[i] + TNB @ local_point
                tube_x[i, j] = global_point[0]
                tube_y[i, j] = global_point[1]
                tube_z[i, j] = global_point[2]

        # 绘制管道表面
        ax.plot_surface(tube_x, tube_y, tube_z, color='purple', alpha=0.3, edgecolor='none')

        ax.scatter(ps[:, 0], ps[:, 1], ps[:, 2], s=5,
                    c=vt, cmap=cmap)
        # plt.colorbar(pad=0.01).ax.set_ylabel('Speed [m/s]')

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

    def estimate_tangents(self):
        ts = np.linspace(self.t[0], self.t[-1], 5000)
        ps = np.array([
            np.interp(ts, self.t, self.p_x),
            np.interp(ts, self.t, self.p_y),
            np.interp(ts, self.t, self.p_z)
        ]).T
        # 计算每个点的切线方向
        dp_x = np.gradient(ps[:, 0])
        dp_y = np.gradient(ps[:, 1])
        dp_z = np.gradient(ps[:, 2])
        tangents = np.vstack((dp_x, dp_y, dp_z)).T
        # 归一化切线方向
        tangents /= np.linalg.norm(tangents, axis=1).reshape(-1, 1)
        # tangents *= 10
        return tangents
    
    def sigmoid(x, bias, max_scale):
        return 1 + max_scale*(-1/(1 + np.exp(bias)) + 1/(1 + np.exp(-(x - bias))))/(1-1/(1 + np.exp(bias)))