"""
 Simulation of a rotating 3D Cube
 Developed by Leonel Machava <leonelmachava@gmail.com>

 http://codeNtronix.com
"""
import sys, math, pygame
from operator import itemgetter

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from quad.motor import calculate_dc_for_motor


class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = float(x), float(y), float(z)
 
    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)
 
    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)
 
    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)
 
    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, self.z)


class Simulation:
    def __init__(self, win_width = 640, win_height = 480):
        pygame.init()

        self.screen = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption("Drone")
        
        self.clock = pygame.time.Clock()

        self.drone_vertices = [
            Point3D(-1,5,0),
            Point3D(1,5,0),
            Point3D(1,1,0),
            Point3D(5,1,0),
            Point3D(5,-1,0),
            Point3D(1,-1,0),
            Point3D(1,-5,0),
            Point3D(-1,-5,0),
            Point3D(-1,-1,0),
            Point3D(-5,-1,0),
            Point3D(-5,1,0),
            Point3D(-1,1,0),
        ]

        # TODO fix Rotate the initial position of the drone
        for k, v in enumerate(self.drone_vertices):
            self.drone_vertices[k] = v.rotateZ(-45)

        self.floor_vertices = [
            Point3D(-5, -5, 3),
            Point3D(-5, 5, 3),
            Point3D(5, 5, 3),
            Point3D(5, -5, 3),
        ]

        self.vertices = []
        self.vertices.extend(self.drone_vertices)
        self.vertices.extend(self.floor_vertices)

        self.vertices_to_draw = []

        # Define the vertices that compose each of the 6 faces. These numbers are
        # indices to the vertices list defined above.
        self.drone_faces = [(0,1,2,11),(2,3,4,5),(8,9,10,11),(5,6,7,8),(11,2,5,8),]
        self.floor_face = [(12,13,14,15)]
        self.faces = []
        self.faces.extend(self.drone_faces)
        self.faces.extend(self.floor_face)

        # Define colors for each face
        self.colors = [(0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255),
                       (0, 255, 255), (0, 100, 0)]

        # self.angle = 0
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0

        self.projection_angle_x = 45
        self.projection_angle_y = 0
        self.projection_angle_z = 0

    def run(self):
        iter = 0
        dc = [0, 0, 0, 0]
        """ Main Loop """
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(50)
            self.screen.fill((0, 32, 0))

            rad_x = iter * math.pi / 180
            rad_y = rad_x + 180
            scale_x = math.sin(rad_x)*20
            # print(scale_x)
            scale_y = math.sin(rad_y)*20
            # print(scale_y)
            self.angle_x = scale_x
            self.angle_y = scale_y

            # self.angle += 1
            # self.angle_z += 1

            sensor_values = {
                'yaw': 0,
                'pitch': self.angle_y,
                'roll': self.angle_x,
            }

            for m in range(4):
                dc[m] = calculate_dc_for_motor(m, .5, sensor_values)
                self.colors[m] = (0, 0, 255*dc[m])
            # print(dc)

            # It will hold transformed vertices.
            t = []

            self.vertices_to_draw = self.vertices[:]

            for k, v in enumerate(self.vertices_to_draw[:-4]):
                # Rotate the drone
                # Rotate the point around X axis, then around Y axis, and finally around Z axis.
                self.vertices_to_draw[k] = v.rotateX(self.angle_x).rotateY(self.angle_y).rotateZ(self.angle_z)
                # Transform the point from 3D to 2D
                # v = r.project(self.screen.get_width(), self.screen.get_height(), 256, 12)
                # Put the point in the list of transformed vertices
                # t.append(p)

            for v in self.vertices_to_draw:
                # Projection
                r = v.rotateX(self.projection_angle_x).rotateY(self.projection_angle_y).rotateZ(self.projection_angle_z)
                # Transform the point from 3D to 2D
                p = r.project(self.screen.get_width(), self.screen.get_height(), 256, 12)
                # Put the point in the list of transformed vertices
                t.append(p)

            # Calculate the average Z values of each face.
            avg_z = []
            i = 0
            for f in self.faces:
                z = (t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z) / 4.0
                avg_z.append([i,z])
                i = i + 1

            # Draw the faces using the Painter's algorithm:
            # Distant faces are drawn before the closer ones.
            for tmp in sorted(avg_z,key=itemgetter(1),reverse=True):
                face_index = tmp[0]
                f = self.faces[face_index]
                pointlist = [(t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y),
                             (t[f[1]].x, t[f[1]].y), (t[f[2]].x, t[f[2]].y),
                             (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y),
                             (t[f[3]].x, t[f[3]].y), (t[f[0]].x, t[f[0]].y)]
                pygame.draw.polygon(self.screen, self.colors[face_index], pointlist)
            
            pygame.display.flip()

            iter += 1
            iter %= 360
            # print(iter)

if __name__ == "__main__":
    Simulation().run()
