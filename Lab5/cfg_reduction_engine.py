import sys
from cfg_validation_engine import parse_config, validate_cfg


def pretty_print(cfg, output_filename):
    variables, start_variables, terminals, productions = cfg

    output_file = open(output_filename, "w")

    output_file.write("Variables:\n")
    for var in variables:
        if var in start_variables:
            output_file.write(f"{var}, S\n")
        else:
            output_file.write(f"{var}\n")
    output_file.write("End\n")

    output_file.write("Terminals:\n")
    for ter in terminals:
        output_file.write(f"{ter}\n")
    output_file.write("End\n")

    output_file.write("Productions:\n")
    for var in productions:
        resulted_string = " | ".join(
            [" ".join(string) for string in productions[var]])
        output_file.write(f"{var} -> {resulted_string}\n")
    output_file.write("End\n")


def deleteUselessProductions(cfg):
    variables, start_variables, terminals, productions = cfg
    w = set()
    for var in productions:
        for string in productions[var]:
            for symbol in string:
                if symbol in terminals:
                    w.add(var)
    w_prev = set()
    while w != w_prev:
        w_prev = w
        for var in productions:
            for string in productions[var]:
                for symbol in string:
                    if symbol in w:
                        w.add(var)

    for var in list(productions.keys()):
        if var not in w:
            productions.pop(var)
        else:
            i = 0
            while i < len(productions[var]):
                for symbol in productions[var][i]:
                    if symbol not in w and symbol in variables:
                        del productions[var][i]
                        i -= 1
                        break
                i += 1
            if productions[var] == []:
                productions[var] = [["#"]]

    y = set(start_variables[0])
    y_prev = set()
    while y != y_prev:
        y_prev = y.copy()
        for symbol in list(y):
            if symbol in productions:
                for string in productions[symbol]:
                    for syb in string:
                        y.add(syb)

    variables = [var for var in variables if var in y]
    terminals = [ter for ter in terminals if ter in y]

    for var in list(productions.keys()):
        if var not in variables:
            productions.pop(var)
        else:
            i = 0
            while i < len(productions[var]):
                for symbol in productions[var][i]:
                    if symbol not in variables and symbol not in terminals and symbol != "#":
                        del productions[var][i]
                        i -= 1
                        break
                i += 1
            if productions[var] == []:
                productions[var] = [["#"]]



def deleteSymbol(symbol_to_delete, symbol, string, productions):
    for i in range(len(string)):
        if string[i] == symbol_to_delete:
            if string[:i]+string[i+1:] not in productions[symbol]:
                productions[symbol].append(string[:i]+string[i+1:])


def deleteNullProductions(cfg):
    variables, start_variables, terminals, productions = cfg

    for symbol in productions:
        if ["#"] in productions[symbol]:
            productions[symbol].remove(["#"])
            for symbol1 in productions:
                for string in productions[symbol1]:
                    if symbol in string:
                        deleteSymbol(symbol, symbol1, string, productions)


input = sys.argv[1]
cfg = parse_config(input)
if validate_cfg(cfg):
    deleteUselessProductions(cfg)
    deleteNullProductions(cfg)
    pretty_print(cfg, "output")
