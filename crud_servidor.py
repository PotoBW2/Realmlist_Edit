from tkinter import *
from tkinter import ttk
from re import split
from bdatos import *
from tkinter import messagebox
from utiles import obtener_servidores, resource_path


def desactivar_conexion(objeto):
    if objeto.CONEXION.get() == 0:
        objeto.SB_numero1["state"] = DISABLED
        objeto.SB_numero2["state"] = DISABLED
        objeto.SB_numero3["state"] = DISABLED
        objeto.SB_numero4["state"] = DISABLED

        objeto.E_url["state"] = NORMAL
    else:
        objeto.E_url["state"] = "readonly"

        objeto.SB_numero1["state"] = NORMAL
        objeto.SB_numero2["state"] = NORMAL
        objeto.SB_numero3["state"] = NORMAL
        objeto.SB_numero4["state"] = NORMAL


def agregar_editar_servidor(padre, objeto, metodo=1, id_servidor=0):
    nombre_servidor = objeto.NOMBRE_SEVIDOR.get()
    if nombre_servidor != "":
        if existe_servidor_nombre(nombre_servidor, id_servidor):
            objeto.state("withdrawn")
            mensaje = messagebox.showerror(title="ERROR", message="El Servidor '" + nombre_servidor + "' ya existe.")
            if mensaje == "ok":
                objeto.state(NORMAL)
        else:
            objeto.CONEXION.get()
            if objeto.CONEXION.get() == 1:
                num_primero = objeto.NUMERO1.get()
                num_segundo = objeto.NUMERO2.get()
                num_tercero = objeto.NUMERO3.get()
                num_cuarto = objeto.NUMERO4.get()
                if existe_servidor_ip(num_primero, num_segundo, num_tercero, num_cuarto, id_servidor):
                    objeto.state("withdrawn")
                    mensaje = messagebox.showerror(title="ERROR",
                                                   message="El IP  '" + str(num_primero) + "." + str(
                                                       num_segundo) + "." + str(num_tercero) + "." + str(
                                                       num_cuarto) + "'  ya existe.")
                    if mensaje == "ok":
                        objeto.state(NORMAL)
                else:
                    if metodo == 1:
                        insertar_servidor_IP(nombre_servidor, num_primero, num_segundo, num_tercero, num_cuarto)
                    else:
                        modificar_servidor_IP(nombre_servidor, num_primero, num_segundo, num_tercero, num_cuarto,
                                              id_servidor)
                    cerrar_ventana_agregar_servidor(padre, objeto, nombre_servidor)
            else:
                url = objeto.URL.get()
                if url != "":
                    if existe_servidor_url(url, id_servidor):
                        objeto.state("withdrawn")
                        mensaje = messagebox.showerror(title="ERROR",
                                                       message="La dirección '" + url + "' ya existe.")
                        if mensaje == "ok":
                            objeto.state(NORMAL)
                    else:
                        if metodo == 1:
                            insertar_servidor_URL(nombre_servidor, url)
                        else:
                            modificar_servidor_URL(nombre_servidor, url, id_servidor)
                        cerrar_ventana_agregar_servidor(padre, objeto, nombre_servidor)
                else:
                    objeto.state("withdrawn")
                    mensaje = messagebox.showerror(title="ERROR", message="Inserte una dirección")
                    if mensaje == "ok":
                        objeto.state(NORMAL)
    else:
        objeto.state("withdrawn")
        mensaje = messagebox.showerror(title="ERROR", message="Inserte un nombre para el servidor")
        if mensaje == "ok":
            objeto.state(NORMAL)


def cerrar_ventana_agregar_servidor(padre, hijo, nombre_servidor=None):
    padre.state(NORMAL)
    padre.attributes("-topmost", 1)
    hijo.destroy()
    if nombre_servidor != None:
        padre.servidor.set(nombre_servidor)


def minusculas_letras(e, objeto):
    objeto.URL.set(objeto.URL.get().lower())


