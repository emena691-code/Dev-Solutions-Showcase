import time
import datetime
from plyer import notification
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import messagebox

color = '#2d486f'

# APP - Control de inventario, ciclos y objetivos "CICO"

fh = time.localtime() # Llama fecha hoy a "fh"

def notificacion(notifi_type):
    notification.notify(
        title = "Alerta CICO",
        message = notifi_type,
        app_name = "Ci-App",
        timeout = 5
        )

# CI Control de inventario 
# (Detecta cuándo los insumos están por debajo de cierto umbral.)

def CI(nombre, inv_p):

    if inv_p <= 0:
        categoria = f"{nombre} esta agotado"
        notificacion(f"{categoria} Stock: {inv_p}") # Notificaciones del sistema
    elif inv_p == 1:
        entradas_vis("No hay stock o alarma de stock")
    elif inv_p <= 7:
        categoria = f"{nombre} esta peligrosamente bajo"
        notificacion(f"{categoria} Stock: {inv_p}") # Notificaciones del sistema
    elif inv_p <= 15:
        categoria = f"{nombre} se esta acabando"
        notificacion(f"{categoria} Stock: {inv_p}") # Notificaciones del sistema
    elif inv_p >= 16:
        categoria = f"Aun hay buen Stock de {nombre}"
        notificacion(f"{categoria} Stock: {inv_p}")
    else:
        entradas_vis(f"{nombre} la celda seleccionada no aplica para anlizar")

# ACC Analizador de ciclos de compra
def ACC(y, m, d, nombre, tiempoDcom):
    fc = datetime.datetime(year=y, month=m, day=d) #Convierte fecha de compra en formato fecha
    entradas_vis(f"la fecha de compra es {fc}")

    fx = datetime.datetime(year=fh[0], month=fh[1], day=fh[2]) #Compone "fh" en "fx" como formato de fecha
    entradas_vis(f"La fecha de hoy es {fx}")

#Analiza diferencia de variables "fh" fecha hoy, "d" dia de compra, "m" mes
    analizadorDmes = fh[1] - m
    if d < fh[2]:
        cate_ana = fh[2] - d
    elif d > fh[2]:    
        cate_ana = d - fh[2]

#Convierte analizador de categoria a varaible "analizadorDdia"
    analizadorDdia = cate_ana

    entradas_vis(f"la diferencia de datos es de {analizadorDmes} mes(es) y {analizadorDdia} dia(s)")
    
    #definir tiempo de recompra de x produto y alerta de compra antes de 2 meses
    if tiempoDcom == 0:
        alertTDcom = 0
    elif tiempoDcom >= 4:
        alertTDcom = tiempoDcom - 2
    elif tiempoDcom <= 4:
        alertTDcom = 100
    else:
        alertTDcom = 0
#Analiza "anlizadorDmes" y "analizadorDdia"
    if tiempoDcom == 0:
        entradas_vis("N/A ciclo de compra")
    elif fc == fx:
        entradas_vis("No ha pasado tiempo desde la compra")
    elif analizadorDdia < 30 and analizadorDmes == 0:
        entradas_vis(f"{nombre} esta en los primeros 30 dias desde su compra: {analizadorDdia} dia(s)")
    elif analizadorDmes == 1:
        entradas_vis(f"Ha pasado un mes desde la compra de {nombre}")
    elif analizadorDmes == 2:
        entradas_vis(f"Ha pasado dos meses desde la compra de {nombre}")
    elif analizadorDmes == alertTDcom:
        entradas_vis(f"Faltan 2 meses para comprar {nombre}")
    elif analizadorDmes == tiempoDcom:
        entradas_vis(f"La fecha de compra de {nombre} paso hace {analizadorDdia} dia(s)")
        notificacion(f"Se necesita comprar {nombre}, retraso: {analizadorDdia} dias(s)")
    elif analizadorDmes >= tiempoDcom:
        M_pasado = analizadorDmes - tiempoDcom
        entradas_vis(f"La fecha de compra de {nombre} paso hace {M_pasado} meses {analizadorDdia} dia(s)")
        notificacion(f"Se necesita comprar {nombre}, retraso: {M_pasado} meses {analizadorDdia} dias(s)")
    else:
        entradas_vis(f"Fecha de renovacion de {nombre} esta fuera de rango")

