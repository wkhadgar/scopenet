import socket
import json


def process_command(command):
    """
    Trata o comando recebido.

    :param command: Comando recebido como dicionário json.
    :return: Resposta ao comando.
    """

    if command['command'] == "TRACK":
        return f"Comando TRACK recebido."
    elif command['command'] == "GOTO":
        return f"Comando GOTO:\nRA={command['metadata']['ra']}, DEC={command['metadata']['dec']}"
    elif command['command'] == "DISCONNECT":
        return "DISCONNECT"
    else:
        return f"Comando '{command['command']}' não reconhecido..."


if __name__ == "__main__":
    HOST = '127.0.0.1'  # Endereço IP local
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Telescópio esperando por comandos...")

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
                        response = "Conexão encerrada."
                        print("Fim de conexão solicitado.")

                    conn.sendall(response.encode())
