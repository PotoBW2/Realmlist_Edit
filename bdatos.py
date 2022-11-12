import sqlite3 as sql
import utiles
import os
import errno

RUTA = "dataConfig"
SERVIDOR = RUTA + "/dataPings.db"


def crear_base_de_datos():
    try:
        os.mkdir(RUTA)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    conn = sql.connect(SERVIDOR)
    cursor = conn.cursor()
    instruccion = """
    CREATE TABLE ip (
	    id_ip               integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
        primero             integer(3) DEFAULT 192 NOT NULL, 
        segundo             integer(3) DEFAULT 168 NOT NULL, 
        tercero             integer(3) DEFAULT 1 NOT NULL, 
        cuarto              integer(3) DEFAULT 0 NOT NULL, 
        Servidorid_servidor integer(2) NOT NULL,  
        FOREIGN KEY(Servidorid_servidor) REFERENCES Servidor(id_servidor));
        """
    instruccion10 = """
    CREATE TABLE Servidor (
      id_servidor     integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
      nombre_servidor varchar(20) NOT NULL UNIQUE
        );
    """
    instruccion3 = """
    CREATE TABLE url (
      id_url              integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
      direccion           varchar(30) NOT NULL UNIQUE, 
      Servidorid_servidor integer(2) NOT NULL,
      FOREIGN KEY(Servidorid_servidor) REFERENCES Servidor(id_servidor));
      """
    instruccion4 = """
    CREATE UNIQUE INDEX ip_id_ip 
        ON ip (id_ip);
    """
    instruccion6 = """
    CREATE UNIQUE INDEX Servidor_id_servidor 
        ON Servidor (id_servidor);
    """
    instruccion7 = """
    CREATE UNIQUE INDEX url_id_url 
        ON url (id_url);
    """
    instruccion8 = """
    INSERT INTO Servidor(id_servidor, nombre_servidor) VALUES (1, 'localhost');
    """
    instruccion9 = """
    INSERT INTO ip(primero, segundo, tercero, cuarto, Servidorid_servidor) VALUES ( 127, 0, 0, 1, 1);
    """
    cursor.execute(instruccion)
    cursor.execute(instruccion10)
    cursor.execute(instruccion3)
    cursor.execute(instruccion4)
    cursor.execute(instruccion6)
    cursor.execute(instruccion7)
    cursor.execute(instruccion8)
    cursor.execute(instruccion9)
    conn.commit()
    conn.close()


def existe_servidor_nombre(nombre_servidor, id_servidor=0):
    datos = obtener_id_servidor(nombre_servidor=nombre_servidor, exepto=id_servidor)
    if len(datos) == 0:
        return False
    else:
        return True


def existe_bd():
    if not os.path.exists(SERVIDOR):
        crear_base_de_datos()
        utiles.existe_configuracion()
    elif not existe_servidor_nombre(nombre_servidor="localhost"):
        conn = sql.connect(SERVIDOR)
        cursor = conn.cursor()
        instruccion = """
        INSERT INTO Servidor(id_servidor, nombre_servidor) VALUES (1, 'localhost');
        """
        instruccion2 = """
        INSERT INTO ip(primero, segundo, tercero, cuarto, Servidorid_servidor) VALUES ( 127, 0, 0, 1, 1);
        """
        cursor.execute(instruccion)
        cursor.execute(instruccion2)
        conn.commit()
        conn.close()
    return sql.connect("dataConfig/dataPings.db")


def cargar_servidores():
    conn = existe_bd()
    cursor = conn.cursor()
    instruccion = f"SELECT nombre_servidor FROM Servidor;"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos


def cargar_servidores2():
    conn = existe_bd()
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM Servidor;"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos


def existe_servidor_url(url, id_servidor=0):
    conn = existe_bd()
    cursor = conn.cursor()
    instruccion = "SELECT id_url FROM url WHERE direccion = '" + url + "'"
    if id_servidor != 0:
        instruccion = instruccion + " AND Servidorid_servidor != " + str(id_servidor)
    instruccion = instruccion + ";"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    if len(datos) == 0:
        return False
    else:
        return True


