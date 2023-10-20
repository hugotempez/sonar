import tkinter
import math


class Robot:
    def __init__(self, canva, image, x=30, y=30, diameter=30, rayon=0, nb_rayon=0):
        """Diamétre et position du robot"""
        self.diameter = diameter
        self.rayon = diameter / 2
        self.x = x + self.rayon
        self.y = y + self.rayon
        """Position de la pointe extérieur de la ligne rouge"""
        self.redline_x = self.x + self.rayon
        self.redline_y = self.y
        """Orientation en degrés"""
        self.direction = 0
        """Rayon de détection du sonar et nombre de capteur(s)"""
        self.rayon_sonar = rayon
        self.nb_rayon = nb_rayon
        self.distance_rayon = 0
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

    def create_sonar(self, nb_rayon=10, rayon=180, distance=100):
        occurences = int(rayon / (nb_rayon - 1))
        for deg in range(0, rayon + 1, occurences):
            rad = deg * math.pi / 180
            x = math.cos(rad) * distance
            y = math.sin(rad) * distance
            self.lines.append(self.canva.create_line(self.x, self.y, self.x + x, self.y + y, fill="blue", width=1))
        self.has_sonar = True

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

    def check_collision(self, image, x=0, y=0):
        if x != 0 or y != 0:
            rgb = image.getpixel((x, y))
        else:
            rgb = image.getpixel((self.x, self.y))

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
