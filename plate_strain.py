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


execfile('blochbound2D.py')

Mdb()

Radius_1=4.57
Radius_2=4.16
Radius_3=4.16
Radius_4=4.57
pitch=20.0
L=pitch
seed_size=0.19
strain=0.28


mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), point2=(pitch, pitch))
mdb.models['Model-1'].Part(dimensionality=TWO_D_PLANAR, name='Part-1', type=DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-1'].BaseShell(sketch=mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

mdb.models['Model-1'].parts['Part-1'].HoleFromEdges(diameter=2*Radius_1, distance1=pitch/4
    , distance2=pitch/4, edge1=mdb.models['Model-1'].parts['Part-1'].edges.findAt(((0.0,1.0,0.0),))[0], 
    edge2=mdb.models['Model-1'].parts['Part-1'].edges.findAt(((1.0,0.0,0.0),))[0])
mdb.models['Model-1'].parts['Part-1'].HoleFromEdges(diameter=2*Radius_2, distance1=pitch/4
    , distance2=pitch/4, edge1=mdb.models['Model-1'].parts['Part-1'].edges.findAt(((1.0,0.0,0.0),))[0], 
    edge2=mdb.models['Model-1'].parts['Part-1'].edges.findAt(((pitch,1.0,0.0),))[0])
mdb.models['Model-1'].parts['Part-1'].HoleFromEdges(diameter=2*Radius_3, distance1=pitch/4
    , distance2=pitch/4, edge1=mdb.models['Model-1'].parts['Part-1'].edges.findAt(((0.0,1.0,0.0),))[0], 
    edge2=mdb.models['Model-1'].parts['Part-1'].edges.findAt(((1.0,pitch,0.0),))[0])
mdb.models['Model-1'].parts['Part-1'].HoleFromEdges(diameter=2*Radius_4, distance1=pitch/4
    , distance2=pitch/4, edge1=mdb.models['Model-1'].parts['Part-1'].edges.findAt(((1.0,pitch,0.0),))[0], 
    edge2=mdb.models['Model-1'].parts['Part-1'].edges.findAt(((pitch,1.0,0.0),))[0])

mdb.models['Model-1'].Part(dimensionality=TWO_D_PLANAR, name='Part-3', type=DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-3'].ReferencePoint(point=(0.0, 0.0, 0.0))
mdb.models['Model-1'].Part(dimensionality=TWO_D_PLANAR, name='Part-4', type=DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-4'].ReferencePoint(point=(0.0, 0.0, 0.0))

#material
mdb.models['Model-1'].Material(name='PDMS')
mdb.models['Model-1'].materials['PDMS'].Hyperelastic(
    materialType=ISOTROPIC, testData=OFF, type=NEO_HOOKE, 
    volumetricResponse=VOLUMETRIC_DATA, table=((0.54, 1.0E-3,), ))
mdb.models['Model-1'].materials['PDMS'].Density(table=((1.05e-09, ), ))
mdb.models['Model-1'].HomogeneousSolidSection(material='PDMS', name='PDMS', thickness=None)
mdb.models['Model-1'].parts['Part-1'].Set(faces=
    mdb.models['Model-1'].parts['Part-1'].faces.findAt(((L/20.0, L/20.0,0.0),), ), name='Set-1')
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Part-1'].sets['Set-1'], sectionName='PDMS', 
    thicknessAssignment=FROM_GEOMETRY)
#FROM_SECTION

mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-1-Re', 
    part=mdb.models['Model-1'].parts['Part-1'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-1-Im', 
    part=mdb.models['Model-1'].parts['Part-1'])

mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Virtual1', 
    part=mdb.models['Model-1'].parts['Part-3'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Virtual2', 
    part=mdb.models['Model-1'].parts['Part-4'])
mdb.models['Model-1'].rootAssembly.Set(name='Virtual1', referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['Virtual1'].referencePoints[1],))
mdb.models['Model-1'].rootAssembly.Set(name='Virtual2', referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['Virtual2'].referencePoints[1],))

#element

mdb.models['Model-1'].rootAssembly.setElementType(elemTypes=(ElemType(
    elemCode=CPE6H, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=DEFAULT), ElemType(
    elemCode=CPE8H, elemLibrary=STANDARD)), regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-Re'].faces.findAt(((L/20.0, L/20.0, 0.0), ), ), ))
mdb.models['Model-1'].rootAssembly.setMeshControls(elemShape=TRI, regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-Re'].faces.findAt(((
    L/20.0, L/20.0, 0.0), ), ))
