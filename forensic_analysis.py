import os
import subprocess
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
username_faraday = os.getenv("USER_FARADAY")
password_faraday = os.getenv("PASS_FARADAY")
host_faraday = os.getenv("HOST_FARADAY")
workspaces_faraday = os.getenv("WORKSPACE_FARADAY")

# Función para ejecutar el análisis forense
def forensic_analysis():
    try:
        # Captura de tráfico de red con Wireshark
        subprocess.run("tshark -i eth0 -a duration:60 -w /ruta/a/captura.pcap", shell=True)  # Reemplazar con la interfaz y ruta correctas
        # Análisis de memoria con Volatility
        subprocess.run("vol.py -f /ruta/a/dump.mem --profile=Win7SP1x64 pslist", shell=True)  # Reemplazar con el perfil correcto
        # Creación de imagen forense con FTK Imager
        subprocess.run("ftkimager /ruta/a/disco /ruta/a/output.dd", shell=True)  # Reemplazar con la ruta correcta
        # Enviar resultados a Faraday
        subprocess.run(f"faraday-cli auth -f {host_faraday} -u {username_faraday} -p {password_faraday}", shell=True)
        subprocess.run(f"faraday-cli workspace select {workspaces_faraday}", shell=True)
        subprocess.run(f"faraday-cli report create 'Análisis Forense' --workspace {workspaces_faraday}", shell=True)
    except Exception as e:
        print(f"Ocurrió un error durante el análisis forense: {e}")

def main():
    forensic_analysis()

if __name__ == '__main__':
    main()
