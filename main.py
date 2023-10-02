import time
import tkinter
from PIL import ImageTk, Image, ImageGrab
from resizeimage import resizeimage

width = 1200
height = 600

window = tkinter.Tk()
window.geometry("1200x600")
window.resizable(False, False)

canva = tkinter.Canvas(width=width, height=height, background="white")
img = Image.open("Map_sonar.png")
resizeimage.resize_width(img, width).save("resize.png")

img_map = ImageTk.PhotoImage(Image.open("resize.png"))
canva.pack()
canva.create_image(width/2, height/2, anchor="center", image=img_map)

robot = canva.create_oval(30, 30, 60, 60, width=3)
pic = ImageGrab.grab()


def gui():
    # while True:
    #     canva.move(robot, 0, 1)
    #     if pic.getpixel((int(canva.coords(robot)[1]), int(canva.coords(robot)[3]))):
    for i in range(1200):
        canva.move(robot, 1, 1)
        print(pic.getpixel((int(canva.coords(robot)[1]), int(canva.coords(robot)[3]))))
        window.update()
        time.sleep(0.01)
    window.mainloop()


def main():
    gui()


main()
