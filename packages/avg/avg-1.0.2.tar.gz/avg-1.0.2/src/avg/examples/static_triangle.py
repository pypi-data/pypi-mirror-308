import math as m
import avg

# Static graphic.

o = avg.shape(1.0, 1.0, stroke=0)
s = avg.shape([-1.0, 1.0, 0.0, -1.0], [-0.866, -0.866, 0.866, -0.866],
    stroke=2.0, color=0x007fff, alpha=0.8)
f = avg.frame(s, x=3.0, y=2.0, ang=45.0, scale=0.1)
avg.animate([o, f], "static_triangle.svg", x_lim=[-10, 10], y_lim=[-10, 10])
