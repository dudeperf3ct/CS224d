import copy
import numpy as np
from itertools import chain
class PartialParse(object):
    def __init__(self, sentence):
        """Initializes this partial parse.

        Your code should initialize the following fields:
            self.stack: The current stack represented as a list with the self.top of the stack as the
                        last element of the list.
            self.buffer: The current buffer represented as a list with the first item on the
                         buffer as the first item of the list
            self.dependencies: The list of dependencies produced so far. Represented as a list of
                    tuples where each tuple is of the form (head, dependent).
                    Order for this list doesn't matter.

        The root token should be represented with the string "ROOT"

        Args:
            sentence: The sentence to be parsed as a list of words.
                      Your code should not modify the sentence.
        """
        # The sentence being parsed is kept for bookkeeping purposes. Do not use it in your code.
        self.sentence = sentence

        ### YOUR CODE HERE
        self.stack = []
        self.buffer = []
        self.dependencies = []
        self.top=0
        self.stack.append("ROOT")
        self.top = self.top+1
        for s in sentence:
            self.buffer.append(s)  
        ### END YOUR CODE

    def parse_step(self, transition):
        """Performs a single parse step by applying the given transition to this partial parse

        Args:
            transition: A string that equals "S", "LA", or "RA" representing the shift, left-arc,
                        and right-arc transitions.
        """
        ### YOUR CODE HERE
        # if transition == 'S':
        #     self.stack.append(self.buffer[0])
        #     self.top = self.top +1
        #     del (self.buffer[0])
        # elif transition == 'LA':
        #     self.top = len(self.stack) - 1
        #     self.dependencies.append(tuple((self.stack[self.top], self.stack[self.top-1])))
        #     del (self.stack[self.top-1]) 
        # elif transition == 'RA':
        #     self.top = len(self.stack) - 1           
        #     self.dependencies.append(tuple((self.stack[self.top-1], self.stack[self.top])))
        #     del (self.stack[self.top]) 
        if transition == 'S':
            self.stack.append(self.buffer.pop(0))
        elif transition == 'LA':
            self.dependencies.append((self.stack[-1], self.stack[-2]))
            self.stack.pop(-2)
        elif transition == 'RA':
            self.dependencies.append((self.stack[-2],self.stack[-1]))
            self.stack.pop(-1)        
        ### END YOUR CODE

    def parse(self, transitions):
        """Applies the provided transitions to this PartialParse

        Args:
            transitions: The list of transitions in the order they should be applied
        Returns:
            dependencies: The list of dependencies produced when parsing the sentence. Represented
                          as a list of tuples where each tuple is of the form (head, dependent)
        """
        for transition in transitions:
            self.parse_step(transition)
        return self.dependencies


