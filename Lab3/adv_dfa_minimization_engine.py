import sys
from dfa_parser import parse_config
from dfa_minimization_engine import buildMinimizedDfa, output_dfa


if len(sys.argv) < 2:
    print("Config file not specified")
    sys.exit()


dfa = parse_config(sys.argv[1])

if dfa is None:
    print("Something went wrong when parsing the dfa config file")
    sys.exit()

dfa = buildMinimizedDfa(dfa)
# output_dfa(dfa,'test')
