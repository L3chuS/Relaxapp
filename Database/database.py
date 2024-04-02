import mysql.connector
import os
import subprocess
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from Database.presets_values import acceso_root

# Variable to get the location of the project.
main_path = os.path.dirname(__file__)
backup_path = main_path + "\Backup"

# Main class of the database.
class Database:
    """Class that contains all the methods to connect, create, select, run queries,
       register and modify users, backup and import copies, etc. Interact with the
       app to perform access management, user registrations or modifications.
    """
    def __init__(self, **kwargs):
        # Conection with MySql server is done. It takes a dict (by default is
        # "root_access") to get the key values.

        self_connection_state = False
        try:
            self.connector = mysql.connector.connect(**kwargs)
            self.cursor = self.connector.cursor()
            self.host = kwargs["host"]
            self.user = kwargs["user"]
            self.password = kwargs["password"]
            self_connection_state = True
            # print("Conection with the server successful")

        # Exception executed if the conection values are invalid.
        except:
            print("Check connection details")

    # Decorator function that checks the status of the connection with the server before each method called.
    # It connects if it's offline and always disconnects it at the end.
    def connection(decorated_function):
        def intern(self, *args, **kwargs):
            try:
                # It pass if it's connected.
                if self_connection_state:
                    pass
                # It connects if it's not.
                else:
                    self.connector = mysql.connector.connect(
                        host = self.host,
                        user = self.user,
                        password = self.password
                        )
                    self.cursor = self.connector.cursor()
                    # print("Conection with the server is reopen.")
                    self_connection_state = True
                decorated_function(self, *args, **kwargs)

            # Exception executed if the conection values are invalid.
            except:
                print("Error! Check the arguments given.")
            finally:
                # Connection is always close after each connection.
                if self_connection_state:
                    self.connector.close()
                    self.cursor.close()
                    self_connection_state = False
                    # print("Connection with the server is closed.")

        return intern

    # Decorator function that shows the list of databases.
    def list_db(decorated_function):
        def intern(self, database):
            decorated_function(self, database)
            Database.show_list_db(self)
        return intern

    # Decorator function that checks if the database exists.
    def check_db(decorated_function):
        def intern(self, database, *args):

            # Query is run to show the list of databases.
            self.cursor.execute("SHOW DATABASES")
            # Values are got.
            get_db = self.cursor.fetchall()
            self_db_exist = False

            # Iteration over each got value to check if the one passed as an argument exists or not.
            for element in get_db:
                if database in element:
                    self_db_exist = True
                    break
            # End the process if the database does not exist.
            if not self_db_exist:
                print(f"Database '{database}' does not exist. Check the information given.")
                
                return
            decorated_function(self, database, *args)
        return intern

    # Decorator function that checks if the table exist. It returns True of False if it does or not.
    def check_table(decorated_function):
        def intern(self, database, table, *args):

            # Query is run to show the list of the tables in the database given.
            self.cursor.execute(f"SHOW TABLES FROM {database}")
            # Values are got.
            get_table = self.cursor.fetchall()
            self.table_exist = False
            # Iteration over each got value to check if the table passed as an argument exists or not.
            for element in get_table:
                if table in element:
                    self.table_exist = True
            decorated_function(self, database, table, *args)
        return intern

    # Decorator function that checks if the values of the indicated columns are correct.
    def check_columns(decorated_function):
        def intern(self, database, table, columns):

            try:
                # Variable that contains an empty string which will be used to create columns into a table.
                self.command_columns = ""
                # Iteration over each value of the keys given from the argument "columns" to create the
                # command to be executed.
                for element in (columns):
                    # "primary_key" value is omited because it will be added at the end.
                    if list(dict.keys(element))[0] == "primary_key":
                        continue
                    self.command_columns += element["name"] + " "
                    self.command_columns += element["type"] + " "
                    self.command_columns += "(" + str(element["lenght"]) + ")"

                    if element["unique"] == True:
                        self.command_columns += " UNIQUE"
                    if element["auto_increment"] == True:
                        self.command_columns += " AUTO_INCREMENT"
                    if element["not_null"] == True:
                        self.command_columns += " NOT NULL"
                    self.command_columns += ","

                self.command_columns += "PRIMARY KEY (" + element["primary_key"] + "));"

            # Exception executed if the keys of the columns are invalid.
            except:
                print("Error! Check the values of the columns given.")
                return

            decorated_function(self, database, table, columns)
        return intern

    # Decorator function that checks if the values given to sign up o update users are valid.
    def check_user(decorated_function):
        def intern(self, database, table, user):

            self.validate_editing = True

            keys1 = ["name", "lastname"]
            keys2 = ["login", "password"]
            valid_values = ["-", " "]

            user["name"] = user["name"].upper()
            user["lastname"] = user["lastname"].upper()

            if user['action'] == "sign_in":
                for key in keys1:
                    # Check if name or last name are not higher than 60 characters.
                    if len(user[key]) > 60 or len(user[key]) < 2:
                        self.validate_editing = False
                        # Variable to create a label to be used in the App.
                        self.message = f"The lenght of the {key} must have at least 2 characters and can't be \nhigher than 60."
                        break

                    elif user[key].isalpha():
                        user[key] = user[key]

                    else:
                        # Invalid characters are checked first.
                        for letter in user[key]:
                            if not letter.isalpha():
                                if letter not in valid_values:
                                    self.validate_editing = False
                                    # Variable to create a label to be used in the App.
                                    self.message = f"The {key} contains invalid characters. Check it again."
                                    break

                    if self.validate_editing:
                        # White spaces are removed.
                        user[key] = user[key].split()
                        user_concatenated = ""
                        # Bucle that concatenate the values of the user given into an empty string but with
                        # the correct white spaces.
                        for value in range(len(user[key])):
                            user_concatenated += user[key][value] + " "
                        user[key] = user_concatenated[:-1]

            # Iteration over each letter of the user or password to check if there're white spaces.
            if self.validate_editing:
                for key in keys2:
                    for letter in user[key]:
                        if letter.isspace():
                            self.validate_editing = False
                            # Variable to create a label to be used in the App.
                            self.message = "The user or password contains white spaces.\nCheck it again."
                            break

            # The lenght of the user or password is checked. It must have at least 5 characters and can't be higher than 20.
            if self.validate_editing:
                if len(user["login"]) < 5 or len(user["password"]) < 5 or len(user["login"]) > 20 or len(user["password"]) > 20:
                    self.validate_editing = False
                    # Variable to create a label to be used in the App.
                    self.message = f"The user or password must have at least 5 characters \nand can't be higher than 20."

            decorated_function(self, database, table, user) 
        return intern

    @connection
    @list_db
    def crear_bd(self, database):
        """Método para crear bases de datos. Necesita un argumento: name de la base de datos (type string)."""
        try:
            # Intenta ejecutar una consulta para ver si la base de datos indicada ya existe.
            self.cursor.execute(f"SHOW DATABASES like '{database}'")
            # Recupera el value de la consulta realizada. Si el value no es "None" entonces existe.
            bd = self.cursor.fetchone()
            if bd:
                print(f"La base de datos '{database}' ya existe.")
                return
            # Comando que crea la base de datos indicada. 
            self.cursor.execute(f"CREATE DATABASE {database}")
            print(f'Se ha creado la base de datos "{database}".')

        # Excepción lanzada en caso de que la base de datos a crear contenga valuees incorrectos.
        except:
            print(f"La base de datos '{database}' no se ha creado correctamente. Revise \
la información introducida.")

    @connection        
    @list_db
    @check_db
    def eliminar_bd(self, database):
        """Método para eliminar bases de datos. Necesita un argumento: name de la base de datos (type string)."""
        # Comando que elimina la base de datos.
        self.cursor.execute(f"DROP DATABASE {database}")
        print(f'Se ha eliminado la base de datos "{database}".')
      
    @connection
    @check_db
    def get_db(self, database):
        """Método para seleccionar una bases de datos. Necesita un argumento: name de la base de datos (type string)."""
        # Se modifica el diccionario principal de conexión para conectarse con la base de datos indicada. 
        acceso_root["database"] = database
        self.cursor = self.connector.cursor()
        print(f'Se ha establecido conexión con la base de datos "{database}".')
    
    @connection
    def show_list_db(self):
        """Método para mostrar la lista de bases de datos."""
        # Comando que ejecuta el listado de bases de datos.
        self.cursor.execute("SHOW DATABASES")
        print(f'Estas son las bases de datos disponibles:')
        # Se itera y formatea sobre cada value obtenido.
        for bd in self.cursor:
            print(f"- {bd[0]}")

    @connection
    def consulta(self, consulta):
        """Método para realizar consultas. Necesita un argumento: Consulta a realizar (type string)."""
        try:
            # Comando que ejecuta la consulta indicada.
            self.cursor.execute(consulta)
            # Recupera todos los valuees de la consulta realizada.
            self.value = self.cursor.fetchall()
            print(f'El resultado de la consulta "{consulta}" es: \n')
            # Devuelve un message en caso de que no existan resultados para mostrar.
            if not self.value:
                print("No hay resultados para mostrar")
                return
            # Se itera y formatea sobre cada value de la consulta realizada.
            
            for consulta in self.value:
                for element in consulta:
                    print(str(element), end=" - ")
                print("")
            print("")
            return self.value
        # Excepción lanzada en caso de que la consulta tenga errores de sintaxis.
        except:
            print(f"Imposible realizar la consulta '{consulta}'. Revise \
la información introducida.")

    
    @connection
    @check_db
    @check_table
    @check_columns
    def crear_table(self, database, table, columns):
        """Método para crear tables. Necesita 3 argumentos: Una base de datos (type string), una table (type string) y unas
        columns (type diccionario) que contiene sus names y características."""
        # Se comprueba si la table existe. Finaliza la llamada en caso de ser True.
        if self.table_exist == True:
                print(f'La table "{table}" ya existe en la base de datos "{database}" \
y no puede ser duplicada. Eliga otro name.')
                return
        try:
            # Selecciona la base de datos en donde se va a crear la table.   
            self.cursor.execute(f"USE {database}")
            # Comando que crea la table indicada.
            self.cursor.execute(f"CREATE TABLE {table}({self.command_columns}")
            self.connector.commit()
            print(f'Se ha creado la table "{table}" en la base de datos "{database}".')
        
        # Excepción lanzada si los valuees de las columns con incorrectos.
        except:
            print(f"Imposible crear la table '{table}'. Revise \
los datos introducidos.")

    @connection
    @check_db
    @check_table
    def eliminar_table(self, database, table):
        """Método para eliminar tables. Necesita 2 argumentos: Una base de datos (type string) y una table (type string)."""
        # Se comprueba si la table existe. Finaliza la llamada en caso de ser False.
        if self.table_exist == False:
            print(f'La table "{table}" no existe en la base de datos "{database}" \
y no puede ser eliminada.')
            return
        # Selecciona la base de datos en donde se va a crear la table. 
        self.cursor.execute(f"USE {database}")
        # Comando que elimina la table indicada.
        self.cursor.execute(f"DROP TABLE {table}")
        print(f'Se ha eliminado la table "{table}" de la base de datos "{database}".')

    @connection
    @check_db
    @check_table
    @check_user  
    def editar_table(self, database, table, user):
        """Método para editar tables. Necesita 3 argumentos: Una base de datos (type string) y una table (type string)
        y un user (type diccionario) que contiene los datos para sign_in o modificarlo."""
        # Se comprueba si la table existe. Finaliza la llamada en caso de ser False.
        if self.table_exist == False:
            print(f'La table "{table}" no existe en la base de datos "{database}". \
Compruebe el name indicado.')
            return
        
        # Se comprueba si los datos introducidos por el user cumplen con los requisitos o no y se retorna a la App.
        if self.validate_editing == False:
            # message de error interno de la terminal.
            print("Error al procesar su solicitud!", self.message)
            return self.validate_editing, self.message
        
        try:
            
            # Se recupera la contraseña indicada por el user para luego encriptarla.
            contrasena = user['password']
            contrasena_encriptada = generate_password_hash(contrasena)

            # Selecciona la base de datos en donde se va a sign_in o modificar el user indicado. 
            self.cursor.execute(f"USE {database}")

            # Comprueba si el login existe en la base de datos.
            self.cursor.execute(f"SELECT login FROM {database}.{table} WHERE login = '{user['login']}'")
            
            # Se recupera el value recién buscado y devuelve una tupla o None. 
            user_existe = self.cursor.fetchone()
                
            # Acción para dar de alta un user.
            if user['action'] == "sign_in":
                # Se comprueba si el login indicado existe. Finaliza la llamada si es True.
                if user_existe:
                    self.validate_editing = False
                    self.message = f'El login que intenta sign_in "{user["login"]}" ya existe y no \npuede ser duplicado. \
Elija otro name.'
                    # Se retornan los valuees hacia la App para determinar si la alta es exitosa o no.
                    return self.validate_editing, self.message
                # user no existe. Se formatea el comando para sign_in el user.
                else:
                    comando_insertar = f"INSERT INTO {table} (name, lastname, login, password) \
            values ('{user['name']}', '{user['lastname']}', '{user['login']}', '{contrasena_encriptada}');"

            # Acción de modificar datos del user    
            elif user['action'] == "modificar":
                if not user_existe:
                    self.validate_editing = False
                    self.message = f'El login que intenta modificar "{user["login"]}" no existe. \nCompruebe los valuees indicados.'
                    # Se retornan los valuees hacia la App para determinar si la modificación es exitosa o no.
                    return self.validate_editing, self.message
                else:
                    # Se formatea el comando para modificar el user.
                    comando_insertar = f"UPDATE {table} SET password = '{contrasena_encriptada}' WHERE login = '{user['login']}'"          

        # Excepción lanzada si el diccionario contiene errores en sus keys.     
        except:
            print("Error! Revise los datos introducidos en el user indicado.")
            return

        try:
            # Comando que ejecuta la acción de sign_in o modificar el user.
            self.cursor.execute(comando_insertar)
            self.connector.commit()
            if user['action'] == "sign_in":
                self.validate_editing = True
                self.message = f'El user "{user["login"]}" ha sido registrado correctamente.'
                # Se añade el mismo user en la table "users_configuraciones" con campos vacíos.
                insertar_users_configuraciones = f"INSERT INTO users_configuraciones (login) values ('{user['login']}');"
                self.cursor.execute(insertar_users_configuraciones)
                self.connector.commit()

                print(self.message)
                return self.validate_editing, self.message
            elif user['action'] == "modificar":
                self.validate_editing = True
                self.message = 'El user ha sido actualizado correctamente.'
                print(self.message)
                return self.validate_editing, self.message       
                
        # Excepción lanzada si el diccionario contiene errores en sus values.
        except:
            self.validate_editing = False
            self.message = "Los campos indicados para este user no son válidos."
            print(self.message)
            return self.validate_editing, self.message
        
    @connection
    @check_db
    @check_table
    def configuraciones_user(self, database, table, user, action, campo, configuracion):
        """Método para añadir en la base de datos las configuraciones que el user realiza desde la aplicación.
        Necesita 5 argumentos: Una base de datos (type string), una table (type string), un user (type string),
        un campo a modificar (type string) y los valuees de la configuración (type string)."""
        # Se comprueba si la table existe. Finaliza la llamada en caso de ser False.
        if self.table_exist == False:
            print(f'La table "{table}" no existe en la base de datos "{database}". \
Compruebe el name indicado.')
            return
            
        try:
            if action == "Actualizar":
                # Selecciona la base de datos en donde se van a guardar los valuees del user indicado. 
                self.cursor.execute(f"USE {database}")
                comando_insertar = f"UPDATE {table} SET {campo[1]} = '{configuracion[1]}' WHERE login = '{user}' and {campo[0]} = '{configuracion[0]}';"
                print("el comando insertado es: ", comando_insertar)
                self.cursor.execute(comando_insertar)
                self.connector.commit()
            elif action == "ActualizarNULL":
                # Selecciona la base de datos en donde se van a guardar los valuees del user indicado. 
                self.cursor.execute(f"USE {database}")
                comando_insertar = f"UPDATE {table} SET {campo[1]} = '{configuracion}' WHERE login = '{user}' and {campo[0]} IS NULL;"
                print("el comando insertado es: ", comando_insertar)
                self.cursor.execute(comando_insertar)
                self.connector.commit()
            elif action == "Agregar":
                self.cursor.execute(f"USE {database}")
                comando_insertar = f"INSERT INTO {table} ({campo}) values ('{user}', '{configuracion[0]}', '{configuracion[1]}', \
                '{configuracion[2]}', '{configuracion[3]}', '{configuracion[4]}', '{configuracion[5]}', '{configuracion[6]}');"
                print("comando final :", comando_insertar)
                self.cursor.execute(comando_insertar)
                self.connector.commit()
            elif action == "Borrar":
                self.cursor.execute(f"USE {database}")
                comando_insertar = f"DELETE FROM {table} WHERE {campo[0]} = '{user}' and {campo[1]} = '{configuracion}';"
                print("comando final :", comando_insertar)
                self.cursor.execute(comando_insertar)
                self.connector.commit()
        
        except:
            print("Error! Revise los datos introducidos en el user indicado.")
            return
    
    @connection
    @check_db
    @check_table
    def eliminar_datos_table(self, database, table, cantidad, user=None):
        """Método para eliminar tables. Necesita 3 argumentos obligatorios y uno opcional: Una base de datos (type string), 
        una table (type string) y una cantidad (type string). El argumento "user" (type diccionario) es opcional en caso
        de que se desee eliminar sólo un user en particualr."""
        
        # Se comprueba si la table existe.
        if self.table_exist == False:
            print(f'La table "{table}" no existe en la base de datos "{database}". \
Compruebe el name indicado.')
            return
        try:
            # Selecciona la base de datos en donde se va a eliminar el o los users indicados.
            self.cursor.execute(f"USE {database}")
            if cantidad == "ALL":
                comando_eliminar = f"DELETE FROM {table} list;"
            elif cantidad == "UNIQUE":
                if user == None:
                    print("No se ha indicado ningún user. Complete todos los campos correctamente.")
                    return
                else:
                    comando_eliminar = f"DELETE FROM {table} WHERE login = '{user}';"

                # Comprueba si el login existe.
                self.cursor.execute(f"SELECT login FROM {database}.{table} WHERE login = '{user}'")
                # Recupera el value de la búsqueda realizada. Si el value es "None" entonces el user no existe y finaliza la llamada.
                value = self.cursor.fetchone()
                if not value:
                    print(f'El login indicado "{user}" no existe y no puede ser eliminado.')
                    return

            # Comando que ejecuta la eliminación del user o los users indicados.
            self.cursor.execute(comando_eliminar)
            self.connector.commit()
            if cantidad == "ALL":
                print(f'Todos los users de la table "{table}" dentro de la base de datos "{database}" \
han sido eliminados correctamente.')
            elif cantidad == "UNIQUE":
                print(f'El user "{user}" ha sido eliminado correctamente de la table "{table}" dentro \
de la base de datos "{database}".')
                
        # Excepción lanzada si el argumento "cantidad" es inválido.
        except:
            print("Error! Revise los argumentos indicados.")

    @connection
    @check_db
    @check_table  
    def verificar_login(self, database, table, user):
        """Método para verificar el login dentro de la app. Necesita 3 argumentos: Una base de datos (type string), una table (type string)
        y un user (type diccionario) que contiene los datos a comprobar (user y contraseña)."""
        # Se comprueba si la table existe.
        if self.table_exist == False:
            print(f'La table "{table}" no existe en la base de datos "{database}". \
Compruebe el name indicado.')
            return
        try:
            # Selecciona la base de datos en donde se va a verificar el user indicado.
            self.cursor.execute(f"USE {database}")
            # Variable que determina si un user y contraseña son válidos para iniciar sesión. Necesita ser "True" para iniciar sesión.
            self.validacion_login = False

            # Comprueba si el login existe.
            self.cursor.execute(f"SELECT login FROM {database}.{table} WHERE login = '{user['login']}'")
            # Recupera el value de la búsqueda realizada. Si el value es "None" entonces el user no existe y finaliza la llamada.
            user_seleccionado = self.cursor.fetchone()
            if not user_seleccionado:
                print(f'El user "{user["login"]}" no existe. Compruebe nuevamente.')
                return self.validacion_login

            # Realiza la búsqueda de la contraseña que el user tiene almacenada en la base de datos.
            self.cursor.execute(f"SELECT password FROM {database}.{table} WHERE login = '{user['login']}'")
            # Recupera el value de la búsqueda realizada.
            pw_seleccionada = self.cursor.fetchone()
            # Desencripta la contraseña almacenada en la base de datos y la compara con el value introducido por el user. 
            # Si es "True" la validación es correcta.
            comparacion = check_password_hash(pw_seleccionada[0], user["password"])

            if not comparacion:
                print(f'La contraseña es incorrecta. Compruebe nuevamente.')
            else:
                print("La validacion es correcta.")
                self.validacion_login = True
            return self.validacion_login
        
        # Excepción lanzada si los argumentos del diccionario "user" son incorrectos.
        except:
            print("Error! Revise los argumentos indicados.")


    @connection
    @check_db
    def copia_seguridad(self, database):
        """Método para realizar copias de seguridad de una base de datos. Necesita un argumento: name de la base de datos (type string)."""
        # Se almacena la fecha y hora en que se realiza la copia de seguridad.
        fecha_hora = datetime.datetime.now().strftime("%d-%m-%Y - %H.%M.%Shs")
        # Variable de control que determina si la copia se realizón con éxito o no.
        copia = False
        # Se crea el fichero que almacena los datos de la copia de seguridad.
        with open(f"{backup_path}/{database} - {fecha_hora}.sql", "w") as salida:
            # Comando para realizar la copia de seguridad.
            comando = subprocess.Popen(f'"C:/Program Files/MySQL/MySQL Workbench 8.0/"mysqldump --user={self.user} \
                            --password={self.password} \
                            --databases {database}', shell=True, stdout=salida)
            # Se recupera el value tras la ejecución del comando
            comando.communicate()

            # Se utiliza "returncode" para determinar si el comando ejecutado fue exitoso o no. 
            # El value 0 indica que la ejecución fue exitosa y 1 que hubo un fallo.
            if comando.returncode == 0:
                print(f'La copia de seguridad de la base de datos "{database}" ha sido realizada correctamente. \
name del archivo: "{database} - {fecha_hora}.sql"')
                copia = True
            else:
                print("Error! La copia de seguridad ha fallado. Revise el comando enviado.")
        
        # Elimina el archivo creado automáticamente al llamar al método "with open" en caso de que la copia no sea exitosa.
        if copia == False:
            ruta = f"{backup_path}/{database} - {fecha_hora}.sql"
            os.remove(ruta)

    @connection
    def importar_database(self, ruta, archivo):
        """Método para realizar la importación de una base de datos. Necesita 2 argumentos: La ruta (type string) donde está
        ubicado el archivo y el name del archivo (type string) con la extensión."""
        # Comando para realizar la importación de la base de datos.
        comando = subprocess.Popen(f'"C:/Program Files/MySQL/MySQL Workbench 8.0/"mysql --user={self.user} \
                            --password={self.password} < "{ruta}/{archivo}"', shell=True)
        # Se recupera el value tras la ejecución del comando
        comando.communicate()

        # Se utiliza "returncode" para determinar si el comando ejecutado fue exitoso o no. 
        # El value 0 indica que la ejecución fue exitosa y 1 que hubo un fallo.
        if comando.returncode == 0:
            print(f'La importación del archivo "{archivo}" se ha realizado correctamente.')
        else:
            print("\nError! La importación de la copia de seguridad ha fallado. Revise los arugumentos intoducidos.")
