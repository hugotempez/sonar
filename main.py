import tkinter
from tkinter import filedialog, messagebox
import sys
import os
from PIL import ImageTk, Image
from robot import Robot
from efficience import Efficience
import multiprocessing

# Path d'execution
PATH = os.path.dirname(sys.argv[0])

# Taille de la fenêtre
WIDTH: int = 1200
HEIGHT: int = 600

# Création de la fenêtre
window = tkinter.Tk()
chosen_map = tkinter.StringVar()
window.geometry("{}x{}".format(WIDTH, HEIGHT))
window.resizable(False, False)

# Variables globales
img_path = ""  # Path de l'image
image: Image  # Image en mémoire pour le check des limites
robot: Robot  # Instance de l'objet robot*
menu_frame: tkinter.Frame  # Frame pour le menu
canva: tkinter.Canvas  # Canvas Tkinter
window_efficience: tkinter.Tk  # Fenêtre fonction efficience
canva_efficience: tkinter.Canvas  # Canvas fonction efficience
data_queue = multiprocessing.Queue()    # Queue pour le multiprocessing

# Paramètres par defaut du robot
nb_rayons = 2
portee_rayon = 40
rayon_lidar = 90


def resize_image(file_path):
    """Redimensionne une image si elle est trouvée, sinon lève une exception."""
    try:
        img = Image.open(file_path)
        img.resize((WIDTH, HEIGHT)).save("resize.png")
        img.close()
    except FileNotFoundError as e:
        print(e)


def main_menu():
    """Affiche le menu principal."""
    global menu_frame, nb_rayons, rayon_lidar, portee_rayon
    menu_frame = tkinter.Frame(window)
    menu_frame.pack()
    simu_frame = tkinter.LabelFrame(menu_frame, text="Simulation")
    simu_frame.grid(row=0, column=0)
    text_label = ("Choisissez votre map en cliquant sur le bouton ci-dessous."
                  "Pour information, les formats acceptés sont png, jpg et jpeg et"
                  " l'image sera automatiquement redimensionné en {}x{}".format(str(WIDTH), str(HEIGHT)))
    label_map_choice = tkinter.Label(simu_frame, text=text_label)
    label_map_choice.pack()
    button_map_choice = tkinter.Button(simu_frame, text="Choix de la map", command=dialogbox_choose_map)
    button_map_choice.pack()
    label_map_chosen = tkinter.Label(simu_frame, textvariable=chosen_map)
    label_map_chosen.pack()
    nb_ray = tkinter.IntVar()
    nb_rayons_slider = tkinter.Scale(simu_frame, variable=nb_ray, orient="horizontal",
                                     from_=2, to=40, label="Nombre de rayons du LIDAR :", length=180,
                                     command=lambda a=nb_ray.get(): set_nb_rayons(a))
    nb_rayons_slider.pack()
    portee_ray = tkinter.IntVar()
    portee_rayons_slider = tkinter.Scale(simu_frame, variable=portee_ray, orient="horizontal",
                                         from_=40, to=1200, label="Portée des rayons du LIDAR :", length=180,
                                         # a checker lucas
                                         command=lambda a=portee_ray.get(): set_portee_rayons(a))
    portee_rayons_slider.pack()
    rayon_lid = tkinter.IntVar()
    rayon_lid_slider = tkinter.Scale(simu_frame, variable=rayon_lid, orient="horizontal",
                                     from_=90, to=360, label="Rayon d'action du LIDAR :", length=180,
                                     command=lambda a=rayon_lid.get(): set_rayon_lidar(a))
    rayon_lid_slider.pack()
    button_launch = tkinter.Button(simu_frame, text="Lancer la simulation", command=init_sim)
    button_launch.pack()


def set_nb_rayons(x):
    """Modifie la valeur de la variable nb_rayons en fonction de l'input utilisateur."""
    global nb_rayons
    nb_rayons = int(x)


def set_portee_rayons(x):
    """Modifie la valeur de la variable portee_rayon en fonction de l'input utilisateur."""
    global portee_rayon
    portee_rayon = int(x)


def set_rayon_lidar(x):
    """Modifie la valeur de la variable rayon_lidar en fonction de l'input utilisateur."""
    global rayon_lidar
    rayon_lidar = int(x)


