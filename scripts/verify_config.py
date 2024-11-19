import json
import netmiko
import os
from datetime import datetime

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

# Función para obtener la configuración completa del router (sh run)
def get_running_config(net_connect):
    try:
        output = net_connect.send_command('show running-config')
        return f"Running Config:\n{output}\n"
    except Exception as e:
        return f"Error al obtener el running-config: {e}\n"

# Función para obtener la configuración de rutas IP
def get_ip_routes(net_connect):
    try:
        output = net_connect.send_command('show ip route')
        return f"IP Routing Table:\n{output}\n"
    except Exception as e:
        return f"Error al obtener las rutas IP: {e}\n"

# Función para desconectar del dispositivo
def disconnect_device(net_connect):
    try:
        net_connect.disconnect()
        print(f"Desconectado de {net_connect.host}.")
    except Exception as e:
        print(f"Error al desconectar de {net_connect.host}: {e}")

# Función para guardar los resultados en un archivo
def save_results_to_file(router_name, results, result_type):
    # Crear directorio si no existe
    results_dir = r"C:\GNS3-PYTHON\GNS3\results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Obtener la fecha actual
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Crear el nombre de archivo según el tipo de resultado
    file_name = os.path.join(results_dir, f"{router_name}_{result_type}_{date_str}.txt")
    
    # Guardar los resultados en un archivo
    with open(file_name, "w") as file:
        file.write(results)
    print(f"Resultados guardados en {file_name}")

# Main loop para conectar y obtener configuraciones
def main():
    # Cargar dispositivos desde el archivo JSON
    devices = load_devices("C:/GNS3-PYTHON/GNS3/configs/devices.json")

    for device in devices:
        net_connect = connect_device(device)
        if net_connect:
            router_name = device['router_name']  # Obtener el nombre del router desde 'router_name'

            # Obtener el running-config
            running_config = get_running_config(net_connect)
            save_results_to_file(router_name, running_config, "running_config")
            
            # Obtener la configuración de rutas IP
            ip_routes = get_ip_routes(net_connect)
            save_results_to_file(router_name, ip_routes, "ip_routes")
            
            # Desconectar del dispositivo
            disconnect_device(net_connect)

if __name__ == "__main__":
    main()
