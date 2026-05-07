# PRUEBAS 

import pandas as pd

def concatenacion_de_datos():
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

concatenacion_de_datos()