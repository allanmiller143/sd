import socket
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Chave de criptografia (carregada do arquivo .env)
chave = os.getenv('SECRET_KEY').encode()

cipher_suite = Fernet(chave)

def encrypt_message(message):
    return cipher_suite.encrypt(message.encode())

def decrypt_message(encrypted_message):
    return cipher_suite.decrypt(encrypted_message).decode()

def discover_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.bind(('', 37020))
    while True:
        data, addr = client_socket.recvfrom(1024)
        if data.startswith(b"SERVER"):
            _, port = data.decode().split(':')
            return addr[0], int(port)

def main():
    # Descoberta do endereço do servidor via broadcast
    print("Procurando pelo servidor...")
    host, port = discover_server()
    print(f"Servidor encontrado em {host}:{port}")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Loop para enviar solicitações de estoque e transferências
    while True:
        print("\nOpções:")
        print("1. Solicitar leitura de estoque")
        print("2. Solicitar transferência de estoque")
        print("3. Sair")

        opcao = input("Escolha uma opção (1/2/3): ")

        if opcao == '1':
            loja_id = input("Digite o ID da loja: ")
            message = f'GET:{loja_id}'
            client_socket.send(encrypt_message(message))
            encrypted_response = client_socket.recv(1024)
            response = decrypt_message(encrypted_response)
            print("Resposta do servidor:", response)

        elif opcao == '2':
            loja_origem = input("Digite o ID da loja de origem: ")
            loja_destino = input("Digite o ID da loja de destino: ")
            produto = input("Digite o nome do produto: ")
            quantidade = input("Digite a quantidade a ser transferida: ")
            message = f'TRANSFER:{loja_origem}:{loja_destino}:{produto}:{quantidade}'
            client_socket.send(encrypt_message(message))
            encrypted_response = client_socket.recv(1024)
            response = decrypt_message(encrypted_response)
            print("Resposta do servidor:", response)

        elif opcao == '3':
            print("Encerrando o cliente...")
            break

        else:
            print("Opção inválida. Escolha novamente.")

    client_socket.close()

if __name__ == "__main__":
    main()
