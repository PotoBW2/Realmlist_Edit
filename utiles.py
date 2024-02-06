import sys

import bdatos
import configparser
import os
import errno
import time
from ping3 import ping as pineador

# ---------------------VARIABLES----------------------------
ANCHO = 2
LARGO = 2
RUTA = "dataConfig"
ARCHIVO = RUTA + "/configuracion.ini"


# ----------------------------------------------------------

# ---------------BASE DE DATOS-----------------
def obtener_servidores():
    resultado = ()
    for servidor in bdatos.cargar_servidores():
        resultado = resultado + servidor
    return resultado


# ----------------------------------------------------------

# ---------------CONFIGURACION------------------------------
def existe_configuracion(objeto=None):
    if not os.path.exists(ARCHIVO):
        crear_configuracion()
        bdatos.existe_bd()
    elif objeto == None:
        guardar_configuracion_ini("servidor_actual", "localhost")
    if objeto != None:
        objeto.read(ARCHIVO)


def crear_configuracion():
    try:
        os.mkdir(RUTA)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    configuracion = configparser.ConfigParser()
    try:
        configuracion.add_section("CONFIGURACION")
    except configparser.DuplicateSectionError:
        pass
    configuracion.set("CONFIGURACION", "servidor_actual", "localhost")
    configuracion.set("CONFIGURACION", "regular_ping", "300")
    configuracion.set("CONFIGURACION", "mal_ping", "1000")
    configuracion.set("CONFIGURACION", "cantidad_pings", "60")
    with open(ARCHIVO, "w") as archivo_de_configuracion:
        configuracion.write(archivo_de_configuracion)


def guardar_configuracion_ini(key, valor):
    configuracion = configparser.ConfigParser()
    existe_configuracion(objeto=configuracion)
    try:
        configuracion.set("CONFIGURACION", key, valor)
        with open(ARCHIVO, "w") as archivo_de_configuracion:
            configuracion.write(archivo_de_configuracion)
    except:
        crear_configuracion()


def crear_obcion(key):
    configuracion = configparser.ConfigParser()
    existe_configuracion(objeto=configuracion)
    try:
        configuracion.set("CONFIGURACION", key, "")
        with open(ARCHIVO, "w") as archivo_de_configuracion:
            configuracion.write(archivo_de_configuracion)
    except configparser.NoSectionError:
        crear_configuracion()


def leer_configuracion(key):
    configuracion = configparser.ConfigParser()
    existe_configuracion(objeto=configuracion)
    try:
        value = configuracion.get("CONFIGURACION", key)
        return value
    except configparser.NoSectionError:
        crear_configuracion()
        return leer_configuracion(key)
    except configparser.NoOptionError:
        crear_obcion(key)
        return leer_configuracion(key)


def servidor_actual():
    return leer_configuracion("servidor_actual")


def regular_ping():
    return leer_configuracion("regular_ping")


def mal_ping():
    return leer_configuracion("mal_ping")


def cantidad_pings():
    return leer_configuracion("cantidad_pings")


# ----------------------------------------------------------

def cerrar_aplicacion(aplicacion):
    aplicacion.hilo = False
    aplicacion.destroy()


def redondear_o_Nulear(dato):
    if dato == None:
        return "---"
    else:
        return round(dato)


def reiniciar_pings(raiz, e):
    raiz.L_maximoping["text"] = "MAX: ---"
    raiz.L_minimoping["text"] = "MIN: ---"
    raiz.L_promedioping["text"] = "PROM: ---"
    raiz.L_perdidaping["text"] = "LOST: ---"
    raiz.F_cobertura.configure(style="Red.TFrame")
    raiz.nueva_direccion = True


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def pinear2(raiz, id):
    if raiz.tv_servidores.condicional:
        raiz.tv_servidores.set(id, 'MAX', str(maximo_ping(raiz.tv_servidores.hilos[id]["pings"])) + "ms")
        raiz.tv_servidores.set(id, 'MIN', str(minimo_ping(raiz.tv_servidores.hilos[id]["pings"])) + "ms")
        raiz.tv_servidores.set(id, 'PROM', str(promedio_ping(raiz.tv_servidores.hilos[id]["pings"])) + "ms")
        raiz.tv_servidores.set(id, 'LOST', str(perdida_ping(raiz.tv_servidores.hilos[id]["pings"])) + "%")


def calcular_ping2(raiz, id, nombre):
    while raiz.tv_servidores.condicional:
        direccion = bdatos.obtener_direccion(nombre)
        tiempo_de_espera = ping_en_profundidad(raiz.tv_servidores.hilos[id]["pings"], direccion)
        pinear2(raiz, id)
        eliminar_pings_vencidos(raiz.tv_servidores.hilos[id]["pings"])
        esperar(tiempo_de_espera)


def maximo_ping(list):
    MAX = None
    for pin in list:
        if pin != None:
            if MAX == None or MAX < pin:
                MAX = pin
    return redondear_o_Nulear(MAX)


def minimo_ping(list):
    MIN = None
    for pin in list:
        if pin != None:
            if MIN == None or MIN > pin:
                MIN = pin
    return redondear_o_Nulear(MIN)


def promedio_ping(list):
    suma_total = None
    conteo = 0
    for pin in list:
        if pin != None:
            if suma_total == None:
                suma_total = pin
            else:
                suma_total += pin
            conteo += 1
    if suma_total == None:
        return redondear_o_Nulear(None)
    else:
        return redondear_o_Nulear(suma_total / conteo)


def perdida_ping(list):
    suma_total = 0
    if len(list) != 0:
        for pin in list:
            if pin == None:
                suma_total += 1
        return redondear_o_Nulear(suma_total / len(list) * 100)
    return "---"


def ping_en_profundidad(list, direccion):
    inicio = time.time()
    try:
        ping = pineador(direccion, timeout=4)
    except:
        ping = False
    if type(ping) in (float, int):
        ping = ping * 1000
        lantencia = round(ping) / 1000
        tiempo_de_espera = 4 - lantencia
        list.append(ping)
    else:
        list.append(None)
        final = time.time()
        tiempo_de_espera = (4000 - (final - inicio)) / 1000
    return tiempo_de_espera




def eliminar_pings_vencidos(list):
    if len(list) > int(leer_configuracion("cantidad_pings")):
        list.pop(0)


def esperar(tiempo_de_espera):
    if tiempo_de_espera > 0:
        time.sleep(tiempo_de_espera)
