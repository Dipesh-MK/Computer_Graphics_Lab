import glfw
import time

from OpenGL.GL import *
from OpenGL.GLU import gluPerspective
from OpenGL.GLUT import glutInit, glutBitmapCharacter, GLUT_BITMAP_HELVETICA_18


def init_window():
    if not glfw.init():
        raise Exception("GLFW initialization failed")

    window = glfw.create_window(800, 600, "VATH OpenGL Demo", None, None)

    if not window:
        glfw.terminate()
        raise Exception("Window creation failed")

    glfw.make_context_current(window)
    return window


def draw_cube():
    vertices = [
        (1, -1, -1),
        (1,  1, -1),
        (-1, 1, -1),
        (-1,-1, -1),
        (1, -1, 1),
        (1,  1, 1),
        (-1,-1, 1),
        (-1, 1, 1)
    ]

    colors = [
        (1,0,0),
        (0,1,0),
        (0,0,1),
        (1,1,0),
        (1,0,1),
        (0,1,1),
        (1,1,1),
        (0.5,0.5,0.5)
    ]

    faces = [
        (0,1,2,3),
        (3,2,7,6),
        (6,7,5,4),
        (4,5,1,0),
        (1,5,7,2),
        (4,0,3,6)
    ]

    glBegin(GL_QUADS)

    for face in faces:
        for vertex in face:
            glColor3fv(colors[vertex])
            glVertex3fv(vertices[vertex])

    glEnd()


def draw_text(x, y, text):
    # Save current matrices
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 800, 0, 600, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Disable depth testing so text stays visible
    glDisable(GL_DEPTH_TEST)

    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(x, y)

    for c in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    glEnable(GL_DEPTH_TEST)

    # Restore matrices
    glPopMatrix()

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit()

    window = init_window()

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800 / 600, 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, 0.0, -5)

    start_time = time.time()

    while not glfw.window_should_close(window):

        glClearColor(0.08, 0.08, 0.1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        elapsed = time.time() - start_time

        glPushMatrix()
        glRotatef(elapsed * 40, 1, 1, 0)
        draw_cube()
        glPopMatrix()

        # Draw text
        draw_text(360, 560, "VATH")

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()