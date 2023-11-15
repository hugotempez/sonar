import time
import tkinter
from tkinter import filedialog
from PIL import ImageTk, Image
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
img_path = ""               # Path de l'image
image: Image                # Image en mémoire pour le check des limites
robot: Robot                # Instance de l'objet robot
menu_frame: tkinter.Frame   # Frame pour le menu
canva: tkinter.Canvas       # Canvas Tkinter


def resize_image(file_path):
    """Redimensionne une image si elle est trouvée, sinon lève une exception"""
    if file_path:
        img = Image.open(file_path)
        img.resize((WIDTH, HEIGHT)).save("resize.png")
        img.close()
    else:
        raise FileNotFoundError


def main_menu():
    global menu_frame
    menu_frame = tkinter.Frame(window)
    menu_frame.pack()
    text_label = ("Choisissez votre map en cliquant sur le bouton ci-dessous."
                  "Pour information, les formats acceptés sont png, jpg et jpeg et"
                  " l'image sera automatiquement redimensionné en {}x{}".format(str(WIDTH), str(HEIGHT)))
    label_map_choice = tkinter.Label(menu_frame, text=text_label)
    label_map_choice.pack()
    button_map_choice = tkinter.Button(menu_frame, text="Choix de la map", command=dialogbox_choose_map)
    button_map_choice.pack()
    label_map_chosen = tkinter.Label(menu_frame, textvariable=chosen_map)
    label_map_chosen.pack()
    button_launch = tkinter.Button(menu_frame, text="Lancer la simulation", command=init_sim)
    button_launch.pack()


def dialogbox_choose_map():
    global img_path
    filetypes = [("Image files", "*.jpg *.png *.jpeg *.gif *.bmp")]
    img_path = filedialog.askopenfilename(initialdir="./", title="Choisissez une image", filetypes=filetypes)
    chosen_map.set(img_path)


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


def popup():
    """A modifier en messagebox"""
    top = tkinter.Toplevel(window)
    top.geometry("600x50")
    top.title("Instructions")
    tkinter.Label(top, text="Placez le robot en cliquant à un endroit de la map. "
                            "Le robot est orientable avec la molette de la souris").pack()


def return_to_menu():
    global canva, menu_frame
    canva.destroy()
    menu_frame.pack()


def init_sim():
    """Initialisation du canva et chargement de l'image"""
    global menu_frame, canva, image, img_path
    if img_path != "":
        try:
            resize_image(img_path)
            menu_frame.pack_forget()
            canva = tkinter.Canvas(width=WIDTH, height=HEIGHT, background="red")
            print(img_path)
            image = Image.open("resize.png")
            img_map = ImageTk.PhotoImage(image)
            #canva.grid(row=1, column=1)
            canva.pack()
            canva.create_image(WIDTH/2, HEIGHT/2, anchor="center", image=img_map)
            # bottom_frame = tkinter.Frame(canva)
            # bottom_frame.grid(row=1, column=2)
            # return_button = tkinter.Button(bottom_frame, text="Quitter", command=return_to_menu)
            # return_button.pack()
            key_bindings()
            popup()
        except Exception as e:
            print(e)
    else:
        raise FileNotFoundError


def gui():
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
    main_menu()
    # gui()
    window.mainloop()


main()
