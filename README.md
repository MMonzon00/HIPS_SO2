# HIPS-SO2

## Descripción
Este proyecto implementa un Sistema de Prevención de Intrusiones en el Host (HIPS) para monitorear y prevenir actividades sospechosas en un sistema.

## Requisitos
- Python 3.x
- FastAPI
- Uvicorn
- Otros paquetes necesarios especificados en `requirements.txt`

## Instalación

### Clonar el repositorio
```bash
git clone https://github.com/MMonzon00/HIPS_SO2.git
cd HIPS-SO2
```

### Crear y activar un entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Configuración
Asegurarse de configurar las variables de entorno necesarias. Puedes usar un archivo .env en el directorio del repositorio.

### Variables de Entorno
Crea un archivo .env en el directorio raíz del proyecto con las siguientes variables:

```makefile
BASIC_AUTH_USERNAME=username
BASIC_AUTH_PASSWORD=password
EMAIL_USER=emailsender@mail.com
EMAIL_PASSWORD=email_sender_password
EMAIL_RECEIVER=emailreceiver@mail.com
```
### Ejecución
Se necesita tener privilegios de sudo para correr el proyecto.

### Iniciar la aplicación
```bash
sudo python main.py
```
