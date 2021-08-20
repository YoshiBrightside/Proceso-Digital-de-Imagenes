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

  def semitonos(self, image, options=None):
    '''
    Definiendo una matriz para simular los puntos en semitonos, aplicamos el
    valor de los semitonos a cada pixel.
    La parte donde se obtienen los valores promedios por mosaico puede volverse
    un metodo independiente, puesto que se usa en el filtro recursivo tambien.
    Actualmente soporta matrices idx con un maximo de 9 valores (ver la
    asignacion del tono al final del metodo).
    '''
    arr = image.load()
    matriz_idx = get_matriz_idx(options['tipo'])
    tamano_mosaico = len(matriz_idx)
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
    # Sustituimos los valores de cada mosaico por su valor respectivo en
    # la matriz de tono que seleccionamos
    for x in range(image.width):
      for y in range(image.height):
        tono = (((arr[x, y][0] + arr[x, y][1] + arr[x, y][2]) // 3) //
                  (255 // (min(tamano_mosaico**2, 9) + 1)))
        if tono >= matriz_idx[x%tamano_mosaico][y%tamano_mosaico]:
          arr[x, y] = (255, 255, 255)
        else:
          arr[x, y] = (0, 0, 0)
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
  filters.append(Filter('semitonos',
                        'test',
                        {'tipo':{'style':'dropdown',
                                 'values':['img2.idx',
                                           'img4.idx',
                                           'img10.idx']}}))
  return filters

if __name__ == '__main__':
    print('This file is meant to be used with UniversalImageFilterApplier.py!')

