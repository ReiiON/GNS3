# GNS3

Proyecto de Automatización de Infraestructura de Red

Este proyecto tiene como objetivo automatizar la configuración de dispositivos de red en un entorno de GNS3, utilizando Python y GitHub Actions para gestionar la infraestructura de red y la ejecución de tareas de configuración.


Descripción

La infraestructura de red se compone de dispositivos de red Cisco (en GNS3) configurados automáticamente utilizando scripts en Python. Se incluye la configuración de SSH, la obtención de la configuración en ejecución (show running-config), y la verificación de las rutas IP en cada dispositivo.
Este proyecto también implementa un pipeline de CI/CD en GitHub Actions para automatizar la ejecución de configuraciones y la verificación en los dispositivos de red, permitiendo un flujo continuo de integración y despliegue.


Estructura del Proyecto

secret/: Contiene scripts de configuración sensibles como config-routers.py, config-ssh.py y verify_config.py.
.github/workflows/: Contiene el archivo ci-cd-pipeline.yml que define el pipeline de CI/CD utilizando GitHub Actions.
configs/: Archivos de configuración que son aplicados a los dispositivos de red (e.g., config_ssh.txt).
tests/: Scripts de prueba y configuraciones comunes.


Requisitos

Python 3.13.0
Netmiko: Para la conexión SSH y ejecución de comandos en los dispositivos de red.
GitHub Actions: Para la integración continua y despliegue.


Uso

Conectar y aplicar configuraciones
Para conectar a los dispositivos de red y aplicar configuraciones automáticamente:
Asegúrate de tener el archivo devices.json con las credenciales y configuraciones de los dispositivos.
Ejecuta el script de configuración correspondiente: python config-routers.py


CI/CD

El archivo .github/workflows/CI-CD.yml define un flujo de trabajo automatizado que se ejecuta cada vez que se realiza un push a la rama main. Este flujo de trabajo se encarga de ejecutar las configuraciones y verificar el estado de los dispositivos de red.

