import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk 
from matplotlib.widgets import Slider
import numpy as np
import imglib 
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#variables Globales

imagen_Original = None
imagen_superpocicion = None

#Colores
var_verde = None
var_azul = None
var_rojo = None
var_amarillo = None
var_celeste = None
var_morado = None
var_brillo = None
var_negativo = None
#Brillo
var_brillo_canal_rojo = None
var_brillo_canal_verde = None
var_brillo_canal_azul = None
var_gris_promedio = None
var_gris_midgray = None
var_gris_luminosidad = None 
var_umbral = None
#Recorte
xinicio = None 
yinicio = None
rectangulo_id = None
#Zoom
var_zoom = None
zoom_actual = 1.0
offset_x = 0
offset_y = 0
imagen_zoom_actual = None
#Reduccion de Resolucio
var_reduccion = None
#rotacion
var_rotacion = None

###############Funciones#############################

def mostrar_en_etiqueta(arreglo):
    imagen_resultado = Image.fromarray(arreglo)
    imagen_resultado = imagen_resultado.resize((400, 400))
    imagen_tk = ImageTk.PhotoImage(imagen_resultado)

    etiqueta_imagen.delete("all")
    etiqueta_imagen.create_image(200, 200, anchor="center", image= imagen_tk)
    etiqueta_imagen.image = imagen_tk


def abrir_imagen():

    global imagen_Original
    ruta = filedialog.askopenfilename(
        title= "Seleccione la imagen",
        filetypes=[("archivos de Imagen", "*.png *.jpg *.jpeg")]
    
    )

    if ruta:
        imagen_Original = Image.open(ruta)
        arreglo = np.array(imagen_Original)
       
        mostrar_en_etiqueta(arreglo)

def abrir_imagen_sobrepocicion():
    global imagen_superpocicion
    ruta = filedialog.askopenfilename(
            title= "Seleccione la imagen",
            filetypes=[("archivos de Imagen", "*.png *.jpg *.jpeg")]
    )

    if ruta: 
        imagen_superpocicion = Image.open(ruta)
        imagen_numpy = np.array(imagen_superpocicion)
        messagebox.showinfo("Exito", "Imagen cargada correctamente")


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


def aplicar_umbral():
    if imagen_Original is None:
        messagebox.showwarning("error de imagen", "No se encontro imagen seleccionada")
        return 

    arreglo = np.array(imagen_Original)
    resultado = imglib.aplicar_binarisacion(arreglo, var_umbral.get())

    mostrar_en_etiqueta(resultado)


def aplicar_suma():
    if imagen_Original is None or imagen_superpocicion is None:
        messagebox.showwarning("Faltan Imagenes", "debes cargar la imagen principal y la imagen a sumar")
        return

    arreglo_fondo = np.array(imagen_Original)
    arreglo_sobre = np.array(imagen_superpocicion)
    resultado = imglib.suma_imagenes(arreglo_fondo, arreglo_sobre)

    mostrar_en_etiqueta(resultado)


def mostrar_histograma():
    if imagen_Original is None:
        return

    arreglo = np.array(imagen_Original)
    R,G,B = imglib.histograma(arreglo)

    fig = plt.figure(figsize=(5, 4), dpi=90)
    ax = fig.add_subplot(111)
    
    ax1 = fig.add_subplot(311)
    ax1.hist(R.ravel(), bins=256, color='red')
    ax1.set_title('Canal Rojo', fontsize=9)
    ax1.tick_params(labelsize=7)
    
    # --- Gráfico 2: Verde ---
    ax2 = fig.add_subplot(312)
    ax2.hist(G.ravel(), bins=256, color='green')
    ax2.set_title('Canal Verde', fontsize=9)
    ax2.tick_params(labelsize=7)
    
    # --- Gráfico 3: Azul ---
    ax3 = fig.add_subplot(313)
    ax3.hist(B.ravel(), bins=256, color='blue')
    ax3.set_title('Canal Azul', fontsize=9)
    ax3.tick_params(labelsize=7)


    for widget in frame_grafico.winfo_children():
        widget.destroy()

    fig.tight_layout()
    canvas_hist = FigureCanvasTkAgg(fig, master=frame_controles)
    canvas_hist.draw()
    canvas_hist.get_tk_widget().pack(fill="both", expand=True)

def actualizar_zoom():
    global imagen_zoom_actual, offset_x, offset_y

    if imagen_zoom_actual is None:
        return

    img_pil = Image.fromarray(imagen_zoom_actual)
    img_tk = ImageTk.PhotoImage(img_pil)


    etiqueta_imagen.delete("all")
    etiqueta_imagen.create_image(offset_x, offset_y, anchor="nw", image=img_tk)
    etiqueta_imagen.image= img_tk

def aplicar_zoom_slider():
    global imagen_zoom_actual, zoom_actual, offset_x, offset_y

    if imagen_Original is None:
        return

    zoom_actual = var_zoom.get()

    arreglo = np.array(imagen_Original)
    resultado = imglib.zoom(arreglo, zoom_actual)
    imagen_zoom_actual = resultado


    offset_x = 0
    offset_y = 0 
    actualizar_zoom()

