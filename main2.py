import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk 
from matplotlib.widgets import Slider
import numpy as np
import imglib 

#variables Globales

imagen_Original = None

def mostrar_en_etiqueta(arreglo):
    imagen_resultado = Image.fromarray(arreglo)
    img_mostrar = imagen_resultado.resize((300,400))
    imagen_tk = ImageTk.PhotoImage(img_mostrar)
    etiqueta_imagen.config(image=imagen_tk)
    etiqueta_imagen.image = imagen_tk

###############definiciones#############################

def abrir_imagen():

    global imagen_Original
    ruta = filedialog.askopenfilename(
        title= "Seleccione la imagen",
        filetypes=[("archivos de Imagen", "*.png *.jpg *.jpeg")]
    
    )

    if ruta:
        imagen_Original = Image.open(ruta)
        imagen_numpy = np.array(imagen_Original)

        #redimensionamiento de imagen
        img_mostrar = imagen_Original.resize((300,400))

        #Conversion a formato compatible
        imagen_tk = ImageTk.PhotoImage(img_mostrar)

        #mostrar Imagen
        etiqueta_imagen.config(image= imagen_tk)
        etiqueta_imagen.image = imagen_tk

def aplicar_capas():
    if imagen_Original is None:
        messagebox.showerror("Error de Imagen", "No has seleccionado la imagen")
        return
    
    arreglo = np.array(imagen_Original)
    acomulador = np.zeros_like(arreglo, dtype=np.uint16)
    alguna_activa = False

    if var_rojo.get():
        acomulador += imglib.obtener_capa_roja(arreglo)
        alguna_activa = True

    if var_verde.get():
        acomulador += imglib.obtener_capa_verde(arreglo)
        alguna_activa = True

    if var_azul.get():
        acomulador += imglib.obtener_capa_azul(arreglo)
        alguna_activa = True

    if not alguna_activa:
        resultado = arreglo
    else:
        resultado = acomulador

    resultado = np.clip(resultado, 0, 255).astype(np.uint8)

    mostrar_en_etiqueta(resultado)


def aplicar_brillo():

    if imagen_Original is None:
        messagebox.showwarning("error de imagen", "No ha seleccinado la Imagen")
        return

    print("aplicando brillo")
    print("valor de slider", var_brillo.get())

    arreglo = np.array(imagen_Original)
    resultado = imglib.aplicar_brillo(arreglo, var_brillo.get())

    print("valor maximo resultado", resultado.max())

    mostrar_en_etiqueta(resultado)


    



########################ventana########################
ventana = tk.Tk()

ventana.title("Copia barata de Photoshop je je je")
ventana.geometry("1000x650")
ventana.configure(bg= "black")
ventana.resizable(True, True)
#################################
var_rojo = tk.BooleanVar()
var_verde = tk.BooleanVar()
var_azul = tk.BooleanVar()
##################################
var_brillo = tk.DoubleVar(value= 0)

#Etiqueta de la imagen
frame_imagen = tk.Frame(
    ventana,
    width=300,
    height=400,
    bg="black",
    highlightbackground="green",
    highlightthickness= 4,
    relief="raised",
)
frame_imagen.place(x= 1,y= 1)
etiqueta_imagen = tk.Label(
    ventana,
)
etiqueta_imagen.place(x= 0, y=0)

button = tk.Button(
    ventana,
    text= "Abrir Imagen",
    bg= "gray",
    command= abrir_imagen
)
button.place(x=120, y= 410 )

frame_panel = tk.Frame(
    ventana,
    bg="black",
    highlightbackground="green",
    highlightthickness= 4,
)
frame_panel.place(x=650, y=0, width=340, height=600)


herramientas_desplegables = [
    "Colores",
    "Brillo",
    "Escala de Grises",
    "Umbralizacion",
    "Suma de Imgenes",
    "Histograma",
    "Geometria"
]

combo_herramientas = ttk.Combobox(
    frame_panel,
    values= herramientas_desplegables,
    state= "readonly"
)
combo_herramientas.pack(pady=10 ,padx=10, fill= "x")

frame_controles = tk.Frame(
    frame_panel,
    bg="black"  
)
frame_controles.pack(fill = "both", expand = True)

def cambiar_categoria(evento):
    seleccion = combo_herramientas.get()

    for widget in frame_controles.winfo_children():
        widget.destroy()


    tk.Label(
        frame_controles,
        text=f"Categoría: {seleccion}\n(Aquí irán los controles)", 
        bg="black", 
        fg="white", 
        font=("arial", 14)).pack(pady=50)

combo_herramientas.bind("<<ComboboxSelected>>", cambiar_categoria)


































































"""""

###################### RGB y CMY #######################################
frame_RGB = tk.Frame(
    ventana,
    bg="black",
    highlightbackground="green",
    highlightthickness= 4,
    relief="raised",
)
frame_RGB.place(x=310, y=0)

etiqueta_RGB = tk.Label(
    frame_RGB,
    text= "Capas RGB y CMY",
    justify= "center",
    font=("arial",12, "bold"),
    fg= "white",
    bg="black"
)
etiqueta_RGB.pack(anchor="center")

check_rojo = tk.Checkbutton(
    frame_RGB,
    text= "Capa Roja",
    variable= var_rojo,
    command= aplicar_capas,
    bg= "black",
    fg= "red",
    selectcolor="black"
    
)
check_rojo.pack(anchor="w")

check_verde = tk.Checkbutton(
    frame_RGB,
    text= "Capa Verde",
    variable= var_verde,
    command= aplicar_capas,
    bg="black",
    fg="green",
    selectcolor= "black"
)
check_verde.pack(anchor="w")


check_azul = tk.Checkbutton(
    frame_RGB,
    text= "Capa Azul",
    variable= var_azul,
    command= aplicar_capas,
    bg= "black",
    fg="blue",
    selectcolor="black",
)
check_azul.pack(anchor="w")

##################### BRILLO ############################

frame_Brillo = tk.Frame(
    ventana,
    bg="black",
    highlightbackground="green",
    highlightthickness= 4,
    relief="raised",
)

frame_Brillo.place(x=700, y=0)

etiqueta_brillo = tk.Label(
    frame_Brillo,
    text= "Brillo",
    fg= "white",
    bg= "black",
    font= ("arial", 12, "bold")
)

etiqueta_brillo.pack(anchor= "center")


slider_brillo = tk.Scale(
    frame_Brillo,
    from_= -100,
    to= 100,
    orient= "horizontal",
    variable= var_brillo,
    command= lambda x: aplicar_brillo(),
    bg= "black",
    highlightbackground= "green",

)

slider_brillo.pack(padx= 10, pady= 10)

#########################################################
opciones = ["OPCION A", "OPCION B","OPCION C"]

combo = ttk.Combobox(ventana, values= opciones)

combo.pack()



 
"""





ventana.mainloop()