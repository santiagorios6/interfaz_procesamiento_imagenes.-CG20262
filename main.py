import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk 
import imglib 

imagen_original = None
def actualizar_brillo(valor_slider):
    global imagen_original
    if imagen_original is None:
        
        return

    valor = int(valor_slider)
    ima_modificada = imglib.aumentar_brillo

def abrir_imagen():
    ruta = filedialog.askopenfilename(
        title= "Select imagen",
        filetypes= [("archivos de imagen","*.png *.jpg *jpeg")]

    )

    if ruta:
        #cargar la imagen
        imagen = Image.open(ruta)

        #redimensionar imagen
        img = imagen.resize((300, 400))

        #convertir a formato compatible
        image_tk = ImageTk.PhotoImage(img)

        #mostrar imagen

        etiqueta_imagen.config(image= image_tk)
        etiqueta_imagen.image = image_tk
        


ventana = tk.Tk()

ventana.title("Proyecto 1")
ventana.geometry("1000x1000")
ventana.configure(bg = "black")

ventana.resizable(False, False)

frame_imagen = tk.Frame(
    ventana,
    width= 300,
    height= 400,
    bg= "gray",
    highlightbackground= "white",
    highlightthickness="2"
)

frame_imagen.place(x = 1, y = 1)

etiqueta_imagen = tk.Label(
    ventana,
)

etiqueta_imagen.place(x= 1, y = 1)



button = tk.Button(
    ventana, 
    text = "Abrir imagen",
    bg= "gray",
    width=84,
    command = abrir_imagen)
button.place(x=3, y=608)

#================================================================================================================================

slider_brillo = tk.Scale(
    ventana,
    from_= -100, to = 100,
    orient= "horizontal",
    label= "ajustar brillo",
    bg= "gray,",
    command= actualizar_brillo

)
slider_brillo.place(x= 400, y= 1)

ventana.mainloop()