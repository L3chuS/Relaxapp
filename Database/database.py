import mysql.connector
import os
import subprocess
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from Database.presets_values import root_access

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

    # Decorator function that checks the status of the connection to the server before each method called.
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
                    # print("Connection to the server is closed.")

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
            self_db_exists = False

            # Iteration over each got value to check if the one passed as an argument exists or not.
            for element in get_db:
                if database in element:
                    self_db_exists = True
                    break
            # End the process if the database does not exist.
            if not self_db_exists:
                print(f"Database '{database}' does not exist. Check the information given.")
                
                return
            decorated_function(self, database, *args)
        return intern

    # Decorator function that checks if the table exists. It returns True of False if it does or not.
    def check_table(decorated_function):
        def intern(self, database, table, *args):

            # Query is run to show the list of the tables in the database given.
            self.cursor.execute(f"SHOW TABLES FROM {database}")
            # Values are got.
            get_table = self.cursor.fetchall()
            self.table_exists = False
            # Iteration over each got value to check if the table passed as an argument exists or not.
            for element in get_table:
                if table in element:
                    self.table_exists = True
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

            if user['action'] == "sign_up":
                for key in keys1:
                    # Check if name or last name are not higher than 60 characters.
                    if len(user[key]) > 60 or len(user[key]) < 2:
                        self.validate_editing = False
                        # Variable to create a label to be used in the App.
                        self.message = f"La logitud del {key} debe tener al menos 2 caracteres y no debe \nsuperar los 60."
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
                                    self.message = f"El {key} contiene caracteres inválidos. Compruebe nuevamente."
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
                            self.message = "El usuario o contraseña contienen espacios en blanco.\nCompruebe nuevamente."
                            break

            # The lenght of the user or password is checked. It must have at least 5 characters and can't be higher than 20.
            if self.validate_editing:
                if len(user["login"]) < 5 or len(user["password"]) < 5 or len(user["login"]) > 20 or len(user["password"]) > 20:
                    self.validate_editing = False
                    # Variable to create a label to be used in the App.
                    self.message = f"El usuario o contraseña deben tener al menos 5 caracteres \ny menos de 20."

            decorated_function(self, database, table, user)
        return intern

    @connection
    @list_db
    def create_db(self, database):
        """Method to create databases. It needs one argument: database name (string type)."""
        try:
            # It tries to execute a query to check if the indicated database exists.
            self.cursor.execute(f"SHOW DATABASES like '{database}'")
            # It gets the value of the query executed. If this value is "None" then it exists.
            bd = self.cursor.fetchone()
            if bd:
                print(f"Database '{database}' already exists.")
                return
            # This command create the indicated database.
            self.cursor.execute(f"CREATE DATABASE {database}")
            print(f'Database "{database}" has been created.')

        # Exception executed if the indicated database contains invalid values.
        except:
            print(f"Database '{database}' couldn't be created. Check the information given.")

    @connection
    @list_db
    @check_db
    def remove_db(self, database):
        """Method to remove databases. It needs one argument: database name (string type)."""
        # Command to remove databases.
        self.cursor.execute(f"DROP DATABASE {database}")
        print(f'Database "{database}" has been removed.')

    @connection
    @check_db
    def get_db(self, database):
        """Method to select a database. It needs one argument: database name (string type)."""
        # The main dictionary to set the connection is modified to set a new connection to the indicated database. 
        root_access["database"] = database
        self.cursor = self.connector.cursor()
        print(f'Connection to the database "{database}" has been established.')

    @connection
    def show_list_db(self):
        """Method to show the list of databases."""
        # Command that execute the list of databases.
        self.cursor.execute("SHOW DATABASES")
        print(f'These are the available databases:')
        # Iteration and format over each value got.
        for bd in self.cursor:
            print(f"- {bd[0]}")

    @connection
    def query(self, query):
        """Method to run queries. It needs one argument: query to run (string type)."""
        try:
            # Command that execute the indicated query.
            self.cursor.execute(query)
            # Variable that contains all the values of the query run.
            self.value = self.cursor.fetchall()
            print(f'The result of the query "{query}" is: \n')
            # It returns a message in the case there's no result to show.
            if not self.value:
                print("There's no result to show.")
                return

            # Iteration and format over each value got.
            for query in self.value:
                for element in query:
                    print(str(element), end=" - ")
                print("")
            print("")
            return self.value

        # Exepction executed if the query given contains sintax errors.
        except:
            print(f"Impossible to run the query '{query}'. Check the information given.")

    @connection
    @check_db
    @check_table
    @check_columns
    def create_table(self, database, table, columns):
        """Method to create tables. It needs 3 arguments: A database (string type), a table (string type) and a columns (dictionary type)
           that contains their names and characteristics."""
        # It checks if the indicated table exists. It finish the call if it's "True".
        if self.table_exists == True:
                print(f'The table "{table}" already exists in the database "{database}" \
and can\'t be duplicated. Choose another name.')
                return
        try:
            # Database is selected where table will be created.
            self.cursor.execute(f"USE {database}")
            # Command that creates indicated table.
            self.cursor.execute(f"CREATE TABLE {table}({self.command_columns}")
            self.connector.commit()
            print(f'Table "{table}" has been created in the database "{database}".')

        # Exception executed if values of the columns are invalid.
        except:
            print(f"Impossible to create the table '{table}'. Check the information given.")

    @connection
    @check_db
    @check_table
    def remove_table(self, database, table):
        """Method to remove tables. It needs 2 arguments: A database (string type) and a table (string type)."""
        # It checks if the indicated table exists. It finish the call if it's "False".
        if self.table_exists == False:
            print(f'The table "{table}" does not exist in the database "{database}" \
and can\'t be removed.')
            return
        # Database is selected where the table will be created.
        self.cursor.execute(f"USE {database}")
        # Command that remove the indicated table.
        self.cursor.execute(f"DROP TABLE {table}")
        print(f'The table "{table}" has been removed from the database "{database}".')

    @connection
    @check_db
    @check_table
    @check_user
    def edit_table(self, database, table, user):
        """Method to edit tables. It needs 3 arguments: A database (string type), a table (string type)
           and a user (dictionary type) that contains the data to sign up or modify it."""

        # It checks if the indicated table exists. It finish the call if it's "False".
        if self.table_exists == False:
            print(f'The table "{table}" does not exist in the database "{database}". Checks the name given.')
            return

        # It checks if the values given by the user are correct or not and it returns to the App.
        if self.validate_editing == False:
            print("An error occurred while processing your request!", self.message)
            return self.validate_editing, self.message

        try:

            # The password given by the user is recovered to be encrypted.
            password = user['password']
            password_encrypted = generate_password_hash(password)

            # Database is selected where user is or will be located.
            self.cursor.execute(f"USE {database}")

            # It checks if user exists in the database.
            self.cursor.execute(f"SELECT login FROM {database}.{table} WHERE login = '{user['login']}'")

            # Variable that contains the query with "None" or a tuple.
            user_exists = self.cursor.fetchone()

            # Step to sign up the user.
            if user['action'] == "sign_up":
                # It checks if the indicated user exists. It finish the call if it's "True".
                if user_exists:
                    self.validate_editing = False
                    self.message = f'El login que intenta registrar "{user["login"]}" ya existe y no \npuede ser duplicado. \
Elija otro nombre.'
                    # Values are returned to the App to indicate if the sign up was successful or not.
                    return self.validate_editing, self.message
                # If user does not exist the command to sign up user is formatted.
                else:
                    execute_command = f"INSERT INTO {table} (name, lastname, login, password) \
            values ('{user['name']}', '{user['lastname']}', '{user['login']}', '{password_encrypted}');"

            # Step to modify the user.
            elif user['action'] == "modify":
                if not user_exists:
                    self.validate_editing = False
                    self.message = f'El login que intenta modificar "{user["login"]}" no existe. \nCompruebe los valores indicados.'
                    # Values are returned to the App to indicate if the modification was successful or not.
                    return self.validate_editing, self.message
                else:
                    # Command to modify user is formatted.
                    execute_command = f"UPDATE {table} SET password = '{password_encrypted}' WHERE login = '{user['login']}'"        

        # Exception executed if the dictionary contains incorrect values in the keys.
        except:
            print("Error! Check the information given of the indicated user.")
            return

        try:
            # Command that executes the query to sign up or modify the user.
            self.cursor.execute(execute_command)
            self.connector.commit()
            if user['action'] == "sign_up":
                self.validate_editing = True
                self.message = f'El usuario "{user["login"]}" ha sido registrado correctamente.'
                # User is added to the table "users_configurations" with empty fields.
                add_users_configurations = f"INSERT INTO users_configurations (login) values ('{user['login']}');"
                self.cursor.execute(add_users_configurations)
                self.connector.commit()

                print(self.message)
                return self.validate_editing, self.message
            elif user['action'] == "modify":
                self.validate_editing = True
                self.message = 'El user ha sido actualizado correctamente.'
                print(self.message)
                return self.validate_editing, self.message 

        # Exception executed if the dictionary contains invalid values.
        except:
            self.validate_editing = False
            self.message = "Los campos indicados para este usuario no son válidos."
            print(self.message)
            return self.validate_editing, self.message

    @connection
    @check_db
    @check_table
    def configuraciones_user(self, database, table, user, action, campo, configuracion):
        """Método para añadir en la base de datos las configuraciones que el user realiza desde la aplicación.
        Necesita 5 argumentos: Una base de datos (type string), una table (type string), un user (type string),
        un campo a modify (type string) y los valuees de la configuración (type string)."""
        # Se comprueba si la table exists. Finaliza la llamada en caso de ser False.
        if self.table_exists == False:
            print(f'La table "{table}" no exists en la base de datos "{database}". \
Compruebe el name indicado.')
            return
            
        try:
            if action == "Actualizar":
                # Selecciona la base de datos en donde se van a guardar los valuees del user indicado. 
                self.cursor.execute(f"USE {database}")
                execute_command = f"UPDATE {table} SET {campo[1]} = '{configuracion[1]}' WHERE login = '{user}' and {campo[0]} = '{configuracion[0]}';"
                print("el comando insertado es: ", execute_command)
                self.cursor.execute(execute_command)
                self.connector.commit()
            elif action == "ActualizarNULL":
                # Selecciona la base de datos en donde se van a guardar los valuees del user indicado. 
                self.cursor.execute(f"USE {database}")
                execute_command = f"UPDATE {table} SET {campo[1]} = '{configuracion}' WHERE login = '{user}' and {campo[0]} IS NULL;"
                print("el comando insertado es: ", execute_command)
                self.cursor.execute(execute_command)
                self.connector.commit()
            elif action == "Agregar":
                self.cursor.execute(f"USE {database}")
                execute_command = f"INSERT INTO {table} ({campo}) values ('{user}', '{configuracion[0]}', '{configuracion[1]}', \
                '{configuracion[2]}', '{configuracion[3]}', '{configuracion[4]}', '{configuracion[5]}', '{configuracion[6]}');"
                print("comando final :", execute_command)
                self.cursor.execute(execute_command)
                self.connector.commit()
            elif action == "Borrar":
                self.cursor.execute(f"USE {database}")
                execute_command = f"DELETE FROM {table} WHERE {campo[0]} = '{user}' and {campo[1]} = '{configuracion}';"
                print("comando final :", execute_command)
                self.cursor.execute(execute_command)
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
        
        # Se comprueba si la table exists.
        if self.table_exists == False:
            print(f'La table "{table}" no exists en la base de datos "{database}". \
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

                # Comprueba si el login exists.
                self.cursor.execute(f"SELECT login FROM {database}.{table} WHERE login = '{user}'")
                # Recupera el value de la búsqueda realizada. Si el value es "None" entonces el user no exists y finaliza la llamada.
                value = self.cursor.fetchone()
                if not value:
                    print(f'El login indicado "{user}" no exists y no puede ser eliminado.')
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
        # Se comprueba si la table exists.
        if self.table_exists == False:
            print(f'La table "{table}" no exists en la base de datos "{database}". \
Compruebe el name indicado.')
            return
        try:
            # Selecciona la base de datos en donde se va a verificar el user indicado.
            self.cursor.execute(f"USE {database}")
            # Variable que determina si un user y contraseña son válidos para iniciar sesión. Necesita ser "True" para iniciar sesión.
            self.validacion_login = False

            # Comprueba si el login exists.
            self.cursor.execute(f"SELECT login FROM {database}.{table} WHERE login = '{user['login']}'")
            # Recupera el value de la búsqueda realizada. Si el value es "None" entonces el user no exists y finaliza la llamada.
            user_seleccionado = self.cursor.fetchone()
            if not user_seleccionado:
                print(f'El user "{user["login"]}" no exists. Compruebe nuevamente.')
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
