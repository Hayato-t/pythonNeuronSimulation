from mpi4py import MPI
# importing MPI must come before loading NEURON
import sys
sys.path.append("/home/hayato/lib/python")
from neuron import h

def f(x):
    """a function with no context that changes except its argument"""
    return x * x

pc = h.ParallelContext()
pc.runworker() # master returns immediately, workers in an
               # infinite loop running jobs from bulletin board

s = 0
if pc.nhost() == 1:          # use the serial form
    for i in range(20):
        s += f(i)
else:                        # use the bulleting board form
    for i in range(20):      # scatter processes
        pc.submit(f, i)      # any context needed by f had better be
                             # the same on all hosts
    while pc.working():      # gather results
        s += pc.pyret()      # the return value for the executed function

print s
pc.done()                    # tell workers to quit
