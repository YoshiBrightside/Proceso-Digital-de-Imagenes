import copy
from PIL import Image, ImageFont, ImageDraw

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

  def marca_de_agua(self,
                image,
                options={'texto':'text',
                         'tamano':'20',
                         'transparencia':'130'}):
    '''
    Filtro marca de agua. Crea una imagen con el texto deseado y la compone
    con la imagen recibida para obtener la imagen.
    '''
    txt_img = Image.new('RGBA', image.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt_img)
    text = options['texto']
    x, y = int(options['x']), int(options['y'])
    transparency = int(options['transparencia'])
    font = ImageFont.truetype(options['fuente'], int(options['tamano']))
    draw.text((x,y), text, font=font, fill=(255,255,255, transparency))
    image = Image.alpha_composite(image.convert('RGBA'), txt_img)
    image = image.convert('RGB')
    return image

def get_filters():
  '''
  Method that returns a list of all available filters.
  To add a new filter, simply add a filters.append() alongside with a method
  with the same filter name.
  '''
  filters = []
  filters.append(Filter('marca_de_agua',
                        'test',
                        {'texto':{'style':'text_box'},
                        'tamano':{'style':'text_box'},
                        'transparencia':{'style':'text_box'},
                        'x':{'style':'text_box'},
                        'y':{'style':'text_box'},
                        'fuente':{'style':'dropdown',
                                  'values':['Gidole-Regular.ttf',
                                            'Albertus.ttf',
                                            'Avengers.ttf',
                                            'modes.ttf',
                                            'Prompt-Medium.ttf']}}))
  return filters

if __name__ == '__main__':
    print('This file is meant to be used with UniversalImageFilterApplier.py!')

