import time
import tkinter
from tkinter import filedialog
from PIL import ImageTk, Image
from resizeimage import resizeimage
from robot import Robot


def user_inputs():
    text_label = ("Choisissez votre map en cliquant sur le bouton ci-dessous."
                  "Pour information, les formats acceptés sont png, jpg et jpeg et"
                  " l'image sera automatiquement redimensionné en "
                  + str(width) + "x" + str(height) + ".")
    label_map_choice = tkinter.Label(window, text=text_label)
    label_map_choice.pack()
    button_map_choice = tkinter.Button(window, text="Choix de la map", command=dialogbox_choose_map)
    button_map_choice.pack()
    label_map_chosen = tkinter.Label(window, textvariable=chosen_map)
    label_map_chosen.pack()
    button_launch = tkinter.Button(window, text="Lancer la simulation", command=gui)
    button_launch.pack()


"""Taille de la fenêtre"""
width: int = 1200
height: int = 600

"""Création de la fenêtre"""
window = tkinter.Tk()
chosen_map = tkinter.StringVar()
window.geometry("{}x{}".format(width, height))
window.resizable(False, False)

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif *.bmp")])
    if file_path:
        image = Image.open(file_path)
        resized_image = image.resize((1200, 600))
        photo = ImageTk.PhotoImage(resized_image)
        canva = tkinter.Canvas(width=width, height=height, background="white")
        canva.pack()
        canva.create_image(width / 2, height / 2, anchor="center", image=photo)
        label.config(image=photo)
        label.photo = photo

def dialogbox_choose_map():
    filetypes = [("png", "*.png"), ("jpg", "*.jpg"), ("jpeg", "*.jpeg")]
    chosen_map.set(filedialog.askopenfilename(initialdir="/", title="Choisissez une image", filetypes=filetypes))

"""Initialisation du canva et formatage de l'image"""
canva = tkinter.Canvas(width=width, height=height, background="white")
img = Image.open("Map_sonar.png")
resizeimage.resize_width(img, width).save("resize.png")

"""Import de l'image formaté et création du canva"""
img_map = ImageTk.PhotoImage(Image.open("resize.png"))
canva.pack()
canva.create_image(width / 2, height / 2, anchor="center", image=img_map)

"""Import de l'image en mémoire pour checker les limites"""
image = Image.open("resize.png")

robot: Robot


def on_mouse_click(eventorigin):
    global x0, y0, robot
    x0 = eventorigin.x
    y0 = eventorigin.y
    robot = Robot(canva, image, x0, y0, 30)

def on_mouse_wheel(eventorigin):
    if eventorigin.delta < 0:
        robot.change_orientation(-10)
    else:
        robot.change_orientation(10)


"""Initialisation du robot"""
canva.bind("<Button 1>", on_mouse_click)
canva.bind("<MouseWheel>", on_mouse_wheel)


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


# Créer un bouton pour ouvrir une image
open_button = tkinter.Button(window, text="Ouvrir une image", command=open_image)
open_button.pack(pady=10)

# Créer une étiquette pour afficher l'image
label = tkinter.Label(window)
label.pack()


def main():
    popup()
    #gui()
    user_inputs()
    window.mainloop()


main()
