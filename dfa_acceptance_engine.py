import sys
from dfa_parser_engine import parse_config, validate_dfa


def test_acceptance(path):

    dfa_structure = parse_config(sys.argv[1])
    (sigma, states, initial_states, final_states, transitions) = dfa_structure

    if not validate_dfa(dfa_structure):
        raise Exception("Invalid DFA")


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
