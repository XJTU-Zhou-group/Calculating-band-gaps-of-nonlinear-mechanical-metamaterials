import os
from abaqus import *
from abaqusConstants import *
from assembly import *
from connectorBehavior import *
from interaction import *
from job import *
from load import *
from material import *
from mesh import *
from odbAccess import *
from part import *
from section import *
from sketch import *
from step import *
from visualization import *
from viewerModules import *
from numpy import *
from decimal import *
from operator import *
from string import *
import datetime
import math
import meshEdit
import os
import random
import shutil
import time
import visualization
import numpy


#change input for MPC
text_file = open('./'+'bloch_3D'+".inp", "w")
ne=0
for line in open('notFinal.inp'):
    if ne==1:
    	if line[0:2]=='10':
            text_file.write(line[0:-1]+', '+'Virtual1' +'\n')
    	elif line[0:2]=='11':
            text_file.write(line[0:-1]+', '+'Virtual2' +'\n')
    	else:
            line_tmp=line.split(',')
            NUM=line_tmp[1]
            NUM_tmp=NUM.strip()
            text_file.write(line[0:-1]+', ImNode-2-'+NUM_tmp[9:]+'\n')
    	ne=0
    else:
    	text_file.write(line)
    if line[0:4]=='*MPC':
    	ne=1
text_file.close()

#run
mdb.JobFromInputFile(explicitPrecision=SINGLE, inputFileName=
    'bloch_3D'+'.inp', memory=14, memoryUnits=GIGA_BYTES, 
    multiprocessingMode=DEFAULT, name='bloch_3D', nodalOutputPrecision=SINGLE, 
    numCpus=12, numDomains=12, parallelizationMethodExplicit=DOMAIN, 
    type=ANALYSIS, userSubroutine='E:/ABAQUS/3D_bloch/'+'SUB.for')

