def clean_string(input_string:str):
  return input_string.replace('\n', '').replace(' ', '')

def convert_set_to_string(set_item):
  return ''.join(sorted(list(set_item)))