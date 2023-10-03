import time
import tkinter
from tkinter import filedialog as filedialog
from PIL import ImageTk, Image
from resizeimage import resizeimage


width: int = 1200
height: int = 600


window = tkinter.Tk()
chosen_map = tkinter.StringVar()
window.geometry("1200x600")
window.resizable(False, False)

canva = tkinter.Canvas(width=width, height=height, background="white")
# img = Image.open("Map_sonar.png")
# resizeimage.resize_width(img, width).save("resize.png")

# img_map = ImageTk.PhotoImage(Image.open("resize.png"))
# canva.pack()
# canva.create_image(width/2, height/2, anchor="center", image=img_map)
#
# robot = canva.create_oval(30, 30, 60, 60, width=3)
# image = Image.open("resize.png")


# def gui():
#     x = int(canva.coords(robot)[0] + canva.coords(robot)[2]) // 2
#     y = int(canva.coords(robot)[1] + canva.coords(robot)[3]) // 2
#     direction = "droite"
#     while True:
#         x, y = move(direction, x, y)
#         rgb = image.getpixel((x, y))
#         print("x = ", x, " ,y = ", y, " ,r = ", rgb[0], " ,g = ", rgb[1], ", b = ", rgb[2])
#         if rgb[0] != 255 and rgb[1] != 255 and rgb[2] != 255:
#             if direction == "droite":
#                 direction = "gauche"
#             elif direction == "gauche":
#                 direction = "droite"
#         window.update()
#         time.sleep(0.00001)
#     window.mainloop()
#
#
# def move(direction, x, y):
#     if direction == "droite":
#         canva.move(robot, 1, 0)
#         x += 1
#     elif direction == "gauche":
#         canva.move(robot, -1, 0)
#         x -= 1
#     elif direction == "haut":
#         canva.move(robot, 0, -1)
#         y -= 1
#     elif direction == "bas":
#         canva.move(robot, 0, 1)
#         y += 1
#     return x, y


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


def dialogbox_choose_map():
    filetypes = [("png", "*.png"), ("jpg", "*.jpg"), ("jpeg", "*.jpeg")]
    chosen_map.set(filedialog.askopenfilename(initialdir="/", title="Choisissez une image", filetypes=filetypes))


def main():
    #gui()
    user_inputs()
    window.mainloop()

main()
