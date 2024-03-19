import socket
import json

target_ra = {"h": 0, "m": 0, "s": 0}
target_dec = {"°": 0, "'": 0, "\"": 0}


def save_target_loc(goto_metadata: dict[str, str]):
    ra_recv = goto_metadata['ra'].split(" ")
    dec_recv = goto_metadata['dec'].split(" ")
    try:
        target_ra[ra_recv[0][-1]] = int(ra_recv[0][:-1])
        target_ra[ra_recv[1][-1]] = int(ra_recv[1][:-1])
        target_ra[ra_recv[2][-1]] = int(ra_recv[2][:-1])

        target_dec[dec_recv[0][-1]] = int(dec_recv[0][:-1])
        target_dec[dec_recv[1][-1]] = int(dec_recv[1][:-1])
        target_dec[dec_recv[2][-1]] = int(dec_recv[2][:-1])
    except:
        return -1
    return 0


def process_command(command):
    """
    Trata o comando recebido.

    :param command: Comando recebido como dicionário json.
    :return: Resposta ao comando.
    """

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


if __name__ == "__main__":
    HOST = '127.0.0.1'  # Endereço IP local
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Telescope is waiting for commands...")

        connected = True
        while connected:
            conn, addr = s.accept()
            with conn:
                while True:
                    # Recebe os dados do cliente
                    data = conn.recv(1024)
                    if not data:
                        break

                    # Decodifica os dados recebidos do cliente
                    command_json = json.loads(data.decode())
                    print(f"[{addr[0]}:{addr[1]}]: {command_json['command']}")
                    response = process_command(command_json)
                    if response == "DISCONNECT":
                        connected = False
                        response = "Telescope turned off."
                        print("Fim de conexão solicitado.")

                    conn.sendall(response.encode())
