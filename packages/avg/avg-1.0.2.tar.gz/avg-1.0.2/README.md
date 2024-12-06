# *A*nimated Scalable *V*ector *G*raphics (SVG)

This library provides an easy way to make animations using the scalable vector
graphics (SVG) format.  SVG is a web-standard format and can be opened by all
modern web browsers.  An SVG can often be placed wherever any other image type
can be placed.  Even many email clients can view SVG animations.  This format
provides an easy way for others to view an animation without requiring any
additional software installation.

## Shapes

First, create your shapes with the `shape` class.  A shape object can be
initialized with the following parameters:

-   `x` **: float or array, default 0.0**
        x values of the shape or the x-axis radius of an ellipse.
-   `y` **: float or array, default 0.0**
        y values of the shape or the y-axis radius of an ellipse.
-   `stroke` **: float or array, default 1.0**
        Stroke width or animated widths.
-   `color` **: float or array, default 0x000000**
        Stroke or fill color or animated colors.  It is a fill color or colors
        if `stroke` is a scalar zero.
-   `alpha` **: float or array, default 1.0**
        Opacity or animated opacity values.  A 0.0 means fully transparent and a
        1.0 means fully opaque.
-   `dur` **: float, default 1.0**
        Animation duration in seconds.

Here is an example:

```python
theta = [2*m.pi*n/(100 - 1) for n in range(100)]
stroke = [0.5 + 0.3*m.sin(2*t) for t in theta]
color = [(cl(t) << 16) +
        (cl(t - 120*m.pi/180) << 8) +
        (cl(t + 120*m.pi/180)) for t in theta]
alpha = [0.6 + 0.4*m.cos(6*t) for t in theta]
tri = avg.shape([-1.0, 1.0, 0.0, -1.0], [-0.866, -0.866, 0.866, -0.866],
        stroke=stroke, color=color, alpha=alpha, dur=10)
```

In this example, the stroke, color, and alpha have all been made to change over
the period of 10 seconds.  The `cl( )` is just a custom triangle function.

## Frames

Second, place shapes or other frames into frames.  The `frame` class provides
the following initialization parameters:

-   `objs` **: shape or frame or list of such**
        A single shape or frame object or a list of such objects.
-   `x` **: float or array_like, default 0.0**
        x-axis values of translation of the objects within the frame.
-   `y` **: float or array_like, default 0.0**
        y-axis values of translation of the objects within the frame.
-   `ang` **: float or array_like, default 0.0**
        Angles of rotation of the objects within the frame in degrees.
-   `scale` **: float or array_like, default 1.0**
        Scaling factors of the objects within the frame.
-   `dur` **: float, default 1.0**
        Animation duration in seconds.

Here is an example:

```python
x = [2*m.sin(3*t) for t in theta]
y = [-m.cos(3*t) for t in theta]
ang = [-3*t*180/m.pi for t in theta]
scale = [1 + 0.5*m.sin(2*t) for t in theta]
frm = avg.frame(tri, x, y, ang, scale, dur=10)
```

So, the `tri` shape will move to the postions `(x, y)`, rotate to the angles
`ang`, and scale by `scale`.  You can put multiple shapes and frames into
another frame.  Suppose `a` and `b` are shapes and `C`, `D`, and `E` are frames.
These can be put into another frame as follows:

```python
frm = avg.frame([a, b, C, D, E], x, y, dur=10)
```

## Animate

When you have finished defining all your shapes and frames, you can create the
animation file using the `animate` function.  This function takes the following
paramters:

-   `obj` **: shape object, frame object, or list of such objects**
        The data to create an animation.
-   `filename` **: string, default 'ani.svg'**
        The desired name of output file.  End it with '.svg' in order for
        your system to know which application to use to open it.
-   `x_lim` **: array, default [-1, 1]**
        A list of the minimum and maximum x values to display in the animation.
-   `y_lim` **: array, default [-1, 1]**
        A list of the minimum and maximum y values to display in the animation.
-   `width` **: float, default 640**
        Desired width of the animation image in pixels.  This is also used in
        determining the scaling factor for the dimensions of the image.  If not
        specified, the image will actually automatically scale to fit the size
        of the browser window.
-   `progress` **: bool, default False**
        Flag to show progress bar.

Here is an example:

```python
avg.animate(frm, x_lim=[-3, 3], y_lim=[-3, 3])
```

Note that not specifying the width will make the image scale to the size of its
container, like the browser window.  However, it also means that parts of the
animation can sometimes be viewable outside the limits specified.