mdb.models['Model-1'].rootAssembly.seedPartInstance(deviationFactor=0.1, 
    minSizeFactor=0.1, regions=(mdb.models['Model-1'].rootAssembly.instances['Part-1-Re'], ), size=seed_size)
mdb.models['Model-1'].rootAssembly.generateMesh(regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-Re'], ))

mdb.models['Model-1'].rootAssembly.setElementType(elemTypes=(ElemType(
    elemCode=CPE6H, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=DEFAULT), ElemType(
    elemCode=CPE8H, elemLibrary=STANDARD)), regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-Im'].faces.findAt(((L/20.0, L/20.0, 0.0), ), ), ))
mdb.models['Model-1'].rootAssembly.setMeshControls(elemShape=TRI, regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-Im'].faces.findAt(((
    L/20.0, L/20.0, 0.0), ), ))
mdb.models['Model-1'].rootAssembly.seedPartInstance(deviationFactor=0.1, 
    minSizeFactor=0.1, regions=(mdb.models['Model-1'].rootAssembly.instances['Part-1-Im'], ), size=seed_size)
mdb.models['Model-1'].rootAssembly.generateMesh(regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-Im'], ))


mdb.models['Model-1'].rootAssembly.Set(edges=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-Re'].edges,), name='PerBound_Re')
mdb.models['Model-1'].rootAssembly.Set(edges=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-Im'].edges,), name='PerBound_Im')

execfile('Per-RK0.py')

BlochBound2D(mdb,'Model-1','PerBound_Re','PerBound_Im',[(L,0.0),(0.0,L)],)


# the first step
mdb.models['Model-1'].StaticStep(name='Step-1', nlgeom=ON, previous='Initial', maxNumInc=500, initialInc=0.01, 
    minInc=1e-09, maxInc=0.0625)

mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'BC-1', region=Region(referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['Virtual2'].referencePoints[1], 
    )), u1=UNSET, u2=-1*strain, ur3=UNSET)

mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'BC-2', region=Region(nodes=mdb.models['Model-1'].rootAssembly.instances['Part-1-Re'].nodes.
    getByBoundingSphere(center=(L/4, L/4-Radius_1, 0), radius=0.05)), u1=0.0, u2=0.0, ur3=UNSET)

mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'BC-3', region=Region(nodes=mdb.models['Model-1'].rootAssembly.instances['Part-1-Im'].nodes.
    getByBoundingSphere(center=(L/4, L/4-Radius_1, 0), radius=0.05)), u1=0.0, u2=0.0, ur3=UNSET)


mdb.Job(contactPrint=OFF, description='', echoPrint=OFF, explicitPrecision=
    SINGLE, historyPrint=OFF, memory=4, memoryUnits=GIGA_BYTES, model=
    'Model-1', modelPrint=OFF, multiprocessingMode=DEFAULT, name='notFinal_1', 
    nodalOutputPrecision=SINGLE, numCpus=1, numDomains=1, 
    parallelizationMethodExplicit=DOMAIN, type=ANALYSIS, 
    userSubroutine='E:/phd/Bloch wave/2D_band gaps/fan60_1.1/'+'SUB.for')

#write input8555
mdb.jobs['notFinal_1'].writeInput()

#change input for MPC
text_file = open('./'+'hole_bloch_1'+".inp", "w")
ne=0
for line in open('notFinal_1.inp'):
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
    'hole_bloch_1'+'.inp', memory=4, memoryUnits=GIGA_BYTES, 
    multiprocessingMode=DEFAULT, name='hole_bloch_1', nodalOutputPrecision=SINGLE, 
    numCpus=1, numDomains=1, parallelizationMethodExplicit=DOMAIN, 
    type=ANALYSIS, userSubroutine='E:/phd/Bloch wave/2D_band gaps/fan60_1.1/'+'SUB.for')

mdb.jobs['hole_bloch_1'].submit(consistencyChecking=OFF)
mdb.jobs['hole_bloch_1'].waitForCompletion()


odb = openOdb(path='hole_bloch_1.odb')
file_summary=open('E:/phd/Bloch wave/2D_band gaps/fan60_1.1/frequecy_summary.txt','a')
for num_step in range(1,61):
    step_name='Step-'+str(num_step+1)
    file_summary.write(str(num_step+1))
    nFrames=len(odb.steps[step_name].frames)
    for num_mode in range(0,(nFrames-1)/2):
#    for num_mode in range(0,nFrames-1):
        fre = odb.steps[step_name].frames[2*num_mode+1].frequency
#        fre = odb.steps[step_name].frames[num_mode+1].frequency
        file_summary.write(' %7.2f '%(fre))
    file_summary.write('\n' )

odb.close()
file_summary.close()
