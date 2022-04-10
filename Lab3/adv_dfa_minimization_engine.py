import sys
from dfa_parser import parse_config
from dfa_minimization_engine import buildMinimizedDfa, output_dfa

    
def get_unreachable_states(dfa):
    (sigma, states, initial_state, final_states, transitions) = dfa
    reachable_states = {initial_state}
    new_states = {initial_state}
    while new_states != set():
        reached_states = set()
        for state in new_states:
            for symbol in sigma:
                for next_state, transiton_symbol in transitions[state]:
                    if transiton_symbol == symbol:
                        reached_states.add(next_state)
                        break
        new_states = reached_states.difference(reachable_states)
        reachable_states = reachable_states.union(new_states)
    unreachable_states = set(states)-reachable_states
    return list(unreachable_states)


def get_dead_states(dfa):
    (sigma, states, initial_states, final_states, transitions) = dfa
    dead_states = []
    for state in states:
        if state not in final_states:
            is_dead_state = True
            for symbol in sigma:
                for next_state, current_symbol in transitions[state]:
                    if current_symbol == symbol and next_state != state:
                        is_dead_state = False
                        break
            if is_dead_state == True:
                dead_states.append(state)
    return dead_states


def delete_states(useless_states, dfa):
    (sigma, states, initial_states, final_states, transitions) = dfa

    new_states = [state for state in states if state not in useless_states]

    new_final_states = [
        state for state in final_states if state not in useless_states]

    new_transitions = {}

    for state in new_states:
        new_transitions[state] = []
        for next_state, symbol in transitions[state]:
            if next_state not in useless_states:
                new_transitions[state].append((next_state, symbol))
    return (sigma, new_states, initial_states, new_final_states, new_transitions)


if len(sys.argv) < 2:
    print("Config file not specified")
    sys.exit()


dfa = parse_config(sys.argv[1])

if dfa is None:
    print("Something went wrong when parsing the dfa config file")
    sys.exit()


# minimize dfa
dfa = buildMinimizedDfa(dfa)

# delete all unreachable states
unreachable_states = get_unreachable_states(dfa)
dfa = delete_states(unreachable_states, dfa)

# delete all dead states
dead_states = get_dead_states(dfa)
while len(dead_states) != 0:
    dfa = delete_states(dead_states, dfa)
    dead_states = get_dead_states(dfa)

output_dfa(dfa, 'adv_minimized_dfa_config_file')
