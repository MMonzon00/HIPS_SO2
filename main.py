import hashlib
import psycopg2
import os

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(database="tu_basededatos", user="tu_usuario", password="tu_contraseña", host="tu_host", port="tu_puerto")
cur = conn.cursor()

def calcular_hash(nombre_archivo):
    with open(nombre_archivo, "rb") as file:
        content = file.read()
        return hashlib.sha256(content).hexdigest()

# Calcular y guardar el hash original de /etc/passwd
hash_passwd = calcular_hash("/etc/passwd")
cur.execute("INSERT INTO archivo_hashes (nombre_archivo, hash_original) VALUES (%s, %s)", ("/etc/passwd", hash_passwd))

# Calcular y guardar el hash original de /etc/shadow
hash_shadow = calcular_hash("/etc/shadow")
cur.execute("INSERT INTO archivo_hashes (nombre_archivo, hash_original) VALUES (%s, %s)", ("/etc/shadow", hash_shadow))

# Guardar registro de evento en los logs
cur.execute("INSERT INTO registros_eventos (evento) VALUES (%s)", ("Hashes originales de archivos binarios guardados en la base de datos",))

# Confirmar y cerrar conexión
conn.commit()
conn.close()
