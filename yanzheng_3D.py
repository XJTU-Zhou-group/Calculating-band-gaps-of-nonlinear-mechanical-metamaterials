# Wang Guoli 20171228

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

execfile('blochbound3D.py')

Mdb()

L=0.03
W=0.0035
R=0.006
nsize=W/2


s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=0.05)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
s.Line(point1=(0.0, R), point2=(0.0, -R))
s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, R), point2=(0.0, -R), direction=CLOCKWISE)
p = mdb.models['Model-1'].Part(name='ball', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['ball']
p.BaseSolidRevolve(sketch=s, angle=90.0, flipRevolveDirection=OFF)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['ball']
del mdb.models['Model-1'].sketches['__profile__']


s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=0.01)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(0.0, 0.0), point2=(W/2, W/2))
p1 = mdb.models['Model-1'].Part(name='beam', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p1 = mdb.models['Model-1'].parts['beam']
p1.BaseSolidExtrude(sketch=s, depth=L)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']


a = mdb.models['Model-1'].rootAssembly
a.Instance(name='beam-1', part=p1, dependent=ON)
a.Instance(name='beam-2', part=p1, dependent=ON)
a.Instance(name='beam-3', part=p1, dependent=ON)
p2 = a.instances['beam-2']
a.rotate(instanceList=('beam-2', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(1.0, 0.0, 0.0), angle=-90.0)
a.translate(instanceList=('beam-2', ), vector=(0.0, 0.0, W/2))
p2 = a.instances['beam-3']
a.rotate(instanceList=('beam-3', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 1.0, 0.0), angle=90.0)
a.translate(instanceList=('beam-3', ), vector=(0.0, 0.0, W/2))

a.LinearInstancePattern(instanceList=('beam-1', ), direction1=(1.0, 0.0, 
    0.0), direction2=(0.0, 1.0, 0.0), number1=2, number2=2, spacing1=L-W/2, spacing2=L-W/2)
a.LinearInstancePattern(instanceList=('beam-2', ), direction1=(0.0, 0.0, 
    1.0), direction2=(1.0, 0.0, 0.0), number1=2, number2=2, spacing1=L-W/2, spacing2=L-W/2)
a.LinearInstancePattern(instanceList=('beam-3', ), direction1=(0.0, 0.0, 
    1.0), direction2=(0.0, 1.0, 0.0), number1=2, number2=2, spacing1=L-W/2, spacing2=L-W/2)


p = mdb.models['Model-1'].parts['ball']
a.Instance(name='ball-1', part=p, dependent=ON)
a.translate(instanceList=('ball-1', ), vector=(0.0, L/2, 0.0))
a.RadialInstancePattern(instanceList=('ball-1', ), point=(L/2, L/2, 0.0), 
    axis=(0.0, 0.0, 1.0), number=4, totalAngle=360.0)
a.RadialInstancePattern(instanceList=('ball-1', ), point=(0.0, L/2, L/2), 
    axis=(1.0, 0.0, 0.0), number=4, totalAngle=360.0)

a.Instance(name='ball-2', part=p, dependent=ON)
a.translate(instanceList=('ball-2', ), vector=(0.0, L/2, 0.0))
a.rotate(instanceList=('ball-2', ), axisPoint=(L/2, 0.0, L/2), axisDirection=(
    0.0, 1.0, 0.0), angle=180.0)
a.RadialInstancePattern(instanceList=('ball-2', ), point=(L/2, L/2, 0.0), 
    axis=(0.0, 0.0, 1.0), number=4, totalAngle=360.0)
a.RadialInstancePattern(instanceList=('ball-2', ), point=(0.0, L/2, L/2), 
    axis=(1.0, 0.0, 0.0), number=4, totalAngle=360.0)


a.InstanceFromBooleanMerge(name='rve', instances=(a.instances['beam-1'], 
    a.instances['beam-2'], a.instances['beam-3'], 
    a.instances['beam-1-lin-1-2'], a.instances['beam-1-lin-2-1'], 
    a.instances['beam-1-lin-2-2'], a.instances['beam-2-lin-1-2'], 
    a.instances['beam-2-lin-2-1'], a.instances['beam-2-lin-2-2'], 
    a.instances['beam-3-lin-1-2'], a.instances['beam-3-lin-2-1'], 
    a.instances['beam-3-lin-2-2'], a.instances['ball-1'], 
    a.instances['ball-1-rad-2'], a.instances['ball-1-rad-3'], 
    a.instances['ball-1-rad-4'], a.instances['ball-1-rad-2-1'], 
    a.instances['ball-1-rad-3-1'], a.instances['ball-1-rad-4-1'], 
    a.instances['ball-2'], a.instances['ball-2-rad-2'], 
    a.instances['ball-2-rad-3'], a.instances['ball-2-rad-4'], 
    a.instances['ball-2-rad-2-1'], a.instances['ball-2-rad-3-1'], 
    a.instances['ball-2-rad-4-1'], ), keepIntersections=ON, 
    originalInstances=SUPPRESS, domain=GEOMETRY)



mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Density(table=((1160.0, ), ))
mdb.models['Model-1'].materials['Material-1'].Elastic(table=((1000000000.0, 0.4), ))
mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', material='Material-1', thickness=None)

p = mdb.models['Model-1'].parts['rve']
c = p.cells
p.SectionAssignment(region=Region(cells=c), sectionName='Section-1', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

p.seedPart(size=nsize, deviationFactor=0.1, minSizeFactor=0.1)
e = p.edges
pickedEdges = e.getSequenceFromMask(mask=(
    '[#4000402 #80400002 #804000 #20010080 #2000010 #4080001 #408000', 
    ' #8100 #10000102 #20 ]', ), )
p.seedEdgeBySize(edges=pickedEdges, size=2.5*nsize, deviationFactor=0.1, 
    minSizeFactor=0.1, constraint=FINER)


p.setMeshControls(regions=c, elemShape=TET, technique=FREE)

elemType1 = ElemType(elemCode=C3D8R, elemLibrary=STANDARD, 
    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=DEFAULT)
elemType2 = ElemType(elemCode=C3D6, elemLibrary=STANDARD, 
    secondOrderAccuracy=OFF, distortionControl=DEFAULT)
elemType3 = ElemType(elemCode=C3D4, elemLibrary=STANDARD, 
    secondOrderAccuracy=OFF, distortionControl=DEFAULT)

#elemType1 = ElemType(elemCode=C3D20R, elemLibrary=STANDARD, 
#    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
#    hourglassControl=DEFAULT, distortionControl=DEFAULT)
#elemType2 = ElemType(elemCode=C3D15, elemLibrary=STANDARD)
#elemType3 = ElemType(elemCode=C3D10, elemLibrary=STANDARD)
#p.setMeshControls(regions=c, elemShape=HEX, technique=STRUCTURED)
#elemType1 = ElemType(elemCode=C3D8R, elemLibrary=STANDARD, 
#    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
#    hourglassControl=DEFAULT, distortionControl=DEFAULT)
#elemType2 = ElemType(elemCode=C3D6, elemLibrary=STANDARD)
#elemType3 = ElemType(elemCode=C3D4, elemLibrary=STANDARD)
p.setElementType(regions=(c, ), elemTypes=(elemType1, elemType2, elemType3))
p.generateMesh()


a.Instance(name='rve-Re', part=p, dependent=ON)
a.Instance(name='rve-Im', part=p, dependent=ON)

del a.features['rve-1']
del a.features['beam-1']
del a.features['beam-2']
del a.features['beam-3']
del a.features['beam-1-lin-1-2']
del a.features['beam-1-lin-2-2']
del a.features['beam-1-lin-2-1']
del a.features['beam-2-lin-1-2']
del a.features['beam-2-lin-2-2']
del a.features['beam-2-lin-2-1']
del a.features['beam-3-lin-1-2']
del a.features['beam-3-lin-2-2']
del a.features['beam-3-lin-2-1']
del a.features['ball-1']
del a.features['ball-1-rad-2']
del a.features['ball-1-rad-3']
del a.features['ball-1-rad-4']
del a.features['ball-1-rad-2-1']
del a.features['ball-1-rad-3-1']
del a.features['ball-1-rad-4-1']
del a.features['ball-2']
del a.features['ball-2-rad-2']
del a.features['ball-2-rad-3']
del a.features['ball-2-rad-4']
del a.features['ball-2-rad-2-1']
del a.features['ball-2-rad-3-1']
del a.features['ball-2-rad-4-1']


###zhijing 2cm midu 1.16g cm3

Refaces=[]
Refaces.append(mdb.models['Model-1'].rootAssembly.instances['rve-Re'].faces.getByBoundingBox(-0.0001,-0.0001,-0.0001,0.0001,L+0.0001,L+0.0001))
Refaces.append(mdb.models['Model-1'].rootAssembly.instances['rve-Re'].faces.getByBoundingBox(-0.0001,-0.0001,-0.0001,L+0.0001,0.0001,L+0.0001))
Refaces.append(mdb.models['Model-1'].rootAssembly.instances['rve-Re'].faces.getByBoundingBox(-0.0001,-0.0001,-0.0001,L+0.0001,L+0.0001,0.0001))
Refaces.append(mdb.models['Model-1'].rootAssembly.instances['rve-Re'].faces.getByBoundingBox(L-0.0001,-0.0001,-0.0001,L+0.0001,L+0.0001,L+0.0001))
Refaces.append(mdb.models['Model-1'].rootAssembly.instances['rve-Re'].faces.getByBoundingBox(-0.0001,L-0.0001,-0.0001,L+0.0001,L+0.0001,L+0.0001))
Refaces.append(mdb.models['Model-1'].rootAssembly.instances['rve-Re'].faces.getByBoundingBox(-0.0001,-0.0001,L-0.0001,L+0.0001,L+0.0001,L+0.0001))
mdb.models['Model-1'].rootAssembly.Set(faces=Refaces, name='PerBound_Re')

Imfaces=[]
Imfaces.append(mdb.models['Model-1'].rootAssembly.instances['rve-Im'].faces.getByBoundingBox(-0.0001,-0.0001,-0.0001,0.0001,L+0.0001,L+0.0001))
Imfaces.append(mdb.models['Model-1'].rootAssembly.instances['rve-Im'].faces.getByBoundingBox(-0.0001,-0.0001,-0.0001,L+0.0001,0.0001,L+0.0001))
Imfaces.append(mdb.models['Model-1'].rootAssembly.instances['rve-Im'].faces.getByBoundingBox(-0.0001,-0.0001,-0.0001,L+0.0001,L+0.0001,0.0001))
Imfaces.append(mdb.models['Model-1'].rootAssembly.instances['rve-Im'].faces.getByBoundingBox(L-0.0001,-0.0001,-0.0001,L+0.0001,L+0.0001,L+0.0001))
Imfaces.append(mdb.models['Model-1'].rootAssembly.instances['rve-Im'].faces.getByBoundingBox(-0.0001,L-0.0001,-0.0001,L+0.0001,L+0.0001,L+0.0001))
Imfaces.append(mdb.models['Model-1'].rootAssembly.instances['rve-Im'].faces.getByBoundingBox(-0.0001,-0.0001,L-0.0001,L+0.0001,L+0.0001,L+0.0001))
mdb.models['Model-1'].rootAssembly.Set(faces=Imfaces, name='PerBound_Im')


#mdb.models['Model-1'].rootAssembly.Surface(side1Faces=
#    mdb.models['Model-1'].rootAssembly.instances['rve-Re'].faces, name='surface_Re')
#mdb.models['Model-1'].rootAssembly.Surface(side1Faces=
#    mdb.models['Model-1'].rootAssembly.instances['rve-Im'].faces, name='surface_Im')

#mdb.models['Model-1'].rootAssembly.Set(faces=(
#    mdb.models['Model-1'].rootAssembly.instances['rve-Re'].faces,), name='PerBound_Re')
#mdb.models['Model-1'].rootAssembly.Set(faces=(
#    mdb.models['Model-1'].rootAssembly.instances['rve-Im'].faces,), name='PerBound_Im')

mdb.models['Model-1'].rootAssembly.Set(nodes=
    mdb.models['Model-1'].rootAssembly.sets['PerBound_Re'].nodes, name='surface_Re')
mdb.models['Model-1'].rootAssembly.Set(nodes=
    mdb.models['Model-1'].rootAssembly.sets['PerBound_Im'].nodes, name='surface_Im')


execfile('Per-RK0.py')

BlochBound3D(mdb,'Model-1','PerBound_Re','PerBound_Im',[(L,0.0,0.0),(0.0,L,0.0),(0.0,0.0,L)],)

#mdb.models['Model-1'].FrequencyStep(acousticCoupling=AC_OFF, eigensolver=SUBSPACE, 
#    maxIterations=1000, name='Step-1', maxEigen=10000.0, normalization=DISPLACEMENT, 
#    numEigen=500, previous='Initial', simLinearDynamics=OFF, vectors=108)
mdb.models['Model-1'].FrequencyStep(name='Step-1', previous='Initial', 
    maxEigen=10000, minEigen=1, numEigen=200, eigensolver=LANCZOS, blockSize=DEFAULT, maxBlocks=DEFAULT)

for i in range(0,120):
#    mdb.models['Model-1'].FrequencyStep(acousticCoupling=AC_OFF, eigensolver=SUBSPACE, 
#        maxIterations=1000, name='Step-'+str(i+2), maxEigen=10000.0, normalization=DISPLACEMENT, 
#        numEigen=500, previous='Step-'+str(i+1), simLinearDynamics=OFF, vectors=108)
    mdb.models['Model-1'].FrequencyStep(name='Step-'+str(i+2), previous='Step-'+str(i+1), 
        maxEigen=10000, minEigen=1, numEigen=200, eigensolver=LANCZOS, blockSize=DEFAULT, maxBlocks=DEFAULT)

mdb.Job(contactPrint=OFF, description='', echoPrint=OFF, explicitPrecision=
    SINGLE, historyPrint=OFF, memory=4, memoryUnits=GIGA_BYTES, model=
    'Model-1', modelPrint=OFF, multiprocessingMode=DEFAULT, name='notFinal', 
    nodalOutputPrecision=SINGLE, numCpus=1, numDomains=1, 
    parallelizationMethodExplicit=DOMAIN, type=ANALYSIS, 
    userSubroutine='E:/ABAQUS/3D_bloch/'+'SUB.for')

#write input8555
mdb.jobs['notFinal'].writeInput()

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
    'bloch_3D'+'.inp', memory=12, memoryUnits=GIGA_BYTES, 
    multiprocessingMode=DEFAULT, name='bloch_3D', nodalOutputPrecision=SINGLE, 
    numCpus=12, numDomains=12, parallelizationMethodExplicit=DOMAIN, 
    type=ANALYSIS, userSubroutine='F:/ABAQUS/3D_bloch/'+'SUB.for')

mdb.jobs['bloch_3D'].submit(consistencyChecking=OFF)
mdb.jobs['bloch_3D'].waitForCompletion()

# PostProgressing 

odb = openOdb(path='bloch_3D1-100.odb')
file_summary=open('E:/ABAQUS/3D_bloch/frequecy_summary.txt','a')
for num_step in range(0,121):
    step_name='Step-'+str(num_step+1)
    file_summary.write(str(num_step+1))
    nFrames=len(odb.steps[step_name].frames)
    for num_mode in range(0,nFrames-1):
    #for num_mode in range(0,nFrames-1):
        fre = odb.steps[step_name].frames[num_mode+1].frequency
        file_summary.write(' %7.2f '%(fre))
    file_summary.write('\n' )

odb.close()
file_summary.close()

