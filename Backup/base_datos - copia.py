import mysql.connector
import os
import subprocess
import datetime

ruta_principal = os.path.dirname(__file__)
ruta_copia_seguridad = ruta_principal + "\Copia_Seguridad"

acceso_root = {"host" : "localhost",
             "user" : "root",
             "password" : "L3chuswork1212*"
            }

acceso_bd = {"host" : "localhost",
             "user" : "root",
             "password" : "L3chuswork1212*",
             "database" : ""
            }

class BaseDatos:
    def __init__(self, **kwargs):
        self.conector = mysql.connector.connect(**kwargs)
        self.cursor = self.conector.cursor()
        self.usuario = kwargs["user"]
        self.contrasena = kwargs["password"]

    def crear_bd(self, base_datos):
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {base_datos}")

    def eliminar_bd(self, base_datos):
        self.cursor.execute(f"DROP DATABASE {base_datos}")

    def seleccionar_bd(self, base_datos):
        acceso_bd["database"] = base_datos
        self.conector = mysql.connector.connect(**acceso_bd)
        self.cursor = self.conector.cursor()

    def mostrar_bd(self):
        self.cursor.execute("SHOW DATABASES")
        for bd in self.cursor:
            print(bd)    

    def consultas(self, consulta):
        self.cursor.execute(consulta)
        return self.cursor
    
    def crear_tablas(self, base_datos, tabla, columnas):

        self.cursor.execute(f"USE {base_datos}")
        comando_columnas = ""
        
        for elemento in (columnas):
            if list(dict.keys(elemento))[0] == "primary_key":
                continue
            comando_columnas += elemento["nombre"] + " "
            comando_columnas += elemento["tipo"] + " "
            comando_columnas += "(" + str(elemento["largo"]) + ")"

            if elemento["unico"] == True:
                comando_columnas += " UNIQUE"
            if elemento["auto_increment"] == True:
                comando_columnas += " AUTO_INCREMENT"
            if elemento["not_null"] == True:
                comando_columnas += " NOT NULL"
            comando_columnas += ","

        comando_columnas += "PRIMARY KEY (" + elemento["primary_key"] + "));"
        tabla_sql = f"CREATE TABLE {tabla}({comando_columnas}"
        self.cursor.execute(tabla_sql)
        self.conector.commit()
        
    def eliminar_tabla(self, base_datos, tabla):
        self.cursor.execute(f"USE {base_datos}")
        self.cursor.execute(f"DROP TABLE {tabla}")
        
    def editar_tabla(self, base_datos, tabla, usuario):

        self.usuario = usuario
        self.cursor.execute(f"USE {base_datos}")
        nombre = self.usuario["nombre"]
        apellido = self.usuario["apellido"]
        login = self.usuario["login"]
        password = self.usuario["password"]

        if self.usuario['accion'] == "registrar":
            comando_insertar = f"INSERT INTO {tabla} (nombre, apellido, login, password) \
        values ('{nombre}', '{apellido}', '{login}', '{password}');"
            
        elif self.usuario['accion'] == "modificar":
            comando_insertar = f"UPDATE {tabla} SET nombre = '{nombre}', apellido = '{apellido}', \
        login = '{login}', password = '{password}'"
      
        self.cursor.execute(comando_insertar)
        self.conector.commit()

    def eliminar_datos_tabla(self, base_datos, tabla, cantidad, usuario=None):
        self.cursor.execute(f"USE {base_datos}")
        if cantidad == "ALL":
            comando_eliminar = f"DELETE FROM {tabla} list;"
        elif cantidad == "UNIQUE":
            comando_eliminar = f"DELETE FROM {tabla} WHERE login = '{usuario}';"
        self.cursor.execute(comando_eliminar)
        self.conector.commit()

    def copia_seguridad(self, base_datos):
        fecha_hora = datetime.datetime.now().strftime("%d-%m-%Y - %H.%M.%Shs")
        with open(f"{ruta_copia_seguridad}/{base_datos} - {fecha_hora}.sql", "w") as salida:
            subprocess.Popen(f'"C:/Program Files/MySQL/MySQL Workbench 8.0/"mysqldump --user={self.usuario} \
                             --password={self.contrasena} \
                             --databases {base_datos}', shell=True, stdout=salida)

    def importar_base_datos(self, ruta, archivo):
        subprocess.Popen(f'"C:/Program Files/MySQL/MySQL Workbench 8.0/"mysql --user={self.usuario} \
                             --password={self.contrasena} < "{ruta}/{archivo}"', shell=True)
        

