import numpy as np
import yaml


def rpy_to_rotation_matrix(rpy):
    r, p, y = np.array(rpy) * np.pi/180
    cos, sin = np.cos, np.sin
    R = np.eye(3)
    R[0, 0] = cos(y) * cos(p)
    R[1, 0] = sin(y) * cos(p)
    R[2, 0] = -sin(p)
    R[0, 1] = cos(y) * sin(p) * sin(r) - sin(y) * cos(r)
    R[1, 1] = sin(y) * sin(p) * sin(r) + cos(y) * cos(r)
    R[2, 1] = cos(p) * sin(r)
    R[0, 2] = cos(y) * sin(p) * cos(r) + sin(y) * sin(r)
    R[1, 2] = sin(y) * sin(p) * cos(r) - cos(y) * sin(r)
    R[2, 2] = cos(p) * cos(r)
    return R


def plot_track(ax, track_file, radius=None, margin=None):
    with open(track_file) as fp:
        track = yaml.safe_load(fp)

    for g in track['orders']:
        g = track[g]

        if g['type'] == 'FreeCorridor':
            raise NotImplementedError("Not support plotting FreeCorridor gate")

        args = {
            'linewidth': 3.0,
            'markersize': 5.0,
            'color': 'black'
        }

        if g['type'] == 'SingleBall':
            position = g['position']
            # r = g['radius'] - g['margin']
            r = g['radius']
            if radius is not None and margin is not None:
                r = np.clip(radius - margin, 0, None)
            a = np.linspace(0, 2*np.pi)
            ax.plot(position[0]+r*np.cos(a),
                    position[1]+r*np.sin(a), '-', **args)
            # draw center
            ax.scatter(position[0], position[1], color='black', s=50)

        elif g['type'] == 'TrianglePrisma':
            position = g['position']
            R = rpy_to_rotation_matrix(g['rpy'])
            # hw = 0.5*(g['width']-g['margin'])
            # hh = 0.5*(g['height']-g['margin'])
            hw = 0.5*g['width']
            hh = 0.5*g['height']
            drift = 0.0
            verts = [
                [-hh, hw, drift],
                [hh, 0.0, drift],
                [-hh, -hw, drift],
                [-hh, hw, drift]
            ] @ R.T + np.array(position).reshape((1,3))
            ax.plot(verts[:,0], verts[:,1], 'o-', **args)

        elif g['type'] == 'RectanglePrisma':
            position = g['position']
            R = rpy_to_rotation_matrix(g['rpy'])
            # hw = 0.5*(g['width']-g['marginW'])
            # hh = 0.5*(g['height']-g['marginH'])
            hw = 0.5*g['width']
            hh = 0.5*g['height']
            drift = 0.0
            verts = [
                [-hh, hw, drift],
                [-hh, -hw, drift],
                [hh, -hw, drift],
                [hh, hw, drift],
                [-hh, hw, drift]
            ] @ R.T + np.array(position).reshape((1,3))
            ax.plot(verts[:,0], verts[:,1], 'o-', **args)

        elif g['type'] == 'PentagonPrisma':
            position = g['position']
            R = rpy_to_rotation_matrix(g['rpy'])
            # ar = g['radius'] - g['margin']
            ar = g['radius']
            cos54 = np.cos(0.3*np.pi)
            sin54 = np.sin(0.3*np.pi)
            nd, on = ar * cos54, ar * sin54
            bc = 2 * nd
            fc = bc * sin54
            of = ar - bc * cos54
            drift = 0.0
            verts = [
                [-on, nd, drift],
                [of, fc, drift],
                [ar, 0.0, drift],
                [of, -fc, drift],
                [-on, -nd, drift],
                [-on, nd, drift]
            ] @ R.T + np.array(position).reshape((1,3))
            ax.plot(verts[:,0], verts[:,1], 'o-', **args)

        elif g['type'] == 'HexagonPrisma':
            position = g['position']
            R = rpy_to_rotation_matrix(g['rpy'])
            # aside = g['side'] - g['margin']
            aside = g['side']
            hside = 0.5 * aside
            height = hside * np.tan(np.pi/3.0)
            drift = 0.0
            verts = [
                [-height, hside, drift],
                [0.0, aside, drift],
                [height, hside, drift],
                [height, -hside, drift],
                [0.0, -aside, drift],
                [-height, -hside, drift],
                [-height, hside, drift]
            ] @ R.T + np.array(position).reshape((1,3))
            ax.plot(verts[:,0], verts[:,1], 'o-', **args)

        else:
            raise ValueError('Unrecognized gate: ' + g['type'])
        