#Analizador de objetivo financiero "AOF"
def AOF(dinero_actual, Objetivo):
    Sem_T = int(fh[7] / 7)
    entradas_vis(f"Van pasando {Sem_T} semanas del año")
    Falt_Sem = int(52 - Sem_T)
    Falt_Mes = int(12 - fh[1])
    entradas_vis(f"Faltan {Falt_Sem} semanas para acabar el año")

    objeAnu = int(Objetivo - dinero_actual) 
    objeMen = int(objeAnu / Falt_Mes)
    objeSem = int(objeAnu / Falt_Sem)
    falt = f"Falta ${objeAnu} para completar el objetivo"
    notificacion(falt)
    entradas_vis(falt)

    #Regla de 3 para porcentaje %
    multi_D = dinero_actual * 100
    porcen_Anu = int(multi_D / objeAnu)
    porcen_Mes = int(multi_D / objeMen)
    porcen_Sem = int(multi_D / objeSem)
    if porcen_Anu <= 100:
        entradas_vis(f"Tu capital es el {porcen_Anu}% de tu objetivo anual: ${objeAnu}")
    else:
        notificacion("Objetivo Anual alcanzado")
    if porcen_Mes <= 100:
        entradas_vis(f"Tu capital es el {porcen_Mes}% de tu objetivo mensual: ${objeMen}")
    else:
        notificacion("Objetivo Mensual alcanzado")
    if porcen_Sem <= 100:
        entradas_vis(f"Tu capital es el {porcen_Sem}% de tu objetivo semanal: ${objeSem}")
    else:
        notificacion("Objetivo Semanal alcanzado")

# PI Promociones inteligentes 
# (finanzas bajas y lanza promociones)
#Hacer un analizador de faltante para obetivo anual y mes actual (asi definir malas finanzas)

def PI(capital_act, objetivo_anu):
    
    Sem_Año = int(fh[7] / 7)
    falt_Sem = int(52 - Sem_Año)
    entradas_vis(f"Van pasando {Sem_Año} semanas del año")
    entradas_vis(f"Faltan {falt_Sem} semanas para acabar el año")

    result_Psem = Sem_Año * 100
    porcentaje_sem = int(result_Psem / 52)
    entradas_vis(f"El año va a un {porcentaje_sem}%")

    multi_D = capital_act * 100
    porcen_Anu = int(multi_D / objetivo_anu)
    entradas_vis(f"Tu objetivo esta al {porcen_Anu}%")

    multi_PD = int(porcen_Anu * 100)
    dife_dinSem = int(multi_PD / porcentaje_sem) # Porcentaje de diferencia en objetivos !IMPORTANTE¡

    if dife_dinSem <= 1:
        Cat_financiera = "El negocio esta en quiebra"
    elif dife_dinSem <= 5:
        Cat_financiera = "Entrando en estado critico"
    elif dife_dinSem <= 10:
        Cat_financiera = "Las finanzas estan peligrosamente bajas"
    elif dife_dinSem <= 25:
        Cat_financiera = "Se necesita realizar un plan de emergencia a corto plazo"
    elif dife_dinSem <= 50:
        Cat_financiera = "Se necesita realizar un plan de emergencia a largo plazo"
    elif dife_dinSem <= 75:
        Cat_financiera = "Revisar tendencia en las finanzas para control de riesgos"
    elif dife_dinSem <= 85:
        Cat_financiera = "El rango financiero es bueno y puede mejorar"
    elif dife_dinSem <= 95:
        Cat_financiera = "El rango financiero actual es exelente y prometedor"
    elif dife_dinSem <= 100:
        Cat_financiera = "Plan de objetivos a su maximo rendimiento"
    else:
        Cat_financiera = f"El capital actual ha roto la barrera del objetivo. Actual: {dife_dinSem}%"
    entradas_vis(Cat_financiera)
    notificacion(Cat_financiera)

# ACC:"Año, Mes, Dia, nombreProducto, cicloDvida" - CI:"nombreProducto, inventario" - AOF:"capítal_actual, objetivo_anual" 
objetivo_anual = 80000

# Convertir "fh" a variables definidas
año_input = fh[0] 
mes_input = fh[1]
dia_input = fh[2]

#Variables para "global"
ing_Egre = ""
prodServ = ""
catD = ""
nombD = ""
clientProv = ""
metPag = ""
canD = 0
subD = 0
totD = 0
obserD = ""

