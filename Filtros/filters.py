class Filter:
  def __init__(self, name, description, options=None):
    self.name = name
    self.description = description
    self.options = options

def apply_filter(filter_name, image, options=None):
  print('filteeer')
  try:
    method = getattr(Filter, filter_name)
  except AttributeError:
    return image
  modded_image = method(image, options)

def test_name(image, options=None):
  print('test_name methoood')

def get_filters():
  filters = []
  filters.append(Filter('test_name', 'test_description', ['test_opt0', 'test_opt1']))
  filters.append(Filter('test_name2', 'test_description2', ['test_opt0', 'test_opt1']))
  return filters
  print('computers are transforming into a noose and a yoke for humans')

if __name__ == '__main__':
    print('This file is meant to be used with UniversalImageFilterApplier.py!')

