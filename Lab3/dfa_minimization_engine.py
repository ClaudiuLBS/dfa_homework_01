from lib2to3.pytree import convert
import sys
from dfa_parser import parse_config
from utils import convert_set_to_string


if len(sys.argv) < 2:
    print("Config file not specified")
    sys.exit()


dfa = parse_config(sys.argv[1])

if dfa is None:
    print("Something went wrong when parsing the dfa config file")
    sys.exit()


def build_pairs_matrix(dfa):
  (sigma, states, initial_states, final_states, transitions) = dfa
  states_count = len(states)
  result_matrix = {}
  contor_care_face_astfel_incat_sa_nu_crape_programul = 0
  for first_state in states:
    contor_care_face_astfel_incat_sa_nu_crape_programul += 1
    copie_contor = contor_care_face_astfel_incat_sa_nu_crape_programul
    if first_state not in result_matrix:
      result_matrix[first_state] = {}

    for second_state in states:
      copie_contor -= 1
      if copie_contor  == 0:
        break

      if (first_state in final_states and second_state not in final_states) or (first_state not in final_states and second_state in final_states):
        result_matrix[first_state][second_state] = 1
      else:
        result_matrix[first_state][second_state] = 0
  return result_matrix


def myhillNerode(dfa):
  (sigma, states, initial_states, final_states, transitions) = dfa
  matrix = build_pairs_matrix(dfa)
  done = False
  while done == False:
    done = True
    for first_state in states:
      for second_state in states:
        if first_state in matrix and second_state in matrix[first_state]:
          if matrix[first_state][second_state] == 0:
            for symbol in sigma:
              delta_first = list(filter(lambda t: t[1] == symbol, transitions[first_state]))
              if len(delta_first) == 0:
                delta_first = None
              else:
                delta_first = delta_first[0][0]

              delta_second = list(filter(lambda t: t[1] == symbol, transitions[second_state]))
              if len(delta_second) == 0:
                delta_second = None
              else:
                delta_second = delta_second[0][0]
              if delta_first != None and delta_second != None:
                if delta_first in matrix and delta_second in matrix[delta_first]:
                  if matrix[delta_first][delta_second] == 1:
                    matrix[first_state][second_state] = 1  
                    done = False
                elif delta_second in matrix and delta_first in matrix[delta_second]:
                  if matrix[delta_second][delta_first] == 1:
                    matrix[first_state][second_state] = 1  
                    done = False
          
  return matrix


def get_new_transitions(new_states, transitions):
  new_transitions = {}
  states = []
  for state_group in new_states:
    state_group = list(state_group)
    new_state_name = ''.join(sorted(state_group))
    states.append(new_state_name)
    new_transitions[new_state_name] = []
    for transition in transitions[state_group[0]]:
      for state in new_states:
        if transition[0] in state:
          new_transitions[new_state_name].append((convert_set_to_string(state), transition[1]))
  return new_transitions



def buildMinimizedDfa(dfa):
  # Build the new states 
  (sigma, states, initial_states, final_states, transitions) = dfa
  matrix = myhillNerode(dfa)
  new_states = []
  for first_state in states:
    for second_state in states:
      if first_state in matrix and second_state in matrix[first_state]:
        if matrix[first_state][second_state] == 0:

          found = False
          for new_state_index in range(len(new_states)):
            if first_state in new_states[new_state_index] or second_state in new_states[new_state_index]:
              new_states[new_state_index] = new_states[new_state_index].union({first_state, second_state})
              found = True
          
          if found == False:
            new_states.append(set({first_state, second_state}))
 
  for first_state in states:
    new_first_state = None
    for new_state_group in new_states:
      for state_group_component in new_state_group:
        if initial_states[0] == state_group_component:
          new_first_state = new_state_group
          break
 
    new_final_states = []
    for new_state_group in new_states:
      for state_group_component in new_state_group:
        if state_group_component in final_states:
          new_final_states.append(new_state_group)
          break
  
  if new_first_state == None:
    new_first_state = {initial_states[0]}

  if len(new_final_states) == 0:
    new_final_states = [{x} for x in final_states]
  
  for state in states:
    found = False
    for new_state in new_states:
      if state in new_state:
        found = True
        break
    if found == False:
      new_states.append({state})
  

  new_transitions = get_new_transitions(new_states, transitions)

  # conversie in stringuri pt state-uri
  for state_index in range(len(new_states)):
    new_states[state_index] = convert_set_to_string(new_states[state_index])
  new_first_state = convert_set_to_string(new_first_state)
  for state_index in range(len(new_final_states)):
    new_final_states[state_index] = convert_set_to_string(new_final_states[state_index])
  return (sigma, new_states, new_first_state, new_final_states, new_transitions)



def output_dfa(dfa, file_name):
  (sigma, states, initial_state, final_states, transitions) = dfa
  
  try:
    output_file = open(file_name, 'w')
  except FileNotFoundError:
    output_file = open(file_name, 'x')
  
  output_file.write('Sigma:\n')
  for item in sigma:
    output_file.write(item + '\n')
  output_file.write('End\n\n')

  output_file.write('States:\n')
  for state in states:
    output_file.write(state)
    if state == initial_state:
      output_file.write(', S')
    if state in final_states:
      output_file.write(', F')
    output_file.write('\n')
  output_file.write('End\n\n')

  output_file.write('Transitions:\n')
  for initial_state in transitions.keys():
    for final_state, symbol in transitions[initial_state]:
      output_file.write(f'{initial_state}, {symbol}, {final_state}\n')
  output_file.write('End')

output_dfa(buildMinimizedDfa(dfa), 'output1')
# output_dfa(buildMinimizedDfa(dfa), 'output2')
