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
      modded_image.save('.temp.jpeg', quality=100)

  def minimo(self, image, options=None):
    '''
    A partir del tamanio de la matriz, se busca en la vecindad el pixel con
    el valor mas blanco, y se escribe sobre el pixel central.
    '''
    copia_imagen = copy.deepcopy(image)
    arr = image.load()
    copy_arr = copia_imagen.load()
    tamano_mosaico = get_matrix_size(options['tamano'])
    for x in range(image.width):
      for y in range(image.height):
        tono = 0
        for i in range(x-tamano_mosaico//2, x+tamano_mosaico//2):
          for j in range(y-tamano_mosaico//2, y+tamano_mosaico//2):
            if i > 0 and i < image.width and j > 0 and j < image.height:
              tono = max(((copy_arr[i, j][0] + copy_arr[i, j][1] + copy_arr[i, j][2])//3),
                          tono)
        arr[x, y] = (tono, tono, tono)
    return image


  def maximo(self, image, options=None):
    '''
    A partir del tamanio de la matriz, se busca en la vecindad el pixel con
    el valor mas oscuro, y se escribe sobre el pixel central.
    '''
    copia_imagen = copy.deepcopy(image)
    arr = image.load()
    copy_arr = copia_imagen.load()
    tamano_mosaico = get_matrix_size(options['tamano'])
    for x in range(image.width):
      for y in range(image.height):
        tono = 255
        for i in range(x-tamano_mosaico//2, x+tamano_mosaico//2):
          for j in range(y-tamano_mosaico//2, y+tamano_mosaico//2):
            if i > 0 and i < image.width and j > 0 and j < image.height:
              tono = min(((copy_arr[i, j][0] + copy_arr[i, j][1] + copy_arr[i, j][2])//3),
                          tono)
        arr[x, y] = (tono, tono, tono)
    return image

def get_matriz_idx(s):
  '''
  Devuelve una matriz que representa la coleccion de semitonos a usar. Se
  compone de una matriz con el valor minimo para activar cada una de las
  celdas.
  '''
  n = int(s.split('.')[0][3:])
  if n == 2:
    return [[4, 2],
            [1, 3]]
  if n == 4:
    return [[8, 3, 7],
            [5, 1, 2],
            [4, 9, 6]]
  if n == 10:
    return [[9, 8, 7, 6, 7, 8, 9],
            [8, 6, 5, 4, 5, 6, 8],
            [7, 5, 3, 2, 3, 5, 7],
            [6, 4, 2, 1, 2, 4, 6],
            [7, 5, 3, 2, 3, 5, 7],
            [8, 6, 5, 4, 5, 6, 8],
            [9, 8, 7, 6, 7, 8, 9]]

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
  filters.append(Filter('minimo',
                        '',
                        {'tamano':{'style':'dropdown',
                                 'values':['3x3',
                                           '5x5',
                                           '7x7',
                                           '9x9']}}))
  filters.append(Filter('maximo',
                        '',
                        {'tamano':{'style':'dropdown',
                                 'values':['3x3',
                                           '5x5',
                                           '7x7',
                                           '9x9']}}))
  return filters

if __name__ == '__main__':
    print('This file is meant to be used with UniversalImageFilterApplier.py!')

