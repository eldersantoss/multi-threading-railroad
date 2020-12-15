#!./venv/bin/python3

import json
import socket
import tkinter as tk
from tkinter import ttk


class AppConnection():

    def __init__(self, host_addr='127.0.0.1', port_number=65432):
        self.HOST = host_addr
        self.PORT = port_number

        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect((self.HOST, self.PORT))

    def send_updates(self, data):
        self.soc.sendall(data)

    def close_connection(self):
        self.soc.close()


class MyApp():

    def __init__(self):
        print('Iniciando app...')
        self.root = tk.Tk()
        self.root.title('Velocidade dos trens')

        self.green_speed = tk.IntVar()
        self.purple_speed = tk.IntVar()
        self.orange_speed = tk.IntVar()
        self.blue_speed = tk.IntVar()

        self.create_widgets()

        self.connection = AppConnection()

        self.root.mainloop()

    def print_values(self, event):
        print(event)
        print('Verde:', self.green_speed.get())
        print('Roxo:', self.purple_speed.get())
        print('Laranja:', self.orange_speed.get())
        print('Azul:', self.blue_speed.get())
        print()

    def update_speeds(self):
        data = {
            'green': self.green_speed.get(),
            'purple': self.purple_speed.get(),
            'orange': self.orange_speed.get(),
            'blue': self.blue_speed.get(),
        }
        data_json = json.dumps(data)
        data_json_bytes = data_json.encode('utf-8')
        self.connection.send_updates(data_json_bytes)

    def create_widgets(self):
        self.content = ttk.Frame(
            self.root,
        ).grid(
            row=0,
            column=0,
        )

        ttk.Label(
            self.content,
            text='Painel de controle de velocidade',
        ).grid(
            row=0,
            column=0,
            rowspan=1,
            columnspan=4,
            padx='20',
            pady='20',
        )

        ttk.Scale(
            self.content,
            variable=self.green_speed,
            from_=0,
            to=100,
            length=100,
            orient=tk.VERTICAL,
        ).grid(
            row=1,
            column=0,
            padx=15,
        )

        ttk.Label(
            self.content,
            text='Verde',
        ).grid(
            row=2,
            column=0,
            padx=20,
            pady=20,
        )

        ttk.Scale(
            self.content,
            variable=self.purple_speed,
            from_=0,
            to=100,
            length=100,
            orient=tk.VERTICAL,
        ).grid(
            row=1,
            column=1,
            padx=15,
        )

        ttk.Label(
            self.content,
            text='Roxo',
        ).grid(
            row=2,
            column=1,
            padx=20,
            pady=20,
        )

        ttk.Scale(
            self.content,
            variable=self.orange_speed,
            from_=0,
            to=100,
            length=100,
            orient=tk.VERTICAL,
        ).grid(
            row=1,
            column=2,
            padx=15,
        )

        ttk.Label(
            self.content,
            text='Laranja',
        ).grid(
            row=2,
            column=2,
            padx=20,
            pady=20,
        )

        ttk.Scale(
            self.content,
            variable=self.blue_speed,
            from_=0,
            to=100,
            length=100,
            orient=tk.VERTICAL,
        ).grid(
            row=1,
            column=3,
            padx=15,
        )

        ttk.Label(
            self.content,
            text='Azul',
        ).grid(
            row=2,
            column=3,
            padx=20,
            pady=20,
        )

        ttk.Button(
            self.content,
            text='Atualizar velocidades',
            command=self.update_speeds
        ).grid(
            row=3,
            column=0,
            columnspan=4,
            ipadx=30,
            ipady=5,
            pady=(0, 20),
        )


if __name__ == "__main__":
    my_app = MyApp()
