import numpy as np
import matplotlib.pyplot as plt
import PIL.Image as Image


def obtener_capa_roja(imagen): 
    capaR = np.copy(imagen)
    capaR [:,:,1] = capaR[:,:,2] = 0
    return capaR

def obtener_capa_verde(imagen):
    capaG = np.copy(imagen)
    capaG[:,:,0] = capaG[:,:,2] = 0
    return capaG
def obtener_capa_azul(imagen):
    capaB = np.copy(imagen)
    capaB[:,:,0] = capaB[:,:,1] = 0
    return capaB


def obtener_capa_amarilla(imagen):
    capaY = np.copy(imagen)
    capaY[:,:,2] = 0
    return capaY

def obtener_capa_celeste(imagen):
    capaC = np.copy(imagen)
    capaC[:,:,0] = 0
    return capaC

def obtener_capa_morada(imagen):
    capaM = np.copy(imagen)
    capaM[:,:,1] = 0
    return capaM


def invertir_color(imagen):

    imagen_invertida =  255 - imagen

    return imagen_invertida



def suma_imagenes(img_fondo, img_sobrepuesta):
    h, w = img_fondo.shape[:2]
    img_sobrepuesta = np.array(Image.fromarray(img_sobrepuesta).resize((w, h)))

    A = img_fondo.astype(np.uint16)
    B = img_sobrepuesta.astype(np.uint16)

    fusion = (A + B)/2
    fusion = np.clip(fusion, 0, 255).astype(np.uint8)

    return fusion


def aplicar_brillo(imagen, valor_brillo):

    img_brillo = imagen.astype(np.float32)
    imagen_clip = np.clip(img_brillo + valor_brillo, 0, 255).astype(np.uint8)

    return imagen_clip


def  aplicar_brillo_capa_roja(imagen, valor_brillo):

    img_brillo_rojo = imagen.astype(np.float32).copy()

    img_brillo_rojo[:,:,0] = np.clip(img_brillo_rojo[:,:,0] + valor_brillo, 0, 255)
    img_brillo_rojo = img_brillo_rojo.astype(np.uint8)

    return img_brillo_rojo


def  aplicar_brillo_capa_verde(imagen, valor_brillo):

    img_brillo_verde = imagen.astype(np.float32).copy()

    img_brillo_verde[:,:,1] = np.clip(img_brillo_verde[:,:,1] + valor_brillo, 0, 255)
    img_brillo_verde = img_brillo_verde.astype(np.uint8)

    return img_brillo_verde


def  aplicar_brillo_capa_azul(imagen, valor_brillo):

    img_brillo_azul = imagen.astype(np.float32).copy()

    img_brillo_azul[:,:,2] = np.clip(img_brillo_azul[:,:,2] + valor_brillo, 0, 255)
    img_brillo_azul = img_brillo_azul.astype(np.uint8)

    return img_brillo_azul

def aplicar_gris_promedio(imagen):
    img_gris_promedio = imagen.astype(np.float32)
    img_gris_promedio = ((img_gris_promedio[:,:,0] + img_gris_promedio[:,:,1] + img_gris_promedio[:,:,2])/3).astype(np.uint8)
    return img_gris_promedio

def aplicar_gris_midgray(imagen):
    img_gris_midgray = imagen.astype(np.float32)

    mx = np.max(imagen, axis= 2)
    mn = np.min(imagen, axis= 2)

    img_gris_midgray = (mx + mn) / 2

    img_gris_midgray = np.clip(img_gris_midgray, 0, 255).astype(np.uint8)

    return img_gris_midgray

def aplicar_gris_luminosidad(imagen):
    img_luminosa = imagen.astype(np.float32)

    img_luminosa = 0.299*imagen[:,:,0] + 0.587*imagen[:,:,1] + 0.114*imagen[:,:,2]

    img_luminosa = np.clip(img_luminosa, 0, 255).astype(np.uint8)

    return img_luminosa

def aplicar_binarisacion(imagen, valor_umbral):

    img = imagen.astype(np.float32)
    img_bin = 0.299*img[:,:,0] + 0.587*img[:,:,1] + 0.14*img[:,:,2]

    T = valor_umbral

    img_bin = np.where(img_bin >= T, 255, 0).astype(np.uint8)

    return img_bin


def recorte(imagen, xini, xfin, yini, yfin):

    alto, ancho = imagen.shape[:2]

    xini = max(0, int(xini))
    xfin = min(ancho, int(xfin))
    yini = max(0, int(yini))
    yfin = min(alto, int(yfin))

    return imagen[yini:yfin,xini:xfin]


def histograma(imagen):

    if imagen.max() <= 1.0:
        imagen = (imagen * 255).astype(np.uint8)

    R = imagen[:,:,0]
    G = imagen[:,:,1]
    B = imagen[:,:,2]

    return R,G,B

def reduccion_resolucion(imagen, valordereduccion):
    f = int(max(1, valordereduccion))

    img_reducida = imagen[::f, ::f]

    return img_reducida


def zoom(imagen, valor_zoom):

    h, w = imagen.shape[:2]

    zoom_area = int(valor_zoom)

    start_row = h // 2 - zoom_area // 2
    end_row = h // 2 + zoom_area // 2
    start_colum = w // 2 - zoom_area // 2
    end_colum = w // 2 +zoom_area //2


    recorte = imagen[start_row:end_row, start_colum:end_colum]

    zoom_factor = 5 

    zoomed = np.kron(recorte, np.ones((zoom_factor, zoom_factor, 1)))

    zoomed = zoomed.astype(imagen.dtype)

    return 






    