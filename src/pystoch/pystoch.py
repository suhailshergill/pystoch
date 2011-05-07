import argparse
import compile as c
from stack import Stack
import sys

class PyStochObj(object):

    def __init__(self):
        self.module_stack = Stack()
        self.class_stack = Stack()
        self.func_stack = Stack()
        self.line_stack = Stack()
        self.loop_stack = Stack()
        
def run(prog, args):
    PYSTOCHOBJ = PyStochObj()
    
    sys.argv = args
    if prog.endswith('.pystoch'):
        execfile(prog)
    else:
        source = c.pystoch_compile(prog)
        print source
        exec(source)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a PyStoch program.')
    parser.add_argument('program', metavar='file', type=str, nargs=1,
                        help='the PyStoch file to execute')
    parser.add_argument('arguments', metavar='arg', type=str, nargs='*',
                        help='arguments to the PyStoch program')

    args = parser.parse_args()
    run(args.program[0], args.arguments)
    
