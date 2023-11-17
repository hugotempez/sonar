import tkinter
import math
import numpy


class Robot:
    counter = 0

    def __init__(self, canva, image, x=30, y=30, diameter=30, rayon=0, nb_rayon=0, portee_rayon=60):
        if Robot.check_counter():
            """Diamétre et position du robot"""
            self.diameter = diameter
            self.rayon = diameter / 2
            self.x = x + self.rayon
            self.y = y + self.rayon
            """Position de la pointe extérieur de la ligne rouge"""
            self.redline_x = self.x + self.rayon
            self.redline_y = self.y
            """Orientation en degrés"""
            self.direction = 180
            """Rayon de détection du sonar et nombre de capteur(s)"""
            self.rayon_sonar = rayon
            self.nb_rayon = nb_rayon
            self.distance_rayon = portee_rayon
            """Import du canva depuis le main programme"""
            self.canva = canva
            """Background image"""
            self.image = image
            """Création du robot et de la ligne directrice, les details des paramètres sont les suivants :
             param1 = debut x, param2 = debut y, param3 = fin x, param4 = fin y 
             (ou inversement si param3 est plus petit que param1 par exemple)"""
            self.robot = canva.create_oval(self.x - self.rayon, self.y - self.rayon,
                                           self.x + self.rayon, self.y + self.rayon, width=2)
            self.robot_direction = canva.create_line(self.x, self.y,
                                                     self.redline_x, self.redline_y, fill="red", width=1)
            self.has_sonar = False
            self.lines = []
            self.create_sonar()
            Robot.increment_counter()
        else:
            print("Il existe deja une instance de cette classe")

    @staticmethod
    def increment_counter():
        Robot.counter += 1

    def destroy(self):
        Robot.counter -= 1
        del self

    @staticmethod
    def check_counter():
        if Robot.counter == 0:
            return True
        else:
            return False

    def create_sonar(self):
        step = self.rayon_sonar / (self.nb_rayon-1)
        for ray in range(self.nb_rayon):
            deg = self.direction - (self.rayon_sonar/2) + (ray*step)
            rad = deg * (math.pi / 180)
            x_start = math.cos(rad) * self.rayon
            y_start = math.sin(rad) * self.rayon
            x_end = math.cos(rad) * self.distance_rayon
            y_end = math.sin(rad) * self.distance_rayon
            x_end, y_end, color = self.sensor_collision(self.x + x_start, self.y + y_start, x_end, y_end)
            #print(ray, x_end, y_end)
            self.lines.append(self.canva.create_line(self.x + x_start, self.y + y_start, self.x + x_end, self.y + y_end,
                                                     fill=color, width=1))
        self.has_sonar = True

    def change_orientation(self, incr=0):
        if self.direction == 0 and incr < 0:
            self.direction = 350
        elif self.direction == 350 and incr > 0:
            self.direction = 0
        else:
            self.direction += incr
        rad = self.direction * math.pi / 180
        x_end = math.cos(rad) * self.rayon
        y_end = math.sin(rad) * self.rayon
        self.canva.coords(self.robot_direction, self.x, self.y, self.x + x_end, self.y + y_end)
        self.kill_sonar()
        self.create_sonar()

    def sensor_collision(self, x_start, y_start, x_end, y_end):
        x_step = (x_end - x_start) / self.distance_rayon
        y_step = (y_end - y_start) / self.distance_rayon

        x, y = x_start, y_start
        for _ in range(self.distance_rayon):
            if self.check_collision(self.x + x, self.y + y):
                return x, y, "red"  # Arrêtez le rayon à l'obstacle
            x += x_step
            y += y_step

        return x_end, y_end, "blue"  # Pas d'obstacle détecté, utilisez la longueur complète du rayon

    def get_lidar_data(self):
        return 1

    def kill_sonar(self):
        for element in self.lines:
            tkinter.Canvas.delete(self.canva, element)
        self.has_sonar = False
        self.lines = []

    def move_robot(self, direction):
        if direction == "droite":
            self.canva.move(self.robot, 1, 0)
            self.canva.move(self.robot_direction, 1, 0)
            if self.has_sonar:
                for i in range(len(self.lines)):
                    self.canva.move(self.lines[i], 1, 0)
            self.x += 1
        elif direction == "gauche":
            self.canva.move(self.robot, -1, 0)
            self.canva.move(self.robot_direction, -1, 0)
            if self.has_sonar:
                for i in range(len(self.lines)):
                    self.canva.move(self.lines[i], -1, 0)
            self.x -= 1
        elif direction == "haut":
            self.canva.move(self.robot, 0, -1)
            self.canva.move(self.robot_direction, 0, -1)
            self.y -= 1
        elif direction == "bas":
            self.canva.move(self.robot, 0, 1)
            self.canva.move(self.robot_direction, 0, 1)
            self.y += 1
        return self.x, self.y

    def check_collision(self, x, y):
        try:
            rgb = self.image.getpixel((x, y))
            if rgb[0] != 255 and rgb[1] != 255 and rgb[2] != 255:
                return True
            else:
                return False
        except IndexError:
            return True

    def move_sonar(self):
        return 0

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def get_robot_position(self):
        return {"x": [int(self.canva.coords(self.robot)[0]), int(self.canva.coords(self.robot)[2])],
                "y": [int(self.canva.coords(self.robot)[1]), int(self.canva.coords(self.robot)[3])]}

    def telemesure(self):
        return 0
