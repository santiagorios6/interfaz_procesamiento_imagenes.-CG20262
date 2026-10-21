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
var_brillo_canal_rojo = None
var_brillo_canal_verde = None
var_brillo_canal_azul = None
var_gris_promedio = None
var_gris_midgray = None
var_gris_luminosidad = None 
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

def aplicar_brillo_capa_roja():
    if imagen_Original is None:
        messagebox.showwarning("error de imagen", "No ha seleccinado la Imagen")
        return

    arreglo = np.array(imagen_Original)
    resultado = imglib.aplicar_brillo_capa_roja(arreglo, var_brillo_canal_rojo.get())

    mostrar_en_etiqueta(resultado)

def aplicar_brillo_capa_verde():
    if imagen_Original is None:
        messagebox.showwarning("error de imagen", "No ha seleccinado la Imagen")
        return

    arreglo = np.array(imagen_Original)
    resultado = imglib.aplicar_brillo_capa_verde(arreglo, var_brillo_canal_verde.get())

    mostrar_en_etiqueta(resultado)

def aplicar_brillo_capa_azul():
    if imagen_Original is None:
        messagebox.showwarning("error de imagen", "No ha seleccinado la Imagen")
        return

    arreglo = np.array(imagen_Original)
    resultado = imglib.aplicar_brillo_capa_azul(arreglo, var_brillo_canal_azul.get())

    mostrar_en_etiqueta(resultado)

def aplicar_grises():
    if imagen_Original is None:
        messagebox.showwarning("error de imagen",  "No has seleccionado la imagen")

    alguna_activa = False

    if var_gris_promedio.get():
        arreglo = np.array(imagen_Original)
        resultado = imglib.aplicar_gris_promedio(arreglo)
        alguna_activa = True
    

    if var_gris_midgray.get():
        arreglo = np.array(imagen_Original)
        resultado = imglib.aplicar_gris_midgray(arreglo)
        alguna_activa = True

   

    if var_gris_luminosidad.get():
        arreglo = np.array(imagen_Original)
        resultado = imglib.aplicar_gris_luminosidad(arreglo)
        alguna_activa = True

    else:
        arreglo = np.array(imagen_Original)

    if not alguna_activa:
        resultado = arreglo
        

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

    elif seleccion == "Escala de Grises":
        construir_panel_grises()


    else:
        tk.Label(
            frame_controles,
            text=f"Categoría: {seleccion}\n(Aquí irán los controles)", 
            bg="black", 
            fg="white", 
            font=("arial", 14)
        ).pack(pady=50)


############ PANEL DE COLORES ##################################################
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
        font=("arial",16, "bold"),
        fg= "white",
        bg="black"
    ).pack(anchor="w", pady=(0,5))

    tk.Checkbutton(
        frame_controles,
        text= "Capa Roja",
        variable= var_rojo,
        command= aplicar_capas,
        font= ("arial", 12),
        bg= "black",
        fg= "red",
        selectcolor="black"
    ).pack(anchor="w")

    tk.Checkbutton(
        frame_controles,
        text= "Capa Verde",
        variable= var_verde,
        command= aplicar_capas,
        font= ("arial", 12),
        bg="black",
        fg="green",
        selectcolor= "black"
    ).pack(anchor="w")


    tk.Checkbutton(
        frame_controles,
        text= "Capa Azul",
        variable= var_azul,
        command= aplicar_capas,
        font= ("arial", 12),
        bg= "black",
        fg="blue",
        selectcolor="black",
    ).pack(anchor="w")

    tk.Checkbutton(
        frame_controles,
        text= "capa Amarilla",
        variable= var_amarillo,
        command= aplicar_capas,
        font= ("arial", 12),
        bg="black",
        fg="yellow",
        selectcolor= "black"
    ).pack(anchor="w")

    tk.Checkbutton(
        frame_controles,
        text= "capa Celeste",
        variable= var_celeste,
        command= aplicar_capas,
        font= ("arial", 12),
        bg="black",
        fg="light blue",
        selectcolor= "black"
    ).pack(anchor="w")

    tk.Checkbutton(
        frame_controles,
        text= "capa Morada",
        variable= var_morado,
        command= aplicar_capas,
        font= ("arial", 12),
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
        font= ("arial", 12),
        bg="black",
        fg="white",
        selectcolor= "black"
    ).pack(anchor="w")

