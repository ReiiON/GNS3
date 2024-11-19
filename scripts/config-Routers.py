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
        net_connect = netmiko.ConnectHandler(
            device_type=device['device_type'],
            host=device['host'],
            username=device['username'],
            password=device['password'],
            port=22  # Puerto SSH predeterminado
        )
        print(f"Conectado a {device['host']}")
        return net_connect
    except Exception as e:
        print(f"Error al conectar con {device['host']}: {e}")
        return None


# Función para aplicar configuración desde un archivo
def apply_config_from_file(net_connect, config_file):
    try:
        net_connect.send_config_from_file(config_file=config_file)
        print(f"Configuración aplicada desde {config_file}")
    except Exception as e:
        print(f"Error al aplicar configuración desde {config_file}: {e}")


# Función para aplicar un conjunto de configuraciones
def apply_config_set(net_connect, config_commands):
    try:
        net_connect.send_config_set(config_commands)
        print("Comandos de configuración aplicados.")
    except Exception as e:
        print(f"Error al aplicar comandos de configuración: {e}")


# Función para verificar la configuración (comando opcional)
def verify_configuration(net_connect):
    try:
        output = net_connect.send_command('show ip int brief')
        print(f"Configuración verificada:\n{output}")
    except Exception as e:
        print(f"Error al verificar la configuración: {e}")


# Función para desconectar del dispositivo
def disconnect_device(net_connect):
    try:
        net_connect.disconnect()
        print("Desconectado del dispositivo.")
    except Exception as e:
        print(f"Error al desconectar: {e}")


# Función para obtener un archivo de configuración específico por router
def get_router_config_file(router_name):
    # Ruta directa para cada router
    router_config_paths = {
        "192.168.42.201": "C:/GNS3-PYTHON/GNS3/configs/R1.txt",
        "192.168.42.202": "C:/GNS3-PYTHON/GNS3/configs/R2.txt",
        "192.168.42.203": "C:/GNS3-PYTHON/GNS3/configs/R3.txt"
    }
    
    # Verificar si el archivo de configuración existe para el router
    config_file = router_config_paths.get(router_name)
    if config_file and os.path.exists(config_file):
        return config_file
    else:
        print(f"No se encontró el archivo de configuración para {router_name}, usando configuración predeterminada.")
        return os.path.join(os.getcwd(), "tests", "common_config.txt")  # Archivo común si no se encuentra el específico


# Main loop para conectar y aplicar configuraciones
def main():
    # Cargar dispositivos desde JSON
    devices = load_devices("C:/GNS3-PYTHON/GNS3/configs/devices.json")

    for device in devices:
        net_connect = connect_device(device)
        if net_connect:
            router_name = device['host']  # Usamos el 'host' como el nombre del router
            router_config_file = get_router_config_file(router_name)  # Buscar archivo de configuración específico

            # Aplicar configuración común
            apply_config_from_file(net_connect, os.path.join(os.getcwd(), "tests", "common_config.txt"))
            # Aplicar configuración desde archivo específico para el router
            apply_config_from_file(net_connect, router_config_file)
            verify_configuration(net_connect)
            disconnect_device(net_connect)


if __name__ == "__main__":
    main()
