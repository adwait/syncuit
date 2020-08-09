import logging

class Graph:

    def __init__(self):
        self.vertices = []
        self.adjlist = dict()

    def pprint(self):
        print("Nodes: ")
        n_str = ""
        for i in self.vertices:
            n_str += (str(i) + " ")
        print("\t" + n_str)
        print("Adjacencies: ")
        for i in self.vertices:
            print(str(i) + ":  " + str(self.adjlist[i]))
        print()


