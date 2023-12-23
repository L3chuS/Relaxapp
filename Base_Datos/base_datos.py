import mysql.connector
import os
import subprocess
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from Base_Datos.valores_presets import acceso_root

# Variables que capturan la ruta donde está ubicado el proyecto.
ruta_principal = os.path.dirname(__file__)
ruta_copia_seguridad = ruta_principal + "\Copia_Seguridad"

# Clase principal de la base de datos. 
class BaseDatos:
    """Clase que contiene todos los métodos para conectarse, crear, selecccionar,
       realizar consultas, registrar y modificar usuarios, copias de seguridad e 
       importación, etc. Interactúa con la app para realizar la gestión de acceso, 
       registros o modificaciones del usuario.
    """
    def __init__(self, **kwargs):
        # Se realiza la conexión con el servidor MySql. Toma un diccionario (por
        # defecto "acceso_root") para obtener los valores de conexión.
        self.estado_conexion = False
        try:
            self.conector = mysql.connector.connect(**kwargs)
            self.cursor = self.conector.cursor()
            self.host = kwargs["host"]
            self.usuario = kwargs["user"]
            self.contrasena = kwargs["password"]
            self.estado_conexion = True
            # print("Se establece conexión con el servidor.")

        # Excepción lanzada en caso de que los valores de conexión sean incorrectos.    
        except:
            print("Revise los datos de la conexión")

    # Función decoradora que comprueba el estado de la conexión con el servidor antes de la llamada de cada método. 
    # Se conecta en caso de que esté desconectado y se desconecta siempre al final. 
    def conexion(funcion_decorada):
        def interna(self, *args, **kwargs):
            try:
                # Se está conectado pasa.
                if self.estado_conexion:
                    pass
                # Se realiza la conexión en caso de que no esté conectado.
                else:
                    self.conector = mysql.connector.connect(
                        host = self.host, 
                        user = self.usuario, 
                        password = self.contrasena
                        )
                    self.cursor = self.conector.cursor()
                    # print("Se reabre conexión con el servidor.")
                    self.estado_conexion = True
                funcion_decorada(self, *args, **kwargs)

            # Excepción lanzada en caso de que los valores de conexión sean incorrectos.
            except:
                print("Error! Revise los argumentos introducidos.")
            finally:
                # Cierra siempre la conexión luego de cada conexión.
                if self.estado_conexion:
                    self.conector.close()
                    self.cursor.close()
                    self.estado_conexion = False
                    # print("Se cierra la conexión con el servidor.")
        return interna

    # Función decoradora que muestra el listado de bases de datos.
    def listar_bd(funcion_decorada):
        def interna(self, base_datos):
            funcion_decorada(self, base_datos)
            BaseDatos.mostrar_lista_bd(self)
        return interna

    # Función decoradora que comprueba si la base de datos existe.
    def comprobar_bd(funcion_decorada):
        def interna(self, base_datos, *args):
            
            # Se ejecuta la instrucción para mostrar la lista de bases de datos. 
            self.cursor.execute("SHOW DATABASES")
            # Se capturan los valores ejecutados. 
            seleccionar_bd = self.cursor.fetchall()
            self.bd_existe = False

            # Se itera sobre cada valor recuperado para comprobar si la que se pasa como argumento 
            # existe o no.
            for elemento in seleccionar_bd:
                if base_datos in elemento:
                    self.bd_existe = True
                    break
            # Finaliza el proceso en caso de que la base de datos no exista. 
            if not self.bd_existe:
                print(f"La base de datos '{base_datos}' no existe. Revise \
la información introducida.")
                return
            funcion_decorada(self, base_datos, *args)
        return interna
    
    # Función decoradora que comprueba si la tabla existe. Sólo establece como True o False si la
    # tabla existe o no. 
    def comprobar_tabla(funcion_decorada):
        def interna(self, base_datos, tabla, *args):

            # Se ejecuta la instrucción para mostrar la lista de tablas dentro de la bases de datos. 
            self.cursor.execute(f"SHOW TABLES FROM {base_datos}")
            # Se capturan los valores ejecutados.
            seleccionar_tabla = self.cursor.fetchall()
            self.tabla_existe = False
            # Se itera sobre cada valor recuperado para comprobar si la tabla que se pasa como argumento 
            # existe o no.
            for elemento in seleccionar_tabla:
                if tabla in elemento:
                    self.tabla_existe = True
            funcion_decorada(self, base_datos, tabla, *args)
        return interna
    
    # Función decoradora que comprueba si los valores de las columnas indicadas son correctos.
    def comprobar_columnas(funcion_decorada):
        def interna(self, base_datos, tabla, columnas):

            try:
                # Se va creando la string que se ejecutará para crear columnas dentro de una tabla. 
                self.comando_columnas = ""
                # Se itera sobre cada valor de las distintas key de las columnas pasada para ir concatenando
                # el comando a ejecutar.
                for elemento in (columnas):
                    # Se omite el valor de la key "primary_key" ya que se debe concatenar al final.
                    if list(dict.keys(elemento))[0] == "primary_key":
                        continue
                    self.comando_columnas += elemento["nombre"] + " "
                    self.comando_columnas += elemento["tipo"] + " "
                    self.comando_columnas += "(" + str(elemento["largo"]) + ")"

                    if elemento["unico"] == True:
                        self.comando_columnas += " UNIQUE"
                    if elemento["auto_increment"] == True:
                        self.comando_columnas += " AUTO_INCREMENT"
                    if elemento["not_null"] == True:
                        self.comando_columnas += " NOT NULL"
                    self.comando_columnas += ","

                self.comando_columnas += "PRIMARY KEY (" + elemento["primary_key"] + "));"
            
            # Excepción lanzada si las keys de las columnas contienen valores erróneos.
            except:
                print("Error! Revise los datos introducidos en las columnas indicadas.")
                return

            funcion_decorada(self, base_datos, tabla, columnas)
        return interna
    
    # Función decoradora que comprueba si los valores de registro o actualización de usuarios son correctos.
    def comprobar_usuario(funcion_decorada):
        def interna(self, base_datos, tabla, usuario):

            self.validacion_editar = True

            keys1 = ["nombre", "apellido"]
            keys2 = ["login", "password"]
            valores_validos = ["-", " "]

            usuario["nombre"] = usuario["nombre"].upper()
            usuario["apellido"] = usuario["apellido"].upper()

            if usuario['accion'] == "registrar":
                for key in keys1:
                    # Controla que el nombre o el apellido no superen los 60 caracteres.
                    if len(usuario[key]) > 60 or len(usuario[key]) < 2:
                        self.validacion_editar = False
                        # Variable para generar la etiqueta en la App.
                        self.mensaje = f"La logitud del {key} debe tener al menos 2 caracteres y no debe \nsuperar los 60."
                        break
                                
                    elif usuario[key].isalpha():
                        usuario[key] = usuario[key]

                    else:
                        # Primero se comprueba que no haya caracteres inválidos.
                        for letra in usuario[key]:
                            if not letra.isalpha():
                                if letra not in valores_validos:
                                    self.validacion_editar = False
                                    # Variable para generar la etiqueta en la App.
                                    self.mensaje = f"El {key} contiene caracteres inválidos. Compruebe nuevamente."
                                    break

                    if self.validacion_editar:    
                        # Quita espacios en blanco.
                        usuario[key] = usuario[key].split()
                        # Variable en donde se concatena la lista creada pero con los espacios en blancos correctos.
                        usuario_concatenado = ""
                        # Concatena las lista creadas con la cantidad de espacios en blancos correctos.
                        for valor in range(len(usuario[key])):
                            usuario_concatenado += usuario[key][valor] + " "
                        usuario[key] = usuario_concatenado[:-1]

            # Se itera sobre cada letra del usuario o la contraseña para comprobar si hay espacios en blanco.
            if self.validacion_editar:
                for key in keys2:
                    for letra in usuario[key]:
                        if letra.isspace():
                            self.validacion_editar = False
                            # Variable para generar la etiqueta en la App.
                            self.mensaje = "El usuario o contraseña contienen espacios en blanco.\nCompruebe nuevamente."
                            break

            # Se comprueba la longitud del usuario o contraseña. Debe tener mas de 8 caracteres y menos de 20.
            if self.validacion_editar:
                if len(usuario["login"]) < 5 or len(usuario["password"]) < 5 or len(usuario["login"]) > 20 or len(usuario["password"]) > 20:
                    self.validacion_editar = False
                    # Variable para generar la etiqueta en la App
                    self.mensaje = f"El usuario o contraseña deben tener al menos 5 caracteres \ny menos de 20."
                
            funcion_decorada(self, base_datos, tabla, usuario)  
        return interna

    @conexion
    @listar_bd
    def crear_bd(self, base_datos):
        """Método para crear bases de datos. Necesita un argumento: Nombre de la base de datos (tipo string)."""
        try:
            # Intenta ejecutar una consulta para ver si la base de datos indicada ya existe.
            self.cursor.execute(f"SHOW DATABASES like '{base_datos}'")
            # Recupera el valor de la consulta realizada. Si el valor no es "None" entonces existe.
            bd = self.cursor.fetchone()
            if bd:
                print(f"La base de datos '{base_datos}' ya existe.")
                return
            # Comando que crea la base de datos indicada. 
            self.cursor.execute(f"CREATE DATABASE {base_datos}")
            print(f'Se ha creado la base de datos "{base_datos}".')

        # Excepción lanzada en caso de que la base de datos a crear contenga valores incorrectos.
        except:
            print(f"La base de datos '{base_datos}' no se ha creado correctamente. Revise \
la información introducida.")

    @conexion        
    @listar_bd
    @comprobar_bd
    def eliminar_bd(self, base_datos):
        """Método para eliminar bases de datos. Necesita un argumento: Nombre de la base de datos (tipo string)."""
        # Comando que elimina la base de datos.
        self.cursor.execute(f"DROP DATABASE {base_datos}")
        print(f'Se ha eliminado la base de datos "{base_datos}".')
      
    @conexion
    @comprobar_bd
    def seleccionar_bd(self, base_datos):
        """Método para seleccionar una bases de datos. Necesita un argumento: Nombre de la base de datos (tipo string)."""
        # Se modifica el diccionario principal de conexión para conectarse con la base de datos indicada. 
        acceso_root["database"] = base_datos
        self.cursor = self.conector.cursor()
        print(f'Se ha establecido conexión con la base de datos "{base_datos}".')
    
    @conexion
    def mostrar_lista_bd(self):
        """Método para mostrar la lista de bases de datos."""
        # Comando que ejecuta el listado de bases de datos.
        self.cursor.execute("SHOW DATABASES")
        print(f'Estas son las bases de datos disponibles:')
        # Se itera y formatea sobre cada valor obtenido.
        for bd in self.cursor:
            print(f"- {bd[0]}")

    @conexion
    def consulta(self, consulta):
        """Método para realizar consultas. Necesita un argumento: Consulta a realizar (tipo string)."""
        try:
            # Comando que ejecuta la consulta indicada.
            self.cursor.execute(consulta)
            # Recupera todos los valores de la consulta realizada.
            self.valor = self.cursor.fetchall()
            print(f'El resultado de la consulta "{consulta}" es: \n')
            # Devuelve un mensaje en caso de que no existan resultados para mostrar.
            if not self.valor:
                print("No hay resultados para mostrar")
                return
            # Se itera y formatea sobre cada valor de la consulta realizada.
            for consulta in self.valor:
                for elemento in consulta:
                    print(str(elemento), end=" - ")
                print("")
            print("")
            return self.valor
        # Excepción lanzada en caso de que la consulta tenga errores de sintaxis.
        except:
            print(f"Imposible realizar la consulta '{consulta}'. Revise \
la información introducida.")

    
    @conexion
    @comprobar_bd
    @comprobar_tabla
    @comprobar_columnas
    def crear_tabla(self, base_datos, tabla, columnas):
        """Método para crear tablas. Necesita 3 argumentos: Una base de datos (tipo string), una tabla (tipo string) y unas
        columnas (tipo diccionario) que contiene sus nombres y características."""
        # Se comprueba si la table existe. Finaliza la llamada en caso de ser True.
        if self.tabla_existe == True:
                print(f'La tabla "{tabla}" ya existe en la base de datos "{base_datos}" \
y no puede ser duplicada. Eliga otro nombre.')
                return
        try:
            # Selecciona la base de datos en donde se va a crear la tabla.   
            self.cursor.execute(f"USE {base_datos}")
            # Comando que crea la tabla indicada.
            self.cursor.execute(f"CREATE TABLE {tabla}({self.comando_columnas}")
            self.conector.commit()
            print(f'Se ha creado la tabla "{tabla}" en la base de datos "{base_datos}".')
        
        # Excepción lanzada si los valores de las columnas con incorrectos.
        except:
            print(f"Imposible crear la tabla '{tabla}'. Revise \
los datos introducidos.")

    @conexion
    @comprobar_bd
    @comprobar_tabla
    def eliminar_tabla(self, base_datos, tabla):
        """Método para eliminar tablas. Necesita 2 argumentos: Una base de datos (tipo string) y una tabla (tipo string)."""
        # Se comprueba si la table existe. Finaliza la llamada en caso de ser False.
        if self.tabla_existe == False:
            print(f'La tabla "{tabla}" no existe en la base de datos "{base_datos}" \
y no puede ser eliminada.')
            return
        # Selecciona la base de datos en donde se va a crear la tabla. 
        self.cursor.execute(f"USE {base_datos}")
        # Comando que elimina la tabla indicada.
        self.cursor.execute(f"DROP TABLE {tabla}")
        print(f'Se ha eliminado la tabla "{tabla}" de la base de datos "{base_datos}".')

    @conexion
    @comprobar_bd
    @comprobar_tabla
    @comprobar_usuario  
    def editar_tabla(self, base_datos, tabla, usuario):
        """Método para editar tablas. Necesita 3 argumentos: Una base de datos (tipo string) y una tabla (tipo string)
        y un usuario (tipo diccionario) que contiene los datos para registrar o modificarlo."""
        # Se comprueba si la table existe. Finaliza la llamada en caso de ser False.
        if self.tabla_existe == False:
            print(f'La tabla "{tabla}" no existe en la base de datos "{base_datos}". \
Compruebe el nombre indicado.')
            return
        
        # Se comprueba si los datos introducidos por el usuario cumplen con los requisitos o no y se retorna a la App.
        if self.validacion_editar == False:
            # Mensaje de error interno de la terminal.
            print("Error al procesar su solicitud!", self.mensaje)
            return self.validacion_editar, self.mensaje
        
        try:
            
            # Se recupera la contraseña indicada por el usuario para luego encriptarla.
            contrasena = usuario['password']
            contrasena_encriptada = generate_password_hash(contrasena)

            # Selecciona la base de datos en donde se va a registrar o modificar el usuario indicado. 
            self.cursor.execute(f"USE {base_datos}")

            # Comprueba si el login existe en la base de datos.
            self.cursor.execute(f"SELECT login FROM {base_datos}.{tabla} WHERE login = '{usuario['login']}'")
            
            # Se recupera el valor recién buscado y devuelve una tupla o None. 
            usuario_existe = self.cursor.fetchone()
                
            # Acción para dar de alta un usuario.
            if usuario['accion'] == "registrar":
                # Se comprueba si el login indicado existe. Finaliza la llamada si es True.
                if usuario_existe:
                    self.validacion_editar = False
                    self.mensaje = f'El login que intenta registrar "{usuario["login"]}" ya existe y no \npuede ser duplicado. \
Elija otro nombre.'
                    # Se retornan los valores hacia la App para determinar si la alta es exitosa o no.
                    return self.validacion_editar, self.mensaje
                # Usuario no existe. Se formatea el comando para registrar el usuario.
                else:
                    comando_insertar = f"INSERT INTO {tabla} (nombre, apellido, login, password) \
            values ('{usuario['nombre']}', '{usuario['apellido']}', '{usuario['login']}', '{contrasena_encriptada}');"

            # Acción de modificar datos del usuario    
            elif usuario['accion'] == "modificar":
                if not usuario_existe:
                    self.validacion_editar = False
                    self.mensaje = f'El login que intenta modificar "{usuario["login"]}" no existe. \nCompruebe los valores indicados.'
                    # Se retornan los valores hacia la App para determinar si la modificación es exitosa o no.
                    return self.validacion_editar, self.mensaje
                else:
                    # Se formatea el comando para modificar el usuario.
                    comando_insertar = f"UPDATE {tabla} SET password = '{contrasena_encriptada}' WHERE login = '{usuario['login']}'"          

        # Excepción lanzada si el diccionario contiene errores en sus keys.     
        except:
            print("Error! Revise los datos introducidos en el usuario indicado.")
            return

        try:
            # Comando que ejecuta la acción de registrar o modificar el usuario.
            self.cursor.execute(comando_insertar)
            self.conector.commit()
            if usuario['accion'] == "registrar":
                self.validacion_editar = True
                self.mensaje = f'El usuario "{usuario["login"]}" ha sido registrado correctamente.'
                # Se añade el mismo usuario en la tabla "usuarios_configuraciones" con campos vacíos.
                insertar_usuarios_configuraciones = f"INSERT INTO usuarios_configuraciones (login) values ('{usuario['login']}');"
                self.cursor.execute(insertar_usuarios_configuraciones)
                self.conector.commit()

                print(self.mensaje)
                return self.validacion_editar, self.mensaje
            elif usuario['accion'] == "modificar":
                self.validacion_editar = True
                self.mensaje = 'El usuario ha sido actualizado correctamente.'
                print(self.mensaje)
                return self.validacion_editar, self.mensaje       
                
        # Excepción lanzada si el diccionario contiene errores en sus values.
        except:
            self.validacion_editar = False
            self.mensaje = "Los campos indicados para este usuario no son válidos."
            print(self.mensaje)
            return self.validacion_editar, self.mensaje
        
    @conexion
    @comprobar_bd
    @comprobar_tabla
    def configuraciones_usuario(self, base_datos, tabla, usuario, accion, campo, configuracion):
        """Método para añadir en la base de datos las configuraciones que el usuario realiza desde la aplicación.
        Necesita 5 argumentos: Una base de datos (tipo string), una tabla (tipo string), un usuario (tipo string),
        un campo a modificar (tipo string) y los valores de la configuración (tipo string)."""
        # Se comprueba si la table existe. Finaliza la llamada en caso de ser False.
        if self.tabla_existe == False:
            print(f'La tabla "{tabla}" no existe en la base de datos "{base_datos}". \
Compruebe el nombre indicado.')
            return
            
        try:
            if accion == "Actualizar":
                # Selecciona la base de datos en donde se van a guardar los valores del usuario indicado. 
                self.cursor.execute(f"USE {base_datos}")
                comando_insertar = f"UPDATE {tabla} SET {campo[1]} = '{configuracion[1]}' WHERE login = '{usuario}' and {campo[0]} = '{configuracion[0]}';"
                self.cursor.execute(comando_insertar)
                self.conector.commit()
            elif accion == "Agregar":
                self.cursor.execute(f"USE {base_datos}")
                comando_insertar = f"INSERT INTO {tabla} ({campo}) values ('{usuario}', '{configuracion[0]}', '{configuracion[1]}', '{configuracion[2]}');"
                print("comando final :", comando_insertar)
                self.cursor.execute(comando_insertar)
                self.conector.commit()
            elif accion == "Borrar":
                self.cursor.execute(f"USE {base_datos}")
                comando_insertar = f"DELETE FROM {tabla} WHERE {campo[0]} = '{usuario}' and {campo[1]} = '{configuracion}';"
                print("comando final :", comando_insertar)
                self.cursor.execute(comando_insertar)
                self.conector.commit()
        
        except:
            print("Error! Revise los datos introducidos en el usuario indicado.")
            return
    
    @conexion
    @comprobar_bd
    @comprobar_tabla
    def eliminar_datos_tabla(self, base_datos, tabla, cantidad, usuario=None):
        """Método para eliminar tablas. Necesita 3 argumentos obligatorios y uno opcional: Una base de datos (tipo string), 
        una tabla (tipo string) y una cantidad (tipo string). El argumento "usuario" (tipo diccionario) es opcional en caso
        de que se desee eliminar sólo un usuario en particualr."""
        
        # Se comprueba si la table existe.
        if self.tabla_existe == False:
            print(f'La tabla "{tabla}" no existe en la base de datos "{base_datos}". \
Compruebe el nombre indicado.')
            return
        try:
            # Selecciona la base de datos en donde se va a eliminar el o los usuarios indicados.
            self.cursor.execute(f"USE {base_datos}")
            if cantidad == "ALL":
                comando_eliminar = f"DELETE FROM {tabla} list;"
            elif cantidad == "UNIQUE":
                if usuario == None:
                    print("No se ha indicado ningún usuario. Complete todos los campos correctamente.")
                    return
                else:
                    comando_eliminar = f"DELETE FROM {tabla} WHERE login = '{usuario}';"

                # Comprueba si el login existe.
                self.cursor.execute(f"SELECT login FROM {base_datos}.{tabla} WHERE login = '{usuario}'")
                # Recupera el valor de la búsqueda realizada. Si el valor es "None" entonces el usuario no existe y finaliza la llamada.
                valor = self.cursor.fetchone()
                if not valor:
                    print(f'El login indicado "{usuario}" no existe y no puede ser eliminado.')
                    return

            # Comando que ejecuta la eliminación del usuario o los usuarios indicados.
            self.cursor.execute(comando_eliminar)
            self.conector.commit()
            if cantidad == "ALL":
                print(f'Todos los usuarios de la tabla "{tabla}" dentro de la base de datos "{base_datos}" \
han sido eliminados correctamente.')
            elif cantidad == "UNIQUE":
                print(f'El usuario "{usuario}" ha sido eliminado correctamente de la tabla "{tabla}" dentro \
de la base de datos "{base_datos}".')
                
        # Excepción lanzada si el argumento "cantidad" es inválido.
        except:
            print("Error! Revise los argumentos indicados.")

    @conexion
    @comprobar_bd
    @comprobar_tabla  
    def verificar_login(self, base_datos, tabla, usuario):
        """Método para verificar el login dentro de la app. Necesita 3 argumentos: Una base de datos (tipo string), una tabla (tipo string)
        y un usuario (tipo diccionario) que contiene los datos a comprobar (Usuario y contraseña)."""
        # Se comprueba si la table existe.
        if self.tabla_existe == False:
            print(f'La tabla "{tabla}" no existe en la base de datos "{base_datos}". \
Compruebe el nombre indicado.')
            return
        try:
            # Selecciona la base de datos en donde se va a verificar el usuario indicado.
            self.cursor.execute(f"USE {base_datos}")
            # Variable que determina si un usuario y contraseña son válidos para iniciar sesión. Necesita ser "True" para iniciar sesión.
            self.validacion_login = False

            # Comprueba si el login existe.
            self.cursor.execute(f"SELECT login FROM {base_datos}.{tabla} WHERE login = '{usuario['login']}'")
            # Recupera el valor de la búsqueda realizada. Si el valor es "None" entonces el usuario no existe y finaliza la llamada.
            usuario_seleccionado = self.cursor.fetchone()
            if not usuario_seleccionado:
                print(f'El usuario "{usuario["login"]}" no existe. Compruebe nuevamente.')
                return self.validacion_login

            # Realiza la búsqueda de la contraseña que el usuario tiene almacenada en la base de datos.
            self.cursor.execute(f"SELECT password FROM {base_datos}.{tabla} WHERE login = '{usuario['login']}'")
            # Recupera el valor de la búsqueda realizada.
            pw_seleccionada = self.cursor.fetchone()
            # Desencripta la contraseña almacenada en la base de datos y la compara con el valor introducido por el usuario. 
            # Si es "True" la validación es correcta.
            comparacion = check_password_hash(pw_seleccionada[0], usuario["password"])

            if not comparacion:
                print(f'La contraseña es incorrecta. Compruebe nuevamente.')
            else:
                print("La validacion es correcta.")
                self.validacion_login = True
            return self.validacion_login
        
        # Excepción lanzada si los argumentos del diccionario "usuario" son incorrectos.
        except:
            print("Error! Revise los argumentos indicados.")


    @conexion
    @comprobar_bd
    def copia_seguridad(self, base_datos):
        """Método para realizar copias de seguridad de una base de datos. Necesita un argumento: Nombre de la base de datos (tipo string)."""
        # Se almacena la fecha y hora en que se realiza la copia de seguridad.
        fecha_hora = datetime.datetime.now().strftime("%d-%m-%Y - %H.%M.%Shs")
        # Variable de control que determina si la copia se realizón con éxito o no.
        copia = False
        # Se crea el fichero que almacena los datos de la copia de seguridad.
        with open(f"{ruta_copia_seguridad}/{base_datos} - {fecha_hora}.sql", "w") as salida:
            # Comando para realizar la copia de seguridad.
            comando = subprocess.Popen(f'"C:/Program Files/MySQL/MySQL Workbench 8.0/"mysqldump --user={self.usuario} \
                            --password={self.contrasena} \
                            --databases {base_datos}', shell=True, stdout=salida)
            # Se recupera el valor tras la ejecución del comando
            comando.communicate()

            # Se utiliza "returncode" para determinar si el comando ejecutado fue exitoso o no. 
            # El valor 0 indica que la ejecución fue exitosa y 1 que hubo un fallo.
            if comando.returncode == 0:
                print(f'La copia de seguridad de la base de datos "{base_datos}" ha sido realizada correctamente. \
Nombre del archivo: "{base_datos} - {fecha_hora}.sql"')
                copia = True
            else:
                print("Error! La copia de seguridad ha fallado. Revise el comando enviado.")
        
        # Elimina el archivo creado automáticamente al llamar al método "with open" en caso de que la copia no sea exitosa.
        if copia == False:
            ruta = f"{ruta_copia_seguridad}/{base_datos} - {fecha_hora}.sql"
            os.remove(ruta)

    @conexion
    def importar_base_datos(self, ruta, archivo):
        """Método para realizar la importación de una base de datos. Necesita 2 argumentos: La ruta (tipo string) donde está
        ubicado el archivo y el nombre del archivo (tipo string) con la extensión."""
        # Comando para realizar la importación de la base de datos.
        comando = subprocess.Popen(f'"C:/Program Files/MySQL/MySQL Workbench 8.0/"mysql --user={self.usuario} \
                            --password={self.contrasena} < "{ruta}/{archivo}"', shell=True)
        # Se recupera el valor tras la ejecución del comando
        comando.communicate()

        # Se utiliza "returncode" para determinar si el comando ejecutado fue exitoso o no. 
        # El valor 0 indica que la ejecución fue exitosa y 1 que hubo un fallo.
        if comando.returncode == 0:
            print(f'La importación del archivo "{archivo}" se ha realizado correctamente.')
        else:
            print("\nError! La importación de la copia de seguridad ha fallado. Revise los arugumentos intoducidos.")
