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

    def create_sonar(self, nb_rayon=10, rayon=180, distance=60):
        occurences = int(rayon / (nb_rayon - 1))
        for deg in range(0, rayon + 1, occurences):
            rad = deg * math.pi / 180
            x_start = math.cos(rad) * self.rayon
            y_start = math.sin(rad) * self.rayon
            x_end = math.cos(rad) * distance
            y_end = math.sin(rad) * distance
            x_step = (self.x + x_start) / (self.x + x_end)
            y_step = (self.y + y_start) / (self.y + y_end)
            #x_end, y_end, color = self.sensor_collision(x_start, x_end, x_step, y_start, y_end, y_step)
            #print("x = {} => {} step => {}, y = {} => {} step => {}".format(self.x + x_start, self.x + x_end, x_step, self.y + y_start, self.y + y_end, y_step))
            self.lines.append(self.canva.create_line(self.x + x_start, self.y + y_start, self.x + x_end, self.y + y_end,
                                                     fill="blue", width=1))
        self.has_sonar = True

    def change_orientation(self, incr):
        self.direction += incr
        if self.direction < 0:
            self.direction = 360
        elif self.direction > 360:
            self.direction = 0
        print(self.direction)
        rad = self.direction * math.pi / 180
        x_end = math.cos(rad) * self.rayon
        y_end = math.sin(rad) * self.rayon
        print(self.redline_x, x_end)
        self.canva.coords(self.robot_direction, self.x, self.y, self.x + x_end, self.y + y_end)


    def sensor_collision(self, x_start, x_end, x_stp, y_start, y_end, y_stp):
        checked = False
        x_copy = x_start
        y_copy = y_start
        i = 0
        while x_copy < x_end and y_copy < y_end or checked:
            checked = self.check_collision(x_copy, y_copy)
            x_copy += x_stp
            y_copy += y_stp
            print(x_copy, y_copy, checked, i)
            i += 1
        if checked:
            print("pas collision")
            return x_end, y_end, "blue"
        else:
            print("collision")
            return x_copy, y_copy, "red"

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


    def check_collision(self, x=0.0, y=0.0):
        if x != 0.0 or y != 0.0:
            rgb = self.image.getpixel((x, y))
        else:
            rgb = self.image.getpixel((self.x, self.y))
        if rgb[0] != 255 and rgb[1] != 255 and rgb[2] != 255:
            return True
        else:
            return False

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
