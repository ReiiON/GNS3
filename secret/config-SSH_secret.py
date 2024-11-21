import netmiko
import json
import os

# Función para cargar dispositivos desde un archivo JSON
def load_devices(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Función para conectarse a un dispositivo
def connect_device(device):
    try:
        # Obtener las credenciales de los secretos (variables de entorno)
        username = os.getenv('ROUTER_USER')  # GitHub inyecta este valor
        password = os.getenv('ROUTER_PASSWORD')  # GitHub inyecta este valor

        net_connect = netmiko.ConnectHandler(
            device_type=device['device_type'],
            host=device['host'],
            username=username,  # Nombre de usuario desde secretos
            password=password,  # Contraseña desde secretos
            port=22  # Puerto SSH predeterminado
        )
        print(f"Conectado a {device['host']}")
        return net_connect
    except Exception as e:
        print(f"Error al conectar con {device['host']}: {e}")
        return None

# Función para configurar SSH en el router
def configure_ssh(net_connect):
    try:
        # Leer configuración SSH desde el archivo
        ssh_config_file = os.path.join(os.getcwd(), "configs", "config_ssh.txt")
        
        # Enviar comandos de configuración
        net_connect.send_config_from_file(config_file=ssh_config_file)
        print("SSH configurado correctamente.")
    except Exception as e:
        print(f"Error al configurar SSH: {e}")

# Función para desconectar del dispositivo
def disconnect_device(net_connect):
    try:
        net_connect.disconnect()
        print("Desconectado del dispositivo.")
    except Exception as e:
        print(f"Error al desconectar: {e}")

# Main loop para conectar y configurar SSH
def main():
    # Cargar dispositivos desde JSON
    devices = load_devices("C:/GNS3-PYTHON/GNS3/configs/devices.json")

    for device in devices:
        net_connect = connect_device(device)
        if net_connect:
            # Configurar SSH
            configure_ssh(net_connect)
            disconnect_device(net_connect)

if __name__ == "__main__":
    main()
