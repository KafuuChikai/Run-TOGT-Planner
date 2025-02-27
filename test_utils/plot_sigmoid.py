import numpy as np
import matplotlib.pyplot as plt

class RacePlotter:
    def sigmoid(self, 
                x: np.ndarray, 
                bias: float, 
                inner_radius: float, 
                outer_radius: float, 
                rate: float) -> np.ndarray:
        left_sigmoid = inner_radius + (outer_radius - inner_radius) * (1 / (1 + np.exp(-rate * (x - bias))))
        right_sigmoid = inner_radius + (outer_radius - inner_radius) * (1 / (1 + np.exp(rate * (x - (max(x) - bias)))))
        return np.minimum(left_sigmoid, right_sigmoid)

plotter = RacePlotter()

max_x = 4
x_values = np.linspace(0, max_x, 500)   # n > 4 * bias
y_values_1 = plotter.sigmoid(x_values, bias=0.5, inner_radius=0.25, outer_radius=1.0, rate=6)
# y_values_1 = plotter.sigmoid(x_values, bias=1.0, inner_radius=0.25, outer_radius=2.0, rate=6)
# y_values = plotter.sigmoid(x_values, bias=0.4, inner_radius=0.5, outer_radius=1, rate=12)
y_values_2 = np.zeros_like(x_values)

mid_scale = 0.5
end_scale = 0.6
change_percentage = 0.2 # 20% of max_x
for i, x in enumerate(x_values):
    if 0 <= x < max_x * change_percentage:
        y_values_2[i] = end_scale - ((end_scale - mid_scale) / (max_x * change_percentage)) * x
    elif max_x * change_percentage <= x < max_x * (1 - change_percentage):
        y_values_2[i] = mid_scale
    elif max_x * (1 - change_percentage) <= x <= max_x:
        y_values_2[i] = mid_scale + ((end_scale - mid_scale) / (max_x * change_percentage)) * (x - max_x * (1 - change_percentage))

plt.figure()
plt.plot(x_values, y_values_1, label="sigmoid", color="blue")
plt.plot(x_values, y_values_1 * y_values_2, label="sigmoid", color="red")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.ylim(0, 1)
plt.gca().set_aspect('equal', adjustable='box')
plt.title("Sigmoid Function")
plt.show()