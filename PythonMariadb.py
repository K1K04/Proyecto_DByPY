import MySQLdb
#pip install MySQLdb
#sudo apt install python3-mysqldb
import sys
from PythonFunciones_Mariadbypostgresql import menu,opciones

try:
    db = MySQLdb.connect(user="root", password="root", host="localhost", database="Direccion_Deportiva")
except MySQLdb.Error as e:
    print("No puedo conectar a la base de datos:",e)
    sys.exit(1)
cursor=db.cursor()
num=0
while num != 7:
    num=menu()
    opciones(num,cursor,db)
    
cursor.close()
db.close()