# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 12:31:51 2017

@author: mario
"""

import numpy as np

#   The reader class opens a file where the automaton is written. The format of the file
#   Can be found in the documentation. When its readed, returns the information obtained so
#   The class table can be created

class reader:
    
    #Initializer gets the name of the file and creates empyt lists    
    def __init__(self,name):        
        self.states = []
        self.alphabet = []
        self.name = name
        
    #gets the states of the automaton
    def getStates(self):
        
        entry = self.file.readline()
        entry = entry[3:]
        self.states = entry.split()
        print(self.states)
    
    #gets the entry alphabet pf the automaton
    def getAlphabet(self):
        entry = self.file.readline()
        entry = entry[3:]
        self.alphabet = entry.split()
        print(self.alphabet)
    
    #opns the file and reads its content so the automaton can be readed
    def read_file(self):
        self.file = open(self.name,"r")
        
        self.getStates()
        self.getAlphabet()
        
        pass

def main():
    r = reader("file.txt")
    r.read_file()
    pass

if __name__ == "__main__":
    main()