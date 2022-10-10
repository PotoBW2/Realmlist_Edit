from tkinter import *
from tkinter import ttk
from re import split
from utiles import *


def cerrar_ventana_configuracion(padre, hijo):
    padre.state(NORMAL)
    padre.attributes("-topmost", 1)
    hijo.destroy()


def cambiar_rango(objeto):
    minimo = objeto.regular.get() + 1
    objeto.S_malping["from_"] = minimo
    if objeto.mal.get() <= minimo:
        objeto.mal.set(minimo)


def guardar_configuracion(padre, objeto):
    guardar_configuracion_ini("regular_ping", str(objeto.regular.get()))
    guardar_configuracion_ini("mal_ping", str(objeto.mal.get()))
    guardar_configuracion_ini("cantidad_pings", str(objeto.cantidad.get()))
    cerrar_ventana_configuracion(padre, objeto)


def ventana_configurar_pings(padre):
    padre.state("withdrawn")
    TL_configuracion = Toplevel(padre, padx=10, pady=10)
    TL_configuracion.resizable(False, False)
    TL_configuracion.attributes("-topmost", 1)
    TL_configuracion.iconbitmap(resource_path("imagenes/logo.ico"))
    TL_configuracion.protocol("WM_DELETE_WINDOW", (lambda: cerrar_ventana_configuracion(padre, TL_configuracion)))
    position = split("\+", str(padre.winfo_geometry()))
    position.pop(0)
    TL_configuracion.geometry("+" + str(int(position[0]) + 50) + "+" + str(int(position[1]) + 50))
    # ----------------------------------------------------VARIABLES-----------------------------------------------------
    TL_configuracion.regular = IntVar(value=regular_ping())
    TL_configuracion.mal = IntVar(value=mal_ping())
    TL_configuracion.cantidad = IntVar(value=cantidad_pings())
    # -----------------------------------------------------VISUAL-------------------------------------------------------
    ttk.Label(TL_configuracion, text="Latencia regular:").grid(column=0, row=0, pady=2)
    ttk.Spinbox(TL_configuracion, from_=1, to=4999, textvariable=TL_configuracion.regular, width=5,
                command=lambda: cambiar_rango(TL_configuracion)).grid(column=1, row=0, pady=2)
    ttk.Label(TL_configuracion, text="Latencia mala:").grid(column=0, row=1, pady=2)
    TL_configuracion.S_malping = ttk.Spinbox(TL_configuracion, from_=TL_configuracion.regular.get() + 1, to=5000,
                                             textvariable=TL_configuracion.mal, width=5)
    TL_configuracion.S_malping.grid(column=1, row=1, pady=2)
    ttk.Label(TL_configuracion, text="Cantidad de pings a guardar:").grid(column=0, row=2, pady=2)
    ttk.Spinbox(TL_configuracion, from_=60, to=600, textvariable=TL_configuracion.cantidad, width=5).grid(column=1, row=2,
                                                                                                     pady=2)
    # ------------------------------------------------------------------------------------------------------------------
    ttk.Separator(TL_configuracion, orient=HORIZONTAL).grid(column=0, row=3, sticky="EW", columnspan=2, pady=5)
    # --------------------------------------------------CONTROLES-------------------------------------------------------
    F_controles = ttk.Frame(TL_configuracion)
    F_controles.grid(column=0, row=4, columnspan=2, sticky=(E))
    ttk.Button(F_controles, text="Aceptar", command=lambda: guardar_configuracion(padre, TL_configuracion)).grid(
        column=0, row=0)
    ttk.Button(F_controles, text="Cancelar",
               command=(lambda: cerrar_ventana_configuracion(padre, TL_configuracion))).grid(column=1, row=0)
    # ------------------------------------------------------------------------------------------------------------------
