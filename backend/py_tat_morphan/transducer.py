from .constants import *
from .shared import match, Indexlist, LetterTrie, FlagDiacriticStateStack
import struct

class Transducer:

    class TransitionIndex:
        
        def __init__(self, arg):
            input, transition = arg
            self.inputSymbol = input
            self.target = transition
            
        def matches(self, symbol):
            return match(self.inputSymbol, symbol)
        
        def isFinal(self):
            return self.inputSymbol == NO_SYMBOL_NUMBER and \
                self.target != NO_TABLE_INDEX

    class IndexTable:

        def __init__(self, file, number_of_indices):
            bytes = file.read(number_of_indices*6) # ushort + uint
            try:
                self.indices = \
                    [Transducer.TransitionIndex(struct.unpack_from("<HI", bytes, x*6)) \
                         for x in xrange(number_of_indices)]
            except:
                self.indices = \
                    [Transducer.TransitionIndex(struct.unpack_from("<HI", bytes, x*6)) \
                         for x in range(number_of_indices)]


    class Transition:
        
        def __init__(self, arg):
            input, output, target = arg
            self.inputSymbol = input
            self.outputSymbol = output
            self.target = target

        def matches(self, symbol):
            return match(self.inputSymbol, symbol)

        def isFinal(self):
            return self.inputSymbol == NO_SYMBOL_NUMBER and \
                self.outputSymbol == NO_SYMBOL_NUMBER and \
                self.target == 1

    class TransitionTable:

        def __init__(self, file, number_of_transitions):
            self.position = 0
            bytes = file.read(number_of_transitions*8) # 2*ushort + uint
            try:
                self.transitions = \
                    [Transducer.Transition(struct.unpack_from("<HHI", bytes, x*8)) \
                         for x in xrange(number_of_transitions)]
            except:
                self.transitions = \
                    [Transducer.Transition(struct.unpack_from("<HHI", bytes, x*8)) \
                         for x in range(number_of_transitions)]


        def set(self, pos):
            if pos >= TRANSITION_TARGET_TABLE_START:
                self.position = pos - TRANSITION_TARGET_TABLE_START
            else:
                self.position = pos

        def at(self, pos):
            return self.transitions[pos - TRANSITION_TARGET_TABLE_START]
        
        def isFinal(self, pos):
            if pos >= TRANSITION_TARGET_TABLE_START:
                return self.transitions[pos - TRANSITION_TARGET_TABLE_START].isFinal()
            return self.transitions[pos].isFinal()

    def __init__(self, file, header, alphabet):
        self.alphabet = alphabet
        self.flagDiacriticOperations = alphabet.flagDiacriticOperations
        self.stateStack = FlagDiacriticStateStack()
        self.letterTrie = LetterTrie()
        for x in range(header.number_of_symbols):
            self.letterTrie.addString(alphabet.keyTable[x], x)
        self.indexTable = self.IndexTable(file, header.size_of_transition_index_table)
        self.indices = self.indexTable.indices
        self.transitionTable = self.TransitionTable(file, header.size_of_transition_target_table)
        self.transitions = self.transitionTable.transitions
        self.displayVector = []
        self.outputString = Indexlist()
        self.inputString = Indexlist()

    def tryEpsilonIndices(self, index):
        if self.indices[index].inputSymbol == 0:
            self.tryEpsilonTransitions(self.indices[index].target - TRANSITION_TARGET_TABLE_START)

    def tryEpsilonTransitions(self, index):
        while True:
            if self.transitions[index].inputSymbol == 0:
                self.outputString.put(self.transitions[index].outputSymbol)
                self.outputString.pos += 1
                self.getAnalyses(self.transitions[index].target)
                self.outputString.pos -= 1
                index += 1
            elif self.transitions[index].inputSymbol in self.flagDiacriticOperations:
                if not self.stateStack.push(self.flagDiacriticOperations[self.transitions[index].inputSymbol]):
                    index += 1
                    continue # illegal state modification; do nothing
                else:
                    self.outputString.put(self.transitions[index].outputSymbol)
                    self.outputString.pos += 1
                    self.getAnalyses(self.transitions[index].target)
                    self.outputString.pos -= 1
                    index += 1
                    self.stateStack.pop()
                    continue
            else:
                return

    def findIndex(self, index):
        if self.indices[index + self.inputString.get(-1)].inputSymbol == self.inputString.get(-1):
            self.findTransitions(self.indices[index + self.inputString.get(-1)].target - TRANSITION_TARGET_TABLE_START)

    def findTransitions(self, index):
        while self.transitions[index].inputSymbol != NO_SYMBOL_NUMBER:
            if self.transitions[index].inputSymbol == self.inputString.get(-1):
                self.outputString.put(self.transitions[index].outputSymbol)
                self.outputString.pos += 1
                self.getAnalyses(self.transitions[index].target)
                self.outputString.pos -= 1
            else:
                return
            index += 1

    def getAnalyses(self, index):
        if index >= TRANSITION_TARGET_TABLE_START:
            index -= TRANSITION_TARGET_TABLE_START
            self.tryEpsilonTransitions(index + 1)
            if self.inputString.get() == NO_SYMBOL_NUMBER:
                if self.transitionTable.isFinal(index):
                    self.noteAnalysis()
                self.outputString.put(NO_SYMBOL_NUMBER)
                return
            self.inputString.pos += 1
            self.findTransitions(index + 1)
        else:
            self.tryEpsilonIndices(index + 1)
            if self.inputString.get() == NO_SYMBOL_NUMBER:
                if self.indices[index].isFinal():
                    self.noteAnalysis()
                self.outputString.put(NO_SYMBOL_NUMBER)
                return
            self.inputString.pos += 1
            self.findIndex(index + 1)
        self.inputString.pos -= 1
        self.outputString.put(NO_SYMBOL_NUMBER)

    def noteAnalysis(self):
        output = u""
        for x in self.outputString.s:
            if x == NO_SYMBOL_NUMBER:
                break
            output += self.alphabet.keyTable[x]
        self.displayVector.append((output, 0.0))

    def analyze(self, string):
        self.outputString = Indexlist([NO_SYMBOL_NUMBER])
        self.inputString = Indexlist()
        self.displayVector = []

        try:
            if not isinstance(string, unicode):
                inputline = Indexlist(unicode(string, "utf-8"))
            else:
                inputline = Indexlist(string) # wrap the input in an indexing container
        except:
            print(1)
            if not isinstance(string, str):
                inputline = Indexlist(str(string, "utf-8"))
            else:
                inputline = Indexlist(string) # wrap the input in an indexing container
        while inputline.pos < len(inputline.s) and \
                self.inputString.last != NO_SYMBOL_NUMBER:
            self.inputString.s.append(self.letterTrie.findKey(inputline))
        if self.inputString.s[-1] == NO_SYMBOL_NUMBER:
            return False
        self.inputString.s.append(NO_SYMBOL_NUMBER)
        self.getAnalyses(0) # start at index zero
        return True # if we get here, we're done analyzing

    def printAnalyses(self):
        for x in self.displayVector:
            print('\t' + x[0].encode("utf-8") + '\t' + str(x[1]))

