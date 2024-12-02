import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# define the sigmoid function
def sigmoid(x, bias, max_scale):
    return 1 + max_scale*(-1/(1 + np.exp(bias)) + 1/(1 + np.exp(-(x - bias))))

# reward to the center
def reward_function_center(x, y, target_x, target_y):
    distance = np.sqrt((x - target_x)**2 + (y - target_y)**2)
    direction_x = (target_x - x) / (distance + 1e-5)
    direction_y = (target_y - y) / (distance + 1e-5)
    return direction_x, direction_y

# reward to the ball
def reward_function_ball(x, y, target_x, target_y, ball_radius=0.75):
    distance = np.sqrt((x - target_x)**2 + (y - target_y)**2)
    direction_angle = np.zeros_like(distance)
    direction_angle[distance > ball_radius] = np.arcsin(ball_radius / distance[distance > ball_radius])
    # select the direction of the ball, right or left
    k = np.ones_like(distance)
    k[x > y] = -1
    current_angle = np.pi + np.arctan2((x - target_x), (y - target_y))
    angle = current_angle + k * direction_angle
    direction_x = np.sin(angle)
    direction_y = np.cos(angle)
    return direction_x, direction_y

# reward to the direction
def reward_function_direction(x, y, target_x, target_y, bias, max_scale, wp_radius_tore, wp_radius=1.0):
    # compute the center direction
    distance = np.sqrt((x - target_x)**2 + (y - target_y)**2)
    center_direction_x = (target_x - x) / (distance + 1e-5)
    center_direction_y = (target_y - y) / (distance + 1e-5)    
    
    # set the track direction
    angle = np.ones_like(x)*-3*np.pi/4
    track_direction_x = np.sin(angle)
    track_direction_y = np.cos(angle)

    # calculate the track scale with sigmoid function
    current_angle = np.arctan2((x - target_x), (y - target_y))
    track_bias = distance * abs(np.sin(current_angle - np.pi / 4))
    track_lang = distance * abs(np.cos(current_angle - np.pi / 4))
    track_scale = sigmoid(track_lang, bias, max_scale)

    # compute the weight of the total direction
    wp_tore = wp_radius_tore * wp_radius
    k = np.ones_like(distance)
    k[track_bias > wp_tore * track_scale] = 1 - (np.clip((track_bias/track_scale)[track_bias > wp_tore * track_scale] / wp_radius, 
                                                         None, 1) - wp_radius_tore) / (1 - wp_radius_tore)
    k = k**2

    # compute the direction with the weight
    direction_x = k * track_direction_x + (1-k) * center_direction_x
    direction_y = k * track_direction_y + (1-k) * center_direction_y
    direction_x[np.logical_and(x+y<-8, distance>1)] = center_direction_x[np.logical_and(x+y<-8, distance>1)]
    direction_y[np.logical_and(x+y<-8, distance>1)] = center_direction_y[np.logical_and(x+y<-8, distance>1)]
    return direction_x, direction_y, k

# calculate the angle between the direction and the track
def calculate_angle(U, V, start_x, start_y, target_x, target_y, x, y, wp_radius=1.0):
    line_x = target_x - start_x
    line_y = target_y - start_y
    direction_x = target_x - x
    direction_y = target_y - y

    # calculate the distance
    distance = np.sqrt((x - target_x)**2 + (y - target_y)**2)

    # calculate the direction angle
    direction_angle = np.ones_like(distance)*np.pi
    direction_angle[distance > wp_radius] = np.arcsin(wp_radius / distance[distance > wp_radius])

    dot_product = U * line_x + V * line_y
    magnitude_UV = np.sqrt(U**2 + V**2)
    magnitude_line = np.sqrt(line_x**2 + line_y**2)
    magnitude_direction = np.sqrt(direction_x**2 + direction_y**2)
    cos_theta = dot_product / (magnitude_UV * magnitude_line + 1e-5)
    bias_angle = np.arccos(abs(U * direction_x + V * direction_y) / (magnitude_UV * magnitude_direction + 1e-5))
    cos_theta[bias_angle > direction_angle] = 0
    return cos_theta

