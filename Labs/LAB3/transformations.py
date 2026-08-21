from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import sys
import threading


# ============================================================
# GLOBAL VARIABLES
# ============================================================

shape = None
points = []
original_points = []

circle_center = (0, 0)
circle_radius = 1

original_circle_center = (0, 0)
original_circle_radius = 1

window_width = 800
window_height = 800

redraw_needed = threading.Event()
should_exit = threading.Event()


# ============================================================
# TEXT HELPER
# ============================================================

def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, ord(ch))


# ============================================================
# DRAW COORDINATE GRAPH
# ============================================================

def draw_graph():

    glColor3f(1.0, 0.0, 0.0)
    glLineWidth(1)

    glBegin(GL_LINES)
    for i in range(-10, 11):
        glVertex2f(i, -10)
        glVertex2f(i, 10)
        glVertex2f(-10, i)
        glVertex2f(10, i)
    glEnd()

    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2)

    glBegin(GL_LINES)
    glVertex2f(-10, 0)
    glVertex2f(10, 0)
    glVertex2f(0, -10)
    glVertex2f(0, 10)
    glEnd()

    glLineWidth(1)
    glColor3f(0.0, 0.0, 0.0)

    for i in range(-10, 11):
        if i == 0:
            continue
        draw_text(i - 0.15, -0.4, str(i))
        draw_text(0.15, i - 0.1, str(i))

    draw_text(0.15, -0.4, "0")


# ============================================================
# DRAW SHAPE (blue = original, red = changed)
# ============================================================

def draw_shape():

    if shape in ("triangle", "square", "rectangle"):

        # Original - blue
        glColor3f(0.0, 0.0, 1.0)
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        for x, y in original_points:
            glVertex2f(x, y)
        glEnd()

        # Changed - red
        glColor3f(1.0, 0.0, 0.0)
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        for x, y in points:
            glVertex2f(x, y)
        glEnd()

    elif shape == "circle":

        # Original - blue
        ocx, ocy = original_circle_center
        glColor3f(0.0, 0.0, 1.0)
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        for i in range(100):
            angle = 2 * math.pi * i / 100
            x = ocx + original_circle_radius * math.cos(angle)
            y = ocy + original_circle_radius * math.sin(angle)
            glVertex2f(x, y)
        glEnd()

        # Changed - red
        cx, cy = circle_center
        glColor3f(1.0, 0.0, 0.0)
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        for i in range(100):
            angle = 2 * math.pi * i / 100
            x = cx + circle_radius * math.cos(angle)
            y = cy + circle_radius * math.sin(angle)
            glVertex2f(x, y)
        glEnd()

    glLineWidth(1)


# ============================================================
# LEGEND
# ============================================================

def draw_legend():

    glColor3f(0.0, 0.0, 1.0)
    draw_text(-9.5, 9.3, "Blue: Original")

    glColor3f(1.0, 0.0, 0.0)
    draw_text(-9.5, 8.7, "Red: Changed")


# ============================================================
# DISPLAY
# ============================================================

def display():

    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    draw_graph()
    draw_shape()
    draw_legend()

    glutSwapBuffers()


# ============================================================
# IDLE - runs on main thread, safe to touch GL/GLUT here
# ============================================================

def idle():

    if should_exit.is_set():
        glutLeaveMainLoop()
        return

    if redraw_needed.is_set():
        redraw_needed.clear()
        glutPostRedisplay()


# ============================================================
# CREATE SHAPES
# ============================================================

def create_triangle():

    cx = float(input("Enter center X: "))
    cy = float(input("Enter center Y: "))
    size = float(input("Enter triangle size: "))

    return [
        (cx, cy + size),
        (cx - size, cy - size),
        (cx + size, cy - size)
    ]


def create_square():

    cx = float(input("Enter center X: "))
    cy = float(input("Enter center Y: "))
    side = float(input("Enter square side length: "))

    half = side / 2

    return [
        (cx - half, cy - half),
        (cx + half, cy - half),
        (cx + half, cy + half),
        (cx - half, cy + half)
    ]


def create_rectangle():

    cx = float(input("Enter center X: "))
    cy = float(input("Enter center Y: "))
    length = float(input("Enter rectangle length: "))
    breadth = float(input("Enter rectangle breadth: "))

    half_l = length / 2
    half_b = breadth / 2

    return [
        (cx - half_l, cy - half_b),
        (cx + half_l, cy - half_b),
        (cx + half_l, cy + half_b),
        (cx - half_l, cy + half_b)
    ]


def create_circle():
    global circle_center, circle_radius

    cx = float(input("Enter circle center X: "))
    cy = float(input("Enter circle center Y: "))
    radius = float(input("Enter circle radius: "))

    circle_center = (cx, cy)
    circle_radius = radius

    return []


# ============================================================
# SELECT SHAPE
# ============================================================

