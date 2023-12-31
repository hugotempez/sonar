import tkinter
import math
import random


class Robot:
    """Class représentant le robot physique et toutes ses méthodes."""
    counter = 0

    def __init__(self, canva, image, x=30, y=30, diameter=30, rayon=0, nb_rayon=0, portee_rayon=60):
        """Constructeur"""
        if Robot.__check_counter():
            # Diamétre et position du robot
            self.diameter = diameter
            self.rayon = diameter / 2
            self.x = x + self.rayon
            self.y = y + self.rayon
            # Position de la pointe extérieur de la ligne rouge
            self.redline_x = self.x + self.rayon
            self.redline_y = self.y
            # Orientation en degrés
            self.direction = 0
            # Rayon de détection du sonar et nombre de capteur(s)
            self.rayon_sonar = rayon
            self.nb_rayon = nb_rayon
            self.distance_rayon = portee_rayon
            # Import du canva depuis le main programme
            self.canva = canva
            # Background image
            self.image = image
            # Création du robot et de la ligne directrice, les details des paramètres sont les suivants :
            # param1 = debut x, param2 = debut y, param3 = fin x, param4 = fin y
            # (ou inversement si param3 est plus petit que param1 par exemple)
            self.robot = canva.create_oval(self.x - self.rayon, self.y - self.rayon,
                                           self.x + self.rayon, self.y + self.rayon, width=2)
            self.robot_direction = canva.create_line(self.x, self.y,
                                                     self.redline_x, self.redline_y, fill="red", width=1)
            self.has_sonar = False
            self.lines = []
            self.collision_data = []
            self.__create_sonar()
            Robot.__increment_counter()
        else:
            print("Il existe deja une instance de cette classe")

    @staticmethod
    def __increment_counter():
        """Incrémente un compteur pour le nombre d'instance de l'objet Robot."""
        Robot.counter += 1

    def destroy(self):
        """Décrement le compteur d'objet et détruit l'objet cible."""
        Robot.counter -= 1
        del self

    @staticmethod
    def __check_counter():
        """Check le nombre d'instance de l'objet, renvoi true s'il n'en existe pas, sinon false."""
        if Robot.counter == 0:
            return True
        else:
            return False

    def __create_sonar(self):
        """Crée le lidar du robot en fonction des paramètres de l'objet."""
        step = self.rayon_sonar / (self.nb_rayon - 1)
        for ray in range(self.nb_rayon):
            deg = self.direction - (self.rayon_sonar / 2) + (ray * step)
            rad = deg * (math.pi / 180)
            x_start = math.cos(rad) * self.rayon
            y_start = math.sin(rad) * self.rayon
            x_end = math.cos(rad) * self.distance_rayon
            y_end = math.sin(rad) * self.distance_rayon
            # Modifiez la longueur des rayons pour s'arrêter à l'obstacle
            x_end, y_end, color = self.__detect_obstacle(x_start, y_start, x_end, y_end)
            if math.sqrt((x_end - x_start) ** 2 + (y_end - y_start) ** 2) < 2:
                # Si oui, déplacer automatiquement le robot dans la direction opposée à l'obstacle
                self.move_robot_opposite_to_obstacle(x_start, y_start, x_end, y_end)
            self.lines.append(self.canva.create_line(
                self.x + x_start, self.y + y_start,
                self.x + x_end, self.y + y_end,
                fill=color, width=1
            ))
        self.has_sonar = True

    def move_robot_opposite_to_obstacle(self, x_start, y_start, x_end, y_end):
        """Déplace le robot aléatoirement à gauche ou à droite par rapport à l'obstacle."""
        # Calculer la direction opposée à l'obstacle
        opposite_direction = math.atan2(y_end - y_start, x_end - x_start) * (180 / math.pi) + 180
        # Choisir aléatoirement la direction gauche (-90) ou droite (90)
        random_direction = random.choice([-90, 90])
        # Changer l'orientation du robot
        self.change_orientation(int(opposite_direction + random_direction - self.direction))
        # Déplacer le robot dans la direction aléatoire
        if random_direction == -90:
            self.__move_robot("gauche")
        else:
            self.__move_robot("droite")
        # Mettre à jour le lidar après le déplacement
        self.__kill_sonar()
        self.__create_sonar()

    def __detect_obstacle(self, x_start, y_start, x_end, y_end):
        """Detecte s'il existe une collision pour chaque rayon, renvoi une coordonée x/y
        de fin et une couleur pour le rayon en fonction du resultat."""
        x_step = (x_end - x_start) / self.distance_rayon
        y_step = (y_end - y_start) / self.distance_rayon
        x, y = x_start, y_start
        for _ in range(self.distance_rayon):
            if self.__check_collision(self.x + x, self.y + y):
                return x, y, "red"  # Arrêtez le rayon à l'obstacle et lui donner la couleur rouge
            x += x_step
            y += y_step
        # Pas d'obstacle détecté, utilisez la longueur complète du rayon et lui donner la couleur bleu
        return x_end, y_end, "blue"

    def change_orientation(self, incr=0):
        """Change l'orientation du robot (rayon de 360°)."""
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
        # Supprime et recrée le sonar avec les nouveaux paramètres
        self.__kill_sonar()
        self.__create_sonar()

    def move_and_change_orientation(self, direction):
        """Déplace le robot, change son orientation si besoin, et supprime/recrée le lidar
         pour pouvoir l'orienter et détecter les eventuels nouvelles collision"""
        self.__move_robot(direction)
        if direction == "haut":
            self.direction = 270
        elif direction == "bas":
            self.direction = 90
        elif direction == "gauche":
            self.direction = 180
        elif direction == "droite":
            self.direction = 0
        rad = self.direction * math.pi / 180
        x_end = math.cos(rad) * self.rayon
        y_end = math.sin(rad) * self.rayon
        if self.__check_collision(x_end, y_end, check_only=True):
            self.canva.coords(self.robot_direction, self.x, self.y, self.x + x_end, self.y + y_end)
            self.__kill_sonar()
            self.__create_sonar()


    def __kill_sonar(self):
        """Supprime le lidar."""
        for element in self.lines:
            tkinter.Canvas.delete(self.canva, element)
        self.has_sonar = False
        self.lines = []

    def __move_robot(self, direction):
        """Déplace le robot et son lidar sur le canva en fonction du paramètre direction."""
        if direction == "droite":
            self.canva.move(self.robot, 5, 0)
            self.canva.move(self.robot_direction, 5, 0)
            if self.has_sonar:
                for i in range(len(self.lines)):
                    self.canva.move(self.lines[i], 5, 0)
            self.x += 5
        elif direction == "gauche":
            self.canva.move(self.robot, -5, 0)
            self.canva.move(self.robot_direction, -5, 0)
            if self.has_sonar:
                for i in range(len(self.lines)):
                    self.canva.move(self.lines[i], -5, 0)
            self.x -= 5
        elif direction == "haut":
            self.canva.move(self.robot, 0, -5)
            self.canva.move(self.robot_direction, 0, -5)
            if self.has_sonar:
                for i in range(len(self.lines)):
                    self.canva.move(self.lines[i], 0, -5)
            self.y -= 5
        elif direction == "bas":
            self.canva.move(self.robot, 0, 5)
            self.canva.move(self.robot_direction, 0, 5)
            if self.has_sonar:
                for i in range(len(self.lines)):
                    self.canva.move(self.lines[i], 0, 5)
            self.y += 5
        return self.x, self.y

    def __check_collision(self, x, y, check_only=False):
        """Check s'il y a une collision sur la trajectoire d'un rayon du lidar, renvoie true si collision
         ou si le duo (x, y) n'existe pas, false sinon."""
        try:
            rgb = self.image.getpixel((x, y))
            if rgb[0] != 255 and rgb[1] != 255 and rgb[2] != 255:
                if check_only:
                    return True
                else:
                    self.collision_data.append({"id": self.__get_last_collision_index(), "x": x, "y": y})
                    return True
            else:
                return False
        except IndexError:
            if check_only:
                return True
            else:
                self.collision_data.append({"id": self.__get_last_collision_index(), "x": x, "y": y})
                return True

    def __get_last_collision_index(self):
        """Retourne la longueur +1 du tableau de collision pour taguer les points de collision avec un id."""
        return len(self.collision_data) + 1