def minibatch_parse(sentences, model, batch_size):
    """Parses a list of sentences in minibatches using a model.

    Args:
        sentences: A list of sentences to be parsed (each sentence is a list of words)
        model: The model that makes parsing decisions. It is assumed to have a function
               model.predict(partial_parses) that takes in a list of PartialParses as input and
               returns a list of transitions predicted for each parse. That is, after calling
                   transitions = model.predict(partial_parses)
               transitions[i] will be the next transition to apply to partial_parses[i].
        batch_size: The number of PartialParses to include in each minibatch
    Returns:
        dependencies: A list where each element is the dependencies list for a parsed sentence.
                      Ordering should be the same as in sentences (i.e., dependencies[i] should
                      contain the parse for sentences[i]).
    """

    ### YOUR CODE HERE
    # partial_parses = []
    # for s in sentences:
    #     partial_parses.append(PartialParse(s)) 
    # unfinished_parses = copy.copy(partial_parses)
    # temp_parses = copy.copy(partial_parses)
    # offset=0
    # missing_num = 0
    # transitions=[]
    # dependencies = []
    # for o in range(len(sentences)):
    #     dependencies.append([])
    # assert (len(sentences) == len(partial_parses)), "Somethings fishy"    
    # while unfinished_parses:

    #     transitions = []
    #     transitions.append(model.predict(unfinished_parses[offset:offset+batch_size]))
    #     for i in range(batch_size):
    #         if (len(unfinished_parses) == 1) :
    #             break
    #         if (offset + i < len(unfinished_parses)):
    #             #print(transitions, transitions[0][i], unfinished_parses[offset+i].sentence)
    #             #print ("offset", offset, i, offset+i, len(sentences), len(partial_parses), len(unfinished_parses))
    #             unfinished_parses[offset+i].parse_step(transitions[0][i])
    #             #print (unfinished_parses[offset+i].dependencies, unfinished_parses[offset+i].stack)
    #             flag = 0
    #             #print ("Yo_0", offset+i, len(unfinished_parses[offset+i].dependencies), len(partial_parses[offset+i].sentence))
    #             if len(unfinished_parses[offset+i].dependencies) == len(partial_parses[offset+i].sentence):
    #                 for l in range(len(temp_parses)) :
    #                     if temp_parses[l].sentence == unfinished_parses[offset+i].sentence :
    #                         missing_num = l
    #                         #print ("Missing", missing_num)
    #                         if (not dependencies[missing_num]) :
    #                             #print ("Chosen", missing_num)                                
    #                             dependencies[missing_num].append(unfinished_parses[offset+i].dependencies) 
    #                             break   
    #             #if len(unfinished_parses[offset+i].stack) == 1:
    #                 #print ("Delete", offset+i, unfinished_parses[offset+i].sentence)       
    #                 del (unfinished_parses[offset+i])
    #                 del (partial_parses[offset+i])
    #                 #print (len(unfinished_parses))
    #                 flag = 1  
    #                 break   

    #     offset += batch_size
    #     #print ("offset", offset, len(unfinished_parses))
    #     if (offset>=len(unfinished_parses)):
    #         offset=0      
    #     if (flag == 1):
    #         offset = 0    
    #     if (len(unfinished_parses) == 1) :
    #         # transitions = []
    #         # transitions.append(model.predict(unfinished_parses[0]))
    #         for z in range(len(unfinished_parses[0].stack)-1):
    #             #print("Yo", transitions[0][1], unfinished_parses[0].sentence)
    #             unfinished_parses[0].parse_step(transitions[0][1])
    #             #print (unfinished_parses[0].dependencies, unfinished_parses[0].stack)
    #         if len(unfinished_parses[0].dependencies) == len(partial_parses[0].sentence):
    #             #print ("Yo")
    #             for l in range(len(temp_parses)) :
    #                 if temp_parses[l].sentence == unfinished_parses[0].sentence :
    #                     missing_num = l
    #                     #print ("Missing", missing_num)
    #                     if (not dependencies[missing_num]) :
    #                         #print ("Chosen", missing_num)
    #                         dependencies[missing_num].append(unfinished_parses[0].dependencies) 
    #                         break   
    #         if len(unfinished_parses[0].stack) == 1:
    #             #print ("Delete", 0)         
    #             del (unfinished_parses[0])     
    #             del (partial_parses[0])
    #             #print(unfinished_parses)     
    #     #break
    # ### END YOUR CODE
    # dependencies = list(chain.from_iterable(dependencies))
    # print (dependencies)
    partial_parses = [PartialParse(i) for i in sentences]
    unfinished_parses = list(partial_parses)
    dependencies = []
    while len(unfinished_parses):
        minibatch = unfinished_parses[:batch_size]
        transitions = model.predict(minibatch)

        for i in range(len(minibatch)):
            minibatch[i].parse_step(transitions[i])

        unfinished_parses = [i for i in partial_parses if len(i.stack)>1 or len(i.buffer)>0]
         
    dependencies = [i.dependencies for i in partial_parses]

    ### END YOUR CODE
    #print (dependencies)
    
    return dependencies


