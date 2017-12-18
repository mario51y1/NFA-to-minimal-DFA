# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 12:31:51 2017

@author: mario
"""

import os
from prettytable import PrettyTable
#   The reader class opens a file where the automaton is written. The format of the file
#   Can be found in the documentation. When its readed, returns the information obtained so
#   The class table can be created

class reader:
    
    #Initializer gets the name of the file and creates empyt lists    
    def __init__(self,name):        
        self.states = []
        self.alphabet = []
        self.initialState = ''
        self.finals = []
        self.transitions = []
        self.name = name
        pass
    
    #gets the states of the automaton
    def getStates(self):
        entry = self.file.readline()
        self.states = entry.split()[2:]
        pass
    
    #gets the entry alphabet pf the automaton
    def getAlphabet(self):
        entry = self.file.readline()
        self.alphabet = entry.split()[2:]
        self.alphabet.append('empty')
        pass
    #gets the initial state of the automaton
    def getInitial(self):
        entry = self.file.readline()
        self.initialState = entry.split()[-1]
        pass
    
    #gets the final states of the automaton
    def getFinals(self):
        entry = self.file.readline()
        self.finals = entry.split()[2:]
        pass
    
    #gets the transitions of the automaton
    def getTransitions(self):
        for line in self.file:
            entry = line.split()

            index_1 = entry.index(";")
            index_2 = entry.index("=")
            
            states = entry[:index_1]
            alpha = entry[index_1+1:index_2]
            next_states = entry[index_2+1:]
            
            self.transitions += [[states[0],alpha,next_states]]          
        
        pass            
    #opens the file and reads the content of the automaton
    def read_file(self):
        self.file = open(self.name,"r")
        
        self.getStates()
        self.getAlphabet()        
        self.getInitial()
        self.getFinals()
        self.getTransitions()
        
        self.file.close()
        pass
    
    #
    def return_values(self):
        packed = (self.states,self.alphabet,self.initialState,self.finals,self.transitions)
        return packed
    
class transitionTable:
    def __init__ (self,values):
        self.states = values[0]
        self.alphabet = values[1]
        self.initialState = values[2]
        self.finals = values[3]
        self.transitions = values[4]
        
        self.createTransitionTable()
        pass
    
    #every row of the table has the entry alphabet, the empty entry and the actual state
    def createTransitionTable(self):
        alphabetSize = len(self.alphabet) + 1
        a = len(self.states)
        t = []
        
        # creates the matrix with empty list with states * alphabet+1 dimension
        for i in range(a):
            t.append([])
        for i in t:
            i.append("")
            for j in range(alphabetSize-1):
                i.append([])
        
        # puts in the first element of each row the actual each state
        num=0
        for i in t:
            i[0]=self.states[num]
            num+=1
        
        for i in self.transitions:
            num = self.states.index(i[0])
            for entry in i[1]:
                index = self.alphabet.index(entry)
                for s in i[2]:
                    t[num][index+1].append(s)
                
        #now removes the repeated states and orders them+
        for i in range(len(t)):            
            for j in range(1,len(t[0])):
                t[i][j] = sorted(set(t[i][j]))
   
        self.table = t

        pass
    
    # returns all the values from the table
    def return_values(self):
        packed = (self.states,self.alphabet,self.initialState,self.finals,self.table)
        return packed
    
    
class algorithm:
    def __init__(self,values):
        self.states = values[0]
        self.alphabet = values[1]
        self.initialState = values[2]
        self.finals = values[3]
        self.transitions = values[4]
    
        self.rowSize = len(self.alphabet) +1
    
        self.initAlgoTable()
        
        self.doAlgorithm()
        
    def printTable(self,final=False):
        s = ['State'] + self.alphabet[:-1] + ["FINAL"]
        
        t = PrettyTable(s)
        for i in self.table:
            t.add_row(i)
        os.system('cls||clear')
        if final:
            print("FINAL STATE OF THE AUTOMATON \n")
        print (t)
        print("\n Press enter to continue")
        input()

    
    # returns the row of the transition table where a state is
    def find_state_in_transitions(self,state):
        i = 0
        found = False
        for t in self.transitions:
            if not(found):
                if t[0] == state:
                    found = True
                else:
                    i+=1      
        if found:
            return i
        else:
            return -1
        
    # adds a row with a new state to the table
    def addRow(self,state):   
        row = []
        for i in range(self.rowSize):
            row.append([])
        row[0]= state
        self.table.append(row)
        self.printTable()
        pass
        
    # initializes the table with the error state and the initial state
    def initAlgoTable(self):
        self.table = []
        
        error_row = []
        for i in range(self.rowSize):
            error_row.append(["error"])
        error_row[-1] = ("Not final")
        self.table.append(error_row)
        
        self.addRow([self.initialState])
        
    # checks if the current cell of the table has the states and if not adds them
    def addStates(self,cell,states):
        for s in states:
            if cell.count(s) == 0:
                if s != "error":
                    cell.append(s)
                    self.printTable()
        
    # checks if a state exists in the automaton
    def exists_state(self,state):
        exists = False
        for r in self.table:
            if not(exists):
                if r[0] == state:
                    exists = True

        return exists

    # check if a state has one of his states as a final state
    def checkFinal(self,row):
        final = False
        for s in row[0]:
            if self.finals.count(s) > 0:
                final = True
        if final:
            row[-1] = "Final state"
        else:
            row[-1] = "Not final"

    # the loop for the algorithm
    def doAlgorithm(self):
        c = 1
        loop = True
        
        # loops while rows are added to th table, if it finishes the last row, it will stop
        # sinc there are no more states in the automaton. Since the table is constantly
        # changing, you need to loop with a boolean, and every time the loops ends
        # it check if you have to still loop (there are more rows that have been added)
        # or not (the last row checked was the final row of the table)
        while loop:
            
            # starts to check rows begining from the last row of the previous iteration
            for row in self.table[c:]:  
                
                # for every simple state in the full state of the DFA we have to check all the transitions
                for s in row[0]:
                    # first step is to add every state that can be accesed from an empty transition
                    # the for checks for every partial state that is part of the actual state in the
                    # DFA automaton
                    
                    # gets the row in transition table for the simple state and ads the empty transitions
                    state_index = self.find_state_in_transitions(s)
                    transition_row = self.transitions[state_index]
                    
                    self.addStates(row[0],transition_row[-1])
                    
                    # we dont need to iterate in the empty transitions, so we erase them
                    transition_row=transition_row[:-1]
                    
                    # we check every transition and add the result states to the current row
                    for i in range(1,len(transition_row)):
                        self.addStates(row[i],transition_row[i])
                        # we check for empty transitions from the added states like we did before
                        for j in row[i]:
                            index_aux = self.find_state_in_transitions(j)
                            aux_transition_row = self.transitions[index_aux]
                            self.addStates(row[i],aux_transition_row[-1])
                            
                # now we have to order the states of the list so the algorithm doesnt take, for example:
                # [a,b] and [b,a] as different states. Also, for empty transitions we add the transition to error               
                for s in range(len(row)):
                    row[s]=sorted(row[s])
                    if row[s] == []:
                        row[s] = ["error"]
                        
                self.checkFinal(row)
                self.printTable()
                # the algorithm checks if all the transitions have a current state of the automaton asociated.
                # if not, adds a row in the table with the state
                for s in row[1:-1]:
                    if not(self.exists_state(s)):
                        self.addRow(s)
               

                # increments the last row that has been checked and checks if it is the last row of the table
                # (no more states have been added to the automaton)
                c += 1
                if c > len(self.table)-1:
                    loop = False
        self.printTable(final=True)
        pass
    
def main():
    r = reader("file.txt")
    r.read_file()
    values = r.return_values()
    
    t = transitionTable(values)
    values = t.return_values()
    
    a = algorithm(values)
    
    pass
if __name__ == "__main__":
    main()