from tkinter import *
from tkinter import ttk
from utiles import *
from bdatos import *
from re import split
import threading
from threading import *


def cerrar_ventana_configuracion(padre, hijo):
    padre.state(NORMAL)
    padre.attributes("-topmost", 1)
    hijo.tv_servidores.condicional = False
    hijo.destroy()


def cambiar_servidor_principal(raiz, e, padre):
    padre.servidor.set(raiz.tv_servidores.item(raiz.tv_servidores.focus())["values"][0])
    padre.L_maximoping["text"] = "MAX: ---"
    padre.L_minimoping["text"] = "MIN: ---"
    padre.L_promedioping["text"] = "PROM: ---"
    padre.L_perdidaping["text"] = "LOST: ---"
    padre.F_cobertura.configure(style="Red.TFrame")
    padre.nueva_direccion = True
    padre.ping_actual = []
    cerrar_ventana_configuracion(padre, raiz)


def ventana_servers(e, padre):
    padre.state("withdrawn")
    TL_servidores = Toplevel(padre, padx=10, pady=10)
    TL_servidores.resizable(False, False)
    TL_servidores.attributes("-topmost", 1)
    TL_servidores.iconbitmap(resource_path("imagenes/logo.ico"))
    TL_servidores.protocol("WM_DELETE_WINDOW", (lambda: cerrar_ventana_configuracion(padre, TL_servidores)))

    TL_servidores.tv_servidores = ttk.Treeview(TL_servidores, columns=("name", 'PROM', 'MAX', 'MIN', 'LOST'))
    TL_servidores.tv_servidores.grid(column=0, row=0)
    TL_servidores.tv_servidores.heading('name', text='Nombre')
    TL_servidores.tv_servidores.heading('PROM', text='Promedio')
    TL_servidores.tv_servidores.heading('MAX', text='Máximo')
    TL_servidores.tv_servidores.heading('MIN', text="Mínimo")
    TL_servidores.tv_servidores.heading('LOST', text="Pérdida")
    TL_servidores.tv_servidores.column('#0', width=35, )
    TL_servidores.tv_servidores.column('name', width=100)
    TL_servidores.tv_servidores.column('PROM', width=60)
    TL_servidores.tv_servidores.column('MAX', width=55)
    TL_servidores.tv_servidores.column('MIN', width=50)
    TL_servidores.tv_servidores.column('LOST', width=50)

    TL_servidores.tv_servidores.hilos = {}
    TL_servidores.tv_servidores.condicional = True

    for elem in cargar_servidores2():
        TL_servidores.tv_servidores.insert('', 'end', str(elem[0]), text=str(elem[0]),
                                           values=(elem[1], "---", "---", "---", "---"))
        TL_servidores.tv_servidores.hilos[str(elem[0])] = {}
        TL_servidores.tv_servidores.hilos[str(elem[0])]["pings"] = []
        TL_servidores.tv_servidores.hilos[str(elem[0])]["hilo"] = threading.Thread(name="pineaje",
                                                                                   target=lambda: calcular_ping2(
                                                                                       TL_servidores,
                                                                                       str(elem[0]), elem[1]),

                                                                                   daemon=True)
        TL_servidores.tv_servidores.hilos[str(elem[0])]["hilo"].start()
    TL_servidores.tv_servidores.bind("<<TreeviewSelect>>",
                                     lambda e: cambiar_servidor_principal(TL_servidores, e, padre=padre))

    position = split("\+", str(padre.winfo_geometry()))
    position.pop(0)
    TL_servidores.geometry("+" + str(int(position[0]) + 25) + "+" + str(int(position[1]) - 50))
