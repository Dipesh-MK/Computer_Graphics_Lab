import glfw
from OpenGL.GL import *

def plot_points(points, title="Plot", scale=8, grid_size=60):
    """points: list of (x, y) integer pixel coordinates centered at origin"""
    if not glfw.init():
        raise Exception("GLFW init failed")

    window_size = grid_size * scale
    window = glfw.create_window(window_size, window_size, title, None, None)
    if not window:
        glfw.terminate()
        raise Exception("Window creation failed")

    glfw.make_context_current(window)
    glOrtho(-grid_size/2, grid_size/2, -grid_size/2, grid_size/2, -1, 1)

    while not glfw.window_should_close(window):
        glClearColor(0.05, 0.05, 0.08, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        glColor3f(0.2, 0.8, 1.0)
        for x, y in points:
            glBegin(GL_QUADS)
            glVertex2f(x, y)
            glVertex2f(x + 1, y)
            glVertex2f(x + 1, y + 1)
            glVertex2f(x, y + 1)
            glEnd()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()