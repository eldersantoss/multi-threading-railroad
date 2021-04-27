#!./venv/bin/python3

import time
import threading
import tkinter as tk


GREEN_COLOR = "#60ad5e"
PURPLE_COLOR = "#6746c3"
RED_COLOR = "#b71c1c"


class MyApp:
    def __init__(self) -> None:
        self.lock = threading.Lock()
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
        y_green = 40

        x_purple = 440
        y_purple = 120

        x_red = 40
        y_red = 260

        self.canvas.create_rectangle(50, 50, 450, 350)
        self.canvas.create_rectangle(50, 50, 250, 200)
        self.canvas.create_rectangle(250, 50, 450, 200)

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

    def move_train(self, train_name, train_id, speed) -> None:

        canvas_limits = {
            "green": {
                "top_left": {"x": 40, "y": 40},
                "bottom_right": {"x": 240, "y": 190},
            },
            "purple": {
                "top_left": {"x": 240, "y": 40},
                "bottom_right": {"x": 440, "y": 190},
            },
            "red": {
                "top_left": {"x": 40, "y": 190},
                "bottom_right": {"x": 440, "y": 340},
            },
        }

        def in_lock_position(x0, y0):
            in_l3 = 220 < x0 < 260 and y0 in [40, 190]
            in_l4 = x0 in [40, 240] and 170 < y0 < 210
            in_l6 = 220 < x0 <= 440 and 170 <= y0 <= 190
            return in_l3 or in_l4 or in_l6

        limits = canvas_limits[train_name]
        while train_id:
            x0, y0, _, _ = self.canvas.coords(train_id)
            train_speed = speed.get()
            x, y = 0, 0
            locked = False
            if in_lock_position(x0, y0):
                locked = self.lock.acquire()
            elif locked:
                self.lock.release()
            if train_speed:
                # Pra cima
                if x0 == limits["top_left"]["x"] and y0 > limits["top_left"]["y"]:
                    y = -10
                # Pra direita
                if y0 == limits["top_left"]["y"] and x0 < limits["bottom_right"]["x"]:
                    x = 10
                # Pra baixo
                if (
                    x0 == limits["bottom_right"]["x"]
                    and y0 < limits["bottom_right"]["y"]
                ):
                    y = 10
                # Pra esquerda
                if y0 == limits["bottom_right"]["y"] and x0 > limits["top_left"]["x"]:
                    x = -10
                self.canvas.move(train_id, x, y)

                sleep_interval = 1 / train_speed
                time.sleep(sleep_interval)

    def move_trains(self) -> None:
        trains = ["green", "purple", "red"]
        for train in trains:
            train_name = train
            train_id = self.trains[train_name]
            thread = threading.Thread(
                target=self.move_train,
                args=(train_name, train_id, self.train_speeds[train_name]),
                daemon=True,
            )
            thread.start()

    def run_app(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    my_app = MyApp()
