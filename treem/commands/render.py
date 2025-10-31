"""Implementation of CLI render command."""

import numpy as np

from treem import Morph, SWC
from treem.utils.geom import rotation

# pylint: disable=redefined-builtin

import OpenGL.GL as GL
import OpenGL.GLU as GLU
import OpenGL.GLUT as GLUT

from PIL import Image, ImageOps

_HELP = """
interactive commands:
    mouse left drag         rotate
    mouse right drag        translate

    Z/z     zoom in/out
    w       white background
    b       black background
    d       dark background
    p       show/hide points
    l       show/hide lines
    n       show/hide nodes
    s       show/hide segments
    W       write image to file
    h/?     help message
"""


class InteractionMatrix():
    """Class for object rotation and translation."""
    # pylint: disable=invalid-name
    def __init__(self):
        self.current_matrix = None
        self.reset()

    def reset(self):
        """Reset current matrix."""
        GL.glPushMatrix()
        GL.glLoadIdentity()
        self.current_matrix = GL.glGetFloatv(GL.GL_MODELVIEW_MATRIX)
        GL.glPopMatrix()

    def add_translation(self, x, y, z):
        """Shift scene by a vector."""
        GL.glPushMatrix()
        GL.glLoadIdentity()
        GL.glTranslatef(x, y, z)
        GL.glMultMatrixf(self.current_matrix)
        self.current_matrix = GL.glGetFloatv(GL.GL_MODELVIEW_MATRIX)
        GL.glPopMatrix()

    def add_rotation(self, angle, x, y, z):
        """Rotate scene around a vector."""
        GL.glPushMatrix()
        GL.glLoadIdentity()
        GL.glRotatef(angle, x, y, z)
        GL.glMultMatrixf(self.current_matrix)
        self.current_matrix = GL.glGetFloatv(GL.GL_MODELVIEW_MATRIX)
        GL.glPopMatrix()

    def get_current_matrix(self):
        """Return current matrix."""
        return self.current_matrix


class MouseInteractor():
    """Class for mouse control."""
    # pylint: disable=invalid-name
    def __init__(self, translation_scale=0.1, rotation_scale=0.2):
        self.scaling_factor_rotation = rotation_scale
        self.scaling_factor_translation = translation_scale
        self.rotation_matrix = InteractionMatrix()
        self.translation_matrix = InteractionMatrix()
        self.mouse_button_pressed = None
        self.old_mouse_pos = [0, 0]
        GLUT.glutMouseFunc(self.mouse_button)
        GLUT.glutMotionFunc(self.mouse_motion)

    def mouse_button(self, button, mode, x, y):
        """Detect button press."""
        if mode == GLUT.GLUT_DOWN:
            self.mouse_button_pressed = button
        else:
            self.mouse_button_pressed = None
        self.old_mouse_pos[0], self.old_mouse_pos[1] = x, y
        GLUT.glutPostRedisplay()

    def mouse_motion(self, x, y):
        """Detect mouse motion."""
        dx = x - self.old_mouse_pos[0]
        dy = y - self.old_mouse_pos[1]
        if self.mouse_button_pressed == GLUT.GLUT_RIGHT_BUTTON:
            tx = dx * self.scaling_factor_translation
            ty = dy * self.scaling_factor_translation
            self.translation_matrix.add_translation(tx, -ty, 0)
        elif self.mouse_button_pressed == GLUT.GLUT_LEFT_BUTTON:
            ry = dx * self.scaling_factor_rotation
            self.rotation_matrix.add_rotation(ry, 0, 1, 0)
            rx = dy * self.scaling_factor_rotation
            self.rotation_matrix.add_rotation(rx, 1, 0, 0)
        else:
            tz = dy * self.scaling_factor_translation
            self.translation_matrix.add_translation(0, 0, tz)
        self.old_mouse_pos[0], self.old_mouse_pos[1] = x, y
        GLUT.glutPostRedisplay()

    def apply(self):
        """Apply matrix manipulations."""
        GL.glMultMatrixf(self.translation_matrix.get_current_matrix())
        GL.glMultMatrixf(self.rotation_matrix.get_current_matrix())