cAi = 0

archivo_csv = ""
archivo_actualizado = ""
archivo_actualizadoI = None

ciclo = 0
inventa = 0

nombreProducto = ""

# Funciones de ventana de entradas y ventana de inventario
def entradasINV(event=None):
    global nombreProducto, ciclo, inventa, root2
    nombreProductoInv = (nombreProducto.get())
    nombreProducto.delete(0, 'end')

    cicloDvidaInv = (ciclo.get())
    ciclo.delete(0, 'end')

    inventarioInv = (inventa.get())
    inventa.delete(0, 'end')

    añI = (año_F.get())

    meI = (mes_F.get())

    diI = (dia_F.get())

    inventarioCSV(añI, meI, diI, nombreProductoInv, cicloDvidaInv, inventarioInv)
    analizar_B = tk.Button(root2, text="Analizar", command=analizar)
    analizar_B.place(x=230, y=120)

def inventarioCSV(añoI,mesI,diaI,nombreProductoI,cicloDvidaI,inventarioI):
    global nombreProducto, archivo_actualizadoI

    # Variables de datos de inventario

    archivo_csv2 = pd.read_csv(r'Inventario.csv')

# Mostrar las primeras filas para referencia
    print("Contenido original del CSV:")
    print(archivo_csv2.head())

# Crear un nuevo DataFrame con los datos a agregar
    nuevos_datosI = {
        "año": [añoI],
        "mes": [mesI],
        "dia": [diaI],
        "nombreProducto": [nombreProductoI],
        "inventario": [inventarioI],        
        "cicloDvida": [cicloDvidaI]
    }
    
    nuevas_filasI = pd.DataFrame(nuevos_datosI)

# Concatenar el DataFrame existente con las nuevas filas
    archivo_actualizadoI = pd.concat([archivo_csv2, nuevas_filasI], ignore_index=True)

# Guardar el DataFrame actualizado de nuevo en el archivo CSV
    archivo_actualizadoI.to_csv(r'Inventario.csv', index=False)
    entradas_vis("Nuevos datos agregados con éxito:")
    print(archivo_actualizadoI.tail())
    concatenacion_de_datos()

# tk de inventario
def inventario_vent():
    global nombreProducto, ciclo, inventa, año_F, mes_F, dia_F, root2
    root2 = tk.Tk()
    root2.geometry("300x200+1335+175")
    root2.title("Inventario del CICO")
    root2.resizable(0, 0)
    root2.iconbitmap("cico_log.ico")
    root2.config(bg="#3b7583")

    #Etiquetas
    Etiq_nombre_del_producto = tk.Label(root2, text="Nombre del producto", background="#3b7583", fg="white")
    Etiq_nombre_del_producto.place(x=170, y=10)

    Etiq_inventario = tk.Label(root2, text="Inventario", background="#3b7583", fg="white")
    Etiq_inventario.place(x=170, y=50)

    Etiq_cicloDvida = tk.Label(root2, text="Ciclo de vida", background="#3b7583", fg="white")
    Etiq_cicloDvida.place(x=170, y=90)

    Etiq_fecha = tk.Label(root2, text="Fecha de compra", background="#3b7583", fg="white")
    Etiq_fecha.place(x=125, y=120)

    # Entradas
    nombreProducto = tk.Entry(root2, bd=1, cursor="circle")
    nombreProducto.place(x=10, y=10, width=150)
    inventa = tk.Entry(root2, bd=1, cursor="circle")
    inventa.place(x=10, y=50, width=150)
    ciclo = tk.Spinbox(root2, values=("0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24"), bd=1, cursor="circle")
    ciclo.place(x=10, y=90, width=150) 
    año_F = tk.Spinbox(root2, values=("2025", "2026"), bd=0, cursor="circle", bg="#3b7583", fg="white", border=0)
    año_F.place(x=10, y=120, width=45) 
    mes_F = tk.Spinbox(root2, values=("1","2","3","4","5","6","7","8","9","10","11","12"), bd=0, cursor="circle", bg="#3b7583", fg="white")
    mes_F.place(x=55, y=120, width=25) 
    dia_F = tk.Spinbox(root2,values=("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"), cursor="circle", bg="#3b7583", fg="white", bd=0)
    dia_F.place(x=80, y=120, width=25) 


    # Botones
    button = tk.Button(root2, text="Enviar datos", command=entradasINV, cursor="star", fg="white", bd=0, bg="#4abb95")
    button.place(x=210, y=160)

    eliminar_inv = Button(root2, text="Eliminar ultima entrada", command=elim_quest2, bg="#fca028", cursor="pirate", bd=0, fg="white")
    eliminar_inv.place(x=10, y=160)

    root2.mainloop()

