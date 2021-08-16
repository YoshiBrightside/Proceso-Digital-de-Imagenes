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
    try:
      method = getattr(Filter, filter_name)
    except AttributeError:
      return image
    modded_image = method(self, image, options)

  def gray_tone(self, image, options={'filter_type':StringVar('RGB')}):
    arr = image.load()
    for x in range(image.width):
      for y in range(image.height):
        if options['filter_type'].get() == 'RGB':
          grey = (arr[x, y][0] + arr[x, y][1] + arr[x, y][2])//3
        if options['filter_type'].get() == 'R.3G.59B.11':
          grey = int(arr[x, y][0]*.3) + int(arr[x, y][1]*.59) + int(arr[x, y][2]*.11)
        if options['filter_type'].get() == 'R.21G.71B.07':
          grey = int(arr[x, y][0]*.21) + int(arr[x, y][1]*.71) + int(arr[x, y][2]*.07)
        if options['filter_type'].get() == 'RmaxGBmin':
          grey = (max(arr[x, y][0], arr[x, y][1], arr[x, y][2]) +
                  min(arr[x, y][0], arr[x, y][1], arr[x, y][2])) // 2
        if options['filter_type'].get() == 'Max':
          grey = max(arr[x, y][0], arr[x, y][1], arr[x, y][2])
        if options['filter_type'].get() == 'Min':
          grey = min(arr[x, y][0], arr[x, y][1], arr[x, y][2])
        if options['filter_type'].get() == 'R':
          grey = arr[x, y][0]
        if options['filter_type'].get() == 'G':
          grey = arr[x, y][1]
        if options['filter_type'].get() == 'B':
          grey = arr[x, y][2]
        arr[x, y] = (grey, grey, grey)

  def brightness(self, image, options={'quantity':StringVar('10')}):
    arr = image.load()
    for x in range(image.width):
      for y in range(image.height):
        modifier = int(options['quantity'].get())
        arr[x, y] = (min(max(arr[x, y][0] + modifier, 0), 255),
                     min(max(arr[x, y][1] + modifier, 0), 255),
                     min(max(arr[x, y][2] + modifier, 0), 255))

  def mosaic(self, image, options={'size':StringVar('10')}):
    arr = image.load()
    w, h = image.width, image.height
    size = int(options['size'].get())
    x, y, r, g, b, m, n = 0, 0, 0, 0, 0, 0, 0
    while x < w:
      m = size if (x + size) < w else w-x
      while y < h:
        n = size if (y + size) < h else h-y
        for i in range(m):
          for j in range(n):
            r, g, b = r + arr[i+x, j+y][0], g + arr[i+x, j+y][1], b + arr[i+x, j+y][2]
        r, g, b = r//(m*n), g//(m*n), b//(m*n)
        for i in range(m):
          for j in range(n):
            arr[i+x, j+y] = (r, g, b)
        y += n
        r, g, b = 0, 0, 0
      x += m
      y = 0


def get_filters():
  '''
  Method that returns a list of all available filters.
  To add a new filter, simply add a filters.append() alongside with a method
  with the same filter name.
  '''
  filters = []
  filters.append(Filter('gray_tone',
                        'test_description',
                        {'filter_type':{'style':'dropdown',
                                        'values':['RGB', 'R.3G.59B.11',
                                                 'R.21G.71B.07',
                                                 'RmaxGBmin', 'Max',
                                                 'Min', 'R', 'G', 'B']}}))
  filters.append(Filter('brightness', 
                        'test_description2',
                        {'quantity':{'style':'dropdown',
                                     'values':['10','-10']}}))
  filters.append(Filter('mosaic',
                        'test_description',
                        {'size':{'style':'dropdown',
                                 'values':['10','20','30']}}))
  return filters

if __name__ == '__main__':
    print('This file is meant to be used with UniversalImageFilterApplier.py!')

