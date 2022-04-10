from nfa_parser_engine import validate_nfa, parse_config
import sys

def set_to_string(set):
    return str("".join(sorted(set)))

def nfa_converter(nfa_config_file):
    nfa_structure = parse_config(nfa_config_file)
    if not validate_nfa(nfa_structure):
        raise Exception("Invalid NFA")
    (sigma, states, initial_states, final_states, transitions) = nfa_structure

    dfa_transitions={}
    dfa_states=[{initial_states[0]}]
    #luam pe rand fiecare stare din dfa
    for state in dfa_states:
        dfa_transitions[set_to_string(state)]=[]
        # pentru fiecare stare luam fiecare simbol 
        for symbol in sigma:
            # gasim starile in care ajungem plecand din starea curenta cu simbolul curent 
            # si le unim intr-o singura stare 'new_state'
            new_state=set()
            for sub_state in state:
                if sub_state == 'q2':
                    print("")
                for transition in filter(lambda t: t[1]==symbol, [] if sub_state not in transitions else transitions[sub_state]):
                    new_state.add(transition[0])

            # adaugam starea noua gasita in multimea de stari a dfa-ului
            if new_state not in dfa_states and new_state!=set():
                dfa_states.append(new_state)

            # adaugam tranzitia nou gasita
            if new_state!=set():
                dfa_transitions[set_to_string(state)].append((symbol, set_to_string(new_state)))
            #else:
            #    dfa_transitions[set_to_string(state)].append(('-',symbol))

    # convertim dfa_states din set in string (optional - pentru print)
    for i in range(len(dfa_states)):
        dfa_states[i]=set_to_string(dfa_states[i])

    # aflam starile finale ale dfa-ului (cele care sunt formate din macar o stare finala din nfa)
    dfa_final_states=[]
    for state in dfa_states:
        for final_state in final_states:
            if final_state in state:
                dfa_final_states.append(state)
                break
    
    return (sigma, dfa_states, initial_states, dfa_final_states, dfa_transitions)


def print_dfa(dfa_structure):
    (sigma, states, initial_states, final_states, transitions)=dfa_structure

    output=open('resulted_dfa', 'w')

    output.write('Sigma:\n')
    for symbol in sigma:
        output.write('\t'+symbol+'\n')
    output.write("End\n\n")

    output.write('States:\n')
    for state in states:
        output.write('\t'+state)
        if state in initial_states:
            output.write(", S")
        if state in final_states:
            output.write(", F")
        output.write('\n')
    output.write("End\n\n")

    output.write('Transition:\n')
    for start_state in transitions:
        for symbol, end_state in transitions[start_state]:
            output.write('\t'+start_state+', '+symbol+', '+end_state+'\n')
    output.write("End\n")

    
nfa_config_file = sys.argv[1]

dfa_structure=nfa_converter(nfa_config_file)
print_dfa(dfa_structure)