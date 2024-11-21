import netmiko
import os


# Función para generar dispositivos dinámicamente en un rango de IPs

def generate_device_list(base_ip, start, end, username, password, device_type):
    devices = []
    for i in range(start, end + 1):
        devices.append({
            "device_type": device_type,
            "host": f"{base_ip}.{i}",
            "username": username,
            "password": password
        })
    return devices


# Función para conectarse a un dispositivo
def connect_device(device):
    try:
        net_connect = netmiko.ConnectHandler(
            device_type=device['device_type'],
            host=device['host'],
            username=device['username'],
            password=device['password'],
            port=22  # Puerto SSH
        )
        print(f"Conectado a {device['host']}")
        return net_connect
    except Exception as e:
        print(f"Error al conectar con {device['host']}: {e}")
        return None


# Función para aplicar configuración desde un archivo
def apply_config_from_file(net_connect, config_file):
    if os.path.exists(config_file):
        try:
            net_connect.send_config_from_file(config_file=config_file)
            print(f"Configuración aplicada desde {config_file}")
        except Exception as e:
            print(f"Error al aplicar configuración desde {config_file}: {e}")
    else:
        print(f"Archivo de configuración no encontrado: {config_file}")


# Función para verificar la configuración
def verify_configuration(net_connect):
    try:
        output = net_connect.send_command('show ip int brief')
        print(f"Verificación de configuración:\n{output}")
    except Exception as e:
        print(f"Error al verificar la configuración: {e}")


# Función para desconectar del dispositivo
def disconnect_device(net_connect):
    try:
        net_connect.disconnect()
        print("Desconectado del dispositivo.")
    except Exception as e:
        print(f"Error al desconectar: {e}")


# Función principal
def main():
    # Solicitar rango de IPs al usuario
    base_ip = input("Ingrese la IP base (por ejemplo, 192.168.42): ")
    start = int(input("Ingrese el número inicial del rango de IPs (por ejemplo, 201): "))
    end = int(input("Ingrese el número final del rango de IPs (por ejemplo, 205): "))
    
    # Credenciales y tipo de dispositivo
    username = "admin"
    password = "pandacode"
    device_type = "cisco_ios"

    # Generar lista de dispositivos
    devices = generate_device_list(base_ip, start, end, username, password, device_type)

    # Archivos de configuración
    common_config_file = os.path.join(os.getcwd(), "configs", "common_config.txt")
    ssh_config_file = os.path.join(os.getcwd(), "configs", "config_ssh.txt")

    # Configurar cada dispositivo
    for device in devices:
        net_connect = connect_device(device)
        if net_connect:
            # Aplicar configuración predeterminada
            apply_config_from_file(net_connect, common_config_file)
            # Aplicar configuración de SSH
            apply_config_from_file(net_connect, ssh_config_file)
            # Verificar configuración
            verify_configuration(net_connect)
            # Desconectar
            disconnect_device(net_connect)


if __name__ == "__main__":
    main()
