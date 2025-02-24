import os

user = os.environ.get("UserMySql")
password = os.environ.get("PasswordMySql")

# Dictionary which contains the values by default to be use to establish connection with the database.

root_access = {
            "host" : "localhost",
            "user" : user,
            "password" : password,
            "database" : ""
            }

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
databases = {"database1": "lechus"}

# Tables used.
tables = {"users_table": "users", 
          "settings_table":"users_configurations"}
