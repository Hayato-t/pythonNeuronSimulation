import sys
import numpy as np
import matplotlib.pyplot as plt
from mpi4py import MPI
sys.path.append("/home/hayato/lib/python")
sys.path.append("./modules")
import neuron
import generateNetworkMod
import setStimulusMod
import ioMod
import argparse

p = argparse.ArgumentParser()
p.add_argument("--nostore", action="store_true")
args = p.parse_args()

# variable
external = True
paths = {}
paths['dynamics_def_path'] = './testdata/graded_single/test1.dyn'
paths['connection_def_path'] = './testdata/graded_single/test1.nwk'
paths['stim_setting_path'] = './testdata/graded_single/test1.stm'
paths['record_setting_path'] = './testdata/graded_single/test1.rec'
## you must set these variable even though 'external' is True
v_init = -65
tstop = 300
## you must set these variable if 'external' is False
neuron_num = 3
dynamics_list = ['HH', 'G', 'HH']
neuron_connection = [[0, 1], [1, 0], [1, 2]]
rec_index_list = [0, 1, 2]
stim_settings = [[1, 50, 50, 0.1], [0, 150, 50, 0.1]]

print("nostore = " + str(args.nostore) + " external = " + str(external) + "\n")

# read external file
if external is True:
    neuron_num, dynamics_list, neuron_connection, stim_settings, rec_index_list = ioMod.readExternalFiles(paths)

# parallelcontext object
pc = neuron.h.ParallelContext()
pc.runworker()

# neuron definition
neuron_list = generateNetworkMod.generateNeuron(neuron_num, dynamics_list=dynamics_list, parallel=pc)
print(neuron_list)

# network definition
con_list = generateNetworkMod.generateNetworks(neuron_list, neuron_connection)
print(con_list)

# stimulation definition
# list elements contain [index, delay, duration, amplitude]
stim_list = setStimulusMod.setStimulus(neuron_list, stim_settings)

# recoding setting
rec_v_list = []
rec_t = neuron.h.Vector()
rec_t.record(neuron.h._ref_t)
for i in rec_index_list:
    rec_v = neuron.h.Vector()
    rec_v.record(neuron_list[i].soma(0.5)._ref_v)
    rec_v_list.append(rec_v)

# simulation
neuron.h.finitialize(v_init)
neuron.run(tstop)

# convert results
t = rec_t.as_numpy()
r_v_list = [r_v.as_numpy() for r_v in rec_v_list]

# show graph
for v in r_v_list:
    plt.plot(t, v)
plt.show()

# pickle all parameters, settings, and results
if args.nostore is False:
    if external is True:
        ioMod.pickleData(external=external, paths=paths, conditions=[v_init, tstop], results={'t': t, 'r_v_list': r_v_list})
    if external is False:
        ioMod.pickleData(external=external, input=[neuron_num, dynamics_list, neuron_connection, stim_settings, rec_index_list], conditions=[v_init, tstop], results={'t': t, 'r_v_list': r_v_list})
