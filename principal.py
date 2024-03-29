import threading
from threading import *

from crud_servidor import *
from configure_pings import *
from servers import *
import time
from ping3 import ping as pineador
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

raiz = Tk()
raiz.title("RealmlistWoW Editor v1.07")
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
                    datos["num4"]))
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
raiz.ping_actual = []
raiz.ping_max = []
raiz.ping_min = []
raiz.ping_prom = []
raiz.ping_loss = []
fig = plt.figure(figsize=(3.8, 2.2))
ax = fig.add_subplot()


# -------------------------------------------------------------------------------
# -----------------------------------HILO----------------------------------------
def pinear(raiz):
    if not raiz.nueva_direccion:
        raiz.L_maximoping["text"] = "MAX: " + str(maximo_ping(raiz.ping_actual)) + "ms"
        raiz.L_minimoping["text"] = "MIN: " + str(minimo_ping(raiz.ping_actual)) + "ms"
        promedio = promedio_ping(raiz.ping_actual)
        raiz.L_promedioping["text"] = "PROM: " + str(promedio) + "ms"
        raiz.L_perdidaping["text"] = "LOST: " + str(perdida_ping(raiz.ping_actual)) + "%"
        if promedio != "---" and promedio < int(regular_ping()):
            raiz.F_cobertura.configure(style="Green.TFrame")
        elif promedio != "---" and promedio < int(mal_ping()):
            raiz.F_cobertura.configure(style="Orange.TFrame")
        else:
            raiz.F_cobertura.configure(style="Red.TFrame")
        list1 = list(range(len(raiz.ping_actual)))
        list2 = [0 if x == None else x for x in raiz.ping_actual]
        eje_y = max_eje_y(raiz)
        plt.ylim(-10, eje_y)
        ax.grid(True)
        line2, = ax.plot(list(range(len(raiz.ping_max))), raiz.ping_max, color='y')
        line3, = ax.plot(list(range(len(raiz.ping_min))), raiz.ping_min, color='b')
        line5, = ax.plot(list(range(len(raiz.ping_loss))), [x*eje_y/100 for x in raiz.ping_loss], color='r')
        line, = ax.plot(list(range(len(raiz.ping_prom))), raiz.ping_prom, color='g')
        line4, = ax.plot(list1, list2, color='purple')
        raiz.canvas.draw()
        line.set_ydata([0])
        line.set_xdata([0])
        line2.set_ydata([0])
        line2.set_xdata([0])
        line3.set_ydata([0])
        line3.set_xdata([0])
        line4.set_ydata([0])
        line4.set_xdata([0])
        line5.set_ydata([0])
        line5.set_xdata([0])

    raiz.nueva_direccion = False


def calcular_ping(raiz):
    while raiz.hilo:
        direccion = obtener_direccion(raiz.servidor.get())
        tiempo_de_espera = ping_en_profundidad(raiz.ping_actual, direccion)
        inicio = time.time()
        obtener_max(raiz)
        obtener_min(raiz)
        obtener_prom(raiz)
        obtener_loss(raiz)
        pinear(raiz)
        final = time.time()
        tiempo_de_espera = tiempo_de_espera - (final - inicio)
        esperar(tiempo_de_espera)


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
raiz.L_minimoping = ttk.Label(frm_latencia, text="MIN: ---", foreground="blue")
raiz.L_minimoping.grid(column=3, row=0, )
raiz.L_maximoping = ttk.Label(frm_latencia, text="MAX: ---", foreground="orange")
raiz.L_maximoping.grid(column=2, row=0, )
raiz.L_perdidaping = ttk.Label(frm_latencia, text="LOST: ---", foreground="red")
raiz.L_perdidaping.grid(column=4, row=0, )
raiz.L_promedioping = ttk.Label(frm_latencia, text="PROM: ---", foreground="green")
raiz.L_promedioping.grid(column=1, row=0, )
raiz.F_cobertura = ttk.Frame(frm_latencia, style="Red.TFrame", width=21, height=21, relief="groove")
raiz.F_cobertura.grid(column=0, row=0, )
ttk.Button(frm_latencia, text="Configurar", command=lambda: ventana_configurar_pings(raiz)).grid(column=5, row=0,
                                                                                                 sticky=(E), )
# ---------------------------------------------------------------------------------
ttk.Separator(f_principal, orient=HORIZONTAL).grid(column=0, row=2, sticky="EW")
# ----------------------------GRAFICA----------------------------------------------
raiz.canvas = FigureCanvasTkAgg(fig, master=f_principal)
raiz.canvas.get_tk_widget().grid(column=0, row=3)
# ---------------------------------------------------------------------------------
ttk.Separator(f_principal, orient=HORIZONTAL).grid(column=0, row=4, sticky="EW")
# ----------------------------CONTROLES--------------------------------------------
frm_controles = ttk.Frame(f_principal, padding=10, )
frm_controles.grid(column=0, row=5, sticky=(E))
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
