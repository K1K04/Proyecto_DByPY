from tabulate import tabulate
#pip install tabulate

def menu():
    print()
    print('''Menú
    1. Lista los jugadores y el número de clubes asociados a cada uno.
    2. Mostrar clubes con contratos de jugadores cuyos salarios están dentro de un rango.
    3. Mostrar clubes y jugadores asociados a un club dado.
    4. Insertar nuevo entrenador.
    5. Eliminar entrenador.
    6. Actualizar palmares de un club.
    7. Salir.''')
    num = input("Elija una opción: ")
    print()
    while not num.isnumeric() or int(num) not in range(1, 8):
        print("Esa opción no existe.")
        num = input("Elija una opción: ")
    return int(num)

def opciones(num, cursor, db):
    if num == 1:
        lista_jugadores(cursor)
    elif num == 2:
        mostrar_clubes_por_salario(cursor)
    elif num == 3:
        mostrar_jugadores_por_club(cursor)
    elif num == 4:
        insertar_entrenador(cursor, db)
    elif num == 5:
        eliminar_entrenador(cursor, db)
    elif num == 6:
        actualizar_palmares_club(cursor, db)

def lista_jugadores(cursor):
    sql = "SELECT Nombre, Apellidos, COUNT(Contrato.DNI_Jugador) AS NumClubes FROM Jugadores LEFT JOIN Contrato ON Jugadores.DNI = Contrato.DNI_Jugador GROUP BY Nombre, Apellidos"
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        if registros:
            print(tabulate(registros, headers=["Nombre", "Apellidos", "NumClubes"], tablefmt="fancy_grid"))
        else:
            print("No hay jugadores en la base de datos.")
    except Exception as e:
        print("Error al listar jugadores:", e)

def mostrar_clubes_por_salario(cursor):
    # Mostrar los clubes y sus salarios
    try:
        cursor.execute("SELECT DISTINCT Nombre_Club, Salario FROM Contrato")
        clubes_salarios = cursor.fetchall()
        if clubes_salarios:
            print("Clubes y sus salarios:")
            print(tabulate(clubes_salarios, headers=["Nombre del Club", "Salario"], tablefmt="fancy_grid"))
        else:
            print("No hay clubes con jugadores en la base de datos.")
        print()
    except Exception as e:
        print("Error al obtener los clubes y sus salarios:", e)
        return
    
    salario_min = input("Salario mínimo: ")
    salario_max = input("Salario máximo: ")

    if salario_min > salario_max:
        print("El salario máximo no puede ser menor que el salario mínimo.")
        return

    sql = f"SELECT DISTINCT Nombre_Club FROM Contrato WHERE Salario BETWEEN {salario_min} AND {salario_max}"
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        if registros:
            print(tabulate(registros, headers=["Nombre_Club"], tablefmt="fancy_grid"))
        else:
            print("No hay clubes con jugadores en el rango salarial especificado.")
    except Exception as e:
        print("Error al mostrar clubes por salario:", e)

def mostrar_jugadores_por_club(cursor):
    # Obtener todos los clubes disponibles
    try:
        cursor.execute("SELECT Nombre FROM Club")
        clubes = cursor.fetchall()
        print("Club disponibles:")
        for club in clubes:
            print(club[0])
        print()
    except Exception as e:
        print("Error al obtener los clubes disponibles:", e)
        return
    
    # Pedir al usuario que ingrese el nombre del club
    club = input("Nombre del club: ")

    # Verificar si el club existe en la base de datos
    sql_verificar_club = f"SELECT Nombre FROM Club WHERE Nombre = '{club}'"
    cursor.execute(sql_verificar_club)
    club_existente = cursor.fetchone()
    
    if club_existente:
        # Si el club existe, continuamos con la consulta original
        sql = f"SELECT Nombre, Apellidos FROM Jugadores WHERE DNI IN (SELECT DNI_Jugador FROM Contrato WHERE Nombre_Club = '{club}')"
        try:
            cursor.execute(sql)
            registros = cursor.fetchall()
            if registros:
                print(tabulate(registros, headers=["Nombre", "Apellidos"], tablefmt="fancy_grid"))
            else:
                print(f"No hay jugadores asociados al club '{club}'.")
        except Exception as e:
            print("Error al mostrar jugadores por club:", e)
    else:
        # Si el club no existe, mostramos un mensaje apropiado
        print(f"No existe ningún club con el nombre '{club}'.")

