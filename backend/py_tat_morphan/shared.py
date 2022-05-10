import struct
from .constants import *

class Header:
    """Read and provide interface to header"""
    
    def __init__(self, file):
        bytes = file.read(5) # "HFST\0"
        # if struct.unpack_from("<5s", bytes, 0) == "('HFST\\x00',)":
        if struct.unpack_from("<5s", bytes, 0) == (b'HFST\x00',):
            # just ignore any hfst3 header
            remaining = struct.unpack_from("<H", file.read(3), 0)[0]
            self.handle_hfst3_header(file, remaining)
            bytes = file.read(56) # 2 unsigned shorts, 4 unsigned ints and 9 uint-bools
        else:
            bytes = bytes + file.read(56 - 5)
        self.number_of_input_symbols             = struct.unpack_from("<H", bytes, 0)[0]
        self.number_of_symbols                   = struct.unpack_from("<H", bytes, 2)[0]
        self.size_of_transition_index_table      = struct.unpack_from("<I", bytes, 4)[0]
        self.size_of_transition_target_table     = struct.unpack_from("<I", bytes, 8)[0]
        self.number_of_states                    = struct.unpack_from("<I", bytes, 12)[0]
        self.number_of_transitions               = struct.unpack_from("<I", bytes, 16)[0]
        self.weighted                            = struct.unpack_from("<I", bytes, 20)[0] != 0
        self.deterministic                       = struct.unpack_from("<I", bytes, 24)[0] != 0
        self.input_deterministic                 = struct.unpack_from("<I", bytes, 28)[0] != 0
        self.minimized                           = struct.unpack_from("<I", bytes, 32)[0] != 0
        self.cyclic                              = struct.unpack_from("<I", bytes, 36)[0] != 0
        self.has_epsilon_epsilon_transitions     = struct.unpack_from("<I", bytes, 40)[0] != 0
        self.has_input_epsilon_transitions       = struct.unpack_from("<I", bytes, 44)[0] != 0
        self.has_input_epsilon_cycles            = struct.unpack_from("<I", bytes, 48)[0] != 0
        self.has_unweighted_input_epsilon_cycles = struct.unpack_from("<I", bytes, 52)[0] != 0

    def handle_hfst3_header(self, file, remaining):
        chars = struct.unpack_from("<" + str(remaining) + "c",
                                   file.read(remaining), 0)
        # assume the h3-header doesn't say anything surprising for now

class Alphabet:
    """Read and provide interface to alphabet"""

    def __init__(self, file, number_of_symbols):
        self.keyTable = [] # list of unicode objects, use foo.encode("utf-8") to print
        self.flagDiacriticOperations = dict() # of symbol numbers to string triples
        for x in range(number_of_symbols):
            symbol = b""
            while True:
                byte = file.read(1)
                if byte == b'\0': # a symbol has ended
                    try:
                        symbol = unicode(symbol, "utf-8")
                    except:
                        symbol = str(symbol)
                    if len(symbol) > 4 and symbol[0] == '@' and\
                    symbol [-1] == '@' and symbol[2] == '.' and symbol[1] in "PNRDCU":
                        # this is a flag diacritic
                        op = feat = val = u""
                        parts = symbol[1:-1].split(u'.')
                        if len(parts) == 2:
                            op, feat = parts
                        elif len(parts) == 3:
                            op, feat, val = parts
                        else:
                            self.keyTable.append(symbol)
                            break
                        self.flagDiacriticOperations[x] = FlagDiacriticOperation(op, feat, val)
                        self.keyTable.append(u"")
                        break
                    self.keyTable.append(symbol)
                    break
                symbol += byte
        self.keyTable[0] = u""

