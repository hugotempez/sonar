import tkinter, time
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

robot = canva.create_oval(10, 10, 40, 40, width=3)



def gui():
    for i in range(500):
        canva.move(robot, 0, 1)
        window.update()
        time.sleep(0.01)
    window.mainloop()



def main():
    gui()



main()
