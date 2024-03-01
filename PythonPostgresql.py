import psycopg2
#pip install psycopg2
#sudo apt install python3-psycopg2
from PythonFunciones_Mariadbypostgresql import menu,opciones

try:
    db=psycopg2.connect(host="localhost",database="pepe",user="postgres",password="usuario",)
except psycopg2.OperationalError as e:
    print("No puedo conectar a la base de datos:",e)
    exit()
cursor=db.cursor()

num=0
while num != 7:
    num=menu()
    opciones(num,cursor,db)

cursor.close()
db.close()