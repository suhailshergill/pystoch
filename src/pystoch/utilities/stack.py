"""
pystoch.utilities.stack
-----------------------

"""

class Stack(object):

    def __init__(self, stacktype):
        if not isinstance(stacktype, type):
            raise ValueError, "stacktype must be a type"
        
        self.stack = []
        self.stacktype = stacktype

    def pop(self):
        if len(self.stack) == 0:
            raise IndexError, "pop from empty stack"
        return self.stack.pop()

    def push(self, elmt):
        if not isinstance(elmt, self.stacktype):
            raise ValueError("elmt must be a %s" % self.stacktype)
        self.stack.append(elmt)

    def set(self, val):
        if not isinstance(val, self.stacktype):
            raise ValueError("val must be a %s" % self.stacktype)
        if len(self.stack) == 0:
            raise IndexError, "setting empty stack"
        self.stack[-1] = val

    def increment(self):
        if len(self.stack) == 0:
            raise IndexError, "incrementing empty stack"
        self.stack[-1] += 1

    def decrement(self):
        if len(self.stack) == 0:
            raise IndexError, "decrementing empty stack"
        self.stack[-1] -= 1

    def peek(self):
        if len(self.stack) > 0:
            return self.stack[-1]
        return 'null'

    def __hash__(self):
        stack = [str(item) for item in self.stack]
        return hash(''.join(stack))

    def __str__(self):
        string = []
        previtem = None
        numprev = 0
        for i in xrange(len(self.stack)):
            item = self.stack[len(self.stack)-i-1]
            if item != previtem:
                if numprev > 1:
                    string[-1] += "*%s" % numprev
                string.insert(0, str(item))
                numprev = 1
            else:
                numprev += 1

            previtem = item

        return ','.join(string)

    def __repr__(self):
        return "<Stack %s>" % self.__str__()

class IntegerStack(Stack):
    def __init__(self):
        super(IntegerStack, self).__init__(int)

class StringStack(Stack):
    def __init__(self):
        super(StringStack, self).__init__(str)
