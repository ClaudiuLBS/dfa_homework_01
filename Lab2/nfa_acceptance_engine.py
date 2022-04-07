from nfa_parser_engine import validate_nfa, parse_config
import sys

nfa_config_file = 'nfa_config_file'
nfa_structure = parse_config(nfa_config_file)
valid = validate_nfa(nfa_structure)

print(nfa_structure[4])
def test_acceptance(path):
  
  nfa_structure = parse_config(sys.argv[1])
  (sigma, states, initial_states, final_states, transitions) = nfa_structure

  if not validate_nfa(nfa_structure):
    raise Exception("Invalid NFA")

  current_state = initial_states[0]
  while path != "":
    current_letter = path[0]
    letter_found = False
    if current_state not in transitions.keys():
      return False    

    for (next_state, next_state_letter) in transitions[current_state]:
      if next_state_letter == current_letter:
        letter_found = True
        current_state = next_state
        path = path[1:]
        break
    if letter_found == False:
      return False
  

  if current_state not in final_states:
    return False

  return True


