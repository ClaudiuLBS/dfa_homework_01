def clean_string(input_string:str):
  return input_string.replace('\n', '').replace(' ', '')

def parse_config(file_name):
  sigma = []
  states = []
  initial_states = []
  final_states = []
  transitions = {}
 
  input_file = open(file_name, 'r')
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
  input_file.close()
  return (sigma, states, initial_states, final_states, transitions)


def pretty_print(input_matrix:dict):
  for key in input_matrix.keys():
    print(f'{key}: ', end='')
    for item in input_matrix[key]:
      print(f'({item[0]}, {item[1]}) ', end='')
    print()

def validate_nfa(nfa_structure):
  (sigma, states, initial_states, final_states, transitions) = nfa_structure
  if len(initial_states) != 1 or len(final_states)==0:
    return False
  for start_state in transitions.keys():
    # drumu nu pleaca dintr-un state valid
    if start_state not in states:
      return False
    # daca exista 2 tranzitii egale, de ex (q1, a, q2), (q1, a, q2)
    if len(transitions[start_state]) != len(set(transitions[start_state])):
      return False

    for end_state,transition_letter in transitions[start_state]:
      # nu-i litera in alfabet
      if transition_letter not in sigma:
        return False
      # drumu nu duce la un state valid
      if end_state not in states:
        return False

  return True

# print(validate_nfa(parse_config('nfa_config_file')))
# pretty_print(parse_config('nfa_config_file')[4])