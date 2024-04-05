import Interfaz.relaxapp as app

# import test as app

root = app.ctk.CTk()

app = app.RelaxApp_Initial_Frame(root)

root.mainloop()

# import Database.database as bd

# from Database.presets_values import columns_users_default, columns_configuration_default

# conectar = bd.Database(**bd.root_access)

# conectar.create_db("lechus")

# conectar.create_table("lechus", "users", columns_users_default)

# conectar.create_table("lechus", "users_configurations", columns_configuration_default)

# conectar.remove_db("lechus")

# conectar.query("SELECT Perfile_Name FROM lechus.users_configurations WHERE login = 'lechu'")

# conectar.edit_table("lechus", "users", usuario)

# conectar.edit_table("lechus", "users", usuario2)

# conectar.remove_table("lechus", "users_configurations")

# conectar.remove_table_values("lechus", "users", "UNIQUE", "lechu")

# conectar.get_db("lechus")

# conectar.show_list_db()

# conectar.query("SHOW TABLES FROM lechus")

# conectar.query("SELECT * FROM lechus.users")

# conectar.query("SELECT * FROM world.city LIMIT 7")

# conectar.remove_table_values("lechus", "users", "UNIQUE", "lechu")

# conectar.verify_login("lechus", "users", usuario)

# conectar.backup("lechus")

# conectar.import_database("E:\Programación\Portfolio\Relaxapp\Base_Datos\Copia_Seguridad", "lechus - 01-10-2023 - 03.35.50hs.sql")