def butonenv(event=None):
    global ing_Egre, cAi
    ing_Egre = (ing_Egre_E.get())

    prodServ = (pro_Serv_E.get())

    catD = (categoria_E.get())
    categoria_E.delete(0, 'end')
    
    nombD = (nomb_E.get())
    nomb_E.delete(0, 'end')

    clientProv = (client_Prov_E.get())
    client_Prov_E.delete(0, 'end')

    metPag = (met_Pag_E.get())

    canD = int(can_E.get())
    can_E.delete(0, 'end')

    subD = int(sub_E.get())
    sub_E.delete(0, 'end')

    obserD = (observaciones.get())
    observaciones.delete(0, 'end')

    # Analizar
    analizar_B1 = tk.Button(root, text="Analizar", command=analizar2)
    analizar_B1.place(x=150, y=260)

    CSV(año_input, mes_input, dia_input, ing_Egre, prodServ, catD, nombD, clientProv, metPag, canD, subD, obserD)
    cAi = archivo_actualizado["Total"].sum() # Capital Actual Input 
    entradas_vis(f"Capital actual: ${cAi}")
    Etiqueta9 = tk.Label(root, text=f"Capital actual: ${cAi}")
    Etiqueta9.place(x=10, y=260)

def CSV(año, mes, dia, ing_egre, pro_serv, cat, nom, client_prov, met_P, can, sub, observ):
    global archivo_actualizado

    archivo_csv = pd.read_csv(r'Finanzas.csv')

# Mostrar las primeras filas para referencia
    print("Contenido original del CSV:")
    print(archivo_csv.head())

# Crear un nuevo DataFrame con los datos a agregar
    nuevos_datos = {
        "año": [año],
        "mes": [mes],
        "dia": [dia],
        "Ingreso/egreso": [ing_egre],
        "Producto/servicio": [pro_serv],
        "Categoria": [cat],
        "Nombre": [nom],
        "Cliente/Provedor": [client_prov],
        "Metodo_de_pago": [met_P], 
        "Cantidad": [can],
        "Subtotal": [sub],
        "Total": [sub * can], 
        "Observaciones": [observ]
    } 
    nuevas_filas = pd.DataFrame(nuevos_datos)

# Concatenar el DataFrame existente con las nuevas filas
    archivo_actualizado = pd.concat([archivo_csv, nuevas_filas], ignore_index=True)

# Guardar el DataFrame actualizado de nuevo en el archivo CSV
    archivo_actualizado.to_csv(r'Finanzas.csv', index=False)
    entradas_vis("Nuevos datos agregados con éxito:")
    entradas_vis(archivo_actualizado.tail())
    concatenacion_de_datos()


def analizar():
    global archivo_actualizadoI
    
    no_iteraciones = len(archivo_actualizadoI)

    for itewr in range(0, no_iteraciones):

        año = int(archivo_actualizadoI.iloc[itewr]["año"])
        mes = int(archivo_actualizadoI.iloc[itewr]["mes"])
        dia = int(archivo_actualizadoI.iloc[itewr]["dia"])

        inventario_arA = archivo_actualizadoI.iloc[itewr]["inventario"] # Inventario

        cicloDvida_arA = archivo_actualizadoI.iloc[itewr]["cicloDvida"] # Ciclo de vida

        NomProd_arA = archivo_actualizadoI.iloc[itewr]["nombreProducto"] # Nombre del producto

        #Definir fecha de compra para analizar ciclo
        entradas_vis("-Analizador de ciclos de compra-")
        ACC(año,mes,dia, NomProd_arA, cicloDvida_arA) # FALTA VINCULAR 
        #Definir producto para analizar stock
        entradas_vis("-Control de inventarios-")
        CI(NomProd_arA, inventario_arA)