# define the range of the plot and the resolution
x_min, x_max, y_min, y_max = -8, 4, -8, 4
# x_min, x_max, y_min, y_max = -6, -2, -6, -2
# resolution = 30
resolution = 200
# arraw_scale = 30
arraw_scale = 70

# set the color map and the normalization
norm = Normalize(vmin=np.sqrt(3)/2, vmax=1.0)
# norm = Normalize(vmin=-1.0, vmax=1.0)
# norm = Normalize(vmin=0, vmax=1)

# generate the mesh grid
x = np.linspace(x_min, x_max, resolution)
y = np.linspace(y_min, y_max, resolution)
X, Y = np.meshgrid(x, y)

# set the start and target point
start_x, start_y = -2.5, -2.5
target_x, target_y = -4, -4
bias = 3
max_scale = 2
wp_radius_tore = 0.3
wp_radius = 1.0

# 45 degree line
line_x = np.linspace(x_min, x_max, resolution)
line_y = line_x

# compute the track side line and inner line with sigmoid function
distance = np.sqrt((x - target_x)**2 + (y - target_y)**2)
current_angle = np.arctan2((x - target_x), (y - target_y))
track_bias = distance * abs(np.sin(current_angle - np.pi / 4))
track_lang = distance * abs(np.cos(current_angle - np.pi / 4))
track_scale = sigmoid(track_lang, bias, max_scale)
track_scale_inner = wp_radius_tore * track_scale
# The track side line
X_up = line_x - track_scale / np.sqrt(2)
Y_up = line_y + track_scale / np.sqrt(2)
X_down = line_x + track_scale / np.sqrt(2)
Y_down = line_y - track_scale / np.sqrt(2)
select_plot_up = np.logical_and(np.logical_and(X_up > x_min, X_up < x_max), 
                                np.logical_and(Y_up > y_min, Y_up < y_max))
select_plot_down = np.logical_and(np.logical_and(X_down > x_min, X_down < x_max), 
                                  np.logical_and(Y_down > y_min, Y_down < y_max))
# The track inner line
X_up_inner = line_x - track_scale_inner / np.sqrt(2)
Y_up_inner = line_y + track_scale_inner / np.sqrt(2)
X_down_inner = line_x + track_scale_inner / np.sqrt(2)
Y_down_inner = line_y - track_scale_inner / np.sqrt(2)
select_plot_up_inner = np.logical_and(np.logical_and(X_up_inner > x_min, X_up_inner < x_max), 
                                      np.logical_and(Y_up_inner > y_min, Y_up_inner < y_max))
select_plot_down_inner = np.logical_and(np.logical_and(X_down_inner > x_min, X_down_inner < x_max), 
                                        np.logical_and(Y_down_inner > y_min, Y_down_inner < y_max))

# compute the gate
gate_x = [target_x + wp_radius / np.sqrt(2), target_x - wp_radius / np.sqrt(2)]
gate_y = [target_y - wp_radius / np.sqrt(2), target_y + wp_radius / np.sqrt(2)]

#######################################
##### Plot the Center reward flow #####
#######################################
# compute the reward direction
U, V = reward_function_center(X, Y, target_x, target_y)
# compute the angle and the flow value
cos_angles = calculate_angle(U, V, start_x, start_y, target_x, target_y, X, Y)

# plot the reward flow
plt.figure(figsize=(8, 6))
plt.quiver(X, Y, U, V, cos_angles, cmap='viridis', scale=arraw_scale, norm=norm)
plt.colorbar(label='Reward Value center')
# plot the track side line and inner line
plt.plot(X_up[select_plot_up], Y_up[select_plot_up], color='black', linewidth=2)
plt.plot(X_down[select_plot_down], Y_down[select_plot_down], color='black', linewidth=2)
plt.plot(X_up_inner[select_plot_up_inner], Y_up_inner[select_plot_up_inner], color='r', linewidth=2)
plt.plot(X_down_inner[select_plot_down_inner], Y_down_inner[select_plot_down_inner], color='r', linewidth=2)
# plot the start point
plt.scatter(start_x, start_y, color='b', marker='x', s=100, label='Start')
# plot the target point (gate)
plt.plot(gate_x, gate_y, color='black', linewidth=5, label='Goal')
# plot the target point (center)
circle = plt.Circle((target_x, target_y), 1.0, color='red', fill=False, linestyle='--', linewidth=2)
plt.gca().add_patch(circle)
# plot the 45 degree line
plt.plot(line_x, line_y, linestyle=':', color='red', label='guide Line')
# set the label and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Center: Reward Flow on X-Y Plane')

