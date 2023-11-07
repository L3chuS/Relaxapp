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
        "largo" : 32,
        "unico" : False,
        "auto_increment" : False,
        "not_null" : True,
    },
    {
        "nombre" : "apellido",
        "tipo" : "VARCHAR",
        "largo" : 64,
        "unico" : False,
        "auto_increment" : False,
        "not_null" : True,
    },
    {
        "nombre" : "login",
        "tipo" : "VARCHAR",
        "largo" : 32,
        "unico" : True,
        "auto_increment" : False,
        "not_null" : True,
    },
    {
        "nombre" : "password",
        "tipo" : "VARCHAR",
        "largo" : 32,
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
        "accion" : "modificar",
        "nombre" : "Esteban3",
        "apellido" : "Santos3",
        "login" : "lechu",
        "password" : "lechu321",
        }

