import tkinter


class Efficience:
    def __init__(self, data_queue, window_data):
        self.collision_data = data_queue
        self.efficience_window = tkinter.Tk()
        self.root_window = window_data
        self.canvas = tkinter.Canvas(self.efficience_window, width=self.root_window["width"],
                                     height=self.root_window["height"], background="white")

    def build_efficience(self):
        self.__build_canvas()
        while True:
        #for element in self.collision_data:
            data = self.collision_data.get()
            if data:
                self.canvas.create_oval(data["x"], data["y"], data["x"], data["y"], fill="green")

    def __build_canvas(self):
        self.canvas.pack()
