import os
import subprocess
import json
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
username_faraday = os.getenv("USER_FARADAY")
password_faraday = os.getenv("PASS_FARADAY")
host_faraday = os.getenv("HOST_FARADAY")
workspaces_faraday = os.getenv("WORKSPACE_FARADAY")

# Autenticación de Google
def authenticate_gmail():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Función para analizar correos
def analyze_email(service):
    try:
        results = service.users().messages().list(userId='me', q='subject:"Asunto Pishing Automatico Faraday"').execute()
        messages = results.get('messages', [])
        if not messages:
            print('No se encontraron correos con el asunto especificado.')
            return
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            print('Correo encontrado:', msg['snippet'])
            # Ejecutar herramientas de detección
            subprocess.run("thepish -i /ruta/a/correo", shell=True)  # Reemplazar con ruta real
            subprocess.run("yara -r /ruta/a/ruleset.yar /ruta/a/correo/adjuntos", shell=True)
            subprocess.run("spamassassin < /ruta/a/correo", shell=True)
            # Enviar resultados a Faraday
            subprocess.run(f"faraday-cli auth -f {host_faraday} -u {username_faraday} -p {password_faraday}", shell=True)
            subprocess.run(f"faraday-cli workspace select {workspaces_faraday}", shell=True)
            subprocess.run(f"faraday-cli report create 'Detección de Amenazas' --workspace {workspaces_faraday}", shell=True)
    except HttpError as error:
        print(f'Ocurrió un error: {error}')

def main():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    while True:
        analyze_email(service)
        time.sleep(300)  # Espera 5 minutos antes de la próxima verificación

if __name__ == '__main__':
    main()
