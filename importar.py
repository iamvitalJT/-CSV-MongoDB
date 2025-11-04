import tkinter as tk
from tkinter import filedialog
import subprocess

selected_file = ""

ventana = tk.Tk()
ventana.title("Importar Mongo to CSV")
ventana.geometry("400x700+500+50")
seleccionado = ""
def selecionar():
    global selecionar_a, seleccionado
    selecionar_a = filedialog.askopenfilename(title="Selecciona el archivo CSV", filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")))
    seleccionado = selecionar_a
    archivo_s = tk.Label(ventana, text=selecionar_a, font=("Arial", 10))
    archivo_s.place(x=150, y=415)

def on_boton_click():
    global  db, collection, connection_string
    db = insertar_db.get()
    collection = insertar_colecion.get()
    connection_string = insertar_texto.get()
    if seleccionado == "":
        resultado.config(text="Por favor, seleccione un archivo.", fg="red")
        return
    elif not db or not collection or not connection_string:
        resultado.config(text="Por favor, complete todos los campos.", fg="red")
        return
    elif " " in db or " " in collection:
        resultado.config(text="La base de datos y la colección\nNO pueden contener espacios.", fg="red")
        return 
    ejecutar_comando()

def ejecutar_comando():
    if selecionar_a[-4:] != ".csv":
        resultado.config(text="Por favor, seleccione un archivo CSV válido.", fg="red")
    comando = (f'.\\mongoimport "{connection_string}" --db {db} --collection {collection} --file "{selecionar_a}" --type csv --headerline')
    confirmacion = subprocess.run(comando, shell=True, capture_output=True, text=True)
    if confirmacion.returncode == 0:    
        resultado.config(text="Importación Exitosa", fg="green")
    else:
        resultado.config(text=" Conexion erronera\n→Mira si la IP esta permitida\n", fg="red")
registro_label = tk.Label(ventana, text="Importar a MongoDB CSV", font=("Arial", 16))
registro_label.pack(pady=70)

label_conexion = tk.Label(ventana, text="Inserte su conexion de Cluster MongoDB", font=("Arial", 16))
label_conexion.pack()

insertar_texto = tk.Entry(ventana, width=40, font=("Arial", 12))
insertar_texto.pack(pady=20)

label_db = tk.Label(ventana, text="Base de datos", font=("Arial", 11))
label_db.place(x=20, y=299)

insertar_db = tk.Entry(ventana, font=("Arial", 12))
insertar_db.place(x=150, y=300)

label_colecion = tk.Label(ventana, text="Colección", font=("Arial", 11))
label_colecion.place(x=20, y=329)

insertar_colecion = tk.Entry(ventana, font=("Arial", 12))
insertar_colecion.place(x=150, y=330)

label_tipo = tk.Label(ventana, text="Tipo de archivo", font=("Arial", 11))
label_tipo.place(x=20, y=359)

tipo = tk.Label(ventana, text="CSV", font=("Arial", 12))
tipo.place(x=150, y=356)

label_archivo = tk.Label(ventana, text="Archivo:", font=("Arial", 11))
label_archivo.place(x=20, y=385)

seleccionar = tk.Button(ventana, text="Seleccionar archivo", font=("Arial", 10), command=selecionar)
seleccionar.place(x=150, y=385)

boton = tk.Button(ventana, text="Importar CVS a MongoDB", command=on_boton_click, font=("Arial", 14))
boton.place(x=80, y=500)

resultado = tk.Label(ventana, text="", font=("Arial", 10))
resultado.place(x=50, y=600)

ventana .mainloop()