def mover_imagen(dx, dy):
    global offset_x, offset_y

    if imagen_zoom_actual is None:
        return

    offset_x += dx
    offset_y += dy
    actualizar_zoom()

def resetear_zoom():
    global offset_x, offset_y

    offset_y = 0
    offset_x = 0
    actualizar_zoom()

def aplicar_reduccion():
    if imagen_Original is None:
        return

    factor = int(var_reduccion.get())
    arreglo = np.array(imagen_Original)
    resultado = imglib.reduccion_resolucion(arreglo, factor)

    mostrar_en_etiqueta(resultado)

def aplicar_rotacion(angulo):
    if imagen_Original is None:
        return

    
    arreglo = np.array(imagen_Original)

    resultado = imglib.rotar_manual(arreglo, angulo, fondo = 0)

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

    elif seleccion == "Suma de Imgenes":
        construir_panel_sumar()

    elif seleccion == "Geometria":
        construir_panel_geometria()

    elif seleccion == "Histograma":
        construir_panel_histograma()


    else:
        tk.Label(
            frame_controles,
            text=f"Categoría: {seleccion}\n(Aquí irán los controles)", 
            bg="black", 
            fg="white", 
            font=("arial", 14)
        ).pack(pady=50)

def iniciar_recorte(evento):
    global xinicio, yinicio, rectangulo_id

    xinicio = evento.x
    yinicio = evento.y

    if rectangulo_id is not None:
        etiqueta_imagen.delete(rectangulo_id)


    rectangulo_id = etiqueta_imagen.create_rectangle(
        xinicio, yinicio, xinicio, yinicio,
        outline="red", width=2
    )


def actualizar_recorte(evento):
    global rectangulo_id
    if rectangulo_id is not None:
        etiqueta_imagen.coords(rectangulo_id, xinicio, yinicio, evento.x, evento.y)


def finalizar_recorte(evento):
    global xinicio, yinicio, rectangulo_id

    if xinicio is None or yinicio is None:
        return

    xfin = evento.x
    yfin = evento.y


    if imagen_Original is not None:
        ancho_real, alto_real = imagen_Original.size
        ancho_canvas = etiqueta_imagen.winfo_width()
        alto_canvas = etiqueta_imagen.winfo_height()

        x_ini_real = (xinicio / ancho_canvas)* ancho_real
        x_fin_real = (xfin / ancho_canvas)* ancho_real
        y_ini_real = (yinicio / alto_canvas)* alto_real
        y_fin_real = (yfin / alto_canvas)* alto_real

        arreglo = np.array(imagen_Original)
        resultado = imglib.recorte(arreglo, x_ini_real, x_fin_real, y_ini_real, y_fin_real)

        mostrar_en_etiqueta(resultado)

        etiqueta_imagen.delete(rectangulo_id)
        rectangulo_id = None
############################## PANEL DE COLORES ##################################################
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


    construir_panel_umbral()


def construir_panel_umbral():
    global var_umbral

    if var_umbral is None:
        var_umbral = tk.DoubleVar(value=0)

   

    tk.Label(
        frame_controles,
        text= "Umbralizacion",
        fg= "white",
        bg= "black",
        font= ("arial", 12),
    ).pack(anchor="w", pady=(0,5))


    tk.Scale(
        frame_controles,
        from_= 0,
        to= 255,
        orient= "horizontal",
        variable= var_umbral,
        command= lambda x: aplicar_umbral(),
        bg= "black",
        fg= "white",
        highlightbackground= "gray"
    ).pack(fill= "x")


def construir_panel_sumar():

    tk.Label(
        frame_controles,
        text= "Suma de Imagenes",
        fg= "white",
        bg= "black",
        font= ("Arial", 16)

    ).pack(anchor="w", pady=(0,10))

    tk.Label(
        frame_controles,
        text="Carga la segunda Imagen",
        fg="white",
        bg= "black",
        font=("arial", 11)

    ).pack(anchor="w", pady=(5,0))

    tk.Button(
        frame_controles,
        text="Carga Imagen a Sumar",
        command= abrir_imagen_sobrepocicion,
        bg="gray",

    ).pack(fill= "x", pady=(0,15))

    tk.Label(
        frame_controles,
        text="2. Aplica la fusión:",
        fg="silver",
        bg="black",
        font=("arial", 11)
    ).pack(anchor="w", pady=(5, 0))

    tk.Button(
        frame_controles,
        text="Sumar Imágenes",
        command=aplicar_suma,
        bg="green",
        fg="white"
    ).pack(fill="x", pady=5)


