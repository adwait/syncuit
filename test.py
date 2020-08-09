#!/usr/bin/python3

#%%
import circuit


myckt = circuit.Ciruit("new circuit")

voltage = circuit.Voltage("v1", 5)
res1 = circuit.Resistor("r1", 10)
res2 = circuit.Resistor("r2", 10)

myckt.add_component(voltage, (0, 1))
myckt.add_component(res1, (0, 2))
myckt.add_component(res2, (2, 1))

myckt.pprint()

#%%
