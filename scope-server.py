"""
 :file: scope-server.py
 :author: Paulo Santos (pauloxrms@gmail.com)
 :brief: Servidor base, representando um observatório.
 :version: 0.1
 :date: 22-02-2024

 :copyright: Copyright Paulo R. Santos (c) 2024
"""

import socket
import json
import threading

HOST = '127.0.0.1'  # Endereço IP local
PORT = 65432  # Porta do servidor

target_ra = {"h": 0, "m": 0, "s": 0}
target_dec = {"°": 0, "'": 0, "\"": 0}

slewing = False


def save_target_loc(goto_metadata: dict[str, str]):
    """
    Atualiza a posição alvo do telescópio.

    :param goto_metadata: Dados obtidos pelo socket, representando a posição de destino.
    :return: -1 em caso de erro, 0 caso contrário.
    """
    ra_recv = goto_metadata['ra'].split(" ")
    dec_recv = goto_metadata['dec'].split(" ")

    try:
        for i, k in enumerate(target_ra.keys()):
            target_ra[k] = int(ra_recv[i][:-1])

        for i, k in enumerate(target_dec.keys()):
            target_dec[k] = int(dec_recv[i][:-1])

    except ValueError:
        return -1

    slewing = True
    return 0


def process_command(command):
    """
    Trata o comando recebido.

    :param command: Comando recebido como dicionário json.
    :return: Resposta ao comando.
    """
    if slewing:
        return "Telescope is slewing. Wait to finish."
    if command["command"] == "TRACK":
        return ("Tracking current position:\n"
                f"RA: {target_ra};\nDEC: {target_dec}")
    elif command["command"] == "GOTO":
        if save_target_loc(command['metadata']) != 0:
            return f"Incorrect data:\nRA={command['metadata']['ra']}, DEC={command['metadata']['dec']}"
        else:
            return f"Going to:\nRA={command['metadata']['ra']}, DEC={command['metadata']['dec']}"
    elif command["command"] == "DISCONNECT":
        return "DISCONNECT"
    else:
        return f"Command '{command['command']}' not recognized..."


def handle_connection(client: socket):
    """
    Thread que gerencia uma conexão socket com um client.

    :param client: Cliente conectado.
    """
    connected = True
    while connected:
        try:
            # Recebe os dados do cliente
            data = client.recv(1024).decode()

            if data:
                # Decodifica os dados recebidos do cliente
                command_json = json.loads(data)
                print(f"[{addr[0]}: {command_json['command']}")
                response = process_command(command_json)

                if response == "DISCONNECT":
                    connected = False
                    response = "Telescope detached"
                    connected_clients.remove(client)
                    print("Fim de conexão solicitado.")

                client.send(response.encode())
        except:
            connected_clients.remove(client)
            connected = False
            print("Conexão perdida.")
    client.close()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()

    connected_clients = []
    print("Telescope is waiting for connection...")

    while True:
        conn, addr = s.accept()
        if conn not in connected_clients:
            print(f"Connected to {addr[0]}! Waiting for commands...")
            connected_clients.append(conn)
            conn.send("Connected successfully.".encode())

            thread = threading.Thread(target=handle_connection, args=(conn,))
            thread.start()
        else:
            conn.send("Already connected.".encode())