########################## PANEL DE BRILLO ###############################################

def construir_panel_brillo():
    global var_brillo
    if var_brillo is None:
        var_brillo = tk.DoubleVar(value= 0)

    tk.Label(
        frame_controles,
        text= "Brillo",
        fg= "silver",
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

    construir_panel_brillo_canal_rojo()
    construir_panel_brillo_canal_verde()
    construir_panel_brillo_canal_azul()

def construir_panel_brillo_canal_rojo():
    global var_brillo_canal_rojo
    if var_brillo_canal_rojo is None:
        var_brillo_canal_rojo = tk.DoubleVar (value = 0)

    tk.Label(
        frame_controles,
        text= "Brillo Capa Roja",
        fg= "red",
        bg= "black",
        font= ("arial", 12, "bold")
    ).pack(anchor="w", pady=(0,5))
    
    tk.Scale(
        frame_controles,
        from_= -100,
        to= 100,
        orient= "horizontal",
        variable= var_brillo_canal_rojo,
        command= lambda x: aplicar_brillo_capa_roja(),
        bg= "black",
        highlightbackground= "green",
    
    ).pack(fill= "x")

def construir_panel_brillo_canal_verde():
    global var_brillo_canal_verde
    if var_brillo_canal_verde is None:
        var_brillo_canal_verde = tk.DoubleVar (value = 0)

    tk.Label(
        frame_controles,
        text= "Brillo Capa verde",
        fg= "green",
        bg= "black",
        font= ("arial", 12, "bold")
    ).pack(anchor="w", pady=(0,5))
        
    tk.Scale(
        frame_controles,
        from_= -100,
        to= 100,
        orient= "horizontal",
        variable= var_brillo_canal_verde,
        command= lambda x: aplicar_brillo_capa_verde(),
        bg= "black",
        highlightbackground= "green",
        
    ).pack(fill= "x")

def construir_panel_brillo_canal_azul():
    global var_brillo_canal_azul
    if var_brillo_canal_azul is None:
        var_brillo_canal_azul = tk.DoubleVar (value = 0)

    tk.Label(
        frame_controles,
        text= "Brillo Capa azul",
        fg= "blue",
        bg= "black",
        font= ("arial", 12, "bold")
    ).pack(anchor="w", pady=(0,5))
        
    tk.Scale(
        frame_controles,
        from_= -100,
        to= 100,
        orient= "horizontal",
        variable= var_brillo_canal_azul,
        command= lambda x: aplicar_brillo_capa_azul(),
        bg= "black",
        highlightbackground= "green",
        
    ).pack(fill= "x")


####################### PANEL ESCALA DE GRISES ##############################################################

def construir_panel_grises():

    global var_gris_promedio, var_gris_midgray, var_gris_luminosidad

    if var_gris_promedio is None:
        var_gris_promedio = tk.BooleanVar()
        var_gris_midgray = tk.BooleanVar()
        var_gris_luminosidad = tk.BooleanVar()

    tk.Label(
        frame_controles,
        text= "SELECCIONAR GRIS ",
        justify= "center",
        font=("arial",16, "bold"),
        fg= "white",
        bg="black"
    ).pack(anchor="w", pady=(0,5))
    
    tk.Checkbutton(
        frame_controles,
        text= "Promedio",
        variable= var_gris_promedio,
        command= aplicar_grises,
        font= ("arial", 12),
        bg= "black",
        fg= "#F0E68C",
        selectcolor="black"
    ).pack(anchor="w")

    tk.Checkbutton(
        frame_controles,
        text= "Midgray",
        variable= var_gris_midgray,
        command= aplicar_grises,
        font= ("arial", 12),
        bg= "black",
        fg= "#D3D3D3",
        selectcolor="black"
    ).pack(anchor="w")

    tk.Checkbutton(
        frame_controles,
        text= "Luminosidad",
        variable= var_gris_luminosidad,
        font= ("arial", 12),
        command= aplicar_grises,
        bg= "black",
        fg= "#90EE90",
        selectcolor="black"
    ).pack(anchor="w")






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