from nfa_parser_engine import validate_nfa, parse_config
import sys

if (len(sys.argv) != 3):
  raise Exception("Correct format is: python nfa_acceptance_engine.py <nfa_config_file> <path>")
  sys.exit()

nfa_config_file = sys.argv[1]
path = sys.argv[2]
nfa_structure = parse_config(nfa_config_file)


def test_acceptance(nfa_structure, path):
  
  (sigma, states, initial_states, final_states, transitions) = nfa_structure
  if not validate_nfa(nfa_structure):
    raise Exception("Invalid NFA")

  queue = [[initial_states[0]]]
  # print(queue)
  path_length = len(path)
  while path != "":
    current_letter = path[0]
    queue_length = len(queue)
    for _ in range(queue_length):
      states_chain = queue.pop(0)
      # daca nu se pleaca nicaieri din state-ul curent, continuam cu lantul urmator de state-uri
      if states_chain[-1] not in transitions.keys():
        continue
      
      # verificam fiecare tranzitie, si bagam in coada drumul catre urmatoarea stare
      for (next_state, next_state_letter) in transitions[states_chain[-1]]:
        if next_state_letter == current_letter:
            queue.append(states_chain + [next_state])
    # print(queue)
    path = path[1:]

  # dupa ce am terminat, verificam daca am ajuns la vreo stare finala
  for item in queue:
    if len(item) > path_length and item[-1] in final_states:
      return True
  return False

print(test_acceptance(nfa_structure, path))