def select_shape():

    global shape, points, original_points
    global original_circle_center, original_circle_radius

    print("\n================================")
    print("          SELECT SHAPE")
    print("================================")
    print("1. Triangle")
    print("2. Square")
    print("3. Rectangle")
    print("4. Circle")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        shape = "triangle"
        points = create_triangle()
        original_points = points.copy()
    elif choice == 2:
        shape = "square"
        points = create_square()
        original_points = points.copy()
    elif choice == 3:
        shape = "rectangle"
        points = create_rectangle()
        original_points = points.copy()
    elif choice == 4:
        shape = "circle"
        points = create_circle()
        original_points = points.copy()
        original_circle_center = circle_center
        original_circle_radius = circle_radius
    else:
        print("Invalid choice.")
        return False

    return True


# ============================================================
# TRANSFORMATIONS (pure data ops — no GL calls, thread-safe)
# ============================================================

def translation():

    global points, circle_center

    tx = float(input("Enter translation in X (tx): "))
    ty = float(input("Enter translation in Y (ty): "))

    if shape == "circle":
        cx, cy = circle_center
        circle_center = (cx + tx, cy + ty)
    else:
        points = [(x + tx, y + ty) for x, y in points]

    print("Translation applied.")


def rotation():

    global points, circle_center

    angle = float(input("Enter rotation angle in degrees: "))
    theta = math.radians(angle)
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)

    if shape == "circle":
        cx, cy = circle_center
        new_x = cx * cos_theta - cy * sin_theta
        new_y = cx * sin_theta + cy * cos_theta
        circle_center = (new_x, new_y)
    else:
        new_points = []
        for x, y in points:
            new_x = x * cos_theta - y * sin_theta
            new_y = x * sin_theta + y * cos_theta
            new_points.append((new_x, new_y))
        points = new_points

    print("Rotation applied.")


def scaling():

    global points, circle_radius, circle_center

    sx = float(input("Enter scaling factor in X (sx): "))
    sy = float(input("Enter scaling factor in Y (sy): "))

    if shape == "circle":
        cx, cy = circle_center
        circle_center = (cx * sx, cy * sy)
        circle_radius = circle_radius * ((abs(sx) + abs(sy)) / 2)
    else:
        points = [(x * sx, y * sy) for x, y in points]

    print("Scaling applied.")


def reflection():

    global points, circle_center

    print("\n================================")
    print("          REFLECTION")
    print("================================")
    print("1. Reflection about X-axis")
    print("2. Reflection about Y-axis")
    print("3. Reflection about Origin")

    choice = int(input("Enter your choice: "))

    if shape == "circle":

        cx, cy = circle_center

        if choice == 1:
            circle_center = (cx, -cy)
        elif choice == 2:
            circle_center = (-cx, cy)
        elif choice == 3:
            circle_center = (-cx, -cy)
        else:
            print("Invalid choice.")
            return

    else:

        new_points = []

        for x, y in points:
            if choice == 1:
                new_x, new_y = x, -y
            elif choice == 2:
                new_x, new_y = -x, y
            elif choice == 3:
                new_x, new_y = -x, -y
            else:
                print("Invalid choice.")
                return
            new_points.append((new_x, new_y))

        points = new_points

    print("Reflection applied.")


def reset():

    global points, circle_center, circle_radius

    points = original_points.copy()

    if shape == "circle":
        circle_center = original_circle_center
        circle_radius = original_circle_radius

    print("Shape reset to original position.")


# ============================================================
# TRANSFORMATION MENU — runs on a background thread
# ============================================================

def transformation_menu():

    while True:

        print("\n================================")
        print("       TRANSFORMATION MENU")
        print("================================")
        print("1. Translation")
        print("2. Rotation")
        print("3. Scaling")
        print("4. Reflection")
        print("5. Reset")
        print("6. Change Shape")
        print("7. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            translation()
        elif choice == 2:
            rotation()
        elif choice == 3:
            scaling()
        elif choice == 4:
            reflection()
        elif choice == 5:
            reset()
        elif choice == 6:
            select_shape()
        elif choice == 7:
            print("Exiting program...")
            should_exit.set()
            return
        else:
            print("Invalid choice.")

        # Signal the main (GL) thread to redraw — don't call GL here
        redraw_needed.set()


# ============================================================
# OPENGL INITIALIZATION
# ============================================================

def init():

    glClearColor(1.0, 1.0, 1.0, 1.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-10, 10, -10, 10)

    glMatrixMode(GL_MODELVIEW)


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n================================")
    print("       2D TRANSFORMATIONS")
    print("================================")

    while not select_shape():
        pass

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 50)
    glutCreateWindow(b"2D Transformation")

    init()

    glutDisplayFunc(display)
    glutIdleFunc(idle)

    # Console menu runs on a background thread; it never touches GL
    menu_thread = threading.Thread(target=transformation_menu, daemon=True)
    menu_thread.start()

    # GLUT owns the main thread — required on Windows
    glutMainLoop()


if __name__ == "__main__":
    main()