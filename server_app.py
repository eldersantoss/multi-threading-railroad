#!./venv/bin/python3

import json
import socket


HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:
        print('Aguardando conexao...')
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)

            while True:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break

                data = json.loads(data)

                for train in data:
                    print(f'{train}: {data[train]}')
                print()

        res = input('Encerrar aplicacao? (s - sim): ')
        if res in ['s', 'S', 'sim', 'sim']:
            break