def dialogbox_choose_map():
    """Ouvre une boite de dialogue pour choisir un fichier map."""
    global img_path
    filetypes = [("Image files", "*.jpg *.png *.jpeg *.gif *.bmp")]
    img_path = filedialog.askopenfilename(initialdir="./", title="Choisissez une image", filetypes=filetypes)
    chosen_map.set(img_path)


def on_mouse_click(eventorigin):
    """Event au click pour placer le robot."""
    global robot, canva, rayon_lidar, nb_rayons, portee_rayon, data_queue
    x0 = eventorigin.x
    y0 = eventorigin.y
    if Robot.counter == 0:
        robot = Robot(canva, image, data_queue, x0, y0, 30, rayon=rayon_lidar, nb_rayon=nb_rayons,
                      portee_rayon=portee_rayon)
    else:
        messagebox.showerror("Erreur", "Il existe deja un robot sur la map.")


def on_mouse_wheel(eventorigin):
    """Event molette pour gérer l'orientation du robot."""
    if eventorigin.delta < 0:
        robot.change_orientation(-10)
    else:
        robot.change_orientation(10)


def on_arrow_click(eventorigin):
    """Event flèches directionnelles pour déplacer le robot"""
    global robot, data_queue
    key = eventorigin.keysym
    if key == "Up":
        data_queue.put(robot.move_and_change_orientation("haut"))
    elif key == "Down":
        robot.move_and_change_orientation("bas")
    elif key == "Left":
        robot.move_and_change_orientation("gauche")
    elif key == "Right":
        robot.move_and_change_orientation("droite")


def key_bindings():
    """Initialisation des binds pour le robot."""
    global canva
    canva.focus_set()
    canva.bind("<Button 1>", on_mouse_click)
    canva.bind("<MouseWheel>", on_mouse_wheel)
    canva.bind("<Up>", on_arrow_click)
    canva.bind("<Down>", on_arrow_click)
    canva.bind("<Left>", on_arrow_click)
    canva.bind("<Right>", on_arrow_click)


def popup():
    """Messagebox d'information pour le placement et l'orientation du robot."""
    messagebox.showinfo("Informations", "Placez le robot en cliquant à un endroit de la map. "
                                        "Le robot est orientable avec la molette de la souris")


def return_to_menu():
    """Fonction de switch entre la simulation et le menu principal."""
    global canva, menu_frame, robot
    try:
        robot.destroy()
        del robot
    except NameError:
        pass
    finally:
        canva.grid_remove()
        menu_frame.pack()
        window.config(menu="")


def init_sim():
    """Initialisation du canva et chargement de l'image"""
    global window, menu_frame, image, img_path, canva
    if img_path == "":
        img_path = "resize.png"
    if img_path != "":
        resize_image(img_path)
        menu_frame.pack_forget()
        canva = tkinter.Canvas(window, width=WIDTH, height=HEIGHT, background="white")
        menubar = tkinter.Menu(canva)
        sim = tkinter.Menu(menubar, tearoff=0)
        sim.add_command(label="Fonction efficience", command=start_side_process)
        sim.add_separator()
        sim.add_command(label="Quitter simulation", command=return_to_menu)
        menubar.add_cascade(label="Simulation", menu=sim)
        window.config(menu=menubar)
        image = Image.open("./resize.png")
        map_image = ImageTk.PhotoImage(image)
        canva.create_image(WIDTH / 2, HEIGHT / 2, anchor="center", image=map_image)
        canva.image = map_image
        canva.grid(row=0, column=0)
        key_bindings()
    else:
        messagebox.showerror("Erreur", "Veuillez choisir une map.")


def start_side_process():
    process = multiprocessing.Process(target=test())
    process.start()


def test():
    global robot
    window_data = {"root": window, "height": HEIGHT, "width": WIDTH}
    eff = Efficience(robot.mp_data_queue, window_data)
    eff.test()


def build_efficience():
    try:
        global data_queue
        print(data_queue.get())
        window_data = {"root": window, "height": HEIGHT, "width": WIDTH}
        if robot.collision_data:
            eff = Efficience(robot.mp_data_queue, window_data)
        else:
            eff = Efficience(robot.mp_data_queue, window_data)
        eff.build_efficience()
    except NameError:
        messagebox.showerror("Erreur", "Aucun robot sur la map, donc aucune donnée à présenter.")


def main():
    """Entry point."""
    main_menu()
    window.mainloop()


main()