class LetterTrie:
    """Insert and prefix-retrieve string / symbol number pairs"""

    class Node:
        
        def __init__(self):
            self.symbols = dict()
            self.children = dict()
            
        def add(self, string, symbolNumber):
            """
            Add string to trie, having it resolve to symbolNumber
            """
            if len(string) > 1:
                if not (string[0] in self.children):
                    self.children[string[0]] = self.__class__() # instantiate a new node
                self.children[string[0]].add(string[1:], symbolNumber)
            elif len(string) == 1:
                self.symbols[string[0]] = symbolNumber
            else:
                self.symbols[string] = symbolNumber

        def find(self, indexstring):
            """
            Find symbol number corresponding to longest match in indexstring
            (starting from the position held by indexstring.pos)
            """
            if indexstring.pos >= len(indexstring.s):
                return NO_SYMBOL_NUMBER
            current = indexstring.get()
            indexstring.pos += 1
            if not (current in self.children):
                if not (current in self.symbols):
                    indexstring.pos -= 1
                    return NO_SYMBOL_NUMBER
                return self.symbols[current]
            temp = self.children[current].find(indexstring)
            if temp == NO_SYMBOL_NUMBER:
                if not (current in symbols):
                    indexstring.pos -= 1
                    return NO_SYMBOL_NUMBER
                return self.symbols[current]
            return temp
    
    def __init__(self):
        self.root = self.Node()

    def addString(self, string, symbolNumber):
        self.root.add(string, symbolNumber)

    def findKey(self, indexstring):
        return self.root.find(indexstring)

class Indexlist:
    """Utility class to keep track of where we are in a list"""

    def __init__(self, items = []):
        self.s = list(items)
        self.pos = 0
    
    def get(self, adjustment = 0):
        return self.s[self.pos + adjustment]

    def put(self, val, adjustment = 0):
        if (self.pos + adjustment) < len(self.s):
            self.s[self.pos + adjustment] = val
        else:
            self.s.append(val)

    def save(self):
        self.temp = self.pos

    def restore(self):
        self.pos = self.temp

    def last(self):
        if len(self.s) > 0:
            return self.s[-1]
        return None

class FlagDiacriticOperation:
    """Represents one flag diacritic operation"""
    
    def __init__(self, op, feat, val):
        self.operation = op
        self.feature = feat
        self.value = val

class FlagDiacriticStateStack:
    """The combined state for all flag diacritics"""

    def __init__(self):
        self.stack = [dict()]

    def pop(self):
        self.stack.pop()

    def duplicate(self):
        self.stack.append(self.stack[-1].copy())

    def push(self, flagDiacritic):
        """
        Attempt to modify flag diacritic state stack. If successful, push new
        state and return True. Otherwise return False.
        """
        if flagDiacritic.operation == 'P': # positive set
            self.duplicate()
            self.stack[-1][flagDiacritic.feature] = (flagDiacritic.value, True)
            return True
        if flagDiacritic.operation == 'N': # negative set
            self.duplicate()
            self.stack[-1][flagDiacritic.feature] = (flagDiacritic.value, False)
            return True
        if flagDiacritic.operation == 'R': # require
            if flagDiacritic.value == '': # empty require
                if self.stack[-1].get(flagDiacritic.feature) == None:
                    return False # empty require = require nonempty value
                else:
                    self.duplicate()
                    return True
            if self.stack[-1].get(flagDiacritic.feature) == (flagDiacritic.value, True):
                self.duplicate()
                return True
            return False
        if flagDiacritic.operation == 'D': # disallow
            if flagDiacritic.value == '': # empty disallow
                if self.stack[-1].get(flagDiacritic.feature) == None:
                    self.duplicate()
                    return True
                else:
                    return False
            if self.stack[-1].get(flagDiacritic.feature) == (flagDiacritic.value, True):
                return False
            self.duplicate()
            return True
        if flagDiacritic.operation == 'C': # clear
            self.duplicate()
            if flagDiacritic.feature in self.stack[-1]:
                del self.stack[-1][flagDiacritic.feature]
            return True
        if flagDiacritic.operation == 'U': # unification
            if not flagDiacritic.feature in self.stack[-1] or \
                    self.stack[-1][flagDiacritic.feature] == (flagDiacritic.value, True) or \
                    (self.stack[-1][flagDiacritic.feature][1] == False and \
                         self.stack[-1][flagDiacritic.feature][0] != flagDiacritic.value):
                self.duplicate()
                self.stack[-1][flagDiacritic.feature] = (flagDiacritic.value, True)
                return True
            return False

def match(transitionSymbol, inputSymbol):
    """Utility function to check whether we want to traverse a transition/index"""
    if transitionSymbol == NO_SYMBOL_NUMBER:
        return False
    if inputSymbol == NO_SYMBOL_NUMBER:
        return True
    return symbol == inputSymbol

