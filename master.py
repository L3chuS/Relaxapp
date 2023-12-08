import Interfaz.Relaxapp as app

# import pruebas as app

root = app.ctk.CTk()

app = app.RelaxApp_Initial_Frame(root)

root.mainloop()

# import Base_Datos.base_datos as bd

# from Base_Datos.valores_presets import columnas_usuario_default, columnas_configuraciones_default

# conectar = bd.BaseDatos(**bd.acceso_root)

# conectar.editar_tabla("lechus", "usuarios", usuario)

# configuraciones_usuario(self, base_datos, tabla, usuario, configuracion_visual, configuracion_estirar)

# conectar.crear_bd("lechus")

# conectar.eliminar_bd("lechus")

# conectar.crear_tabla("lechus", "usuarios", columnas_usuario_default)

# conectar.crear_tabla("lechus", "usuarios_configuraciones", columnas_configuraciones_default)

# conectar.eliminar_tabla("lechus", "usuario_configuraciones")

# conectar.eliminar_datos_tabla("lechus", "usuarios", "UNIQUE", "lechu")

# conectar.seleccionar_bd("lechus")

# conectar.mostrar_lista_bd()

# conectar.consulta("SHOW TABLES FROM lechus")

# conectar.consulta("SELECT * FROM lechus.usuarios")

# conectar.consulta("SELECT * FROM world.city LIMIT 7")

# conectar.editar_tabla("lechus", "usuarios", usuario)

# conectar.consulta("SELECT Configuracion_Visual FROM lechus.usuarios_configuraciones WHERE login = 'lechu'")

# conectar.editar_tabla("lechus", "usuarios", usuario)

# conectar.editar_tabla("lechus", "usuarios", usuario2)

# conectar.eliminar_datos_tabla("lechus", "usuarios", "UNIQUE", "lechu")

# conectar.verificar_login("lechus", "usuarios", usuario)

# conectar.copia_seguridad("lechus")

# conectar.eliminar_bd("lechus")

# conectar.importar_base_datos("E:\Programación\Portfolio\Relaxapp\Base_Datos\Copia_Seguridad", "lechus - 01-10-2023 - 03.35.50hs.sql")

