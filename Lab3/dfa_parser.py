from utils import clean_string

def parse_config(file_name):
 
  sigma = []
  states = []
  initial_states = []
  final_states = []
  transitions = {}
 

  try:
    input_file = open(file_name, 'r')
  except FileNotFoundError:  
    return None

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
        
        # Parse the only if it's not an empty string
        if clean_string(line) == '':
          line = input_file.readline()
          continue
        
        line = clean_string(line)
        [state1, road, state2] = line.split(',')

        if state1 in transitions:
          transitions[state1].append((state2, road))
        else:
          transitions[state1] = [(state2, road)]
        line = input_file.readline()
  input_file.close()
  return (sigma, states, initial_states, final_states, transitions)