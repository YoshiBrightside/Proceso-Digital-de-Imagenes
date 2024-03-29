import copy
from PIL import Image, ImageFont, ImageDraw

class StringVar():
  '''
  class StringVar just so we can skip using horrible tkinter's StringVar class
  '''
  def __init__(self, string):
    self.string = string

  def get(self):
    return self.string

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

  def high_contrast(self, image, options=None):
    '''
    Ver metodo inverse().
    (-) (-) = +
    '''
    self.inverse(image)
    self.inverse(image)
    return image

  def inverse(self, image, options=None):
    '''
    Revisa cada pixel y lo define como negro o blanco, segun los valores rgb
    que tengan. Recibe una imagen.
    '''
    arr = image.load()
    for x in range(image.width):
      for y in range(image.height):
        if arr[x, y][0] > 127 and arr[x, y][1] > 127 and arr[x, y][2] > 127:
          arr[x, y] = (0, 0, 0)
        else:
          arr[x, y] = (255, 255, 255)
    return image

  def rgb_filter(self, image, options={'channel':StringVar('Red')}):
    '''
    Elimina los valores que no sean del canal seleccionado.
    '''
    arr = image.load()
    for x in range(image.width):
      for y in range(image.height):
        if options['channel'].get() == 'Red':
          arr[x, y] = (arr[x, y][0], 0, 0)
        if options['channel'].get() == 'Green':
          arr[x, y] = (0, arr[x, y][1], 0)
        if options['channel'].get() == 'Blue':
          arr[x, y] = (0, 0, arr[x, y][2])
    return image

  def convolusion(self, image, matrix, factor=1, bias=0):
    '''
    Toma una matriz especifica a un filtro y la aplica a una imagen.
    Recibe una imagen, un factor en caso de necesitar normalizar, y un valor
    para compensar los valores rgb de un pixel.
    '''
    img_copy = copy.deepcopy(image)
    arr = image.load()
    copy_arr = img_copy.load()
    for x in range(image.width):
      for y in range(image.height):
        new_value = [0, 0, 0]
        for mx in range(len(matrix)):
          for my in range(len(matrix)):
            cur_pixel = [x+mx-(len(matrix)//2), y+my-(len(matrix)//2)]
            if (matrix[mx][my] and
                cur_pixel[0] < image.width and cur_pixel[0] >= 0 and
                cur_pixel[1] < image.height and cur_pixel[1] >= 0):
              new_value[0] += copy_arr[cur_pixel[0], cur_pixel[1]][0]*matrix[mx][my]
              new_value[1] += copy_arr[cur_pixel[0], cur_pixel[1]][1]*matrix[mx][my]
              new_value[2] += copy_arr[cur_pixel[0], cur_pixel[1]][2]*matrix[mx][my]
        try:
          arr[x, y] = (int(new_value[0]*factor)+bias,
                      int(new_value[1]*factor)+bias,
                      int(new_value[2]*factor)+bias)
        except Exception:
          print(arr[x, y], x, y)
    image.save('.temp.jpeg')
    return image
    

  def blur(self, image, options={'size':StringVar('3x3')}):
    '''
    Filtro para desenfocar imagenes. Recibe una imagen y un valor de matriz.
    '''
    size = get_matrix_size(options['size'].get())
    if size == 3:
      matrix =[[0, .2, 0],
              [.2, .2, .2],
              [0, .2, 0]]
      factor = 1
    else:
      matrix =[[0, 0, 1, 0, 0],
              [0, 1, 1, 1, 0],
              [1, 1, 1, 1, 1],
              [0, 1, 1, 1, 0],
              [0, 0, 1, 0, 0]]
      factor = 1/13
    self.convolusion(image, matrix, factor=factor)

  def motion_blur(self, image, options={'size':StringVar('9x9')}):
    '''
    Filtro para desenfocar imagenes con cierta direccion de movimiento.
    Recibe una imagen y un valor de matriz.
    '''
    matrix =[[1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 1]]
    self.convolusion(image, matrix, factor=(1/9))

  def find_edges(self, image, options={'size':StringVar('5x5')}):
    '''
    Filtro para encontrar orillas. Recibe una imagen y un valor de matriz.
    '''
    matrix =[[-1, 0, 0, 0, 0],
             [ 0, -2, 0, 0, 0],
             [ 0, 0, 6, 0, 0],
             [ 0, 0, 0, -2, 0],
             [ 0, 0, 0, 0, -1]]
    self.convolusion(image, matrix, factor=(1/5))

  def sharpen(self, image, options={'size':StringVar('3x3')}):
    '''
    Filtro para 'afilar' imagenes. Recibe una imagen y un valor de matriz.
    '''
    matrix =[[-1, -1, -1],
             [-1, 9, -1],
             [-1, -1, -1]]
    self.convolusion(image, matrix)

  def emboss(self, image, options={'size':StringVar('5x5')}):
    '''
    Filtro para 'abollar' imagenes. Recibe una imagen y un valor de matriz.
    '''
    matrix =[[-1, -1, -1, -1, 0],
             [-1, -1, -1, 0, 1],
             [-1, -1, 0, 1, 1],
             [-1, 0, 1, 1, 1],
             [ 0, 1, 1, 1, 1]]
    self.convolusion(image, matrix, bias=128)

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
  filters.append(Filter('high_contrast',
                        'test', {}))
  filters.append(Filter('inverse',
                        'test', {}))
  filters.append(Filter('rgb_filter',
                        'test',
                        {'channel':{'style':'dropdown',
                                    'values':['Red','Green','Blue']}}))
  filters.append(Filter('blur',
                        'test',
                        {'size':{'style':'dropdown',
                                 'values':['3x3', '5x5']}}))
  filters.append(Filter('motion_blur',
                        'test',
                        {'size':{'style':'dropdown',
                                 'values':['9x9']}}))
  filters.append(Filter('find_edges',
                        'test',
                        {'size':{'style':'dropdown',
                                 'values':['5x5']}}))
  filters.append(Filter('sharpen',
                        'test',
                        {'size':{'style':'dropdown',
                                 'values':['3x3']}}))
  filters.append(Filter('emboss',
                        'test',
                        {'size':{'style':'dropdown',
                                 'values':['5x5']}}))
  return filters

if __name__ == '__main__':
    print('This file is meant to be used with UniversalImageFilterApplier.py!')