class App:
    """Interactive application."""
    # pylint: disable=invalid-name
    # pylint: disable=too-many-instance-attributes
    def __init__(self, morph, title='render'):
        GLUT.glutInit()
        GLUT.glutInitDisplayMode(GLUT.GLUT_SINGLE | GLUT.GLUT_RGB | GLUT.GLUT_DEPTH)
        GLUT.glutInitWindowSize(1200, 900)
        GLUT.glutInitWindowPosition(100, 100)
        GLUT.glutCreateWindow(title)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glMatrixMode(GL.GL_MODELVIEW)

        GLUT.glutDisplayFunc(self.display)
        GLUT.glutKeyboardFunc(self.keyboard)

        morph.data[:, SWC.XYZ] -= morph.root.coord()
        self.cmin = morph.data[:, 2:5].min(axis=0)
        self.cmax = morph.data[:, 2:5].max(axis=0)

        self.mouse = MouseInteractor(0.1, 1.0)
        self.center = morph.root.coord()
        self.view_size = np.linalg.norm(self.cmax - self.cmin) / 4
        self.camera_dist = self.view_size
        self.camera_tilt = 30.0
        self.camera_rot = 30.0
        self.img_count = 0

        self.color = {
            'dark': (0.3, 0.3, 0.3),
            'white': (1.0, 1.0, 1.0),
            'black': (0.0, 0.0, 0.0),
            'axon': (0.6, 0.6, 0.6),
            'dend': (0.3, 0.5, 0.9),
            'apic': (1.0, 0.4, 0.6),
            'soma': (0.1, 0.3, 0.7),
        }
        red, green, blue = self.color['dark']
        GL.glClearColor(red, green, blue, 0)

        light_ambient = [0.5, 0.5, 0.5, 1.0]
        light_diffuse = [0.8, 0.8, 0.8, 1.0]
        light_position = [self.cmin[0], self.cmax[1], self.cmax[2], 0.0]

        GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT, light_ambient)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, light_diffuse)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, light_position)

        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_DEPTH_TEST)

        GL.glColorMaterial(GL.GL_FRONT, GL.GL_AMBIENT_AND_DIFFUSE)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_NORMALIZE)

        self.disp_points = self.genlist_points(morph)
        self.disp_lines = self.genlist_lines(morph)
        self.disp_nodes = self.genlist_nodes(morph)
        self.disp_segments = self.genlist_segments(morph)

        self.show_points = False
        self.show_lines = True
        self.show_nodes = True
        self.show_segments = True

    def set_nrncolor(self, objtype):
        """Change current color."""
        if objtype == 1:
            GL.glColor(self.color['soma'])
        elif objtype == 2:
            GL.glColor(self.color['axon'])
        elif objtype == 3:
            GL.glColor(self.color['dend'])
        elif objtype == 4:
            GL.glColor(self.color['apic'])
        else:
            GL.glColor3f(0.5, 0.5, 0.5)

    def genlist_points(self, morph):
        """Create display list for points."""
        disp_list = GL.glGenLists(1)
        GL.glNewList(disp_list, GL.GL_COMPILE)

        GL.glBegin(GL.GL_POINTS)
        self.set_nrncolor(morph.root.type())
        GL.glVertex(morph.root.coord())
        GL.glEnd()

        for stem in morph.stems():
            GL.glBegin(GL.GL_POINTS)
            self.set_nrncolor(stem.type())
            for node in stem.walk():
                GL.glVertex(node.coord())
            GL.glEnd()

        GL.glEndList()
        GL.glPointSize(3)
        return disp_list

    def genlist_lines(self, morph):
        """Create display list for lines."""
        disp_list = GL.glGenLists(1)
        GL.glNewList(disp_list, GL.GL_COMPILE)

        for stem in morph.stems():
            self.set_nrncolor(stem.type())
            for node in stem.walk():
                GL.glBegin(GL.GL_LINES)
                GL.glVertex(node.parent.coord())
                GL.glVertex(node.coord())
                GL.glEnd()

        GL.glEndList()
        return disp_list

    def genlist_nodes(self, morph):
        """Create display list for nodes."""
        disp_list = GL.glGenLists(1)
        GL.glNewList(disp_list, GL.GL_COMPILE)

        self.set_nrncolor(morph.root.type())
        nx, ny, nz = morph.root.coord()
        nr = morph.root.radius()
        GL.glPushMatrix()
        GL.glTranslatef(nx, ny, nz)
        GLUT.glutSolidSphere(nr, 8, 8)
        GL.glPopMatrix()

        for stem in morph.stems():
            self.set_nrncolor(stem.type())
            for node in stem.walk():
                nx, ny, nz = node.coord()
                nr = node.radius() * 0.95
                GL.glPushMatrix()
                GL.glTranslatef(nx, ny, nz)
                GLUT.glutSolidSphere(nr, 8, 8)
                GL.glPopMatrix()

        GL.glEndList()
        return disp_list

    def genlist_segments(self, morph):
        """Create display list for segments."""
        disp_list = GL.glGenLists(1)
        GL.glNewList(disp_list, GL.GL_COMPILE)

        for stem in morph.stems():
            self.set_nrncolor(stem.type())
            for node in stem.walk():
                nr = node.radius()
                px, py, pz = node.parent.coord()
                pr = node.parent.radius()
                GL.glPushMatrix()
                GL.glTranslatef(px, py, pz)
                axis, angle = rotation(
                    (0.0, 0.0, 1.0), node.coord() - node.parent.coord())
                rx, ry, rz = axis
                GL.glRotate(angle / np.pi * 180, rx, ry, rz)
                GLU.gluCylinder(GLU.gluNewQuadric(), pr, nr, node.length(), 8, 1)
                GL.glPopMatrix()

        GL.glEndList()
        return disp_list

    def display(self):
        """Display callback function."""
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        width, height = GL.glGetFloatv(GL.GL_VIEWPORT)[2:4]
        aspect = width / height
        total_size = np.linalg.norm(self.cmax - self.cmin)
        GL.glOrtho((self.center[0] - self.view_size) * aspect,
                (self.center[0] + self.view_size) * aspect,
                self.center[1] - self.view_size,
                self.center[1] + self.view_size,
                -total_size, total_size)
        GL.glTranslate(0.0, 0.0, -self.camera_dist)
        GL.glRotate(self.camera_tilt, 1.0, 0.0, 0.0)
        GL.glRotate(self.camera_rot, 0.0, 1.0, 0.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        self.mouse.apply()

        if self.show_points:
            GL.glCallList(self.disp_points)
        if self.show_lines:
            GL.glCallList(self.disp_lines)
        if self.show_nodes:
            GL.glCallList(self.disp_nodes)
        if self.show_segments:
            GL.glCallList(self.disp_segments)

        GL.glFlush()

    def write_img(self):
        """Save image buffer to file."""
        # pylint: disable=no-value-for-parameter
        GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)
        width, height = GL.glGetFloatv(GL.GL_VIEWPORT).astype(int)[2:4]
        data = GL.glReadPixels(0, 0, width, height, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE)
        image = Image.frombytes('RGBA', (width, height), data)
        image = ImageOps.flip(image)
        self.img_count += 1
        image.save(f'render_{self.img_count}.png', 'PNG')

    def keyboard(self, key, x, y):  # pylint: disable=unused-argument
        """Keyboard callback function."""
        key = key.decode('UTF-8')
        if key == 'z':
            self.view_size *= 1.1
        elif key == 'Z':
            self.view_size *= 0.9
        elif key == 'w':
            red, green, blue = self.color['white']
            GL.glClearColor(red, green, blue, 0)
        elif key == 'b':
            red, green, blue = self.color['black']
            GL.glClearColor(red, green, blue, 0)
        elif key == 'd':
            red, green, blue = self.color['dark']
            GL.glClearColor(red, green, blue, 0)
        elif key == 'p':
            self.show_points = not self.show_points
        elif key == 'l':
            self.show_lines = not self.show_lines
        elif key == 'n':
            self.show_nodes = not self.show_nodes
        elif key == 's':
            self.show_segments = not self.show_segments
        elif key == 'W':
            self.write_img()
        elif key in ('h', '?'):
            print(_HELP)
        GLUT.glutPostRedisplay()

    def run(self):
        """Enter event processing loop."""
        GLUT.glutMainLoop()


def render(args):
    """Shows 3D model of morphology reconstruction."""
    morph = Morph(args.file)
    app = App(morph, title=args.file)
    app.run()
