# import Interface.relaxapp as app

# # import test as app

# root = app.ctk.CTk()

# app = app.RelaxApp_Initial_Frame(root)

# root.mainloop()

import Database.database as bd

from Database.presets_values import columns_users_default, columns_configuration_default

connect = bd.Database(**bd.root_access)

# connect.create_db("lechus")

# connect.create_table("lechus", "users", columns_users_default)

# connect.create_table("lechus", "users_configurations", columns_configuration_default)

# connect.remove_db("lechus")

# connect.query("SELECT Perfile_Name FROM lechus.users_configurations WHERE login = 'lechu'")

# connect.edit_table("lechus", "users", usuario)

# connect.edit_table("lechus", "users", usuario2)

# connect.remove_table("lechus", "users_configurations")

# connect.remove_table_values("lechus", "users", "UNIQUE", "lechu")

# connect.get_db("lechus")

# connect.show_list_db()

# connect.query("SHOW TABLES FROM lechus")

# connect.query("SELECT * FROM lechus.users")

# connect.query("SELECT * FROM world.city LIMIT 7")

# connect.remove_table_values("lechus", "users", "UNIQUE", "lechu")

# connect.verify_login("lechus", "users", usuario)

# connect.backup("lechus")

# connect.import_database("E:\Programación\Portfolio\Relaxapp\Base_Datos\Copia_Seguridad", "lechus - 01-10-2023 - 03.35.50hs.sql")

