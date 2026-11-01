import os
import mod_backend as be
import mod_frontend as fe

def main():
    os.chdir(os.path.dirname(__file__))
    archivo_db_nombre = 'inventario.db'
    tabla_nombre = 'productos'
    campos = ('id', 'nombre', 'descripcion', 'cantidad', 'precio', 'categoria')
    pk = campos[0]
    campos_sin_pk = campos[1::]
    
    create_table_sql = f'''
CREATE TABLE IF NOT EXISTS "{tabla_nombre}" (
	"id"	INTEGER NOT NULL UNIQUE,
	"nombre"	TEXT NOT NULL CHECK((trim("nombre") <> '' AND trim("nombre") GLOB '[A-Za-z0-9]*') AND length("nombre") <= 30),
	"descripcion"	TEXT,
	"cantidad"	INTEGER NOT NULL CHECK(("cantidad" >= 0)),
	"precio"	REAL NOT NULL CHECK(("precio" >= 0)),
	"categoria"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
) STRICT;'''
    
    be.inicializa_db(archivo_db_nombre, create_table_sql)
    
    while True: # Bucle principal
        fe.limpiar_pantalla()
        print("""
############
# Programa de CRUD TFI.
############

1) Agregar producto.
2) Visualizar productos.
3) Actualizar producto.
4) Eliminar producto.
5) Búsqueda de producto por id.
6) Reporte de productos con bajo stock.
0) Salir
    """)
        opcion = input('Ingrese la opción deseada y presione Enter: ')
        if opcion == '1': # Agrega
            be.agregar_registro(archivo_db_nombre, tabla_nombre, campos_sin_pk)
        elif opcion == '2': # Visualiza
            fe.imprime_tabla(campos, be.seleccionar_registros(archivo_db_nombre, tabla_nombre))
        elif opcion == '3': # Actualiza
            be.actualizar_registro(archivo_db_nombre, tabla_nombre, campos, pk)
        elif opcion == '4': # Elimina
            be.eliminar_registro(archivo_db_nombre, tabla_nombre, pk)
        elif opcion == '5': # Búsqueda
            fe.imprime_tabla(campos, be.busca_registros_id(archivo_db_nombre, tabla_nombre, pk))
        elif opcion == '6': # Reporte
            fe.imprime_tabla(campos, be.reporte_por_cantidad(archivo_db_nombre, tabla_nombre))
        elif opcion == '0': # Salir
            print('Gracias por utilizar el programa, saliendo...')
            fe.pausa() # Esta pausa es necesaria para la terminal de windows cuando hagamos un .exe de este código.
            break
        else:
            print('La opción ingresada es incorrecta, inténtelo nuevamente...')
        fe.pausa()
        
if __name__ == '__main__': # Punto de entrada de la aplicación
    main()