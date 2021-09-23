#Created by wanggl
#2017/10/27
#CREATED IN ABAQUS VERSION 6.11-1.

#FUNCTION TO APPLY PERIODIC BOUNDARY CONDITIONS IN 3D
#mdb: model database
#NameModel: 	A string with the name of your model
#NameSet: 	A string with the name of your set (for a faster script, this set 
#		should only contain those nodes that will have periodic boundary conditions applied to them)
#LatticeVec:	An array with the lattice vectors, for example [(1.0, 0.0), (1.0, 1.0)] for a square lattice
def BlochBound3D(mdb,NameModel,NameSetRe,NameSetIm,LatticeVec):
    #Get all nodes
    nodesAllRe=mdb.models[NameModel].rootAssembly.sets[NameSetRe].nodes
    nodesAllReCoor=[]
    for nodRe in mdb.models[NameModel].rootAssembly.sets[NameSetRe].nodes:
	nodesAllReCoor.append(nodRe.coordinates)
    nodesAllIm=mdb.models[NameModel].rootAssembly.sets[NameSetIm].nodes
    nodesAllImCoor=[]
    for nodIm in mdb.models[NameModel].rootAssembly.sets[NameSetIm].nodes:
	nodesAllImCoor.append(nodIm.coordinates)
    repConst=0
    #Find periodically located nodes and apply mpc constraints
    ranNodesRe=range(0,len(nodesAllRe))
    ranNodesIm=range(0,len(nodesAllIm))	#Index array of nodes not used in mpc constraint
    for Rerepnod1 in range(0,len(nodesAllRe)):
	stop=False			#Stop will become true when mpc constraint is made between nodes
	#nod1=nodesAll[repnod1]		#Select Node 1 for possible mpc constraint
	ReCoor1=nodesAllReCoor[Rerepnod1]		#Coordinates of Node 1
	for Rerepnod2 in ranNodesRe:	#Loop over all available nodes
	    #nod2=nodesAll[repnod2]	#Select Node 2 for possible mpc constraint
	    ReCoor2=nodesAllReCoor[Rerepnod2]	#Coordinates of Node 
	    dx=ReCoor2[0]-ReCoor1[0]; dy=ReCoor2[1]-ReCoor1[1]; dz=ReCoor2[2]-ReCoor1[2];  #X and Y Distance between nodes
	    for comb in range(0,len(LatticeVec)):	#Check if nodes are located exactly the vector lattice apart
		if int(round(1000.0*(LatticeVec[comb][0]-dx)))==0:
		    if int(round(1000.0*(LatticeVec[comb][1]-dy)))==0:
			    if int(round(1000.0*(LatticeVec[comb][2]-dz)))==0:
			#Correct combination found
			#Create sets for use in mpc constraints
				mdb.models[NameModel].rootAssembly.Set(name='ReNode-1-'+str(repConst), nodes=
				    mdb.models[NameModel].rootAssembly.sets[NameSetRe].nodes[Rerepnod1:Rerepnod1+1])
				mdb.models[NameModel].rootAssembly.Set(name='ReNode-2-'+str(repConst), nodes=
				    mdb.models[NameModel].rootAssembly.sets[NameSetRe].nodes[Rerepnod2:Rerepnod2+1])
				for Imrepnod in ranNodesIm:
				    ImCoor=nodesAllImCoor[Imrepnod]
				    if (int(round(1000.0*(ImCoor[0]-ReCoor1[0])))==0) and (int(round(1000.0*(ImCoor[1]-ReCoor1[1])))==0) and (int(round(1000.0*(ImCoor[2]-ReCoor1[2])))==0):
					mdb.models[NameModel].rootAssembly.Set(name='ImNode-1-'+str(repConst), nodes=
					    mdb.models[NameModel].rootAssembly.sets[NameSetIm].nodes[Imrepnod:Imrepnod+1])
				    elif (int(round(1000.0*(ImCoor[0]-ReCoor2[0])))==0) and (int(round(1000.0*(ImCoor[1]-ReCoor2[1])))==0) and (int(round(1000.0*(ImCoor[2]-ReCoor2[2])))==0):
					mdb.models[NameModel].rootAssembly.Set(name='ImNode-2-'+str(repConst), nodes=
					    mdb.models[NameModel].rootAssembly.sets[NameSetIm].nodes[Imrepnod:Imrepnod+1])
			#Create mpc constraints for each dof
				mdb.models['Model-1'].MultipointConstraint(controlPoint=
				    mdb.models['Model-1'].rootAssembly.sets['ReNode-2-'+str(repConst)], csys=None, mpcType=USER_MPC, 
				    name='Fre-Re-'+str(repConst), surface=mdb.models['Model-1'].rootAssembly.sets['ReNode-1-'+str(repConst)], 
				    userMode=NODE_MODE_MPC, userType=2*comb+1)
				mdb.models['Model-1'].MultipointConstraint(controlPoint=
				    mdb.models['Model-1'].rootAssembly.sets['ReNode-2-'+str(repConst)], csys=None, mpcType=USER_MPC, 
				    name='Fre-Im-'+str(repConst), surface=mdb.models['Model-1'].rootAssembly.sets['ImNode-1-'+str(repConst)], 
				    userMode=NODE_MODE_MPC, userType=2*comb+2)
#			mdb.models['Model-1'].MultipointConstraint(controlPoint=
#			    mdb.models['Model-1'].rootAssembly.sets['ReNode-2-'+str(repConst)], csys=None, mpcType=USER_MPC, 
#			    name='Dis-Re-'+str(repConst), surface=mdb.models['Model-1'].rootAssembly.sets['ReNode-1-'+str(repConst)], 
#			    userMode=NODE_MODE_MPC, userType=10+comb)
#			mdb.models['Model-1'].MultipointConstraint(controlPoint=
#			    mdb.models['Model-1'].rootAssembly.sets['ImNode-2-'+str(repConst)], csys=None, mpcType=USER_MPC, 
#			    name='Dis-Im-'+str(repConst), surface=mdb.models['Model-1'].rootAssembly.sets['ImNode-1-'+str(repConst)], 
#			    userMode=NODE_MODE_MPC, userType=10+comb)
				repConst=repConst+1	#Increase integer for naming mpc constraint
				ranNodesRe.remove(Rerepnod2)#Remove used node from available list
				stop=True		#Don't look further, go to following node.
				break
		    if stop:
        		break
    #Return coordinates of free node so that it can be fixed
#    return (nodesAllRe[ranNodesRe[0]].coordinates)