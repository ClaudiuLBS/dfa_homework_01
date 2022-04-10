from nfa_parser_engine import validate_nfa, parse_config
import sys

if (len(sys.argv) < 2):
    raise Exception("Correct format is: python nfa_acceptance_engine.py <nfa_config_file> <path>")

nfa_config_file = sys.argv[1]

# Daca nu specificam nimic ca CLI param pt path, atunci consideram ca e gol
path = ""
if len(sys.argv) >= 3:
    path = sys.argv[2]
nfa_structure = parse_config(nfa_config_file)


def test_acceptance(nfa_structure, path):
    (sigma, states, initial_states, final_states, transitions) = nfa_structure
    if not validate_nfa(nfa_structure, True):
        raise Exception("Invalid NFA")

    queue = [[initial_states[0]]]
    # print(queue)
    path_length = len(path)

    remaining_epsilon_transitions = True

    while path != "" or remaining_epsilon_transitions == True:


        # Daca am ajuns sa consum toate literele, nu voi mai continua
        # cu urmatoarea iteratie in while decat daca la acest pas
        # gasesc un drum catre alta stare prin epsilon
        if path == "":
            remaining_epsilon_transitions = False
        current_letter = path[0] if path != "" else "*"
        queue_length = len(queue)
        for _ in range(queue_length):
            states_chain = queue.pop(0)
            # Daca ultima stare din drum e deja finala, atunci am gasit un path complet si deci
            # cuvantul a fost validat
            complete_path = check_complete_path(queue, path_length, final_states)
            # Incheiem executia functiei prin a returna true doar daca am gasit deja un path compplet,
            # altfel continuam
            if complete_path:
                return complete_path
            # daca nu se pleaca nicaieri din state-ul curent, continuam cu lantul urmator de state-uri
            if states_chain[-1] not in transitions.keys():
                continue

            # verificam fiecare tranzitie, si bagam in coada drumul catre urmatoarea stare
            for (next_state, next_state_letter) in transitions[states_chain[-1]]:
                if next_state_letter == current_letter:
                    queue.append(states_chain + [next_state])
                    #print("Trecem din {} in {} prin simbolul {}".format(states_chain[-1], next_state, next_state_letter))
                # De asemenea, daca avem stari la care ajungem din starea curenta prin epsilon,
                # atunci adaugam drumuri drumuri si prentru acestea
                # if next_state_letter == '*':
                #     queue.append(states_chain + [next_state])
                #     remaining_epsilon_transitions = True

        # print(queue)
        if path != "":
            path = path[1:]

    return check_complete_path(queue, path_length, final_states)




#verificam daca am ajuns la vreo stare finala, adica daca cuvantul a fost valdiat
def check_complete_path(queue, path_length, final_states):
    for item in queue:
        if len(item) > path_length and item[-1] in final_states:
            return True
    return False

print(test_acceptance(nfa_structure, path))
