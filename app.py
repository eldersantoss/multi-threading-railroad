#!./venv/bin/python3

import time
import threading
import tkinter as tk


GREEN_COLOR = "#60ad5e"
PURPLE_COLOR = "#6746c3"
RED_COLOR = "#b71c1c"


class MyApp:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.create_widgets()
        self.set_initial_state()
        self.run_app()

    def create_widgets(self) -> None:
        self.root = tk.Tk()
        self.root.title("Ferrovia")
        self.content = tk.Frame(self.root)
        self.content.grid(row=0, column=0, columnspan=3, rowspan=5)
        self.canvas = tk.Canvas(self.content, width=500, height=375)
        self.canvas.grid(row=0, column=0, columnspan=3, rowspan=1)

        tk.Label(self.content, text="Controle de velocidade").grid(
            row=1, column=1, rowspan=1, columnspan=1, pady=20
        )

        self.train_speeds = {
            "green": tk.IntVar(),
            "purple": tk.IntVar(),
            "red": tk.IntVar(),
        }
        tk.Scale(
            self.content,
            variable=self.train_speeds["green"],
            from_=0,
            to=100,
            length=100,
            orient=tk.VERTICAL,
        ).grid(
            row=2,
            column=0,
            padx=15,
        )
        tk.Label(self.content, text="Verde").grid(
            row=3,
            column=0,
            padx=20,
            pady=20,
        )

        tk.Scale(
            self.content,
            variable=self.train_speeds["purple"],
            from_=0,
            to=100,
            length=100,
            orient=tk.VERTICAL,
        ).grid(
            row=2,
            column=1,
            padx=15,
        )
        tk.Label(self.content, text="Roxo").grid(
            row=3,
            column=1,
            padx=20,
            pady=20,
        )

        tk.Scale(
            self.content,
            variable=self.train_speeds["red"],
            from_=0,
            to=100,
            length=100,
            orient=tk.VERTICAL,
        ).grid(
            row=2,
            column=2,
            padx=15,
        )
        tk.Label(self.content, text="Vermelho").grid(
            row=3,
            column=2,
            padx=20,
            pady=20,
        )

        tk.Button(self.content, text="Iniciar", command=self.move_trains).grid(
            row=4,
            column=0,
            columnspan=3,
            ipadx=30,
            ipady=5,
            pady=(0, 20),
        )

    def set_initial_state(self) -> None:
        train_width = 20
        train_height = 20

        x_green = 40
        y_green = 115

        x_purple = 440
        y_purple = 115

        x_red = 40
        y_red = 260

        self.canvas.create_rectangle(50, 50, 450, 350)
        self.canvas.create_rectangle(50, 50, 250, 200)
        self.canvas.create_rectangle(250, 50, 450, 200)
        self.canvas_limits = {
            "green": [40, 40, 240, 190],
            "purple": [240, 40, 440, 190],
            "red": [40, 190, 440, 340],
        }
        self.safe_distance = 30

        green_train = self.canvas.create_rectangle(
            x_green,
            y_green,
            x_green + train_width,
            y_green + train_height,
            fill=GREEN_COLOR,
        )
        purple_train = self.canvas.create_rectangle(
            x_purple,
            y_purple,
            x_purple + train_width,
            y_purple + train_height,
            fill=PURPLE_COLOR,
        )
        red_train = self.canvas.create_rectangle(
            x_red,
            y_red,
            x_red + train_width,
            y_red + train_height,
            fill=RED_COLOR,
        )
        self.trains = {
            "green": green_train,
            "purple": purple_train,
            "red": red_train,
        }

    def run_app(self) -> None:
        self.root.mainloop()

    def _move_up(self, train_id, train_speed, y_min):
        _, y0, _, _ = self.canvas.coords(train_id)
        while y0 > y_min:
            speed = train_speed.get()
            if speed:
                x, y = 0, -10
                self.canvas.move(train_id, x, y)
                time.sleep(1 / speed)
                _, y0, _, _ = self.canvas.coords(train_id)

    def _move_right(self, train_id, train_speed, x_max):
        x0, _, _, _ = self.canvas.coords(train_id)
        while x0 < x_max:
            speed = train_speed.get()
            if speed:
                x, y = 10, 0
                self.canvas.move(train_id, x, y)
                time.sleep(1 / speed)
                x0, _, _, _ = self.canvas.coords(train_id)

    def _move_down(self, train_id, train_speed, y_max):
        _, y0, _, _ = self.canvas.coords(train_id)
        while y0 < y_max:
            speed = train_speed.get()
            if speed:
                x, y = 0, 10
                self.canvas.move(train_id, x, y)
                time.sleep(1 / speed)
                _, y0, _, _ = self.canvas.coords(train_id)

    def _move_left(self, train_id, train_speed, x_min):
        x0, _, _, _ = self.canvas.coords(train_id)
        while x0 > x_min:
            speed = train_speed.get()
            if speed:
                x, y = -10, 0
                self.canvas.move(train_id, x, y)
                time.sleep(1 / speed)
                x0, _, _, _ = self.canvas.coords(train_id)

    def cross_l1(self, train_id, train_speed, train_name=None):
        y_min = self.canvas_limits["green"][1]
        self._move_up(train_id, train_speed, y_min)

    def cross_l2(self, train_id, train_speed, train_name=None):
        x_max = self.canvas_limits["green"][2] - self.safe_distance
        self._move_right(train_id, train_speed, x_max)

    def cross_l3(self, train_id, train_speed, train_name=None):
        x_min, y_min, x_max, y_max = self.canvas_limits[train_name]
        if train_name == "green":
            self._move_right(train_id, train_speed, x_max)
            self._move_down(train_id, train_speed, y_max)
        else:
            self._move_left(train_id, train_speed, x_min)
            self._move_up(train_id, train_speed, y_min)

    def cross_l4(self, train_id, train_speed, train_name=None):
        x_min, y_min, x_max, y_max = self.canvas_limits[train_name]
        if train_name == "green":
            self._move_down(train_id, train_speed, y_max)
            self._move_left(train_id, train_speed, x_min)
        else:
            x_max -= self.safe_distance
            self._move_up(train_id, train_speed, y_min)
            self._move_right(train_id, train_speed, x_max)

    def cross_l5(self, train_id, train_speed, train_name=None):
        y_max = self.canvas_limits["purple"][3] - self.safe_distance
        self._move_down(train_id, train_speed, y_max)

    def cross_l6(self, train_id, train_speed, train_name=None):
        x_min, y_min, x_max, y_max = self.canvas_limits[train_name]
        if train_name == "purple":
            self._move_down(train_id, train_speed, y_max)
            self._move_left(train_id, train_speed, x_min)
        else:
            self._move_right(train_id, train_speed, x_max)

    def cross_l7(self, train_id, train_speed, train_name=None):
        x_max = self.canvas_limits["purple"][2]
        self._move_right(train_id, train_speed, x_max)

    def cross_l8(self, train_id, train_speed, train_name=None):
        y_min = self.canvas_limits["red"][1] + self.safe_distance
        self._move_up(train_id, train_speed, y_min)

    def cross_l9(self, train_id, train_speed, train_name=None):
        y_max = self.canvas_limits["red"][3]
        self._move_down(train_id, train_speed, y_max)

    def cross_l10(self, train_id, train_speed, train_name=None):
        x_min = self.canvas_limits["red"][0]
        self._move_left(train_id, train_speed, x_min)

    def cross_l3l4(self, train_id, train_speed, train_name=None):
        with self._lock:
            self.cross_l3(train_id, train_speed, train_name)
            self.cross_l4(train_id, train_speed, train_name)

    def cross_l6l3(self, train_id, train_speed, train_name=None):
        with self._lock:
            self.cross_l6(train_id, train_speed, train_name)
            self.cross_l3(train_id, train_speed, train_name)

    def cross_l4l6(self, train_id, train_speed, train_name=None):
        with self._lock:
            self.cross_l4(train_id, train_speed, train_name)
            self.cross_l6(train_id, train_speed, train_name)

    def move_train(self, train_name, train_id, train_speed) -> None:
        train_paths = {
            "green": [self.cross_l1, self.cross_l2, self.cross_l3l4],
            "purple": [self.cross_l5, self.cross_l6l3, self.cross_l7],
            "red": [self.cross_l8, self.cross_l4l6, self.cross_l9, self.cross_l10],
        }
        paths = train_paths[train_name]
        while train_id:
            for rail in paths:
                rail(train_id, train_speed, train_name)

    def move_trains(self) -> None:
        trains = ["green", "purple", "red"]
        for train in trains:
            train_name = train
            train_id = self.trains[train_name]
            train_speed = self.train_speeds[train_name]
            thread = threading.Thread(
                target=self.move_train,
                args=(train_name, train_id, train_speed),
                daemon=True,
            )
            thread.start()


if __name__ == "__main__":
    my_app = MyApp()
