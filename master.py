import Interfaz.Relaxapp as app

root = app.ctk.CTk()
app = app.RelaxApp_Initial_Frame(root)
root.mainloop()

# import Base_Datos.base_datos as bd

# from Base_Datos.valores_presets import columnas_default

# conectar = bd.BaseDatos(**bd.acceso_root)

# conectar.editar_tabla("lechus", "usuarios", usuario)

# conectar.eliminar_datos_tabla("lechus", "usuarios", "UNIQUE", "lechu")

# conectar.seleccionar_bd("lechus")

# conectar.crear_bd("lechus")

# conectar.mostrar_lista_bd()

# conectar.crear_bd("lechus")

# conectar.eliminar_bd("lechus2")

# conectar.crear_tabla("lechus", "usuarios", columnas_default)

# conectar.eliminar_tabla("lechus", "usuarios1")

# conectar.crear_tabla("lechus", "usuarios", columnas_default)

# conectar.consulta("SHOW TABLES FROM lechus")

# conectar.consulta("SELECT * FROM lechus.usuarios")

# conectar.consulta("SELECT * FROM world.city LIMIT 7")

# conectar.editar_tabla("lechus", "usuarios", usuario)

# conectar.consulta("SELECT nombre FROM lechus.usuarios WHERE login = 'lechu4'")

# conectar.editar_tabla("lechus", "usuarios", usuario)

# conectar.editar_tabla("lechus", "usuarios", usuario2)

# conectar.eliminar_datos_tabla("lechus", "usuarios", "UNIQUE", "lechu")

# conectar.verificar_login("lechus", "usuarios", usuario)

# conectar.copia_seguridad("lechus")

# conectar.eliminar_bd("lechus")

# conectar.importar_base_datos("E:\Programación\Portfolio\Relaxapp\Base_Datos\Copia_Seguridad", "lechus - 01-10-2023 - 03.35.50hs.sql")

