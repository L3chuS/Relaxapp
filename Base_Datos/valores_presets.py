import os

user = os.environ.get("UsuarioMySql")
password = os.environ.get("PasswordMySql")

# Diccionario que contiene los valores por defecto para realizar la conexión a la base de datos.

acceso_root = {
            "host" : "localhost",
            "user" : user,
            "password" : password,
            "database" : ""
            }

#Lista de diccionarios que funciona como presets para cargar nuevas tablas.
#En los índices del [0:-1] representan cada columna con los valores a modificar.
#En el índice [-1] se establece la clave primaria. 

columnas_usuario_default = [
    {
        "nombre" : "id",
        "tipo" : "INT",
        "largo" : 10,
        "unico" : True,
        "auto_increment" : True,
        "not_null" : True,
    },
    {
        "nombre" : "nombre",
        "tipo" : "VARCHAR",
        "largo" : 60,
        "unico" : False,
        "auto_increment" : False,
        "not_null" : True,
    },
    {
        "nombre" : "apellido",
        "tipo" : "VARCHAR",
        "largo" : 60,
        "unico" : False,
        "auto_increment" : False,
        "not_null" : True,
    },
    {
        "nombre" : "login",
        "tipo" : "VARCHAR",
        "largo" : 20,
        "unico" : True,
        "auto_increment" : False,
        "not_null" : True,
    },
    {
        "nombre" : "password",
        "tipo" : "VARCHAR",
        "largo" : 500,
        "unico" : False,
        "auto_increment" : False,
        "not_null" : True,
    },
    {
        "primary_key" : "id"
    }]

columnas_configuraciones_default = [
    {
        "nombre" : "id",
        "tipo" : "INT",
        "largo" : 10,
        "unico" : True,
        "auto_increment" : True,
        "not_null" : True,
    },
    {
        "nombre" : "login",
        "tipo" : "VARCHAR",
        "largo" : 30,
        "unico" : True,
        "auto_increment" : False,
        "not_null" : True,
    },
    {
        "nombre" : "Configuracion_Visual",
        "tipo" : "VARCHAR",
        "largo" : 150,
        "unico" : False,
        "auto_increment" : False,
        "not_null" : False,
    },
    {
        "nombre" : "Configuracion_Estirar",
        "tipo" : "VARCHAR",
        "largo" : 150,
        "unico" : False,
        "auto_increment" : False,
        "not_null" : False,
    },
    {
        "nombre" : "Configuracion_Sonidos_Final",
        "tipo" : "VARCHAR",
        "largo" : 300,
        "unico" : False,
        "auto_increment" : False,
        "not_null" : False,
    },
    {
        "nombre" : "Configuracion_Sonidos_Lapse",
        "tipo" : "VARCHAR",
        "largo" : 300,
        "unico" : False,
        "auto_increment" : False,
        "not_null" : False,
    },
    {
        "primary_key" : "id"
    }]

# Diccionario que recupera los datos introducidos por el usuario para registar, actualizar o eliminar un usuario.
# Valores sólo editables desde la interfaz gráfica.

user = {
        "accion" : "",
        "nombre" : "",
        "apellido" : "",
        "login" : "",
        "password" : "",
        }

# Main database used.
databases = {"database1": "lechus"}

# Tables used.
tables = {"users_table": "usuarios", 
          "settings_table":"usuarios_configuraciones"}