class TransducerW(Transducer):

    class TransitionIndex(Transducer.TransitionIndex):

        def getFinalWeight(self):
            return float(self.target)

    class IndexTable:

        def __init__(self, file, number_of_indices):
            bytes = file.read(number_of_indices*6) # ushort + uint
            try:
                self.indices = \
                    [TransducerW.TransitionIndex(struct.unpack_from("<HI", bytes, x*6)) \
                         for x in xrange(number_of_indices)]
            except:
                self.indices = \
                    [TransducerW.TransitionIndex(struct.unpack_from("<HI", bytes, x*6)) \
                         for x in range(number_of_indices)]


    class Transition(Transducer.Transition):
            
        def __init__(self, arg):
            input, output, target, weight = arg
            Transducer.Transition.__init__(self, (input, output, target))
            self.weight = weight
            
    class TransitionTable(Transducer.TransitionTable):

        def __init__(self, file, number_of_transitions):
            self.position = 0
            bytess = file.read(number_of_transitions*12)
            # 2* ushort + uint + float
            try:
                self.transitions = \
                    [TransducerW.Transition(struct.unpack_from("<HHIf",
                                                               bytess,
                                                               x*12)) \
                         for x in xrange(number_of_transitions)]
            except:
                self.transitions = \
                    [TransducerW.Transition(struct.unpack_from("<HHIf",
                                                               bytess,
                                                               x*12)) \
                         for x in range(number_of_transitions)]

                
    def __init__(self, file, header, alphabet):
        self.alphabet = alphabet
        self.flagDiacriticOperations = alphabet.flagDiacriticOperations
        self.stateStack = FlagDiacriticStateStack()
        self.letterTrie = LetterTrie()
        for x in range(header.number_of_symbols):
            self.letterTrie.addString(alphabet.keyTable[x], x)
        self.indexTable = self.IndexTable(file, header.size_of_transition_index_table)
        # self.indexTable = self.IndexTable(file, 103855)
        self.indices = self.indexTable.indices
        self.transitionTable = self.TransitionTable(file, header.size_of_transition_target_table)
        # self.transitionTable = self.TransitionTable(file, 103855)
        self.transitions = self.transitionTable.transitions
        self.displayVector = []
        self.outputString = Indexlist()
        self.inputString = Indexlist()
        self.current_weight = 0.0

    def traverse(self, index):
        self.outputString.put(self.transitions[index].outputSymbol)
        self.outputString.pos += 1
        self.current_weight += self.transitions[index].weight
        self.getAnalyses(self.transitions[index].target)
        self.outputString.pos -= 1
        self.current_weight -= self.transitions[index].weight

    def tryEpsilonTransitions(self, index): # epsilons and flag diacritics
        while True:
            if self.transitions[index].inputSymbol == 0:
                self.traverse(index)
                index += 1
            elif self.transitions[index].inputSymbol in self.flagDiacriticOperations:
                if not self.stateStack.push(self.flagDiacriticOperations[self.transitions[index].inputSymbol]):
                    index += 1
                    continue # illegal state modification; do nothing
                else:
                    self.traverse(index)
                    index += 1
                    self.stateStack.pop()
                    continue
            else:
                return

    def findTransitions(self, index):
        while self.transitions[index].inputSymbol != NO_SYMBOL_NUMBER:
            if self.transitions[index].inputSymbol == self.inputString.get(-1):
                self.traverse(index)
            else:
                return
            index += 1
                
    def getAnalyses(self, index):
        if index >= TRANSITION_TARGET_TABLE_START:
            index -= TRANSITION_TARGET_TABLE_START
            self.tryEpsilonTransitions(index + 1)
            if self.inputString.get() == NO_SYMBOL_NUMBER:
                if self.transitionTable.isFinal(index):
                    self.current_weight += self.transitions[index].weight
                    self.noteAnalysis()
                    self.current_weight -= self.transitions[index].weight
                    self.outputString.put(NO_SYMBOL_NUMBER)
                    return
            self.inputString.pos += 1
            self.findTransitions(index + 1)
        else:
                self.tryEpsilonIndices(index + 1)
                if self.inputString.get() == NO_SYMBOL_NUMBER:
                    if self.indices[index].isFinal():
                        self.current_weight += self.indices[index].getFinalWeight()
                        self.noteAnalysis()
                        self.current_weight -= self.indices[index].getFinalWeight()
                    self.outputString.put(NO_SYMBOL_NUMBER)
                    return
                self.inputString.pos += 1
                self.findIndex(index + 1)
        self.inputString.pos -= 1
        self.outputString.put(NO_SYMBOL_NUMBER)

    def noteAnalysis(self):
        output = u""
        for x in self.outputString.s:
            if x == NO_SYMBOL_NUMBER:
                break
            output += self.alphabet.keyTable[x]
        self.displayVector.append((output, self.current_weight))
