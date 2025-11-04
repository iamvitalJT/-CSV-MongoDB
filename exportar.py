import tkinter as tk
from tkinter import filedialog
import subprocess
import datetime

ventana = tk.Tk()
ventana.title("Exportar Mongo to CSV")
ventana.geometry("400x800+500+20")
campo_cmd = ""
ruta_seleccionada = ""
def borrarcampo():
    insertar_campos.delete(0, tk.END)
def campo():
    global campo_cmd 
    campo = insertar_campos.get()
    if campo == "":
        resultado.config(text="Por favor, ingrese un campo válido.", fg="red")
        return
    elif campo_cmd == "":
        campo_cmd = campo
        campos.config(text=f'{campo_cmd}\n', fg="black")
    else:
        campo_cmd = f'{campo_cmd},{campo}'
    borrarcampo()
    campos.config(text=f'{campo_cmd}', fg="black")
def seleccionar_ruta():
    global ruta_seleccionada
    ruta_seleccionada = filedialog.askdirectory(title="Selecciona la Carpeta de Proyectos")
def comando():
    global  db, collection, connection_string, ruta_seleccionada, campo_cmd, nombre_archivo
    db = insertar_db.get()
    collection = insertar_colecion.get()
    connection_string = insertar_texto.get()
    nombre_archivo = f'{collection}_{fecha}'
    if not ruta_seleccionada:
        resultado.config(text="Por favor\nSeleccione una carpeta de salida.", fg="red")
        return
    elif not db or not collection or not connection_string:
        resultado.config(text="Por favor\nComplete todos los campos.", fg="red")
        return
    elif " " in db or " " in collection:
        resultado.config(text="La base de datos y la colección\nNO pueden contener espacios.", fg="red")
        return
    elif campo_cmd == "":
        resultado.config(text="Por favor\nIngrese al menos un campo a exportar.", fg="red")
        return
    ejecutar_comando()
def ejecutar_comando():
    comando = (f'.\\mongoexport "{connection_string}" --db {db} --collection {collection} --type=csv --fields="{campo_cmd}" --out="{ruta_seleccionada}/{nombre_archivo}.csv"')
    confirmacion = subprocess.run(comando, shell=True, capture_output=True, text=True)
    if confirmacion.returncode == 0:    
        resultado.config(text=f'Exportación Exitosa en\n{ruta_seleccionada}{nombre_archivo}.csv', fg="green")
    else:
        resultado.config(text=" Conexion erronera\n→Mira si la IP esta permitida\n", fg="red")

fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

exportarlabel = tk.Label(ventana, text="Exportar MongoDB CSV", font=("Arial", 16))
exportarlabel.pack(pady=70)

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

seleccionar_carpeta_label = tk.Label(ventana, text="Ruta salida", font=("Arial", 11))
seleccionar_carpeta_label .place(x=20, y=385)   

seleccionar_carpeta_btn = tk.Button(ventana, text="Seleccionar Carpeta", font=("Arial", 10), command=seleccionar_ruta)
seleccionar_carpeta_btn.place(x=150, y=381)

campo_label = tk.Label(ventana, text="Campos a exportar", font=("Arial", 10))
campo_label.place(x=20, y=419)

insertar_campos = tk.Entry(ventana, font=("Arial", 12))
insertar_campos.place(x=150, y=420)

boton_campos = tk.Button(ventana, text="+", font=("Arial", 9), command=campo)
boton_campos.place(x=350, y=420)

campos = tk.Label(ventana, text="", font=("Arial", 10))
campos.place(x=150, y=447)

boton_exportar = tk.Button(ventana, text="Exportar", font=("Arial", 12), width=15, height=2, command=comando)
boton_exportar.place(x=130, y=600)

resultado = tk.Label(ventana, text="", font=("Arial", 14))
resultado.place(x=50, y=700)

ventana .mainloop()