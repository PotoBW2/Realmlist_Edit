import threading
from threading import *

from crud_servidor import *
from configure_pings import *
from servers import *
import time
from ping3 import ping as pineador
import os

raiz = Tk()
raiz.title("RealmlistWoW Editor v1.01")
raiz.resizable(False, False)
raiz.iconbitmap(resource_path("imagenes/logo.ico"))

# ------------------ESTILOS--------------------
s = ttk.Style()
s.configure("Green.TFrame", background="green")
s.configure("Orange.TFrame", background="orange")
s.configure("Red.TFrame", background="red")


# ----------------------------------------------
def activar_servidor(objeto):
    if os.path.exists('realmlist.wtf'):
        realmlist = open('realmlist.wtf', 'w')
        datos = datos_servidor(objeto.servidor.get())
        if datos["conexion"] == 0:
            realmlist.write('set realmlist ' + datos["direccion"])
        else:
            realmlist.write(
                'set realmlist ' + str(datos["num1"]) + "." + str(datos["num2"]) + "." + str(datos["num3"]) + "." + str(
                    datos["num4"]) + ".")
        realmlist.close()
        guardar_configuracion_ini("servidor_actual", objeto.servidor.get())
        cerrar_aplicacion(aplicacion=objeto)
    else:
        objeto.state("withdrawn")
        mensaje = messagebox.showerror(title="ERROR",
                                       message='No se encuentra el archivo "realmlist.wtf" asegurese de que el software este copiado en la raiz del WoW.')
        if mensaje == "ok":
            objeto.state(NORMAL)


# ----------------------------VARIABLES------------------------------------------
tupla_servidores = obtener_servidores()
raiz.servidor = StringVar()
raiz.servidor.set(servidor_actual())
raiz.hilo = True
raiz.nueva_direccion = False
raiz.pines = []


# -------------------------------------------------------------------------------
# -----------------------------------HILO----------------------------------------
def pinear(raiz):
    if not raiz.nueva_direccion:
        raiz.L_maximoping["text"] = "MAX: " + str(redondear_o_Nulear(maximo_ping())) + "ms"
        raiz.L_minimoping["text"] = "MIN: " + str(redondear_o_Nulear(minimo_ping())) + "ms"
        promedio = promedio_ping()
        raiz.L_promedioping["text"] = "PROM: " + str(redondear_o_Nulear(promedio)) + "ms"
        raiz.L_perdidaping["text"] = "LOST: " + str(perdida_ping()) + "%"
        if promedio != None and promedio < int(regular_ping()):
            raiz.F_cobertura.configure(style="Green.TFrame")
        elif promedio != None and promedio < int(mal_ping()):
            raiz.F_cobertura.configure(style="Orange.TFrame")
        else:
            raiz.F_cobertura.configure(style="Red.TFrame")
    raiz.nueva_direccion = False


def calcular_ping(raiz):
    while raiz.hilo:
        direccion = obtener_direccion(raiz.servidor.get())
        inicio = time.time()
        servidor = raiz.servidor.get()
        ping = pineador(direccion)
        final = time.time()
        if type(ping) in (float, int):
            ping = ping * 1000
            lantencia = round(ping) / 1000
            tiempo_de_espera = 1 - lantencia
            guardar_ping(nombre_servidor=servidor, latencia=ping)
            if tiempo_de_espera > 0:
                time.sleep(tiempo_de_espera)
        else:
            tiempo_de_espera = (1000 - (final - inicio)) / 1000
            guardar_ping(nombre_servidor=servidor)
            if tiempo_de_espera > 0:
                time.sleep(tiempo_de_espera)
        pinear(raiz)


pineaje = threading.Thread(name="pineaje", target=lambda: calcular_ping(raiz), daemon=True)
pineaje.start()
raiz.protocol("WM_DELETE_WINDOW", lambda: cerrar_aplicacion(raiz))
# -------------------------------------------------------------------------------

