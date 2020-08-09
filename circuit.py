import enum
import logging
from collections import Counter

import graph


class ComponentType(enum.Enum):
    DEFAULT = 0
    WIRE = 1
    RESISTOR = 2
    VOLTAGE = 3

class Component:
    c_count = 0

    def __init__(self, name=""):
        self.c_id = Component.c_count
        Component.c_count += 1
        self.name = name
        self.type = ComponentType.DEFAULT
        self.value = 0

    def pprint(self):
        print("Component id: " + str(self.c_id) \
            + "  name: " + self.name + "  type: " \
            + str(self.type) + "  value: " + str(self.value))


class Resistor(Component):
    unit = 'Ohms'

    def __init__(self, name="", value=0):
        super().__init__(name)
        self.value = value
        self.type = ComponentType.RESISTOR      

class Voltage(Component):
    unit = 'Volts'

    def __init__(self, name="", value=0):
        super().__init__(name)
        self.value = value
        self.type = ComponentType.VOLTAGE



class Ciruit:
    
    def __init__(self, name=""):
        self.name = name
        self.skeleton = graph.Graph()
        self.components = []

    def pprint(self):
        print("printing Circuit " + self.name + " ...")
        print()
        print("Skeletal Graph:")
        self.skeleton.pprint()
        print("Components:")
        for (comp, ncs) in self.components:
            comp.pprint() 
            print("\t\t is connected between " + str(ncs[0]) + ", " + str(ncs[1]))
        
    def get_connection_ends(self, component):
        for (comp, conns) in self.components:
            if comp == component:
                return conns

        return False

    def add_component(self, component, nodeconns):
        self.components.append((component, nodeconns))
        nc0 = nodeconns[0]
        nc1 = nodeconns[1]

        if nc0 in self.skeleton.vertices:
            if component.type in self.skeleton.adjlist[nc0]:
                self.skeleton.adjlist[nc0][component.type][nc1] += 1
            else:
                self.skeleton.adjlist[nc0][component.type] = Counter({nc1: 1})
        else:
            self.skeleton.adjlist[nc0] = dict()
            self.skeleton.adjlist[nc0][component.type] = Counter({nc1: 1})
            self.skeleton.vertices.append(nc0)

        if nc1 in self.skeleton.vertices:
            if component.type in self.skeleton.adjlist[nc1]:
                self.skeleton.adjlist[nc1][component.type][nc0] += 1
            else:
                self.skeleton.adjlist[nc1][component.type] = Counter({nc0: 1})
        else:
            self.skeleton.adjlist[nc1] = dict()
            self.skeleton.adjlist[nc1][component.type] = Counter({nc0: 1})
            self.skeleton.vertices.append(nc1)


    def remove_component(self, component):
        found = None

        for (comp, conns) in self.components[:]:
            if component.c_id == comp.c_id:
                self.skeleton.adjlist[conns[0]][component.type][conns[1]] -= 1
                self.skeleton.adjlist[conns[1]][component.type][conns[0]] -= 1
                found = True
                break

        if found:
            print((component, conns))
            self.components.remove((component, conns))
            return conns

        return False

    def to_dot(self):
        g_str = "digraph {\n"
        vert_str = '; '.join(['n'+str(vert) for vert in self.skeleton.vertices])
        g_str += ('\t' + vert_str + '\n')
        for (component, conns) in self.components:
            if component.type == ComponentType.RESISTOR:
                g_str += ('n{0} -> n{1} [label="{2}",dir=none]\n'.format(conns[0], conns[1], 'R'))
            elif component.type == ComponentType.VOLTAGE:
                g_str += ('n{0} -> n{1} [label="{2}"]\n'.format(conns[0], conns[1], 'V'))
            

        g_str += '}\n'

        graphfile = 'circuit.dot'
        file = open(graphfile, 'w')
        file.write(g_str)

        logging.info('GraphViz dot file: {} generated'.format(graphfile))

    
    # def remove_component(self, component):
    #     if isinstance(component, Component):
    #         self.remove_component_by_comp()
    #     elif isinstance(component, tuple):
    #         self.remove_component_by_tup()
    #     else:
    #         logging.error("argument to remove component failed due to incompatible type")
        