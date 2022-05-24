import sys
from parse_cfg import parse_config, validate_cfg

def pretty_print(cfg, output_filename):
    variables, start_variables, terminals, productions = cfg

    output_file=open(output_filename, "w")

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
        resulted_string=" | ".join([" ".join(string) for string in productions[var]])
        output_file.write(f"{var} -> {resulted_string}\n")
    output_file.write("End\n")

def reduce_cfg(cfg):
    variables, start_variables, terminals, productions = cfg
    w = []
    for var in productions:
        for string in productions[var]:
            for symbol in string:
                if symbol in terminals:
                    w.append(var)
    w_prev=[]
    while w!=w_prev:
        w_prev=w
        for var in productions:
            for string in productions[var]:
                for symbol in string:
                    if symbol in w:
                        w.append(var)

    for var in list(productions.keys()):
        if var not in w:
            productions.pop(var)
        else:
            i = 0
            while i < len(productions[var]):
                for symbol in productions[var][i]:
                    if symbol not in w and symbol in variables: #!!
                        del productions[var][i]
                        i-=1
                        break
                i+=1
            
    y=[start_variables[0]]
    y_prev=[]
    while y!=y_prev:
        y_prev=y
        for symbol in y:
            if symbol in productions:
                for string in productions[symbol]:
                    for syb in string:
                        y.append(syb)

    variables=[var for var in variables if var in y]    
    terminals=[ter for ter in terminals if ter in y]

    for var in list(productions.keys()):
        if var not in variables:
            productions.pop(var)
        else:
            i = 0
            while i < len(productions[var]):
                for symbol in productions[var][i]:
                    if symbol not in variables and symbol not in terminals and symbol!="#": #!!
                        del productions[var][i]
                        i-=1
                        break
                i+=1

    return variables, start_variables, terminals, productions


if len(sys.argv)>2:
    input = sys.argv[1]
    output = sys.argv[2]
    cfg = parse_config(input)
    if validate_cfg(cfg):
        cfg1=reduce_cfg(cfg)
        pretty_print(cfg1, output)
else:
    print("Please introduce input file and output file")