def ventana_agregar_servidor(padre, nombre_servidor="", conexion=1, num1=192, num2=168, num3=1, num4=0, url="",
                             metodo=1, id_servidor=0):
    padre.state("withdrawn")
    TLAgregarServidor = Toplevel(padre, padx=10, pady=10)
    TLAgregarServidor.resizable(False, False)
    TLAgregarServidor.attributes("-topmost", 1)
    TLAgregarServidor.iconbitmap(resource_path("imagenes/logo.ico"))
    TLAgregarServidor.protocol("WM_DELETE_WINDOW", (lambda: cerrar_ventana_agregar_servidor(padre, TLAgregarServidor)))
    position = split("\+", str(padre.winfo_geometry()))
    position.pop(0)
    TLAgregarServidor.geometry("+" + str(int(position[0]) + 50) + "+" + str(int(position[1]) + 50))
    # ----------------------------------------------------VARIABLES-----------------------------------------------------
    TLAgregarServidor.NOMBRE_SEVIDOR = StringVar(value=nombre_servidor)
    TLAgregarServidor.CONEXION = IntVar(value=conexion)
    TLAgregarServidor.NUMERO1 = IntVar(value=num1)
    TLAgregarServidor.NUMERO2 = IntVar(value=num2)
    TLAgregarServidor.NUMERO3 = IntVar(value=num3)
    TLAgregarServidor.NUMERO4 = IntVar(value=num4)
    TLAgregarServidor.URL = StringVar(value=url)
    # ----------------------------------------------------NOMBRE--------------------------------------------------------
    ttk.Label(TLAgregarServidor, text="Nombre del servidor:").grid(column=0, row=0, pady=2)
    TLAgregarServidor.nombre_servidor = ttk.Entry(TLAgregarServidor, textvariable=TLAgregarServidor.NOMBRE_SEVIDOR)
    TLAgregarServidor.nombre_servidor.grid(column=1, row=0, pady=2 ,sticky=(W,E))
    # ------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------CONEXION------------------------------------------------------
    ttk.Label(TLAgregarServidor, text="Tipo de conexión:").grid(column=0, row=1, pady=2)
    F_conexion = ttk.Frame(TLAgregarServidor)
    F_conexion.grid(column=1, row=1, pady=2)
    RB_ip = ttk.Radiobutton(F_conexion, text='IP', variable=TLAgregarServidor.CONEXION, value=1,
                            command=lambda: desactivar_conexion(TLAgregarServidor))
    RB_url = ttk.Radiobutton(F_conexion, text='URL', variable=TLAgregarServidor.CONEXION, value=0,
                             command=lambda: desactivar_conexion(TLAgregarServidor))
    RB_ip.grid(column=0, row=0, pady=2)
    RB_url.grid(column=1, row=0, pady=2)
    # ------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------IP------------------------------------------------------------
    ttk.Label(TLAgregarServidor, text="IP:").grid(column=0, row=2, pady=2)
    F_ip = ttk.Frame(TLAgregarServidor)
    F_ip.grid(column=1, row=2, pady=2)
    TLAgregarServidor.SB_numero1 = ttk.Spinbox(F_ip, from_=1, to=255, textvariable=TLAgregarServidor.NUMERO1, width=4)
    TLAgregarServidor.SB_numero1.grid(column=0, row=0, pady=2)
    ttk.Label(F_ip, text=".").grid(column=1, row=0, pady=2)
    TLAgregarServidor.SB_numero2 = ttk.Spinbox(F_ip, from_=0, to=255, textvariable=TLAgregarServidor.NUMERO2, width=4)
    TLAgregarServidor.SB_numero2.grid(column=2, row=0, pady=2)
    ttk.Label(F_ip, text=".").grid(column=3, row=0, pady=2)
    TLAgregarServidor.SB_numero3 = ttk.Spinbox(F_ip, from_=0, to=255, textvariable=TLAgregarServidor.NUMERO3, width=4)
    TLAgregarServidor.SB_numero3.grid(column=4, row=0, pady=2)
    ttk.Label(F_ip, text=".").grid(column=5, row=0, pady=2)
    TLAgregarServidor.SB_numero4 = ttk.Spinbox(F_ip, from_=0, to=255, textvariable=TLAgregarServidor.NUMERO4, width=4)
    TLAgregarServidor.SB_numero4.grid(column=6, row=0, pady=2)
    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------URL------------------------------------------------------------
    ttk.Label(TLAgregarServidor, text="Dirección:").grid(column=0, row=3, pady=2)
    TLAgregarServidor.E_url = ttk.Entry(TLAgregarServidor, textvariable=TLAgregarServidor.URL)
    TLAgregarServidor.E_url.grid(column=1, row=3, pady=2,sticky=(W,E))
    TLAgregarServidor.E_url.bind("<KeyRelease>", lambda e: minusculas_letras(e, TLAgregarServidor))
    # ------------------------------------------------------------------------------------------------------------------
    ttk.Separator(TLAgregarServidor, orient=HORIZONTAL).grid(column=0, row=4, sticky="EW", columnspan=2, pady=5)
    # --------------------------------------------------CONTROLES-------------------------------------------------------
    F_controles = ttk.Frame(TLAgregarServidor)
    F_controles.grid(column=0, row=5, columnspan=2, sticky=(E))
    if metodo == 1:
        titulo = "Agregar"
    else:
        titulo = "Editar"
    ttk.Button(F_controles, text=titulo,
               command=lambda: agregar_editar_servidor(padre=padre, objeto=TLAgregarServidor, metodo=metodo,
                                                       id_servidor=id_servidor)).grid(column=0, row=0)
    ttk.Button(F_controles, text="Cancelar",
               command=(lambda: cerrar_ventana_agregar_servidor(padre, TLAgregarServidor))).grid(column=1, row=0)
    # ------------------------------------------------------------------------------------------------------------------
    desactivar_conexion(objeto=TLAgregarServidor)


def ventana_editar_servidor(padre, nombre_servidor):
    servidor = datos_servidor(nombre_servidor)
    if servidor["conexion"] == 1:
        ventana_agregar_servidor(padre=padre, nombre_servidor=servidor["nombre_servidor"],
                                 conexion=servidor["conexion"], num1=servidor["num1"], num2=servidor["num2"],
                                 num3=servidor["num3"], num4=servidor["num4"], metodo=0,
                                 id_servidor=servidor["id_servidor"])
    else:
        ventana_agregar_servidor(padre=padre, nombre_servidor=servidor["nombre_servidor"],
                                 conexion=servidor["conexion"], url=servidor["direccion"], metodo=0,
                                 id_servidor=servidor["id_servidor"])


def eliminar_servidor(padre, nombre_servidor):
    padre.state("withdrawn")
    respuesta = messagebox.askyesno(message="¿Desea realmente eliminar el servidor '" + nombre_servidor + "'?",
                                    title='Borrar servidor')
    if respuesta:
        borrar_servidor(nombre_servidor)
        lista_de_servidores = obtener_servidores()
        padre.servidor.set(lista_de_servidores[0])
    padre.state(NORMAL)
    padre.attributes("-topmost", 1)