def analizar2():
    #Definir dinero actual y objetivo anual para analizar progreso en %
    entradas_vis("-Analizador de objetivo financiero-")
    AOF(cAi, objetivo_anual)
    # Definir capital actual y objetivo anual para analizar estado financiero
    entradas_vis("-Analizador de estado financiero-")
    PI(cAi, objetivo_anual)
    
oAi = 80000 # Objetivo Anual Input

def elim_quest():
    alerta_elim1 = messagebox.askquestion("Eliminar", message="Esta acción es permanente", icon="warning")
    if alerta_elim1 == "yes":
        eliminar_ultim_entradas()
    else:
        entradas_vis("Eliminacion cancelada por el usuario")
def eliminar_ultim_entradas():
    entradas_vis("Eliminar ultima entrada y salida")
    archivo_csv = pd.read_csv(r'Finanzas.csv')
    entradas_vis(f"Archivo eliminado - {archivo_csv.iloc[-1]}")
    archivo_csv = archivo_csv.iloc[:-1]
    archivo_csv.to_csv(r'Finanzas.csv', index=False)

def elim_quest2():
    alerta_elim2 = messagebox.askquestion("Eliminar", message="Esta acción es permanente", icon="warning")
    if alerta_elim2 == "yes":
        eliminar_ultim_inventario()
    else:
        entradas_vis("Eliminacion cancelada por el usuario")
def eliminar_ultim_inventario():
    entradas_vis("Eliminar ultimo inventario")
    archivo_csv2 = pd.read_csv(r'Inventario.csv')
    archivo_csv2 = archivo_csv2.iloc[:-1]
    archivo_csv2.to_csv(r'Inventario.csv', index=False)
    print(archivo_csv2.tail())

def absorver_datos_entradas(): # absorver datos
    entradas_vis("Absorviendo Datos...")
    archivo_csv2 = pd.read_csv(r'Inventario.csv')
    archivo_csv3 = pd.read_csv(r'Finanzas.csv')
    stop_csv1 = len(archivo_csv2)
    stop_csv = stop_csv1 - 1
    stop_iter = 0
    while stop_iter <= stop_csv:
        i = stop_iter
        nombre_csv = archivo_csv2.loc[i, "nombreProducto"] # absorver datos de inventario  
        conteo = (archivo_csv3["Nombre"] == nombre_csv).sum()
        a1 = (f"{nombre_csv} aparece:", conteo, "veces")
        entradas_vis(a1)
        suma_datos_esp = archivo_csv3.loc[archivo_csv3['Nombre']==nombre_csv, 'Cantidad'].sum() # absorve datos especificos "seleccion vertical"
        a2 = (f"Se vendieron {suma_datos_esp} productos de {nombre_csv}")
        entradas_vis(a2)
        stop_iter += 1

def noty_version():
    messagebox.showinfo("Version", message="V 0.0.3")

def concatenacion_de_datos(): # Eliminar inventario condatos de Finanzas
    # Cargar inventario y movimientos
    inv = pd.read_csv("Inventario.csv")
    mov = pd.read_csv("Finanzas.csv")
    print(inv)

    ultimo = mov.iloc[-1]

    prod = ultimo["Nombre"]
    cambio = ultimo["Cantidad"]
    tipo = ultimo["Ingreso/egreso"]

    if tipo == "Ingreso":
        inv.loc[inv["nombreProducto"] == prod, "inventario"] -= cambio
    elif tipo == "Egreso":
        inv.loc[inv["nombreProducto"] == prod, "inventario"] += cambio

    # Guardar inventario actualizado
    inv.to_csv("Inventario.csv", index=False)

# Tkinter

root = tk.Tk()
root.geometry("1125x320+200+175")
root.title("CICO")
root.resizable(0, 0)
root.iconbitmap("cico_log.ico")
root.config(bg=color)


menuBar = Menu(root) #donde vive Menu

root.config(menu=menuBar) #menu dentro del root

archivoMenu = Menu(menuBar) #Menu

archivoMenu.add_command(label="info", command=noty_version) #cascade

menuBar.add_cascade(label="Info", menu=archivoMenu) #Menu


# Etiquetas para entradas de CSV Principal
Etiqueta1 = tk.Label(root, text="Ingreso / Egreso", bg='#2d486f', fg='white')
Etiqueta1.place(x=270, y=10)

Etiqueta2 = tk.Label(root, text="Producto / Servicio", bg='#2d486f', fg='white')
Etiqueta2.place(x=270, y=50)

