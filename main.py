import tkinter
from PIL import ImageTk, Image
from resizeimage import resizeimage


window = tkinter.Tk()
window.geometry("1200x600")
window.resizable(False, False)

frame_map = tkinter.Frame(window, width=1200, height=600, background="")
frame_map.pack()
frame_map.place(anchor='center', relx=0.5, rely=0.5)

img = Image.open("Map_sonar.png")
out_image = resizeimage.resize_width(img, 1200)
out_image.save("resize.png")

img_map = ImageTk.PhotoImage(Image.open("resize.png"))

label_map = tkinter.Label(frame_map, image=img_map)

label_map.pack()

robot = tkinter.Canvas().create_oval(40, 40, 40, 40, fill="black")


def gui():
    window.mainloop()


def main():
    gui()


main()
