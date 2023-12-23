Original code written by Leo Medina 2015, adapted by Nathan Titus 2022

This code was based off of the "MRG" Fiber Model described in:

McIntyre CC, Richardson AG, and Grill WM. Modeling the excitability of
mammalian nerve fibers: influence of afterpotentials on the recovery
cycle. Journal of Neurophysiology 87:995-1006, 2002.

This code was run using: 
NEURON 7.7 (with python)
Python 3

Simmulations for Gilbert et al were run using the resources of the Duke Computing Cluster.

This code was run in a linux environment but could be run on other platforms.

To run this code:
1. You will need to have installed NEURON and Python
2. Compile the .mod files in the mechanisms folder and add the resulting dll file to the main directory.
3. Use RunDCFiber.py to run the simulations.
4. The variables instantiated with command line arguments should match one of the voltage distribution files.

The rights to this code are reserved by the Warren Grill lab group; however, we allow use and redistribution of the code for non-commercial applications.

The copyrights of this software are owned by Duke University. As such, two licenses for this software are offered:

1. An open-source license under the GPLv2 license for non-commercial use.

2. A custom license with Duke University, for commercial use without the GPLv2 license restrictions. 

 

As a recipient of this software, you may choose which license to receive the code under. Outside contributions to the Duke-owned code base cannot be accepted unless the contributor transfers the copyright to those changes over to Duke University.

To enter a custom license agreement without the GPLv2 license restrictions, please contact the Digital Innovations department at the Duke Office for Translation & Commercialization (OTC) (https://olv.duke.edu/software/) at otcquestions@duke.edu with reference to “OTC File No. T-007874 in your email. 

 

Please note that this software is distributed AS IS, WITHOUT ANY WARRANTY; and without the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.