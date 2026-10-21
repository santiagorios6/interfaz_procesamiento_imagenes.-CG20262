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


"""def obtener_cmy(imagen):

    capaC = np.copy(imagen)
    capaC[:,:,0] = 0

    capaM = np.copy(imagen)
    capaM[:,:,1] = 0

    capaY = np.copy(imagen)
    capaY[:,:,2] = 0 """


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
