#RK0

RK0Type=1
nB=20

B=[pi/L]*nB

for i in range(nB):
    B[i]=(i+1.0)*pi/L/float(nB)
#B=[2.0*pi/L]
nP=[1]*nB

#RA
RA=[L]

#write RK0 and RA to SUBBAS.f
text_file=open('./'+'SUB.for',"w")
for line in open("SUB_PRE.for"):
    if line[0:-1]=="      PUT THE VARIABLES HERE":
        text_file.write('      DIMENSION RK0(%d,1), RA(%d,1)\n' % (len(B),len(RA)))
        text_file.write('      RK0(%d,1)=%10.6f\n' % (0,2.0*B[len(B)-1]))
	for i in range(0,len(B)):
	    text_file.write('      RK0(%d,1)=%10.6f\n' % (i+1,B[i]))
	for i in range(0,len(RA)):
	    text_file.write('      RA(%d,1)=%10.6f\n' % (i+1,RA[i]))
    else:
    	text_file.write(line)
text_file.close()
