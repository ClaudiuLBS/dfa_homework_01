input_file = open('dfa_config_file', 'r')

sigma = []
states = []
initial_states = []
final_states = []
transitions = {}

def clean_string(input_string:str):
  return input_string.replace('\n', '').replace(' ', '')


line = None
while line != '':
  line = input_file.readline()
  if 'sigma' in line.lower():
    line = input_file.readline()
    while line.strip().lower() != 'end':
      sigma.append(clean_string(line))
      line = input_file.readline()

  if 'states' in line.lower():
    line = input_file.readline()
    while line.strip().lower() != 'end':
      line = clean_string(line)
      state_tokens = line.split(',')
      state_tokens[0] = clean_string(state_tokens[0])
      states.append(state_tokens[0])

      if len(state_tokens) > 1:
        if 'F' in state_tokens:
          final_states.append(state_tokens[0])
          # print(state_tokens)
        if 'S' in state_tokens:
          initial_states.append(state_tokens[0])
      line = input_file.readline()

  if 'transitions' in line.lower():
    line = input_file.readline()
    while line.strip().lower() != 'end':
      line = clean_string(line)
      [state1, road, state2] = line.split(',')

      if state1 in transitions:
        transitions[state1].append((state2, road))
      else:
        transitions[state1] = [(state2, road)]
      line = input_file.readline()


def pretty_print(input_matrix:dict):
  for key in input_matrix.keys():
    print(f'{key}: ', end='')
    for item in input_matrix[key]:
      print(f'({item[0]}, {item[1]}) ', end='')
    print()


pretty_print(transitions)
# print(sigma, states, initial_states, final_states ,sep='\n')