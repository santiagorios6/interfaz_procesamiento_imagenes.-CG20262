import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk 
from matplotlib.widgets import Slider
import numpy as np
import imglib 

#variables Globales

imagen_Original = None

var_verde = None
var_azul = None
var_rojo = None
var_amarillo = None
var_celeste = None
var_morado = None
var_brillo = None
var_negativo = None

###############Funciones#############################

def mostrar_en_etiqueta(arreglo):
    imagen_resultado = Image.fromarray(arreglo)
    img_mostrar = imagen_resultado.resize((300,400))
    imagen_tk = ImageTk.PhotoImage(img_mostrar)
    etiqueta_imagen.config(image=imagen_tk)
    etiqueta_imagen.image = imagen_tk

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

    if var_amarillo.get():
        acomulador += imglib.obtener_capa_amarilla(arreglo)
        alguna_activa = True

    if var_celeste.get():
        acomulador += imglib.obtener_capa_celeste(arreglo)
        alguna_activa = True

    if var_morado.get():
        acomulador += imglib.obtener_capa_morada(arreglo)
        alguna_activa = True

    if not alguna_activa:
        resultado = arreglo
    else:
        resultado = acomulador

    resultado = np.clip(resultado, 0, 255).astype(np.uint8)

    mostrar_en_etiqueta(resultado)

def aplicar_negativo():
    if imagen_Original is None:
        messagebox.showwarning("error de imagen", "No ha seleccinado la Imagen")
        return
    if var_negativo.get():
        arreglo = np.array(imagen_Original)
        resultado = imglib.invertir_color(arreglo)
        mostrar_en_etiqueta(resultado)

    else:
        arreglo = np.array(imagen_Original)
        mostrar_en_etiqueta(arreglo)


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


############PANELES#########################

def cambiar_categoria(evento):
    seleccion = combo_herramientas.get()

    for widget in frame_controles.winfo_children():
        widget.destroy()

    if seleccion == "Colores":
        construir_panel_colores()

    elif seleccion == "Brillo":
        construir_panel_brillo()

    else:
        tk.Label(
            frame_controles,
            text=f"Categoría: {seleccion}\n(Aquí irán los controles)", 
            bg="black", 
            fg="white", 
            font=("arial", 14)
        ).pack(pady=50)

def construir_panel_colores():
    global var_rojo, var_verde, var_azul, var_amarillo, var_celeste, var_morado, var_negativo

    if var_rojo is None:
        var_rojo = tk.BooleanVar()
        var_verde = tk.BooleanVar()
        var_azul = tk.BooleanVar()
        var_amarillo = tk.BooleanVar()
        var_celeste = tk.BooleanVar()
        var_morado = tk.BooleanVar()
        var_negativo = tk.BooleanVar()

    tk.Label(
        frame_controles,
        text= "Seleccionar Canal",
        justify= "center",
        font=("arial",12, "bold"),
        fg= "white",
        bg="black"
    ).pack(anchor="w", pady=(0,5))

    tk.Checkbutton(
        frame_controles,
        text= "Capa Roja",
        variable= var_rojo,
        command= aplicar_capas,
        bg= "black",
        fg= "red",
        selectcolor="black"
    ).pack(anchor="w")

    tk.Checkbutton(
        frame_controles,
        text= "Capa Verde",
        variable= var_verde,
        command= aplicar_capas,
        bg="black",
        fg="green",
        selectcolor= "black"
    ).pack(anchor="w")


    tk.Checkbutton(
        frame_controles,
        text= "Capa Azul",
        variable= var_azul,
        command= aplicar_capas,
        bg= "black",
        fg="blue",
        selectcolor="black",
    ).pack(anchor="w")

    tk.Checkbutton(
        frame_controles,
        text= "capa Amarilla",
        variable= var_amarillo,
        command= aplicar_capas,
        bg="black",
        fg="yellow",
        selectcolor= "black"
    ).pack(anchor="w")

    tk.Checkbutton(
            frame_controles,
            text= "capa Celeste",
            variable= var_celeste,
            command= aplicar_capas,
            bg="black",
            fg="light blue",
            selectcolor= "black"
        ).pack(anchor="w")

    tk.Checkbutton(
            frame_controles,
            text= "capa Morada",
            variable= var_morado,
            command= aplicar_capas,
            bg="black",
            fg="purple",
            selectcolor= "black"
        ).pack(anchor="w")

    tk.Frame(
        frame_controles, 
        height=2, 
        bg="gray"
    ).pack(fill="x", pady=10)

    tk.Checkbutton(
            frame_controles,
            text= "capa Negativa",
            variable= var_negativo,
            command= aplicar_negativo,
            bg="black",
            fg="white",
            selectcolor= "black"
        ).pack(anchor="w")

def construir_panel_brillo():
    global var_brillo
    if var_brillo is None:
        var_brillo = tk.DoubleVar(value= 0)

    tk.Label(
    frame_controles,
    text= "Brillo",
    fg= "white",
    bg= "black",
    font= ("arial", 12, "bold")
    ).pack(anchor="w", pady=(0,5))

    tk.Scale(
    frame_controles,
    from_= -100,
    to= 100,
    orient= "horizontal",
    variable= var_brillo,
    command= lambda x: aplicar_brillo(),
    bg= "black",
    highlightbackground= "green",

).pack(fill= "x")




########################ventana########################
ventana = tk.Tk()

ventana.title("Copia barata de Photoshop je je je")
ventana.geometry("1000x650")
ventana.configure(bg= "black")
ventana.resizable(True, True)


############Variables de Color#####################
var_rojo = tk.BooleanVar()
var_verde = tk.BooleanVar()
var_azul = tk.BooleanVar()
var_amarillo = tk.BooleanVar()
var_celeste = tk.BooleanVar()
var_morado = tk.BooleanVar()
var_negativo = tk.BooleanVar()
var_brillo = tk.DoubleVar(value= 0)

############## PANEL IZQUIERDO #####################
frame_izquierdo = tk.Frame(
    ventana,
    bg= "black"
)
frame_izquierdo.pack(side="left", fill="y", padx=10, pady=10)

#Etiqueta de la imagen
frame_imagen = tk.Frame(
    frame_izquierdo,
    width=400,
    height=400,
    bg="black",
    highlightbackground="green",
    highlightthickness= 4,
    relief="raised",
)
frame_imagen.pack(pady=(0,10))
frame_imagen.pack_propagate(False)


etiqueta_imagen = tk.Label(
    frame_imagen,
    bg="black"
)   
etiqueta_imagen.pack(fill="both",expand=True)

_button_abrir = tk.Button(
    frame_izquierdo,
    text= "Abrir Imagen",
    bg= "gray",
    command= abrir_imagen,
    font= ("arial", 10)
)
_button_abrir.pack(fill="x")

#############PANEL DERECHO#############################

frame_panel = tk.Frame(
    ventana,
    bg="black",
    highlightbackground="green",
    highlightthickness= 4,
)
frame_panel.pack(fill="both", side="right", expand=True, padx=10, pady=10)


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
frame_controles.pack(fill = "both", expand = True, padx=10, pady=10)

combo_herramientas.bind("<<ComboboxSelected>>", cambiar_categoria)

ventana.mainloop()