import glfw
from OpenGL.GL import *
from OpenGL.GLUT import glutInit, glutBitmapCharacter, GLUT_BITMAP_HELVETICA_10

_glut_ready = False


def _ensure_glut():
    global _glut_ready
    if not _glut_ready:
        glutInit()
        _glut_ready = True


def _draw_text(x, y, text):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, ord(ch))


def _draw_grid(grid_size):

    half = grid_size / 2

    # Red grid lines, every unit
    glColor3f(1.0, 0.0, 0.0)
    glLineWidth(1)

    glBegin(GL_LINES)
    for i in range(-int(half), int(half) + 1):
        glVertex2f(i, -half)
        glVertex2f(i, half)
        glVertex2f(-half, i)
        glVertex2f(half, i)
    glEnd()

    # Bold black axes
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2)

    glBegin(GL_LINES)
    glVertex2f(-half, 0)
    glVertex2f(half, 0)
    glVertex2f(0, -half)
    glVertex2f(0, half)
    glEnd()

    glLineWidth(1)

    step = max(1, int(half) // 15)

    glColor3f(0.0, 0.0, 0.0)

    for i in range(-int(half), int(half) + 1, step):
        if i == 0:
            continue
        _draw_text(i - 0.3, -1.2, str(i))
        _draw_text(0.3, i - 0.3, str(i))

    _draw_text(0.3, -1.2, "0")


def _apply_projection(width, height, grid_size):
    """Update viewport + ortho so content fills the window on resize,
    without distorting the circle (aspect-corrected)."""

    if height == 0:
        height = 1

    glViewport(0, 0, width, height)

    aspect = width / height
    half = grid_size / 2

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if aspect >= 1:
        glOrtho(-half * aspect, half * aspect, -half, half, -1, 1)
    else:
        glOrtho(-half, half, -half / aspect, half / aspect, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def plot_points(points, title="Plot", scale=8, grid_size=60):
    """points: list of (x, y) integer pixel coordinates centered at origin"""
    if not glfw.init():
        raise Exception("GLFW init failed")

    # Antialiasing (multisampling) - must be requested before window creation
    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.RESIZABLE, True)

    window_size = grid_size * scale
    window = glfw.create_window(window_size, window_size, title, None, None)
    if not window:
        glfw.terminate()
        raise Exception("Window creation failed")

    glfw.make_context_current(window)

    def on_resize(win, width, height):
        _apply_projection(width, height, grid_size)

    glfw.set_framebuffer_size_callback(window, on_resize)

    # Initial projection setup (use framebuffer size, not window size,
    # to account for HiDPI/Retina scaling)
    fb_width, fb_height = glfw.get_framebuffer_size(window)
    _apply_projection(fb_width, fb_height, grid_size)

    _ensure_glut()

    # Smooth edges on lines and filled shapes
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)

    while not glfw.window_should_close(window):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        _draw_grid(grid_size)

        glColor4f(0.2, 0.4, 1.0, 0.95)
        for x, y in points:
            # Centered on the grid intersection (x, y), not offset to
            # the upper-right of it — this is what was making the
            # circle look shifted off-center.
            glBegin(GL_QUADS)
            glVertex2f(x - 0.5, y - 0.5)
            glVertex2f(x + 0.5, y - 0.5)
            glVertex2f(x + 0.5, y + 0.5)
            glVertex2f(x - 0.5, y + 0.5)
            glEnd()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()