def construir_panel_histograma():
    global frame_grafico

    tk.Label(
        frame_controles,
        text="Histograma",
        fg="white",
        bg="black",

    ).pack(anchor="w", pady=(0,10))

    tk.Label(
        frame_controles,
        text="Generar Histograma",
        fg= "silver",
        bg="black",
        
    ).pack(anchor= "w", pady= (0, 15))


    tk.Button(
        frame_controles,
        text= "Mostrar Histograma",
        command= mostrar_histograma,
        bg="gray"
    ).pack(fill="x")

    frame_grafico = tk.Frame(
        frame_controles,
        bg= "black",
    
    )
    frame_grafico.pack(fill="both", expand= True)

############# RECORTE #######################################################################################

def construir_panel_geometria():
    global xinicio, yinicio, rectangulo_id

    xinicio = None
    yinicio = None
    rectangulo_id = None


    tk.Label(
        frame_controles,
        text= "Geometria",
        fg= "white",
        bg= "black",
        font= ("arial", 16),
    ).pack(anchor="w", pady=(0,10))

    tk.Button(
        frame_controles,
        text= "Activar Recorte",
        command=activar_modo_recorte,
        bg= "gray",

    ).pack(fill="x", pady=5)

    construir_zoom()
    reduccion_resolucion()
    rotacion()
    

def activar_modo_recorte():
    etiqueta_imagen.bind("<ButtonPress-1>", iniciar_recorte)
    etiqueta_imagen.bind("<B1-Motion>", actualizar_recorte)
    etiqueta_imagen.bind("<ButtonRelease-1>", finalizar_recorte)

def construir_zoom():
    global var_zoom
    if var_zoom is None:
        var_zoom = tk.DoubleVar(value= 100.0)

    tk.Label(
        frame_controles,
        text="ZOOM",
        fg="white",
        bg="black",
        font= ("arial", 12)
    ).pack(anchor= "w", pady= (0,5))

    tk.Scale(
        frame_controles,
        from_= 10,
        to= 300,
        resolution= 10,
        orient= "horizontal",
        variable= var_zoom,
        command= lambda x: aplicar_zoom_slider(),
        bg= "black",
        highlightbackground= "green",

    ).pack(fill= "x")


    #controles

    frame_mover = tk.Frame(
        frame_controles,
        bg="black",

    )
    frame_mover.pack(pady= 5)

    tk.Button(
        frame_mover,
        text= "Arriba",
        command= lambda:mover_imagen(0,-30),
        width= 3,

    ).grid(row= 0, column= 1)

    tk.Button(
            frame_mover,
            text= "Izq",
            command= lambda:mover_imagen(-30, 0),
            width= 3,
    
        ).grid(row= 1, column= 0)

    tk.Button(
            frame_mover,
            text= "reset",
            command= lambda:resetear_zoom(),
            width= 5,
    
        ).grid(row= 1, column= 1)

    tk.Button(
            frame_mover,
            text= "Derecha",
            command= lambda:mover_imagen(30,0),
            width= 3,
    
        ).grid(row= 1, column= 2)
    
    tk.Button(
            frame_mover,
            text= "Abajo",
            command= lambda:mover_imagen(0, 30),
            width= 3,
    
        ).grid(row= 2, column= 1)


    tk.Frame(
        frame_controles,
        height=2,
        bg= "gray",

    ).pack(fill= "x", pady=10)

def reduccion_resolucion():

    global var_reduccion

    if var_reduccion is None:
        var_reduccion = tk.DoubleVar(value= 1.0)
        
    tk.Label(
        frame_controles,
        text="Reducción de Resolución", 
        fg="white", 
        bg="black", 
        font=("arial", 12, "bold")
    ).pack(anchor="w", pady=(0, 5))

    tk.Scale(
        frame_controles,
        from_= 1,
        to= 30,
        resolution= 1,
        orient= "horizontal",
        variable= var_reduccion,
        command= lambda x: aplicar_reduccion(),
        bg= "black",
        highlightbackground="gray",

    ).pack(fill="x")

    tk.Label(
        frame_controles,
        text="(1 = Normal, 10 = Muy pequeña)",
        fg="gray", bg="black",
        font=("arial", 9),
    ).pack(anchor="w")


def rotacion():
    tk.Frame(
        
        frame_controles, 
        height=2, 
        bg="gray"
        ).pack(fill="x", pady=10)
    
    tk.Label(
        frame_controles,
        text="Rotación", 
        fg="white", bg="black", 
        font=("arial", 12, "bold")
    ).pack(anchor="w", pady=(0, 5))

    frame_botones_rot = tk.Frame(frame_controles, bg="black")
    frame_botones_rot.pack(fill="x", pady=5)

    
    tk.Button(
        frame_botones_rot, 
        text="⬅ Girar Izquierda", 
        command=lambda: aplicar_rotacion(90), 
        bg="gray"
    ).pack(side="left", expand=True, fill="x", padx=2)

    
    tk.Button(
        frame_botones_rot, 
        text="Girar Derecha ➡", 
        command=lambda: aplicar_rotacion(-90), 
        bg="gray"
    ).pack(side="left", expand=True, fill="x", padx=2)

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


etiqueta_imagen = tk.Canvas(
    frame_imagen,
    bg="black",
    highlightthickness=0
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