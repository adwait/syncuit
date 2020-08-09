import numpy as np

import circuit
import random
import config


class CircuitSyn(circuit.Ciruit):

    def __init__(self, name=""):
        super().__init__(name)
        self.cost = 0
        self.answer = 0
        # self.model_initialize()

    def series_augment(self, component):
        
        new_node = len(self.skeleton.vertices)
        new_value = random.choice(config.RES_VALS)

        res = circuit.Resistor("r" + str(new_node), new_value)
        conns = self.remove_component(component)

        self.add_component(component, (conns[0], new_node))
        self.add_component(res, (new_node, conns[1]))

        self.cost += 2.0


    def parallel_augment(self, component):
        
        new_node = len(self.skeleton.vertices)
        new_value = random.choice(config.RES_VALS)

        conns = self.get_connection_ends(component)

        res = circuit.Resistor("r" + str(new_node), new_value)
        self.add_component(res, (conns[0], conns[1]))

        self.cost += 3.0


    def augment(self):
        
        weights = np.array(config.WEIGHTS)
        weights = [i/sum(weights) for i in weights]

        print(weights)

        aug_func = np.random.choice([self.series_augment, self.parallel_augment], 1, p=weights)
        r_comp = random.choice(self.components)
        
        aug_func[0](r_comp[0])
        

    def pprint(self):
        super().pprint()
        print()
        print("\tsolve cost is {}".format(self.cost))