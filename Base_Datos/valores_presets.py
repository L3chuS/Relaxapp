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

columnas_default = [
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


# Diccionario que recupera los datos introducidos por el usuario para registar, actualizar o eliminar un usuario.
# Valores sólo editables desde la interfaz gráfica.

usuario = {
        "accion" : "",
        "nombre" : "",
        "apellido" : "",
        "login" : "",
        "password" : "",
        }

