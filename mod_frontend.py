import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')
    return None

def pausa():
    input('Presione Enter para continuar...')
    return None

def valida_entero_positivo(mensaje):
    """Pide un valor y no sale del bucle hasta que sea un entero >= 0."""
    while True:
        entrada = input(mensaje)
        if entrada.isdecimal(): 
            return int(entrada)
        print('Error: Debe ingresar un número entero positivo sin decimales.')

def solicita_datos_producto():
    """Pide los datos para un nuevo producto aplicando .capitalize() al texto."""
    print("\n--- Registrar Nuevo Producto ---")
    
    nombre = input("Nombre: ").strip().capitalize()
    descripcion = input("Descripción: ").strip().capitalize()
    
    cantidad = valida_entero_positivo("Cantidad en stock: ")
    
    while True:
        try:
            precio = float(input("Precio (use punto para decimales si aplica): "))
            if precio >= 0:
                break
            print("El precio no puede ser negativo.")
        except ValueError:
            print("Error: Ingrese un número válido para el precio.")
            
    categoria = input("Categoría: ").strip().capitalize()
    return (nombre, descripcion, cantidad, precio, categoria)

def solicita_datos_actualizar(campos_sin_pk):
    """Pide los campos a actualizar aplicando .capitalize() si es texto."""
    print("\n--- Actualizar Producto ---")
    print("Deje el campo vacío (Presione Enter) si NO desea modificarlo.\n")
    nuevos_valores = {}
    
    for campo in campos_sin_pk:
        valor = input(f"Nuevo valor para {campo.capitalize()}: ").strip()
        if valor != "":
            if campo == "cantidad":
                while not valor.isdecimal():
                    print("Error: La cantidad debe ser un entero positivo.")
                    valor = input(f"Nuevo valor para {campo.capitalize()}: ").strip()
                nuevos_valores[campo] = int(valor)
            elif campo == "precio":
                while True:
                    try:
                        val_float = float(valor)
                        if val_float >= 0:
                            nuevos_valores[campo] = val_float
                            break
                        print("El precio no puede ser negativo.")
                    except ValueError:
                        print("Error: Ingrese un precio válido.")
                    valor = input(f"Nuevo valor para {campo.capitalize()}: ").strip()
            else:
                nuevos_valores[campo] = valor.capitalize()
    return nuevos_valores

def imprime_tabla(campos, filas):
    """Muestra los registros ordenados con separador de miles y 2 decimales."""
    if not filas:
        print("\nNo se encontraron registros para mostrar.")
        return None
        
    print("\n" + "=" * 90)
    encabezado = "".join([f"{str(c).upper().ljust(15)}" for c in campos])
    print(encabezado)
    print("-" * 90)
    

    for fila in filas:
        linea = ""
        for i, valor in enumerate(fila):
            if campos[i] == 'precio' and isinstance(valor, (int, float)):
                texto_precio = f"{valor:,.2f}"
                texto_precio = texto_precio.replace(",", "X").replace(".", ",").replace("X", ".")
                linea += texto_precio.ljust(15)
            elif campos[i] == 'cantidad' and isinstance(valor, int):
                texto_cantidad = f"{valor:,}".replace(",", ".")
                linea += texto_cantidad.ljust(15)
            else:
                linea += str(valor).ljust(15)
        print(linea)
    print("=" * 90 + "\n")
    return None