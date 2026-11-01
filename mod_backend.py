import sqlite3
import sys
import mod_frontend as fe

def inicializa_db(archivo_db, create_table_sql):
    try:
        with sqlite3.connect(archivo_db) as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error crítico de base de datos al inicializar: {e}")
        sys.exit()

def agregar_registro(archivo_db, tabla, campos_sin_pk):
    datos = fe.solicita_datos_producto()
    
    placeholders = ", ".join(["?" for _ in campos_sin_pk])
    nombres_campos = ", ".join(campos_sin_pk)
    query = f'INSERT INTO "{tabla}" ({nombres_campos}) VALUES ({placeholders})'
    
    try:
        with sqlite3.connect(archivo_db) as conn:
            cursor = conn.cursor()
            cursor.execute(query, datos)
            conn.commit()
            print("\n¡Producto agregado con éxito!")
    except sqlite3.IntegrityError:
        print("\nError: No se pudo agregar. El nombre no cumple con las restricciones (máx 30 caracteres, no vacío o duplicado).")
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
        sys.exit()

def seleccionar_registros(archivo_db, tabla):
    query = f'SELECT * FROM "{tabla}"'
    try:
        with sqlite3.connect(archivo_db) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
        sys.exit()

def busca_registros_id(archivo_db, tabla, pk):
    id_buscar = fe.valida_entero_positivo("Ingrese el ID del producto que desea buscar: ")
    query = f'SELECT * FROM "{tabla}" WHERE "{pk}" = ?'
    try:
        with sqlite3.connect(archivo_db) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id_buscar,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
        sys.exit()

def eliminar_registro(archivo_db, tabla, pk):
    id_eliminar = fe.valida_entero_positivo("Ingrese el ID del producto que desea eliminar: ")
    
    query_check = f'SELECT 1 FROM "{tabla}" WHERE "{pk}" = ?'
    query_delete = f'DELETE FROM "{tabla}" WHERE "{pk}" = ?'
    
    try:
        with sqlite3.connect(archivo_db) as conn:
            cursor = conn.cursor()
            cursor.execute(query_check, (id_eliminar,))
            if not cursor.fetchone():
                print(f"\nNo se encontró ningún producto con el ID {id_eliminar}.")
                return
            
            cursor.execute(query_delete, (id_eliminar,))
            conn.commit()
            print(f"\n¡Producto con ID {id_eliminar} eliminado correctamente!")
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
        sys.exit()

def actualizar_registro(archivo_db, tabla, campos, pk):
    id_actualizar = fe.valida_entero_positivo("Ingrese el ID del producto que desea modificar: ")
    
    query_check = f'SELECT * FROM "{tabla}" WHERE "{pk}" = ?'
    try:
        with sqlite3.connect(archivo_db) as conn:
            cursor = conn.cursor()
            cursor.execute(query_check, (id_actualizar,))
            producto = cursor.fetchone()
            
            if not producto:
                print(f"\nNo se encontró ningún producto con el ID {id_actualizar}.")
                return
            
            campos_sin_pk = campos[1::]
            nuevos_valores = fe.solicita_datos_actualizar(campos_sin_pk)
            
            if not nuevos_valores:
                print("\nNo se ingresaron cambios. El producto permanece igual.")
                return
                
            set_query = ", ".join([f'"{campo}" = ?' for campo in nuevos_valores.keys()])
            valores = list(nuevos_valores.values())
            valores.append(id_actualizar) # Para el WHERE
            
            query_update = f'UPDATE "{tabla}" SET {set_query} WHERE "{pk}" = ?'
            
            cursor.execute(query_update, valores)
            conn.commit()
            print("\n¡Producto actualizado con éxito!")
            
    except sqlite3.IntegrityError:
        print("\nError: Los nuevos datos violan las restricciones de la base de datos.")
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
        sys.exit()

def reporte_por_cantidad(archivo_db, tabla):
    limite = fe.valida_entero_positivo("Ingrese el stock máximo para el reporte de bajo stock: ")
    query = f'SELECT * FROM "{tabla}" WHERE "cantidad" <= ?'
    try:
        with sqlite3.connect(archivo_db) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (limite,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
        sys.exit()
        