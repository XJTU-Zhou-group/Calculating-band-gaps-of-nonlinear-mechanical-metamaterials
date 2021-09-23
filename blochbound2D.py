

def BlochBound2D(mdb,NameModel,NameSetRe,NameSetIm,LatticeVec):
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
    ranNodesRe=range(0,len(nodesAllRe))
    ranNodesIm=range(0,len(nodesAllIm))	
    for Rerepnod1 in range(0,len(nodesAllRe)):
	stop=False	
	ReCoor1=nodesAllReCoor[Rerepnod1]	
	for Rerepnod2 in ranNodesRe:	
	    #nod2=nodesAll[repnod2]	
	    ReCoor2=nodesAllReCoor[Rerepnod2]	
	    dx=ReCoor2[0]-ReCoor1[0]; dy=ReCoor2[1]-ReCoor1[1]	
	    for comb in range(0,len(LatticeVec)):	
		if int(round(1000.0*(LatticeVec[comb][0]-dx)))==0:
		    if int(round(1000.0*(LatticeVec[comb][1]-dy)))==0:
			mdb.models[NameModel].rootAssembly.Set(name='ReNode-1-'+str(repConst), nodes=
			    mdb.models[NameModel].rootAssembly.sets[NameSetRe].nodes[Rerepnod1:Rerepnod1+1])
			mdb.models[NameModel].rootAssembly.Set(name='ReNode-2-'+str(repConst), nodes=
			    mdb.models[NameModel].rootAssembly.sets[NameSetRe].nodes[Rerepnod2:Rerepnod2+1])
			for Imrepnod in ranNodesIm:
			    ImCoor=nodesAllImCoor[Imrepnod]
			    if (int(round(1000.0*(ImCoor[0]-ReCoor1[0])))==0) and (int(round(1000.0*(ImCoor[1]-ReCoor1[1])))==0):
				mdb.models[NameModel].rootAssembly.Set(name='ImNode-1-'+str(repConst), nodes=
				    mdb.models[NameModel].rootAssembly.sets[NameSetIm].nodes[Imrepnod:Imrepnod+1])
			    elif (int(round(1000.0*(ImCoor[0]-ReCoor2[0])))==0) and (int(round(1000.0*(ImCoor[1]-ReCoor2[1])))==0):
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
			mdb.models['Model-1'].MultipointConstraint(controlPoint=
			    mdb.models['Model-1'].rootAssembly.sets['ReNode-2-'+str(repConst)], csys=None, mpcType=USER_MPC, 
			    name='Dis-Re-'+str(repConst), surface=mdb.models['Model-1'].rootAssembly.sets['ReNode-1-'+str(repConst)], 
			    userMode=NODE_MODE_MPC, userType=10+comb)
			mdb.models['Model-1'].MultipointConstraint(controlPoint=
			    mdb.models['Model-1'].rootAssembly.sets['ImNode-2-'+str(repConst)], csys=None, mpcType=USER_MPC, 
			    name='Dis-Im-'+str(repConst), surface=mdb.models['Model-1'].rootAssembly.sets['ImNode-1-'+str(repConst)], 
			    userMode=NODE_MODE_MPC, userType=10+comb)
			repConst=repConst+1	
			ranNodesRe.remove(Rerepnod1)
			stop=True		
			break
	    if stop:
        	break