import tkinter
from PIL import ImageTk, Image
from resizeimage import resizeimage

width = 1200
height = 600

window = tkinter.Tk()
window.geometry("1200x600")
window.resizable(False, False)

canva = tkinter.Canvas(width=width, height=height, bg="white")
img = Image.open("Map_sonar.png")
out_image = resizeimage.resize_width(img, width)
out_image.save("resize.png")

img_map = ImageTk.PhotoImage(Image.open("resize.png"))
canva.pack()
canva.create_image(width/2, height/2, anchor="center", image=img_map)


# frame_map = tkinter.Frame(window, width=1200, height=600)
# frame_map.pack()
# frame_map.place(anchor="center", relx=0.5, rely=0.5)
#
# img = Image.open("Map_sonar.png")
# out_image = resizeimage.resize_width(img, 1200)
# out_image.save("resize.png")
#
# img_map = ImageTk.PhotoImage(Image.open("resize.png"))
#
# label_map = tkinter.Label(frame_map, image=img_map)
#
# label_map.pack()

robot = canva.create_oval(175, 100, 100, 175, width=3)


def gui():
    window.mainloop()


def main():
    gui()


main()
