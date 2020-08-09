#!/usr/bin/python3

#%%
import sys
import argparse
import logging

import circuit
import synthesize

def main(args):

    loglevel = args.loglevel
    numeric_level = getattr(logging, loglevel.upper(), None)
    logging.basicConfig(format='%(levelname)s: at %(asctime)s: %(message)s', filename='example.log',level=numeric_level)

    myckt = synthesize.CircuitSyn("new circuit")

    voltage = circuit.Voltage("v1", 5)
    res1 = circuit.Resistor("r1", 10)
    res2 = circuit.Resistor("r2", 10)

    myckt.add_component(voltage, (0, 1))
    myckt.add_component(res1, (0, 2))
    myckt.add_component(res2, (2, 1))

    # myckt.parallel_augment(res1)
    # myckt.remove_component(res1)
    for i in range(3):
        myckt.augment()


    myckt.pprint()
    myckt.to_dot()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', "--log", help="logging level", dest='loglevel')

    args = parser.parse_args()

    main(args)