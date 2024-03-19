import socket
import json
import tkinter as tk
from tkinter import ttk

# Configurações do cliente.
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 65432  # Porta do servidor


def send_command(command: dict) -> str:
    """
    Envia comandos ao servidor (telescópio na rede)

    :param command: dicionário de instruções em formato de json
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(json.dumps(command).encode())
            response = s.recv(1024)
            return "Successfully sent command\n" + ("-" * 70) + "\n" + f"Response: {response.decode()}"
    except ConnectionRefusedError:
        return "Unable to connect with telescope.\n" + ("-" * 70) + "\n"


# Exemplo de comandos


def on_track():
    response = send_command({
        "command": "TRACK",
        "metadata": "NULL"
    })

    response_label.config(text=response)


def on_goto():
    ra_value = f"{ra_hour.get()}h {ra_minute.get()}m {ra_second.get()}s"
    dec_value = f"{dec_degree.get()}° {dec_minute.get()}' {dec_second.get()}\""
    command = {
        "command": "GOTO",
        "metadata": {
            "ra": ra_value,
            "dec": dec_value
        }
    }
    response = send_command(command)

    response_label.config(text=response)


def on_dc():
    response = send_command({
        "command": "DISCONNECT",
        "metadata": "NULL"
    })

    response_label.config(text=response)


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 12), padding=5)
    root.title("Cliente ScopeNet")
    root.iconbitmap("assets/favicon.ico")

    btn_track = ttk.Button(root, text="Track", command=on_track)
    btn_track.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    separator = ttk.Separator(root, orient='horizontal')
    separator.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=5)

    frame_goto = ttk.Frame(root)
    frame_goto.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    btn_goto = ttk.Button(frame_goto, text="GoTo", command=on_goto)
    btn_goto.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    frame_ra = ttk.Frame(frame_goto)
    frame_ra.grid(row=0, column=0, padx=10, pady=5)

    ra_hour = tk.StringVar()
    ra_minute = tk.StringVar()
    ra_second = tk.StringVar()

    ra_hour_entry = ttk.Entry(frame_ra, width=5, textvariable=ra_hour)
    ra_hour_entry.grid(row=0, column=0, padx=(0, 5))

    ra_minute_entry = ttk.Entry(frame_ra, width=5, textvariable=ra_minute)
    ra_minute_entry.grid(row=0, column=2, padx=(0, 5))

    ra_second_entry = ttk.Entry(frame_ra, width=5, textvariable=ra_second)
    ra_second_entry.grid(row=0, column=4, padx=(0, 5))

    ttk.Label(frame_ra, text="h").grid(row=0, column=1, padx=(0, 5))
    ttk.Label(frame_ra, text="m").grid(row=0, column=3, padx=(0, 5))
    ttk.Label(frame_ra, text="s").grid(row=0, column=5)

    frame_dec = ttk.Frame(frame_goto)
    frame_dec.grid(row=0, column=1, padx=10, pady=5)

    dec_degree = tk.StringVar()
    dec_minute = tk.StringVar()
    dec_second = tk.StringVar()

    dec_degree_entry = ttk.Entry(frame_dec, width=5, textvariable=dec_degree)
    dec_degree_entry.grid(row=0, column=0, padx=(0, 5))

    dec_minute_entry = ttk.Entry(frame_dec, width=5, textvariable=dec_minute)
    dec_minute_entry.grid(row=0, column=2, padx=(0, 5))

    dec_second_entry = ttk.Entry(frame_dec, width=5, textvariable=dec_second)
    dec_second_entry.grid(row=0, column=4, padx=(0, 5))

    ttk.Label(frame_dec, text="°").grid(row=0, column=1, padx=(0, 5))
    ttk.Label(frame_dec, text="'").grid(row=0, column=3, padx=(0, 5))
    ttk.Label(frame_dec, text="\"").grid(row=0, column=5)

    separator = ttk.Separator(root, orient='horizontal')
    separator.grid(row=3, column=0, columnspan=2, sticky='ew', padx=10)

    response_label = tk.Label(root, text="-" * 70 + "\n", font=('Arial', 12), wraplength=400)
    response_label.grid(row=4, column=0, columnspan=2, padx=10, pady=(10, 0))

    btn_finish = tk.Button(root, text="Finish Connection", command=on_dc)
    btn_finish.grid(row=5, column=0, columnspan=2, padx=10, pady=(10, 0))

    root.mainloop()
