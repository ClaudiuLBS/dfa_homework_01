import sys


def clean_string(input_string: str):
    return input_string.replace('\n', '').replace(' ', '')


def parse_config(filename):
    variables = []
    start_variables = []
    terminals = []
    productions = {}

    input_file = open(filename, 'r')

    line = input_file.readline()
    while line != '':
        if "variables" in line.lower():
            line = clean_string(input_file.readline())
            while line.lower() != "end":
                var = line.split(',')
                if "S" in var or "s" in var:
                    start_variables.append(var[0])
                variables.append(var[0])
                line = clean_string(input_file.readline())

        if "terminals" in line.lower():
            line = clean_string(input_file.readline())
            while line.lower() != "end":
                terminals.append(line)
                line = clean_string(input_file.readline())

        if "productions" in line.lower():
            line = input_file.readline()
            while line.lower() != "end":
                variable, string = line.rstrip("\n").split("->")
                variable = variable.strip()
                strings = [str.split() for str in string.split("|")]
                if variable not in productions:
                    productions[variable] = []
                productions[variable].extend(strings)
                line = input_file.readline()

        line = input_file.readline()

    input_file.close()

    return (variables, start_variables, terminals, productions)


def validate_cfg(cfg):
    variables, start_variables, terminals, productions = cfg

    if len(start_variables) != 1:
        return False
    if start_variables[0] not in variables:
        return False
    if start_variables[0] not in productions:
        return False
    if len(set(variables).intersection(terminals)):
        return False

    for variable in variables:
        found = False
        if variable in productions:
            found = True
        else:
            for var_key in productions:
                for string in productions[var_key]:
                    if variable in string:
                        found = True
                        break
        if found == False:
            return False

    for ter in terminals:
        found = False
        for var in productions:
            for string in productions[var]:
                if ter in string:
                    found = True
                    break
        if found == False:
            return False

    for var in productions:
        if var not in variables:
            return False
        for string in productions[var]:
            for symbol in string:
                if symbol not in variables and symbol not in terminals and symbol != "#":
                    return False

    return True


if len(sys.argv) > 1:
    filename = sys.argv[1]
    cfg = parse_config(filename)
    if validate_cfg(cfg):
        print("VALID")
    else:
        print("INVALID")
else:
    print("Please introduce input file name")
