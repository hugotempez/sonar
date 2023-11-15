import time
import tkinter
from tkinter import filedialog
from PIL import ImageTk, Image
from resizeimage import resizeimage
from robot import Robot


# Taille de la fenêtre
WIDTH: int = 1200
HEIGHT: int = 600

# Création de la fenêtre
window = tkinter.Tk()
chosen_map = tkinter.StringVar()
window.geometry("{}x{}".format(WIDTH, HEIGHT))
window.resizable(False, False)

# Variables globales
image: Image                # Image en mémoire pour le check des limites
robot: Robot                # Instance de l'objet robot
canva: tkinter.Canvas       # Canvas Tkinter


def resize_image(file_path):
    global image
    img = Image.open(file_path)
    img.resize((WIDTH, HEIGHT)).save("resize.png")


def init_sim():
    global canva
    """Initialisation du canva et formatage de l'image"""
    canva = tkinter.Canvas(width=WIDTH, height=HEIGHT, background="white")
    img_map = ImageTk.PhotoImage(Image.open("resize.png"))
    canva.pack()
    canva.create_image(WIDTH / 2, HEIGHT / 2, anchor="center", image=img_map)


def user_inputs():
    text_label = ("Choisissez votre map en cliquant sur le bouton ci-dessous."
                  "Pour information, les formats acceptés sont png, jpg et jpeg et"
                  " l'image sera automatiquement redimensionné en {}x{}".format(str(WIDTH), str(HEIGHT)))
    label_map_choice = tkinter.Label(window, text=text_label)
    label_map_choice.pack()
    button_map_choice = tkinter.Button(window, text="Choix de la map", command=dialogbox_choose_map)
    button_map_choice.pack()
    label_map_chosen = tkinter.Label(window, textvariable=chosen_map)
    label_map_chosen.pack()
    button_launch = tkinter.Button(window, text="Lancer la simulation", command=init_sim)
    button_launch.pack()


def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif *.bmp")])
    if file_path:
        image = Image.open(file_path)
        resized_image = image.resize((1200, 600))
        photo = ImageTk.PhotoImage(resized_image)
        canva = tkinter.Canvas(width=WIDTH, height=HEIGHT, background="white")
        canva.pack()
        canva.create_image(WIDTH / 2, HEIGHT / 2, anchor="center", image=photo)
        label.config(image=photo)
        label.photo = photo
    else:
        raise Exception


def dialogbox_choose_map():
    filetypes = [("Image files", "*.jpg *.png *.jpeg *.gif *.bmp")]
    chosen_map.set(filedialog.askopenfilename(initialdir="/", title="Choisissez une image", filetypes=filetypes))


def on_mouse_click(eventorigin):
    global robot
    x0 = eventorigin.x
    y0 = eventorigin.y
    robot = Robot(canva, image, x0, y0, 30)


def on_mouse_wheel(eventorigin):
    if eventorigin.delta < 0:
        robot.change_orientation(-10)
    else:
        robot.change_orientation(10)


def key_bindings():
    """Initialisation des binds pour le robot"""
    canva.bind("<Button 1>", on_mouse_click)
    canva.bind("<MouseWheel>", on_mouse_wheel)


# Créer une étiquette pour afficher l'image
label = tkinter.Label(window)
label.pack()


def popup():
    top = tkinter.Toplevel(window)
    top.geometry("600x50")
    top.title("Instructions")
    tkinter.Label(top, text="Placez le robot en cliquant à un endroit de la map. "
                            "Le robot est dirigeable avec la molette de la souris").pack()


def gui():
    popup()
    #pos = robot.get_robot_position()
    direction = "droite"
    while True:
        x, y = robot.move_robot(direction)
        rgb = image.getpixel((x, y))
        #print("x = ", x, " ,y = ", y, " ,r = ", rgb[0], " ,g = ", rgb[1], ", b = ", rgb[2])
        if rgb[0] != 255 and rgb[1] != 255 and rgb[2] != 255:
            if direction == "droite":
                direction = "gauche"
            elif direction == "gauche":
                direction = "droite"
        window.update()
        time.sleep(0.005)


def main():
    popup()
    # gui()
    user_inputs()
    window.mainloop()


main()
