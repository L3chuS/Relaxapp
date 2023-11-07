import Base_Datos.base_datos as bd
from Base_Datos.valores_presets import columnas_default, usuario

conectar = bd.BaseDatos(**bd.acceso_root)


# conectar.crear_bd("lechus")
# conectar.eliminar_bd("lechus")

# conectar.mostrar_bd()

# conectar.seleccionar_bd("lechus")

# consulta1 = conectar.consultas("SHOW TABLES")

# conectar.crear_tablas("lechus", "usuarios", columnas_default)

# conectar.eliminar_bd("lechus")

conectar.eliminar_tabla("lechus", "usuarios")

# conectar.editar_tabla("lechus", "usuarios", usuario)

# conectar.eliminar_datos_tabla("lechus", "usuarios", "UNIQUE", "lechusnqn11")

# conectar.copia_seguridad("lechus")

# conectar.importar_base_datos("E:\Programación\Portfolio\Relaxapp\Base_Datos\Copia_Seguridad", "lechus - 25-09-2023 - 06.44.53hs.sql")