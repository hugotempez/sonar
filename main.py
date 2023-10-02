import tkinter
from PIL import ImageTk, Image
from resizeimage import resizeimage


window = tkinter.Tk()
window.geometry("1200x600")
window.resizable(False, False)
frame = tkinter.Frame(window, width=1200, height=600)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)
img = Image.open("Map_sonar.png")
out_image = resizeimage.resize_width(img, 1200)
out_image.save("resize.png")
img = ImageTk.PhotoImage(Image.open("resize.png"))
label = tkinter.Label(frame, image=img)
label.pack()


def gui():
    window.mainloop()


def main():
    gui()


main()