def existe_servidor_ip(primero, segundo, tercero, cuarto, id_servidor=0):
    conn = existe_bd()
    cursor = conn.cursor()
    instruccion = "SELECT id_ip FROM ip WHERE primero=" + str(primero) + " AND segundo=" + str(
        segundo) + " AND tercero=" + str(tercero) + " AND cuarto=" + str(cuarto)
    if id_servidor != 0:
        instruccion = instruccion + " AND Servidorid_servidor != " + str(id_servidor) + ""
    instruccion = instruccion + ";"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    if len(datos) == 0:
        return False
    else:
        return True


def insertar_servidor_IP(nombre_servidor, num_primero, num_segundo, num_tercero, num_cuatro):
    conn = existe_bd()
    cursor = conn.cursor()
    instruccion = "INSERT INTO Servidor( nombre_servidor) VALUES ('" + nombre_servidor + "');"
    cursor.execute(instruccion)
    instruccion2 = "SELECT id_servidor FROM Servidor WHERE nombre_servidor = '" + nombre_servidor + "'"
    cursor.execute(instruccion2)
    datos = cursor.fetchall()
    instruccion3 = "INSERT INTO ip (primero,segundo,tercero,cuarto,Servidorid_servidor)VALUES('" + str(
        num_primero) + "','" + str(num_segundo) + "','" + str(num_tercero) + "','" + str(num_cuatro) + "'," + str(
        datos[0][
            0]) + ");"
    cursor.execute(instruccion3)
    conn.commit()
    conn.close()


def modificar_servidor_IP(nombre_servidor, num_primero, num_segundo, num_tercero, num_cuatro, id_servidor):
    conn = existe_bd()
    cursor = conn.cursor()
    instruccion = "UPDATE Servidor SET nombre_servidor = '" + nombre_servidor + "' WHERE id_servidor = " + str(
        id_servidor) + ";"
    cursor.execute(instruccion)
    instruccion2 = "DELETE FROM url WHERE Servidorid_servidor = " + str(id_servidor) + ";"
    cursor.execute(instruccion2)
    instruccion3 = "DELETE FROM ip WHERE Servidorid_servidor = " + str(id_servidor) + ";"
    cursor.execute(instruccion3)
    instruccion3 = "INSERT INTO ip (primero,segundo,tercero,cuarto,Servidorid_servidor)VALUES('" + str(
        num_primero) + "','" + str(num_segundo) + "','" + str(num_tercero) + "','" + str(num_cuatro) + "'," + str(
        id_servidor) + ");"
    cursor.execute(instruccion3)
    conn.commit()
    conn.close()


def insertar_servidor_URL(nombre_servidor, url):
    conn = existe_bd()
    cursor = conn.cursor()
    instruccion = "INSERT INTO Servidor( nombre_servidor) VALUES ('" + nombre_servidor + "');"
    cursor.execute(instruccion)
    instruccion2 = "SELECT id_servidor FROM Servidor WHERE nombre_servidor = '" + nombre_servidor + "'"
    cursor.execute(instruccion2)
    datos = cursor.fetchall()
    instruccion3 = "INSERT INTO url(direccion, Servidorid_servidor) VALUES ('" + url + "', " + str(datos[0][0]) + ");"
    cursor.execute(instruccion3)
    conn.commit()
    conn.close()


def modificar_servidor_URL(nombre_servidor, url, id_servidor):
    conn = existe_bd()
    cursor = conn.cursor()
    instruccion = "UPDATE Servidor SET nombre_servidor = '" + nombre_servidor + "' WHERE id_servidor = " + str(
        id_servidor) + ";"
    cursor.execute(instruccion)
    instruccion2 = "DELETE FROM url WHERE Servidorid_servidor = " + str(id_servidor) + ";"
    cursor.execute(instruccion2)
    instruccion3 = "DELETE FROM ip WHERE Servidorid_servidor = " + str(id_servidor) + ";"
    cursor.execute(instruccion3)
    instruccion3 = "INSERT INTO url(direccion, Servidorid_servidor) VALUES ('" + url + "', " + str(id_servidor) + ");"
    cursor.execute(instruccion3)
    conn.commit()
    conn.close()


