import mysql.connector
import os
import subprocess
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from Database.presets_values import root_access

# Variable to get the location of the project.
main_path = os.path.dirname(__file__)
backup_path = main_path + "\\Backup"

# Main class of the database.
class Database:
    """Class that contains all the methods to connect, create, select, run queries,
       register and modify users, backup and import copies, etc. Interact with the
       app to perform access management, user registrations or modifications.
    """
    def __init__(self, **kwargs):
        # Conection with MySql server is done. It takes a dict (by default is
        # "root_access") to get the key values.

        self.connection_status = False
        try:
            self.connector = mysql.connector.connect(**kwargs)
            self.cursor = self.connector.cursor()
            self.host = kwargs["host"]
            self.user = kwargs["user"]
            self.password = kwargs["password"]
            self.connection_status = True
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
                if self.connection_status:
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
                    self.connection_status = True
                decorated_function(self, *args, **kwargs)

            # Exception executed if the conection values are invalid.
            except:
                print("Error! Check the arguments given.")
            finally:
                # Connection is always close after each connection.
                if self.connection_status:
                    self.connector.close()
                    self.cursor.close()
                    self.connection_status = False
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
            # Values are gotten.
            get_db = self.cursor.fetchall()
            self_db_exists = False

            # Iteration over each gotten value to check if the one passed as an argument exists or not.
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
            # Values are gotten.
            get_table = self.cursor.fetchall()
            self.table_exists = False
            # Iteration over each gotten value to check if the table passed as an argument exists or not.
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
                        self.message = "La logitud del nombre o del apellido deben tener al menos 2 \ncaracteres y no deben superar los 60."
                        self.message_terminal = f"Lenght of the {key} must have at least 2 characters and can't be higher than 60."
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
                                    self.message = f"El nombre o el apellido contienen caracteres inválidos. \nCompruebe nuevamente."
                                    self.message_terminal = f"The {key} contains invalid characters. Check it again."
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
                            self.message_terminal = "User or password contains white spaces. Check it again."
                            break

            # The lenght of the user or password is checked. It must have at least 5 characters and can't be higher than 20.
            if self.validate_editing:
                if len(user["login"]) < 5 or len(user["password"]) < 5 or len(user["login"]) > 20 or len(user["password"]) > 20:
                    self.validate_editing = False
                    # Variable to create a label to be used in the App.
                    self.message = f"El usuario o contraseña deben tener al menos 5 caracteres \ny menos de 20."
                    self.message_terminal = "User or password must have at least 5 characters and can't be higher than 20."

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
        # Iteration and format over each value gotten.
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

            # Iteration and format over each value gotten.
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
            print("An error occurred while processing your request!", self.message_terminal)
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
                    self.message_terminal = f'Login "{user["login"]}" you\'re trying to sign up already exist and can\'t be duplicated. \
Choose another name.'
                    # Values are returned to the App to indicate if the sign up was successful or not.
                    return self.validate_editing, self.message
                # If user does not exist the command to sign up user is formatted.
                else:     
                    execute_command = f"INSERT INTO {table} (name, last_name, login, password) \
values ('{user['name']}', '{user['lastname']}', '{user['login']}', '{password_encrypted}');"

            # Step to modify the user.
            elif user['action'] == "modify":
                if not user_exists:
                    self.validate_editing = False
                    self.message = f'El login que intenta modificar "{user["login"]}" no existe. \nCompruebe los valores indicados.'
                    self.message_terminal = f'Login "{user["login"]}" you\'re trying to modify does not exist. \nCheck the information given.'
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
                self.message_terminal = f'User "{user["login"]}" has been created successfully.'
                # User is added to the table "users_configurations" with empty fields.
                add_users_configurations = f"INSERT INTO users_configurations (login) values ('{user['login']}');"
                self.cursor.execute(add_users_configurations)
                self.connector.commit()

                print(self.message_terminal)
                return self.validate_editing, self.message
            elif user['action'] == "modify":
                self.validate_editing = True
                self.message = "El user ha sido actualizado correctamente."
                self.message_terminal = "User has been updated successfully."
                print(self.message_terminal)
                return self.validate_editing, self.message 

        # Exception executed if the dictionary contains invalid values.
        except:
            self.validate_editing = False
            self.message = "Los campos indicados para este usuario no son válidos."
            self.message_terminal = "The fields given for this user are not valid."
            print(self.message_terminal)
            return self.validate_editing, self.message

    @connection
    @check_db
    @check_table
    def user_configuration(self, database, table, user, action, field=None, configuration=None):
        """Method to add in the database configurations that the user makes from the application.
           It needs 5 arguments: A database (string type), a table (string type), a user (string type),
           a field to modify (string type) and the configuration values (string type)."""
        # It checks if the indicated table exists. It finish the call if it's "False".
        self.validate_config = False

        if self.table_exists == False:
            print(f'Table "{table}" does not exists in the database "{database}". Check the information given.')
            return
            
        try:
            self.cursor.execute(f"USE {database}")
            if action == "Update":
                # Database is selected where the values of the user will be saved.
                execute_command = f"UPDATE {table} SET {field[1]} = '{configuration[1]}' WHERE login = '{user}' and {field[0]} = '{configuration[0]}';"
                print("The command executed is: ", execute_command)
            elif action == "UpdateNULL":
                # Database is selected where the values of the user will be saved.
                execute_command = f"UPDATE {table} SET {field[1]} = '{configuration}' WHERE login = '{user}' and {field[0]} IS NULL;"
                print("The command executed is: ", execute_command)
            elif action == "Add":
                execute_command = f"INSERT INTO {table} ({field}) values ('{user}', '{configuration[0]}', '{configuration[1]}', \
                '{configuration[2]}', '{configuration[3]}', '{configuration[4]}', '{configuration[5]}', '{configuration[6]}');"
                print("Final command: ", execute_command)
            elif action == "Restore":
                execute_command = f"UPDATE {table} SET Visual_Configuration = '', Stretch_Configuration = '', Final_Sounds_Configuration = '', \
                Lapse_Sounds_Configuration = '' WHERE login = '{user}' and Profile_Name IS NULL;"
                print("Final command: ", execute_command)
            elif action == "Restart":
                execute_command = f"UPDATE {table} SET {field} = '', Final_Sounds_Configuration = '', Lapse_Sounds_Configuration = '' \
                WHERE login = '{user}' and Profile_Name IS NULL;"
                print("Final command: ", execute_command)
            elif action == "Import Profile":
                date_time = datetime.datetime.now().strftime("%d-%m-%Y - %H.%M.%Shs")

                if len(configuration[5]) == 4:
                    execute_command = f"UPDATE {table} SET Profile_Name = '{configuration[0]}', Date_Time = '{date_time}', Profile_Default = 'True', \
                    Visual_Configuration = '{configuration[1]}', Stretch_Configuration = '{configuration[2]}', Final_Sounds_Configuration = '{configuration[3]}', \
                    Lapse_Sounds_Configuration = '{configuration[4]}' WHERE login = '{user}' and ID = '{configuration[5][-1]}';"
                    print("Final command: ", execute_command)
                elif len(configuration[5]) < 4:
                    execute_command = f"INSERT INTO {table} ({field}) values ('{user}', '{configuration[0]}', '{date_time}', \
                    'True', '{configuration[1]}', '{configuration[2]}', '{configuration[3]}', '{configuration[4]}');"
                    print("Final command: ", execute_command)
                for i in range(1, len(configuration[5]) - 1):
                    id = configuration[5][i]
                    set_all_false = f"UPDATE {table} SET Profile_Default = 'False' WHERE login = '{user}' and ID = '{id}';"
                    self.cursor.execute(set_all_false)

            elif action == "Remove":
                execute_command = f"DELETE FROM {table} WHERE {field[0]} = '{user}' and {field[1]} = '{configuration}';"
                print("Final command: ", execute_command)
            
            elif action == "Remove Account":
                execute_command = f"DELETE FROM {table} WHERE login = '{user}';"
                print("Final command: ", execute_command)

            self.cursor.execute(execute_command)
            self.connector.commit()

        except:
            print("Error! Check the information given of the indicated user.")

    @connection
    @check_db
    @check_table
    def remove_table_values(self, database, table, amount, user=None):
        """Method to remove tables. It needs 3 mandatory arguments and 1 optional: A database (string type), a table
           (string type) and a quantity (string type). The "user" argument (dictionary type) is optional in case that
           you only want to delete a particular user."""

        # It checks if table exists.
        if self.table_exists == False:
            print(f'Table "{table}" does not exists in the database "{database}". Check the information given.')
            return
        try:
            # Database is selected where user or users will be removed. 
            self.cursor.execute(f"USE {database}")
            if amount == "ALL":
                remove_command = f"DELETE FROM {table} list;"
            elif amount == "UNIQUE":
                if user == None:
                    print("Any user was given. Fullfil all fields propertly.")
                    return
                else:
                    remove_command = f"DELETE FROM {table} WHERE login = '{user}';"

                # It checks if login exists.
                self.cursor.execute(f"SELECT login FROM {database}.{table} WHERE login = '{user}'")
                # Value of the query executed is gotten. If this value is "None" then user does not exist and the call is ended.
                value = self.cursor.fetchone()
                if not value:
                    print(f'Login given "{user}" does not exist and can\'t be removed.')
                    return

            # Command that executes the elimination of the indicated user or users.
            self.cursor.execute(remove_command)
            self.connector.commit()
            if amount == "ALL":
                print(f'All users in the table "{table}" in the database "{database}" \
has been removed successfully.')
            elif amount == "UNIQUE":
                print(f'User "{user}" has been removed successfully from the table "{table}" in \
the database "{database}".')

        # Exception executed if the "amount" argument is invalid.
        except:
            print("Error! Check the arguments given.")

    @connection
    @check_db
    @check_table
    def verify_login(self, database, table, user):
        """Method to verify the sign in with the app. It requires 3 arguments: A database (string type), a table
           (string type) and a user (dictionary type) that contains the data to be checked (user and password)."""
        # It checks if table exists.
        if self.table_exists == False:
            print(f'The table "{table}" does not exist in the database "{database}". Check the information given.')
            return
        try:
            # Database is selected where user will be verify.
            self.cursor.execute(f"USE {database}")
            # Variable which defines if user and password are valid to sign in. It needs to be "True".
            self.valid_login = False

            # It checks if login exists.
            self.cursor.execute(f"SELECT login FROM {database}.{table} WHERE login = '{user['login']}'")
            # Value of the query executed is gotten. If it's "None" then user does not exist and it ends the call.
            selected_user = self.cursor.fetchone()
            if not selected_user:
                print(f'User "{user["login"]}" does not exists. Check it again.')
                return self.valid_login

            # Password saved in the database is searched.
            self.cursor.execute(f"SELECT password FROM {database}.{table} WHERE login = '{user['login']}'")
            # Variable that contains the value of the executed query.
            selected_pw = self.cursor.fetchone()
            # Decrypts the password stored in the database and compares it with the value entered by the user.
            # If it's "True" the validation is correct.
            verification = check_password_hash(selected_pw[0], user["password"])

            if not verification:
                print(f'Password incorrect. Try it again.')
            else:
                print("Validation successful.")
                self.valid_login = True
            return self.valid_login

        # Exception executed if the arguments of the dictionary "user" are invalid.
        except:
            print("Error! Check the arguments given.")

    @connection
    @check_db
    def backup(self, database):
        """Method to make a backup copies of a database. It needs one argument: database name (string type)."""
        # Variable that saved the time and date when the backup is done.
        date_time = datetime.datetime.now().strftime("%d-%m-%Y - %H.%M.%Shs")
        # Varible to be used to confirm if backup was successful or not.
        copy = False
        # File that contains the information of the backup is created.
        with open(f"{backup_path}/{database} - {date_time}.sql", "w") as exit:
            # Variable that contains the command to be used to do the backup.
            command = subprocess.Popen(f'"C:/Program Files/MySQL/MySQL Workbench 8.0/"mysqldump --user={self.user} \
                            --password={self.password} \
                            --databases {database}', shell=True, stdout=exit)
            # Value if executed command is gotten.
            command.communicate()

            # "returncode" is used to check if command was executed successfully or not.
            # "0" means execution was successful and 1 it wasn't.
            if command.returncode == 0:
                print(f'Backup of the database "{database}" was executed successfully. \
File name: "{database} - {date_time}.sql"')
                copy = True

            else:
                print("Error! Backup has failed. Check the command given.")

        # It removes the file created automatically while calling the method "with open" if backup failed.
        if copy == False:
            path = f"{backup_path}/{database} - {date_time}.sql"
            os.remove(path)

    @connection
    def import_database(self, path, file):
        """Method to import a database. It needs 2 arguments: The path (string type) where the file it's located and the name
           of the file (string type) with the extension."""
        # Variable that contains the command to import the database.
        command = subprocess.Popen(f'"C:/Program Files/MySQL/MySQL Workbench 8.0/"mysql --user={self.user} \
                            --password={self.password} < "{path}/{file}"', shell=True)
        # Value if executed command is gotten.
        command.communicate()

        # "returncode" is used to check if command was executed successfully or not.
        # "0" means execution was successful and 1 it wasn't.
        if command.returncode == 0:
            print(f'Import of the file "{file}" was executed successfully.')
        else:
            print("\nError! Import of the backup has failed. Check the arguments given.")