f_principal = ttk.Frame(raiz, padding=10, )
f_principal.grid()

# ----------------------------SERVIDOR--------------------------------------------
f_servidor = ttk.Frame(f_principal, padding=10, )
f_servidor.grid(column=0, row=0)
raiz.E_servidores = ttk.Entry(f_servidor, textvariable=raiz.servidor, width=20, state="readonly")
raiz.E_servidores.grid(column=0, row=0)
raiz.E_servidores.bind("<ButtonPress-1>", lambda e: ventana_servers(e, padre=raiz))
ttk.Button(f_servidor, text="Editar",
           command=lambda: ventana_editar_servidor(padre=raiz, nombre_servidor=raiz.servidor.get())).grid(column=2,
                                                                                                          row=0)
ttk.Button(f_servidor, text="Eliminar", command=lambda: eliminar_servidor(raiz, raiz.servidor.get())).grid(column=3,
                                                                                                           row=0)
b_agregar = ttk.Button(f_servidor, text="Agregar",
                       command=lambda: ventana_agregar_servidor(padre=raiz, nombre_servidor=""))
b_agregar.grid(column=4, row=0)
# ---------------------------------------------------------------------------------
# ----------------------------LATENCIA--------------------------------------------
frm_latencia = ttk.Frame(f_principal, padding=10, )
frm_latencia.grid(column=0, row=1, sticky=(W, E))
frm_latencia.columnconfigure(0, weight=1)
frm_latencia.columnconfigure(1, weight=1)
frm_latencia.columnconfigure(2, weight=1)
frm_latencia.columnconfigure(3, weight=1)
frm_latencia.columnconfigure(4, weight=1)
frm_latencia.columnconfigure(5, weight=1)
raiz.L_minimoping = ttk.Label(frm_latencia, text="MIN: ---", foreground="green")
raiz.L_minimoping.grid(column=3, row=0, )
raiz.L_maximoping = ttk.Label(frm_latencia, text="MAX: ---", foreground="orange")
raiz.L_maximoping.grid(column=2, row=0, )
raiz.L_perdidaping = ttk.Label(frm_latencia, text="LOST: ---", foreground="red")
raiz.L_perdidaping.grid(column=4, row=0, )
raiz.L_promedioping = ttk.Label(frm_latencia, text="PROM: ---", foreground="blue")
raiz.L_promedioping.grid(column=1, row=0, )
raiz.F_cobertura = ttk.Frame(frm_latencia, style="Red.TFrame", width=21, height=21, relief="groove")
raiz.F_cobertura.grid(column=0, row=0, )
ttk.Button(frm_latencia, text="Configurar", command=lambda: ventana_configurar_pings(raiz)).grid(column=5, row=0,
                                                                                                 sticky=(E), )
# ---------------------------------------------------------------------------------
ttk.Separator(f_principal, orient=HORIZONTAL).grid(column=0, row=2, sticky="EW")
# ----------------------------CONTROLES--------------------------------------------
frm_controles = ttk.Frame(f_principal, padding=10, )
frm_controles.grid(column=0, row=3, sticky=(E))
ttk.Button(frm_controles, text="Prueba", command=lambda: ventana_servers(padre=raiz)).grid(column=3, row=0, )
ttk.Button(frm_controles, text="Aceptar", command=lambda: activar_servidor(raiz)).grid(column=0, row=0, )
ttk.Button(frm_controles, text="Cancelar",
           command=lambda: cerrar_aplicacion(aplicacion=raiz)
           ).grid(column=1, row=0, )
# ---------------------------------------------------------------------------------
# ------------------------------------EVENTOS--------------------------------------
# ---------------------------------------------------------------------------------
raiz.update()
raiz.geometry("+" + str(round(raiz.winfo_screenwidth() / 2 - raiz.winfo_reqwidth() / 2)) + "+" + str(
    round(raiz.winfo_screenheight() / 2 - raiz.winfo_reqheight() / 2)))
raiz.update()

raiz.mainloop()
