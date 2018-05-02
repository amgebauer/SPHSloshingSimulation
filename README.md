# PBM project: Sloshing simulation with DualSPHysics

This is a small python project controlling the execution of
DualSPHysics simulating the sloshing of a fluid within a
rotating container.

** Work in progress! **

## Setup

Create a subdirectory `execs` and place the executables of DualSPHysics there.

Execute the simulation with python with the following command:

```
python simulate.py
```

If you are using windows as operating system, add the paths of the DualSPHysics executables in the
corresponding section in `lib/config.py`.

## Requirements

* Python 3
* DualSPHysics 4
* Ubuntu 16.04 (other linux systems should work)
* Windows (with adaptions, see section Setup)

MAC OS X is not supported since DualSPHysics cannot be compiled for MAC right now.