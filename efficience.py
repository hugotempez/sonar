import tkinter


class Efficience:
    def __init__(self, collision_data, window_data):
        self.collision_data = collision_data
        self.efficience_window = tkinter.Tk()
        self.efficience_window.title("Fonction efficience")
        self.efficience_window.resizable(False, False)
        self.root_window = window_data
        self.canvas = tkinter.Canvas(self.efficience_window, width=self.root_window["width"],
                                     height=self.root_window["height"], background="white")

    def build_efficience(self):
        self.__build_canvas()
        for element in self.collision_data:
            self.canvas.create_oval(element["x"], element["y"], element["x"], element["y"], fill="green")

    def __build_canvas(self):
        self.canvas.pack()