def insertar_entrenador(cursor, db):
    # Mostrar los entrenadores disponibles
    try:
        cursor.execute("SELECT DNI, Nombre FROM Entrenador")
        entrenadores = cursor.fetchall()
        if entrenadores:
            print("Entrenadores disponibles:")
            print(tabulate(entrenadores, headers=["DNI", "Nombre"], tablefmt="fancy_grid"))
        else:
            print("No hay entrenadores en la base de datos.")
        print()
    except Exception as e:
        print("Error al obtener los entrenadores:", e)
        return
    
    # Continuar con la inserción del entrenador
    dni = input("DNI del entrenador: ")
    nombre = input("Nombre del entrenador: ")

    try:
        sql_insert_entrenador = f"INSERT INTO Entrenador (DNI, Nombre) VALUES ('{dni}', '{nombre}')"
        
        cursor.execute(sql_insert_entrenador)
        db.commit()
        print("Entrenador insertado con éxito.")
    except Exception as e:
        db.rollback()
        print("Error al insertar entrenador:", e)

def eliminar_entrenador(cursor, db):
    # Mostrar los entrenadores disponibles
    try:
        cursor.execute("SELECT DNI, Nombre FROM Entrenador")
        entrenadores = cursor.fetchall()
        if entrenadores:
            print("Entrenadores disponibles:")
            print(tabulate(entrenadores, headers=["DNI", "Nombre"], tablefmt="fancy_grid"))
        else:
            print("No hay entrenadores en la base de datos.")
        print()
    except Exception as e:
        print("Error al obtener los entrenadores:", e)
        return
    
    # Continuar con la eliminación del entrenador
    dni = input("DNI del entrenador a eliminar: ")
    
    # Verificar si el entrenador existe en la base de datos
    try:
        cursor.execute(f"SELECT DNI FROM Entrenador WHERE DNI = '{dni}'")
        entrenador_existente = cursor.fetchone()
        if not entrenador_existente:
            print(f"No existe ningún entrenador con el DNI '{dni}'.")
            return
    except Exception as e:
        print("Error al verificar la existencia del entrenador:", e)
        return
    
    try:
        sql_delete_entrenador = f"DELETE FROM Entrenador WHERE DNI = '{dni}'"
        
        cursor.execute(sql_delete_entrenador)
        db.commit()
        print("Entrenador eliminado con éxito.")
    except Exception as e:
        db.rollback()
        print("Error al eliminar entrenador:", e)

def actualizar_palmares_club(cursor, db):
    # Mostrar los clubes y su palmarés
    try:
        cursor.execute("SELECT Nombre, Palmares FROM Club")
        clubes = cursor.fetchall()
        if clubes:
            print("Clubes y su palmarés:")
            print(tabulate(clubes, headers=["Nombre del Club", "Palmarés"], tablefmt="fancy_grid"))
        else:
            print("No hay clubes en la base de datos.")
        print()
    except Exception as e:
        print("Error al obtener los clubes y su palmarés:", e)
        return
    
    nombre_club = input("Nombre del club: ")
    nuevo_palmares = input("Nuevo palmarés del club: ")

    sql_actualizar_palmares = f"UPDATE Club SET Palmares = {nuevo_palmares} WHERE Nombre = '{nombre_club}'"

    try:
        cursor.execute(sql_actualizar_palmares)
        db.commit()
        print("Palmarés actualizado con éxito.")
    except Exception as e:
        db.rollback()
        print("Error al actualizar palmarés del club:", e)
