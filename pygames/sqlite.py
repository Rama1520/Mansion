import sqlite3


with sqlite3.connect("puntuacion.db") as conexion:
    try: 
        sentencia = """ create table MansionSpooky
        (
        id integer primary key autoincrement,
        Nombre text,
        Tiempo text
        )
        """

        conexion.execute(sentencia)
        print("Se creo la MansionSpooky")
    except sqlite3.OperationalError:
        pass
    cursor = conexion.execute("SELECT * FROM MansionSpooky")
    jugador = list()
    for fila in cursor:
        print(fila)
def guardar_datos(nombre1,tiempo1):
    with sqlite3.connect("puntuacion.db") as conexion:
        conexion.execute("INSERT INTO MansionSpooky (Nombre,Tiempo) values (?,?)", (nombre1,tiempo1))
