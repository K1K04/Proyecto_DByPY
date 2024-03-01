import oracledb
#pip install oracledb
#sudo apt install python3-oracledb
from PythonFunciones_oracle import menu, opciones
try:
    # Conexión a la base de datos Oracle
    db = oracledb.connect("c##usuario/c##usuario@172.22.6.24/XE")
    print("Conexión exitosa a la base de datos Oracle.")
except oracledb.DatabaseError as e:
    print("No se puede conectar a la base de datos:", e)
    exit()

# Crear un cursor para ejecutar consultas SQL
cursor = db.cursor()

# Ciclo principal del programa
num = 0
while num != 7:
    num = menu()  # Mostrar el menú y obtener la opción seleccionada por el usuario
    opciones(num, cursor, db)  # Ejecutar la opción seleccionada

# Cerrar cursor y conexión a la base de datos
cursor.close()
db.close()
