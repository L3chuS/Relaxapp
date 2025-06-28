import os
from io import StringIO
from dotenv import dotenv_values
from cryptography.fernet import Fernet
from Database import dcfile
from utils import get_resource_path

fernet = Fernet(dcfile.dcpath)

abs_path = get_resource_path("Database")

# Dataserver file is loaded.
ec_dataserver = os.path.join(abs_path, "ec_dataserver.env")

with open(ec_dataserver, "rb") as file:
    ec_data = file.read()

dc_data = fernet.decrypt(ec_data).decode()

env_vars = dotenv_values(stream=StringIO(dc_data))

# The values of the server are gotten from dataserver.env.
host = env_vars.get("MYSQL_HOST")
port = env_vars.get("MYSQL_PORT")
user = env_vars.get("MYSQL_USER")
password = env_vars.get("MYSQL_PASSWORD")
database = env_vars.get("MYSQL_DATABASE")

# Dictionary which contains the values by default to be use to establish connection with the database.
root_access = {
            "host" : host,
            "port" : port,
            "user" : user,
            "password" : password,
            "database" : database
            }
print(root_access)
# List of dictionaries to be used as presets to create new tables.
# Between index [0:-1] there're each name of the column with their specific configuration.
# In the index [-1] primary key is set.

columns_users_default = [
    {
        "name" : "ID",
        "type" : "INT",
        "lenght" : 10,
        "unique" : True,
        "auto_increment" : True,
        "not_null" : True,
    },
    {
        "name" : "Name",
        "type" : "VARCHAR",
        "lenght" : 60,
        "unique" : False,
        "auto_increment" : False,
        "not_null" : True,
    },
    {
        "name" : "Last_Name",
        "type" : "VARCHAR",
        "lenght" : 60,
        "unique" : False,
        "auto_increment" : False,
        "not_null" : True,
    },
    {
        "name" : "Login",
        "type" : "VARCHAR",
        "lenght" : 20,
        "unique" : True,
        "auto_increment" : False,
        "not_null" : True,
    },
    {
        "name" : "Password",
        "type" : "VARCHAR",
        "lenght" : 500,
        "unique" : False,
        "auto_increment" : False,
        "not_null" : True,
    },
    {
        "primary_key" : "ID"
    }]

columns_configuration_default = [
    {
        "name" : "ID",
        "type" : "INT",
        "lenght" : 10,
        "unique" : True,
        "auto_increment" : True,
        "not_null" : True,
    },
    {
        "name" : "Login",
        "type" : "VARCHAR",
        "lenght" : 30,
        "unique" : False,
        "auto_increment" : False,
        "not_null" : True,
    },
    {
        "name" : "Profile_Name",
        "type" : "VARCHAR",
        "lenght" : 30,
        "unique" : False,
        "auto_increment" : False,
        "not_null" : False,
    },
    {
        "name" : "Date_Time",
        "type" : "VARCHAR",
        "lenght" : 30,
        "unique" : False,
        "auto_increment" : False,
        "not_null" : False,
    },
    {
        "name" : "Default_Profile",
        "type" : "VARCHAR",
        "lenght" : 10,
        "unique" : False,
        "auto_increment" : False,
        "not_null" : False,
    },
    {
        "name" : "Visual_Configuration",
        "type" : "VARCHAR",
        "lenght" : 150,
        "unique" : False,
        "auto_increment" : False,
        "not_null" : False,
    },
    {
        "name" : "Stretch_Configuration",
        "type" : "VARCHAR",
        "lenght" : 150,
        "unique" : False,
        "auto_increment" : False,
        "not_null" : False,
    },
    {
        "name" : "Final_Sounds_Configuration",
        "type" : "VARCHAR",
        "lenght" : 300,
        "unique" : False,
        "auto_increment" : False,
        "not_null" : False,
    },
    {
        "name" : "Lapse_Sounds_Configuration",
        "type" : "VARCHAR",
        "lenght" : 300,
        "unique" : False,
        "auto_increment" : False,
        "not_null" : False,
    },
    {
        "primary_key" : "ID"
    }]

# Dictionary to be used to get values given by users and sign up, update or remove them (only editables from the GUI).
user = {
        "action" : "",
        "name" : "",
        "lastname" : "",
        "login" : "",
        "password" : "",
        }

# Main database used.
databases = {"database1": database}

# Tables used.
tables = {"users_table": "users", 
          "settings_table":"users_configurations"}