Etiqueta3 = tk.Label(root, text="Categoria", bg='#2d486f', fg='white')
Etiqueta3.place(x=270, y=90)

Etiqueta4 = tk.Label(root, text="Nombre", bg='#2d486f', fg='white')
Etiqueta4.place(x=270, y=130)

Etiqueta5 = tk.Label(root, text="Cliente / Provedor", bg='#2d486f', fg='white')
Etiqueta5.place(x=432, y=10)

Etiqueta6 = tk.Label(root, text="Metodo de pago", bg='#2d486f', fg='white')
Etiqueta6.place(x=440, y=50)

Etiqueta7 = tk.Label(root, text="Cantidad", bg='#2d486f', fg='white')
Etiqueta7.place(x=480, y=90)

Etiqueta8 = tk.Label(root, text="Subtotal", bg='#2d486f', fg='white')
Etiqueta8.place(x=483, y=130)

Etiqueta10 = tk.Label(root, text="Observaciones", bg='#2d486f', fg='white')
Etiqueta10.place(x=630, y=260)

#Entradas de datos para CSV principal
ing_Egre_E = tk.Spinbox(root,values=("Ingreso", "Egreso"), bd=1, cursor="circle")
ing_Egre_E.place(x=10, y=10, width=250)

pro_Serv_E = tk.Spinbox(root,values=("Producto", "Servicio"), bd=1, cursor="circle")
pro_Serv_E.place(x=10, y=50, width=250)

categoria_E = tk.Entry(root, bd=1, cursor="circle")
categoria_E.place(x=10, y=90, width=250)

nomb_E = tk.Entry(root, bd=1, cursor="circle")
nomb_E.place(x=10, y=130, width=250)

client_Prov_E = tk.Entry(root, bd=1, cursor="circle")
client_Prov_E.place(x=540, y=10, width=250)

met_Pag_E = tk.Spinbox(root,values=("Transferencia", "Efectivo", "Cheque", "Criptomoneda"), bd=1, cursor="circle")
met_Pag_E.place(x=540, y=50, width=250)

can_E = tk.Entry(root, bd=1, cursor="circle")
can_E.place(x=540, y=90, width=250)

sub_E = tk.Entry(root, bd=1, cursor="circle")
sub_E.place(x=540, y=130, width=250)

observaciones = tk.Entry(root, bd=1, cursor="circle")
observaciones.place(x=540, y=170, width=250,height=80)

# Botones para enviar datos y entrar a inventario

# Enviar datos
BotonEV = tk.Button(root, text="Enviar datos", cursor="star", command=butonenv, bg="#4abb95", fg="white", bd=0)
BotonEV.place(x=350, y=260, width=100)
# Mostrar datos

# Inventario
invent = tk.Button(root, text="Inventario", cursor="star", command=inventario_vent, bg="#3b8377", fg="white", bd=0, activebackground="#3aa87f")
invent.place(x=10, y=170, width=75, height=75)

# Botones eliminar

eliminar_entr = Button(root, text="Eliminar ultima entrada", command=elim_quest, bg="#fca028", cursor="pirate", bd=0, fg="white")
eliminar_entr.place(x=335, y=230)

def entradas_vis(dato):
    pantalla_vis.insert(END, dato)
    cant_vis = pantalla_vis.size()
    if cant_vis >= 16:
        pantalla_vis.after(1000, lambda: pantalla_vis.delete(0))

pantalla_vis = Listbox(root, width=52, height=17)
pantalla_vis.insert(0, "Datos de transito en CICO")
pantalla_vis.place(x=800,y=8)

absorver_datos_entradas()

root.mainloop()

#Conectar CSV para vincular ingresos y egresos con inventario y definir variables ACC:"Año, Mes, Dia, nombreProducto, cicloDvida" - CI:"nombreProducto, inventario" - AOF:"capítal_actual, objetivo_anual" 
#Hacer interfaz de recepcion de datos 

# Agregar botones de fecha a inventario 
# Conectar 

# Absorber datos de cantidad de productos vendidos y obsorver datos de inventario de producto
# Conectar datos de csv especificos para Spinbox values=""  

# OP Optimizacion de produccion 
# (Decide cuanto produccir segun demanda, capacidad y costos)
#dem = demanda
#cap = capacidad
#cos = costos

# crear sistema de guardado de objetivo anual 
