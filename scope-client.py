"""
 :file: scope-client.py
 :author: Paulo Santos (pauloxrms@gmail.com)
 :brief: Cliente base, representando um controlador do observatório.
 :version: 0.1
 :date: 22-02-2024

 :copyright: Copyright Paulo R. Santos (c) 2024
"""

import socket
import json
import threading
import tkinter as tk
from tkinter import ttk

# Configurações do cliente.
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 65432  # Porta do servidor

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

command_requests = {
    "DISCONNECT": False,
    "GOTO": False,
    "TRACK": False,
}

commands = {
    "DISCONNECT": {
        "command": "DISCONNECT",
        "metadata": "NULL"
    },
    "GOTO": {
        "command": "GOTO",
        "metadata": {
            "ra": "",
            "dec": "",
        }
    },
    "TRACK": {
        "command": "TRACK",
        "metadata": "NULL"
    },
}


def on_track():
    command_requests["TRACK"] = True


def on_goto():
    commands["GOTO"]["metadata"]["ra"] = f"{ra_hour.get()}h {ra_minute.get()}m {ra_second.get()}s"
    commands["GOTO"]["metadata"]["dec"] = f"{dec_degree.get()}° {dec_minute.get()}' {dec_second.get()}\""
    command_requests["GOTO"] = True


def on_dc():
    command_requests["DISCONNECT"] = True


def message_manager():
    """
    Thread responsável pelo gerenciamento de mensagens a serem enviadas para o servidor.
    """
    response = ("-" * 70) + "\n" + f"{s.recv(1024).decode()}"
    response_label.config(text=response)
    run = True
    while run:
        for cbr in list(command_requests.keys()):
            if command_requests[cbr]:
                try:
                    s.send(json.dumps(commands[cbr]).encode())
                    response = "Successfully sent command\n" + ("-" * 70) + "\n" + f"Response: {s.recv(1024).decode()}"
                except:
                    response = "Unable to connect with telescope.\n" + ("-" * 70) + "\n"
                    s.close()
                    run = False
                command_requests[cbr] = False
                response_label.config(text=response)


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 12), padding=5)
    root.title("Cliente ScopeNet")
    root.iconbitmap("assets/favicon.ico")

    separator = ttk.Separator(root, orient='horizontal')
    separator.grid(row=0, column=0, columnspan=2, sticky='ew', padx=10, pady=5)

    frame_ra = ttk.Frame(root)
    frame_ra.grid(row=1, column=0, padx=10, pady=5)
    ra_hour = tk.StringVar()
    ra_hour_entry = ttk.Entry(frame_ra, width=5, textvariable=ra_hour)
    ra_hour_entry.grid(row=0, column=0, padx=(0, 5))
    ttk.Label(frame_ra, text="h").grid(row=0, column=1, padx=(0, 5))
    ra_minute = tk.StringVar()
    ra_minute_entry = ttk.Entry(frame_ra, width=5, textvariable=ra_minute)
    ra_minute_entry.grid(row=0, column=2, padx=(0, 5))
    ttk.Label(frame_ra, text="m").grid(row=0, column=3, padx=(0, 5))
    ra_second = tk.StringVar()
    ra_second_entry = ttk.Entry(frame_ra, width=5, textvariable=ra_second)
    ra_second_entry.grid(row=0, column=4, padx=(0, 5))
    ttk.Label(frame_ra, text="s").grid(row=0, column=5)

    frame_dec = ttk.Frame(root)
    frame_dec.grid(row=1, column=1, padx=10, pady=5)
    dec_degree = tk.StringVar()
    dec_degree_entry = ttk.Entry(frame_dec, width=5, textvariable=dec_degree)
    dec_degree_entry.grid(row=0, column=0, padx=(0, 5))
    ttk.Label(frame_dec, text="°").grid(row=0, column=1, padx=(0, 5))
    dec_minute = tk.StringVar()
    dec_minute_entry = ttk.Entry(frame_dec, width=5, textvariable=dec_minute)
    dec_minute_entry.grid(row=0, column=2, padx=(0, 5))
    ttk.Label(frame_dec, text="'").grid(row=0, column=3, padx=(0, 5))
    dec_second = tk.StringVar()
    dec_second_entry = ttk.Entry(frame_dec, width=5, textvariable=dec_second)
    dec_second_entry.grid(row=0, column=4, padx=(0, 5))
    ttk.Label(frame_dec, text="\"").grid(row=0, column=5)

    btn_goto = ttk.Button(root, text="GoTo", command=on_goto)
    btn_goto.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    separator = ttk.Separator(root, orient='horizontal')
    separator.grid(row=3, column=0, columnspan=2, sticky='ew', padx=10)

    btn_track = ttk.Button(root, text="Track", command=on_track)
    btn_track.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    response_label = tk.Label(root, text="-" * 70 + "\n", font=('Arial', 12), wraplength=400)
    response_label.grid(row=5, column=0, columnspan=2, padx=10, pady=(10, 0))

    btn_finish = tk.Button(root, text="Finish Connection", command=on_dc)
    btn_finish.grid(row=6, column=0, columnspan=2, padx=10, pady=(10, 0))

    thread = threading.Thread(target=message_manager)
    thread.start()

    root.mainloop()