def borrar_servidor(nombre_servidor):
    conn = existe_bd()
    cursor = conn.cursor()
    instruccion = "SELECT id_servidor FROM Servidor WHERE nombre_servidor = '" + nombre_servidor + "';"
    cursor.execute(instruccion)
    dato = cursor.fetchall()
    instruccion2 = "DELETE FROM Servidor WHERE nombre_servidor = '" + nombre_servidor + "';"
    cursor.execute(instruccion2)
    instruccion3 = "DELETE FROM url WHERE Servidorid_servidor = " + str(dato[0][0]) + ";"
    cursor.execute(instruccion3)
    instruccion4 = "DELETE FROM ip WHERE Servidorid_servidor = " + str(dato[0][0]) + ";"
    cursor.execute(instruccion4)
    conn.commit()
    conn.close()


def datos_servidor(nombre_servidor):
    conn = existe_bd()
    cursor = conn.cursor()
    id = obtener_id_servidor_sin_fallos(nombre_servidor)
    respuesta = {"id_servidor": id, "nombre_servidor": nombre_servidor}
    instruccion2 = "SELECT direccion FROM url WHERE Servidorid_servidor =" + str(id) + ";"
    cursor.execute(instruccion2)
    datos2 = cursor.fetchall()
    if len(datos2) > 0:
        respuesta["conexion"] = 0
        respuesta["direccion"] = datos2[0][0]
    else:
        instruccion3 = "SELECT primero, segundo, tercero, cuarto FROM ip WHERE Servidorid_servidor=" + str(id) + ";"
        cursor.execute(instruccion3)
        datos3 = cursor.fetchall()
        respuesta["conexion"] = 1
        respuesta["num1"] = datos3[0][0]
        respuesta["num2"] = datos3[0][1]
        respuesta["num3"] = datos3[0][2]
        respuesta["num4"] = datos3[0][3]
    conn.commit()
    conn.close()
    return respuesta


def obtener_direccion(nombre_servidor):
    conn = existe_bd()
    cursor = conn.cursor()
    id = obtener_id_servidor_sin_fallos(nombre_servidor)
    instruccion2 = "SELECT direccion FROM url WHERE Servidorid_servidor =" + str(id) + ";"
    cursor.execute(instruccion2)
    datos2 = cursor.fetchall()
    if len(datos2) > 0:
        respuesta = datos2[0][0]
    else:
        instruccion3 = "SELECT primero, segundo, tercero, cuarto FROM ip WHERE Servidorid_servidor=" + str(id) + ";"
        cursor.execute(instruccion3)
        datos3 = cursor.fetchall()
        respuesta = str(datos3[0][0]) + "." + str(datos3[0][1]) + "." + str(datos3[0][2]) + "." + str(datos3[0][3])
    conn.commit()
    conn.close()
    return respuesta


def obtener_id_servidor(nombre_servidor, exepto=0):
    conn = sql.connect(SERVIDOR)
    cursor = conn.cursor()
    instruccion = "SELECT id_servidor FROM Servidor WHERE nombre_servidor = '" + nombre_servidor + "'"
    if exepto != 0:
        instruccion = instruccion + " AND id_servidor != " + str(exepto) + ""
    instruccion = instruccion + ";"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.close()
    return datos


def obtener_id_servidor_sin_fallos(nombre_servidor):
    return obtener_id_servidor(nombre_servidor=nombre_servidor)[0][0]

# ----------EJEMPLOS------------------------------------------
# def createDB():
#     conn = sql.connect("bd_prueba.db")
#     conn.commit()
#     conn.close()
#
#
# def createTable():
#     conn = sql.connect("bd_prueba.db")
#     cursor = conn.cursor()
#     cursor.execute(
#         """"CREATE TABLE prueba (
#         name text,
#         followers integer,
#         subs integer
#         )"""
#     )
#     conn.commit()
#     conn.close()
#
#
# def insertRow():
#     conn = sql.connect("dataPings.db")
#     cursor = conn.cursor()
#     instruccion = f"INSERT INTO Servidor(id_servidor, nombre_servidor) VALUES (3, 'Prueba 1');"
#     cursor.execute(instruccion)
#     conn.commit()
#     conn.close()
#
#
# def readRows():
#     conn = sql.connect("dataPings.db")
#     cursor = conn.cursor()
#     instruccion = f"SELECT id_servidor, nombre_servidor FROM Servidor;"
#     cursor.execute(instruccion)
#     datos = cursor.fetchall()
#     conn.commit()
#     conn.close()
#     print(datos)
#
#
# if __name__ == "__main__":
#     # createDB()
#     # createTable()
#     # insertRow()
#     # readRows()
#     pass