def test_step(name, transition, stack, buf, deps,
              ex_stack, ex_buf, ex_deps):
    """Tests that a single parse step returns the expected output"""
    pp = PartialParse([])
    pp.stack, pp.buffer, pp.dependencies = stack, buf, deps

    pp.parse_step(transition)
    stack, buf, deps = (tuple(pp.stack), tuple(pp.buffer), tuple(sorted(pp.dependencies)))
    assert stack == ex_stack, \
        "{:} test resulted in stack {:}, expected {:}".format(name, stack, ex_stack)
    assert buf == ex_buf, \
        "{:} test resulted in buffer {:}, expected {:}".format(name, buf, ex_buf)
    assert deps == ex_deps, \
        "{:} test resulted in dependency list {:}, expected {:}".format(name, deps, ex_deps)
    print "{:} test passed!".format(name)


def test_parse_step():
    """Simple tests for the PartialParse.parse_step function
    Warning: these are not exhaustive
    """
    test_step("SHIFT", "S", ["ROOT", "the"], ["cat", "sat"], [],
              ("ROOT", "the", "cat"), ("sat",), ())
    test_step("LEFT-ARC", "LA", ["ROOT", "the", "cat"], ["sat"], [],
              ("ROOT", "cat",), ("sat",), (("cat", "the"),))
    test_step("RIGHT-ARC", "RA", ["ROOT", "run", "fast"], [], [],
              ("ROOT", "run",), (), (("run", "fast"),))


def test_parse():
    """Simple tests for the PartialParse.parse function
    Warning: these are not exhaustive
    """
    sentence = ["parse", "this", "sentence"]
    dependencies = PartialParse(sentence).parse(["S", "S", "S", "LA", "RA", "RA"])
    dependencies = tuple(sorted(dependencies))
    expected = (('ROOT', 'parse'), ('parse', 'sentence'), ('sentence', 'this'))
    assert dependencies == expected,  \
        "parse test resulted in dependencies {:}, expected {:}".format(dependencies, expected)
    assert tuple(sentence) == ("parse", "this", "sentence"), \
        "parse test failed: the input sentence should not be modified"
    print "parse test passed!"


class DummyModel:
    """Dummy model for testing the minibatch_parse function
    First shifts everything onto the stack and then does exclusively right arcs if the first word of
    the sentence is "right", "left" if otherwise.
    """
    def predict(self, partial_parses):
   
        return [("RA" if pp.stack[1] is "right" else "LA") if len(pp.buffer) == 0 else "S"
                for pp in partial_parses]


def test_dependencies(name, deps, ex_deps):
    """Tests the provided dependencies match the expected dependencies"""
    deps = tuple(sorted(deps))
    assert deps == ex_deps, \
        "{:} test resulted in dependency list {:}, expected {:}".format(name, deps, ex_deps)


def test_minibatch_parse():
    """Simple tests for the minibatch_parse function
    Warning: these are not exhaustive
    """
    sentences = [["right", "arcs", "only"],
                 ["right", "arcs", "only", "again"],
                 ["left", "arcs", "only"],
                 ["left", "arcs", "only", "again"]]
    deps = minibatch_parse(sentences, DummyModel(), 2)
    print (deps, len(deps))    
    test_dependencies("minibatch_parse", deps[0],
                      (('ROOT', 'right'), ('arcs', 'only'), ('right', 'arcs')))
    test_dependencies("minibatch_parse", deps[1],
                      (('ROOT', 'right'), ('arcs', 'only'), ('only', 'again'), ('right', 'arcs')))
    test_dependencies("minibatch_parse", deps[2],
                      (('only', 'ROOT'), ('only', 'arcs'), ('only', 'left')))
    test_dependencies("minibatch_parse", deps[3],
                      (('again', 'ROOT'), ('again', 'arcs'), ('again', 'left'), ('again', 'only')))
    print "minibatch_parse test passed!"

if __name__ == '__main__':
    test_parse_step()
    test_parse()
    test_minibatch_parse()
