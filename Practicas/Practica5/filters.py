import copy
from PIL import Image, ImageFont, ImageDraw
import math

class Filter:
  def __init__(self, name, description, options=None):
    self.name = name
    self.description = description
    self.options = options

  def apply_filter(self, filter_name, image, options=None):
    '''
    Metodo que invoca el filtro seleccionado a partir de getattr. Una vez
    finalizado el proceso, guarda una imagen temporal como '.temp.jpeg'
    '''
    try:
      method = getattr(Filter, filter_name)
    except AttributeError:
      return image
    modded_image = method(self, image, options)
    if modded_image != None:
      modded_image.save('.temp.jpeg')

  def recursivo(self, image, options=None):
    '''
    Filtro recursivo. Toma una imagen y devuelve una esta hecha con mosaicos
    de si misma. Puede elegir entre grises y rgb, ademas de tamano de
    mosaico.
    '''
    arr = image.load()
    tamano_mosaico = get_matrix_size(options['tamano'])
    imagen_mosaico = copy.deepcopy(image).resize((tamano_mosaico,tamano_mosaico))
    arr_mos = imagen_mosaico.load()
    mosaicos = [[[0, 0, 0] for _ in range(math.ceil(image.height/tamano_mosaico))]
                           for _ in range(math.ceil(image.width/tamano_mosaico))]
    pixeles_por_mosaico = [[0 for _ in range(len(mosaicos[0]))]
                              for _ in range(len(mosaicos))]
    # Primero obtenemos los valores promedio por mosaico
    for x in range(image.width):
      for y in range(image.height):
        mosaicos[x//tamano_mosaico][y//tamano_mosaico][0] += arr[x, y][0]
        mosaicos[x//tamano_mosaico][y//tamano_mosaico][1] += arr[x, y][1]
        mosaicos[x//tamano_mosaico][y//tamano_mosaico][2] += arr[x, y][2]
        pixeles_por_mosaico[x//tamano_mosaico][y//tamano_mosaico] += 1
    for x in range(len(mosaicos)):
      for y in range(len(mosaicos[0])):
        mosaicos[x][y][0] //= pixeles_por_mosaico[x][y]
        mosaicos[x][y][1] //= pixeles_por_mosaico[x][y]
        mosaicos[x][y][2] //= pixeles_por_mosaico[x][y]
    # Aplicamos a la imagen el valor del pixel del mosaico correspondiente
    # mas el valor promedio del mosaico por si mismo
    for x in range(image.width):
      for y in range(image.height):
        if options['tipo'] == 'escala_grises':
          arr[x, y] = ((arr_mos[x%tamano_mosaico, y%tamano_mosaico][0] +
                        mosaicos[x//tamano_mosaico][y//tamano_mosaico][0])//2,
                        (arr_mos[x%tamano_mosaico, y%tamano_mosaico][0] +
                        mosaicos[x//tamano_mosaico][y//tamano_mosaico][0])//2,
                        (arr_mos[x%tamano_mosaico, y%tamano_mosaico][0] +
                        mosaicos[x//tamano_mosaico][y//tamano_mosaico][0])//2)
        else:
          arr[x, y] = ((arr_mos[x%tamano_mosaico, y%tamano_mosaico][0] +
                        mosaicos[x//tamano_mosaico][y//tamano_mosaico][0])//2,
                        (arr_mos[x%tamano_mosaico, y%tamano_mosaico][1] +
                        mosaicos[x//tamano_mosaico][y//tamano_mosaico][1])//2,
                        (arr_mos[x%tamano_mosaico, y%tamano_mosaico][2] +
                        mosaicos[x//tamano_mosaico][y//tamano_mosaico][2])//2)
    return image

def get_matrix_size(s):
  '''
  Recibe un string s con formato NxN, y devuelve el valor N en entero.
  '''
  return int(s.split('x')[0])

def get_filters():
  '''
  Method that returns a list of all available filters.
  To add a new filter, simply add a filters.append() alongside with a method
  with the same filter name.
  '''
  filters = []
  filters.append(Filter('recursivo',
                        'descripcion_prueba',
                        {'tipo':{'style':'dropdown',
                                 'values':['escala_grises','color']},
                         'tamano':{'style':'dropdown',
                                   'values':['5x5','10x10','20x20','30x30']}}))
  return filters

if __name__ == '__main__':
    print('This file is meant to be used with UniversalImageFilterApplier.py!')