def plot_track_3d(ax, track_file, radius=None, margin=None, color=None):
    if color is None:
        color = 'r'

    with open(track_file) as fp:
        track = yaml.safe_load(fp)

    for g in track['orders']:
        g = track[g]

        if g['type'] == 'FreeCorridor':
            raise NotImplementedError("Not support plotting FreeCorridor gate")

        args = {
            'linewidth': 3.0,
            'markersize': 5.0,
            'color': 'black'
        }

        if g['type'] == 'SingleBall':
            position = g['position']
            r = g['radius'] - g['margin']
            if radius is not None and margin is not None:
                r = np.clip(radius - margin, 0, None)

            # create sphere
            u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
            x = position[0] + r * np.cos(u) * np.sin(v)
            y = position[1] + r * np.sin(u) * np.sin(v)
            z = position[2] + r * np.cos(v)
            # draw sphere
            ax.plot_surface(x, y, z, color=color, alpha=0.3, edgecolor='none')
            # draw center
            ax.scatter(position[0], position[1], position[2], color='black', s=50)
            
        elif g['type'] == 'TrianglePrisma':
            position = g['position']
            R = rpy_to_rotation_matrix(g['rpy'])
            # hw = 0.5*(g['width']-g['margin'])
            # hh = 0.5*(g['height']-g['margin'])
            hw = 0.5*g['width']
            hh = 0.5*g['height']
            drift = 0.0
            verts = [
                [-hh, hw, drift],
                [hh, 0.0, drift],
                [-hh, -hw, drift],
                [-hh, hw, drift]
            ] @ R.T + np.array(position).reshape((1,3))
            ax.plot(verts[:,0], verts[:,1], verts[:,2], 'o-', **args)

        elif g['type'] == 'RectanglePrisma':
            position = g['position']
            R = rpy_to_rotation_matrix(g['rpy'])
            # hw = 0.5*(g['width']-g['marginW'])
            # hh = 0.5*(g['height']-g['marginH'])
            hw = 0.5*g['width']
            hh = 0.5*g['height']
            drift = 0.0
            verts = [
                [-hh, hw, drift],
                [-hh, -hw, drift],
                [hh, -hw, drift],
                [hh, hw, drift],
                [-hh, hw, drift]
            ] @ R.T + np.array(position).reshape((1,3))
            ax.plot(verts[:,0], verts[:,1], verts[:,2], 'o-', **args)

        elif g['type'] == 'PentagonPrisma':
            position = g['position']
            R = rpy_to_rotation_matrix(g['rpy'])
            # ar = g['radius'] - g['margin']
            ar = g['radius']
            cos54 = np.cos(0.3*np.pi)
            sin54 = np.sin(0.3*np.pi)
            nd, on = ar * cos54, ar * sin54
            bc = 2 * nd
            fc = bc * sin54
            of = ar - bc * cos54
            drift = 0.0
            verts = [
                [-on, nd, drift],
                [of, fc, drift],
                [ar, 0.0, drift],
                [of, -fc, drift],
                [-on, -nd, drift],
                [-on, nd, drift]
            ] @ R.T + np.array(position).reshape((1,3))
            ax.plot(verts[:,0], verts[:,1], verts[:,2], 'o-', **args)

        elif g['type'] == 'HexagonPrisma':
            position = g['position']
            R = rpy_to_rotation_matrix(g['rpy'])
            # aside = g['side'] - g['margin']
            aside = g['side']
            hside = 0.5 * aside
            height = hside * np.tan(np.pi/3.0)
            drift = 0.0
            verts = [
                [-height, hside, drift],
                [0.0, aside, drift],
                [height, hside, drift],
                [height, -hside, drift],
                [0.0, -aside, drift],
                [-height, -hside, drift],
                [-height, hside, drift]
            ] @ R.T + np.array(position).reshape((1,3))
            ax.plot(verts[:,0], verts[:,1], verts[:,2], 'o-', **args)

        else:
            raise ValueError('Unrecognized gate: ' + g['type'])
