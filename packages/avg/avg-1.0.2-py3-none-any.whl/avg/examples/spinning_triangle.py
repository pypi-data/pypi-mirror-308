import math as m
import avg

def cl(t):
    x = t/(2*m.pi)
    return 255 - int(512*abs(x - m.floor(x + 0.5)))

# Dynamic animation.

theta = [2*m.pi*n/(100 - 1) for n in range(100)]
stroke = [0.5 + 0.3*m.sin(2*t) for t in theta]
color = [(cl(t) << 16) +
        (cl(t - 120*m.pi/180) << 8) +
        (cl(t + 120*m.pi/180)) for t in theta]
alpha = [0.6 + 0.4*m.cos(6*t) for t in theta]
tri = avg.shape([-1.0, 1.0, 0.0, -1.0], [-0.866, -0.866, 0.866, -0.866],
        stroke=stroke, color=color, alpha=alpha, dur=10)
x = [2*m.sin(3*t) for t in theta]
y = [-m.cos(3*t) for t in theta]
ang = [-3*t*180/m.pi for t in theta]
scale = [1 + 0.5*m.sin(2*t) for t in theta]
frm = avg.frame(tri, x, y, ang, scale, dur=10)

avg.animate(frm, "spinning_triangle.svg", x_lim=[-3, 3], y_lim=[-3, 3])