#######################################
###### Plot the Ball reward flow ######
#######################################
# compute the reward direction
U, V = reward_function_ball(X, Y, target_x, target_y)
# compute the angle and the flow value
angles = calculate_angle(U, V, start_x, start_y, target_x, target_y, X, Y)
rewards = angles
# plot the reward flow outside the ball
distance_mesh = np.sqrt((X - target_x)**2 + (Y - target_y)**2)
# visualize the reward flow
plt.figure(figsize=(8, 6))
plt.quiver(X[distance_mesh>0.75], 
           Y[distance_mesh>0.75], 
           U[distance_mesh>0.75], 
           V[distance_mesh>0.75], 
           rewards[distance_mesh>0.75], 
           cmap='viridis', scale=arraw_scale, norm=norm)
plt.colorbar(label='Reward Value ball')
# plot the track side line and inner line
plt.plot(X_up[select_plot_up], Y_up[select_plot_up], color='black', linewidth=2)
plt.plot(X_down[select_plot_down], Y_down[select_plot_down], color='black', linewidth=2)
plt.plot(X_up_inner[select_plot_up_inner], Y_up_inner[select_plot_up_inner], color='r', linewidth=2)
plt.plot(X_down_inner[select_plot_down_inner], Y_down_inner[select_plot_down_inner], color='r', linewidth=2)
# plot the start point
plt.scatter(start_x, start_y, color='b', marker='x', s=100, label='Start')
# plot the target point (gate)
plt.plot(gate_x, gate_y, color='black', linewidth=5, label='Goal')
# plot the target point (center)
circle = plt.Circle((target_x, target_y), 1.0, color='red', fill=False, linestyle='--', linewidth=2)
plt.gca().add_patch(circle)
# plot the 45 degree line
plt.plot(line_x, line_y, linestyle=':', color='red', label='guide Line')
# set the label and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Ball: Reward Flow on X-Y Plane')

#######################################
###### Plot the Track reward flow #####
#######################################
# compute the reward direction and the weight
U, V, K = reward_function_direction(X, Y, target_x, target_y, 
                                    bias=bias, 
                                    max_scale=max_scale, 
                                    wp_radius_tore=wp_radius_tore, 
                                    wp_radius=wp_radius)

# compute the angle and the flow value
angles = calculate_angle(U, V, start_x, start_y, target_x, target_y, X, Y)
# select the flow value
rewards = angles
# rewards = K

# visualize the reward flow
plt.figure(figsize=(8, 6))
plt.quiver(X, Y, U, V, rewards, cmap='viridis', scale=arraw_scale, norm=norm)
plt.colorbar(label='Reward Value direction')
# plot the track side line and inner line
plt.plot(X_up[select_plot_up], Y_up[select_plot_up], color='black', linewidth=2)
plt.plot(X_down[select_plot_down], Y_down[select_plot_down], color='black', linewidth=2)
plt.plot(X_up_inner[select_plot_up_inner], Y_up_inner[select_plot_up_inner], color='r', linewidth=2)
plt.plot(X_down_inner[select_plot_down_inner], Y_down_inner[select_plot_down_inner], color='r', linewidth=2)
# plot the start point
plt.scatter(start_x, start_y, color='b', marker='x', s=100, label='Start')
# plot the target point (gate)
plt.plot(gate_x, gate_y, color='black', linewidth=5, label='Goal')
# plot the target point (center)
circle = plt.Circle((target_x, target_y), 1.0, color='red', fill=False, linestyle='--', linewidth=2)
plt.gca().add_patch(circle)
# plot the 45 degree line
plt.plot(line_x, line_y, linestyle=':', color='red', label='guide Line')
# set the label and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Reward Flow on X-Y Plane')

plt.show()