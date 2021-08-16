import copy

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

  def high_contrast(self, image, options=None):
    self.inverse(image)
    self.inverse(image)

  def inverse(self, image, options=None):
    arr = image.load()
    for x in range(image.width):
      for y in range(image.height):
        if arr[x, y][0] > 127 and arr[x, y][1] > 127 and arr[x, y][2] > 127:
          arr[x, y] = (0, 0, 0)
        else:
          arr[x, y] = (255, 255, 255)

  def rgb_filter(self, image, options={'channel':StringVar('Red')}):
    arr = image.load()
    for x in range(image.width):
      for y in range(image.height):
        if options['channel'].get() == 'Red':
          arr[x, y] = (arr[x, y][0], 0, 0)
        if options['channel'].get() == 'Green':
          arr[x, y] = (0, arr[x, y][1], 0)
        if options['channel'].get() == 'Blue':
          arr[x, y] = (0, 0, arr[x, y][2])

  def convolusion(self, image, matrix):
    img_copy = copy.deepcopy(image)
    arr = image.load()
    copy_arr = img_copy.load()
    for x in range(image.width):
      for y in range(image.height):
        new_value = [0, 0, 0]
        pixel_count = 0
        for mx in range(len(matrix)):
          for my in range(len(matrix)):
            cur_pixel = [x+mx-(len(matrix)//2), y+my-(len(matrix)//2)]
            if (matrix[mx][my] and
                cur_pixel[0] < image.width and cur_pixel[0] >= 0 and
                cur_pixel[1] < image.height and cur_pixel[1] >= 0):
              new_value[0] += copy_arr[cur_pixel[0], cur_pixel[1]][0]*matrix[mx][my]
              new_value[1] += copy_arr[cur_pixel[0], cur_pixel[1]][1]*matrix[mx][my]
              new_value[2] += copy_arr[cur_pixel[0], cur_pixel[1]][2]*matrix[mx][my]
              pixel_count += abs(matrix[mx][my])
        arr[x, y] = (int(new_value[0]/pixel_count),
                     int(new_value[1]/pixel_count),
                     int(new_value[2]/pixel_count))
        pixel_count = 0
    

  def blur(self, image, options={'size':StringVar('3x3')}):
    size = get_matrix_size(options['size'].get())
    if size == 3:
      matrix =[[0, .2, 0],
              [.2, .2, .2],
              [0, .2, 0]]
    else:
      matrix =[[0, 0, 1, 0, 0],
              [0, 1, 1, 1, 0],
              [1, 1, 1, 1, 1],
              [0, 1, 1, 1, 0],
              [0, 0, 1, 0, 0]]
    self.convolusion(image, matrix)

  def motion_blur(self, image, options={'size':StringVar('9x9')}):
    matrix =[[1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 1]]
    self.convolusion(image, matrix)

  def find_edges(self, image, options={'size':StringVar('5x5')}):
    matrix =[[-1, 0, 0, 0, 0],
             [ 0, -2, 0, 0, 0],
             [ 0, 0, 6, 0, 0],
             [ 0, 0, 0, -2, 0],
             [ 0, 0, 0, 0, -1]]
    self.convolusion(image, matrix)
    return

  def sharpen(self, image, options={'size':StringVar('3x3')}):
    matrix =[[-1, -1, -1],
             [-1, 9, -1],
             [-1, -1, -1]]
    self.convolusion(image, matrix)
    return

  def emboss(self, image, options={'size':StringVar('5x5')}):
    matrix =[[-1, -1, -1, -1, 0],
             [-1, -1, -1, 0, -1],
             [-1, -1, 0, -1, -1],
             [-1, 0, -1, -1, -1],
             [ 0, -1, -1, -1, -1]]
    self.convolusion(image, matrix)
    return

def get_matrix_size(s):
  return int(s.split('x')[0])

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

