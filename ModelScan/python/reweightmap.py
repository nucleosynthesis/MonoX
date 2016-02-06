#! /usr/bin/env python
import commands,sys,os,subprocess,ROOT,numpy
from optparse import OptionParser
from array import array

#Available samples
samples = { 
    #'ggH125_signal'           :[0,805,125,    1],  # Ntuple  : [Final State,Proc,med,DM]
    'Axial_Mphi-1000_Mchi-10_0.root_0'       : [0,801,1000, 10],
    'Axial_Mphi-1000_Mchi-150_0.root_0'      : [0,801,1000,150],
    'Axial_Mphi-1000_Mchi-1_0.root_0'        : [0,801,1000,  1],
    'Axial_Mphi-100_Mchi-100_0.root_0'       : [0,801, 100,100],
    'Axial_Mphi-100_Mchi-10_0.root_0'        : [0,801, 100, 10],
    'Axial_Mphi-100_Mchi-1_0.root_0'         : [0,801, 100,  1],
    'Axial_Mphi-100_Mchi-50_0.root_0'        : [0,801, 100, 50],
    'Axial_Mphi-10_Mchi-10_0.root_0'         : [0,801,  10, 10],
    'Axial_Mphi-10_Mchi-1_0.root_0'          : [0,801,  10,  1],
    'Axial_Mphi-2000_Mchi-100_0.root_0'      : [0,801,2000,100],
    'Axial_Mphi-2000_Mchi-150_0.root_0'      : [0,801,2000,150],
    'Axial_Mphi-200_Mchi-10_0.root_0'        : [0,801, 200, 10],
    'Axial_Mphi-20_Mchi-10_0.root_0'         : [0,801,  20, 10],
    'Axial_Mphi-20_Mchi-1_0.root_0'          : [0,801,  20,  1],
    'Axial_Mphi-300_Mchi-100_0.root_0'       : [0,801, 300,100],
    'Axial_Mphi-300_Mchi-10_0.root_0'        : [0,801, 300, 10],
    'Axial_Mphi-300_Mchi-150_0.root_0'       : [0,801, 300,150],
    'Axial_Mphi-300_Mchi-1_0.root_0'         : [0,801, 300,  1],
    'Axial_Mphi-300_Mchi-50_0.root_0'        : [0,801, 300, 50],
    'Axial_Mphi-5000_Mchi-100_0.root_0'      : [0,801,5000,100],
    'Axial_Mphi-5000_Mchi-10_0.root_0'       : [0,801,5000, 10],
    'Axial_Mphi-5000_Mchi-150_0.root_0'      : [0,801,5000,150],
    'Axial_Mphi-5000_Mchi-1_0.root_0'        : [0,801,5000,  1],
    'Axial_Mphi-5000_Mchi-50_0.root_0'       : [0,801,5000, 50],
    'Axial_Mphi-500_Mchi-100_0.root_0'       : [0,801, 500,100],
    'Axial_Mphi-500_Mchi-10_0.root_0'        : [0,801, 500, 10],
    'Axial_Mphi-500_Mchi-150_0.root_0'       : [0,801, 500,150],
    'Axial_Mphi-500_Mchi-1_0.root_0'         : [0,801, 500,  1],
    'Axial_Mphi-500_Mchi-500_0.root_0'       : [0,801, 500,500],
    'Axial_Mphi-500_Mchi-50_0.root_0'        : [0,801, 500, 50],
    'Axial_Mphi-50_Mchi-10_0.root_0'         : [0,801,  50, 10],
    'Axial_Mphi-50_Mchi-1_0.root_0'          : [0,801,  50,  1],
    'Axial_Mphi-50_Mchi-50_0.root_0'         : [0,801,  50, 50],
    'Pseudoscalar_Mphi-1000_Mchi-100_0.root_0' : [0,806,1000,100],
    'Pseudoscalar_Mphi-1000_Mchi-150_0.root_0' : [0,806,1000,150],
    'Pseudoscalar_Mphi-1000_Mchi-1_0.root_0'   : [0,806,1000,  1],
    #'Pseudoscalar_Mphi-1000_Mchi-500_0.root_0' : [0,806,1000,500],
    'Pseudoscalar_Mphi-1000_Mchi-50_0.root_0'  : [0,806,1000, 50],
    'Pseudoscalar_Mphi-100_Mchi-100_0.root_0'  : [0,806, 100,100],
    'Pseudoscalar_Mphi-100_Mchi-10_0.root_0'   : [0,806, 100, 10],
    #'Pseudoscalar_Mphi-100_Mchi-50_0.root_0'   : [0,806,  10, 50],
    'Pseudoscalar_Mphi-10_Mchi-10_0.root_0'    : [0,806,  10, 10],
    'Pseudoscalar_Mphi-10_Mchi-1_0.root_0'     : [0,806,  10,  1],
    #'Pseudoscalar_Mphi-200_Mchi-100_0.root_0'  : [0,806, 200,100],
    'Pseudoscalar_Mphi-200_Mchi-10_0.root_0'   : [0,806, 200, 10],
    'Pseudoscalar_Mphi-200_Mchi-150_0.root_0'  : [0,806, 200,150],
    'Pseudoscalar_Mphi-200_Mchi-1_0.root_0'    : [0,806, 200,  1],
    'Pseudoscalar_Mphi-200_Mchi-50_0.root_0'   : [0,806, 200, 50],
    #'Pseudoscalar_Mphi-20_Mchi-10_0.root_0'    : [0,806,  20, 10],
    'Pseudoscalar_Mphi-20_Mchi-1_0.root_0'     : [0,806,  20,  1],
    'Pseudoscalar_Mphi-300_Mchi-100_0.root_0'  : [0,806, 300,100],
    'Pseudoscalar_Mphi-300_Mchi-10_0.root_0'   : [0,806, 300, 10],
    #'Pseudoscalar_Mphi-300_Mchi-150_0.root_0'  : [0,806, 300,150],
    'Pseudoscalar_Mphi-300_Mchi-50_0.root_0'   : [0,806, 300, 50],
    'Pseudoscalar_Mphi-5000_Mchi-10_0.root_0'  : [0,806,5000, 10],
    'Pseudoscalar_Mphi-500_Mchi-100_0.root_0'  : [0,806, 500,100],
    'Pseudoscalar_Mphi-500_Mchi-10_0.root_0'   : [0,806, 500, 10],
    'Pseudoscalar_Mphi-500_Mchi-150_0.root_0'  : [0,806, 500,150],
    'Pseudoscalar_Mphi-500_Mchi-1_0.root_0'    : [0,806, 500,  1],
    'Pseudoscalar_Mphi-500_Mchi-50_0.root_0'   : [0,806, 500, 50],
    'Pseudoscalar_Mphi-50_Mchi-10_0.root_0'    : [0,806,  50, 10],
    'Pseudoscalar_Mphi-50_Mchi-1_0.root_0'     : [0,806,  50,  1],
    'Pseudoscalar_Mphi-50_Mchi-50_0.root_0'    : [0,806,  50, 50],
    'Scalar_Mphi-1000_Mchi-10_0.root_0'        : [0,805,1000, 10],
    'Scalar_Mphi-1000_Mchi-150_0.root_0'       : [0,805,1000,150],
    'Scalar_Mphi-1000_Mchi-1_0.root_0'         : [0,805,1000,  1],
    'Scalar_Mphi-1000_Mchi-50_0.root_0'        : [0,805,1000, 50],
    'Scalar_Mphi-100_Mchi-100_0.root_0'        : [0,805, 100,100],
    'Scalar_Mphi-100_Mchi-10_0.root_0'         : [0,805, 100, 10],
    'Scalar_Mphi-100_Mchi-1_0.root_0'          : [0,805, 100,  1],
    #'Scalar_Mphi-100_Mchi-50_0.root_0'         : [0,805, 100, 50],
    'Scalar_Mphi-10_Mchi-10_0.root_0'          : [0,805,  10, 10],
    'Scalar_Mphi-10_Mchi-1_0.root_0'           : [0,805,  10,  1],
    #'Scalar_Mphi-200_Mchi-100_0.root_0'        : [0,805, 200,100],
    'Scalar_Mphi-200_Mchi-10_0.root_0'         : [0,805, 200, 10],
    'Scalar_Mphi-200_Mchi-1_0.root_0'          : [0,805, 200,  1],
    'Scalar_Mphi-200_Mchi-50_0.root_0'         : [0,805, 200, 50],
    'Scalar_Mphi-20_Mchi-10_0.root_0'          : [0,805,  20, 10],
    'Scalar_Mphi-20_Mchi-1_0.root_0'           : [0,805,  20,  1],
    'Scalar_Mphi-300_Mchi-100_0.root_0'        : [0,805, 300,100],
    'Scalar_Mphi-300_Mchi-10_0.root_0'         : [0,805, 300, 10],
    #'Scalar_Mphi-300_Mchi-150_0.root_0'        : [0,805, 300,150],
    'Scalar_Mphi-300_Mchi-1_0.root_0'          : [0,805, 300,  1],
    'Scalar_Mphi-300_Mchi-50_0.root_0'         : [0,805, 300, 50],
    'Scalar_Mphi-5000_Mchi-100_0.root_0'       : [0,805,5000,100],
    'Scalar_Mphi-5000_Mchi-150_0.root_0'       : [0,805,5000,150],
    'Scalar_Mphi-5000_Mchi-1_0.root_0'         : [0,805,5000,  1],
    'Scalar_Mphi-5000_Mchi-50_0.root_0'        : [0,805,5000, 50],
    'Scalar_Mphi-500_Mchi-10_0.root_0'         : [0,805, 500, 10],
    'Scalar_Mphi-500_Mchi-150_0.root_0'        : [0,805, 500,150],
    'Scalar_Mphi-500_Mchi-1_0.root_0'          : [0,805, 500,  1],
    'Scalar_Mphi-500_Mchi-50_0.root_0'         : [0,805, 500, 50],
    'Scalar_Mphi-50_Mchi-10_0.root_0'          : [0,805,  50, 10],
    'Scalar_Mphi-50_Mchi-1_0.root_0'           : [0,805,  50,  1],
    'Vector_Mphi-1000_Mchi-100_0.root_0'       : [0,800,1000,100],
    'Vector_Mphi-1000_Mchi-150_0.root_0'       : [0,800,1000,150],
    'Vector_Mphi-1000_Mchi-50_0.root_0'        : [0,800,1000, 50],
    'Vector_Mphi-100_Mchi-100_0.root_0'        : [0,800, 100,100],
    'Vector_Mphi-100_Mchi-10_0.root_0'         : [0,800, 100, 10],
    'Vector_Mphi-100_Mchi-50_0.root_0'         : [0,800, 100, 50],
    'Vector_Mphi-10_Mchi-10_0.root_0'          : [0,800,  10, 10],
    'Vector_Mphi-10_Mchi-1_0.root_0'           : [0,800,  10,  1],
    'Vector_Mphi-2000_Mchi-100_0.root_0'       : [0,800,2000,100],
    'Vector_Mphi-200_Mchi-10_0.root_0'         : [0,800, 200, 10],
    'Vector_Mphi-200_Mchi-150_0.root_0'        : [0,800, 200,150],
    'Vector_Mphi-200_Mchi-1_0.root_0'          : [0,800, 200,  1],
    'Vector_Mphi-200_Mchi-50_0.root_0'         : [0,800, 200, 50],
    'Vector_Mphi-20_Mchi-10_0.root_0'          : [0,800,  20, 10],
    'Vector_Mphi-20_Mchi-1_0.root_0'           : [0,800,  20,  1],
    'Vector_Mphi-300_Mchi-100_0.root_0'        : [0,800, 300,100],
    'Vector_Mphi-300_Mchi-10_0.root_0'         : [0,800, 300, 10],
    'Vector_Mphi-300_Mchi-150_0.root_0'        : [0,800, 300,150],
    'Vector_Mphi-300_Mchi-50_0.root_0'         : [0,800, 300, 50],
    'Vector_Mphi-500_Mchi-10_0.root_0'         : [0,800, 500, 10],
    'Vector_Mphi-500_Mchi-150_0.root_0'        : [0,800, 500,150],
    'Vector_Mphi-500_Mchi-1_0.root_0'          : [0,800, 500,  1],
    'Vector_Mphi-500_Mchi-500_0.root_0'        : [0,800, 500,500],
    'Vector_Mphi-500_Mchi-50_0.root_0'         : [0,800, 500, 50],
    'Vector_Mphi-50_Mchi-10_0.root_0'          : [0,800,  50, 10],
    'Vector_Mphi-50_Mchi-1_0.root_0'           : [0,800,  50, 10],
    'Vector_Mphi-50_Mchi-50_0.root_0'          : [0,800,  50, 50],
    'AxialTotal_MonoZ_10000.root_0'            : [23,800,10000, 1], 
    'AxialTotal_MonoW_10000.root_0'            : [24,800,10000, 1]
}
def filtered(iSamples,iEntry,iVal):
    oSamples = {}
    tSamples = iSamples.keys()
    for sample in tSamples:
        entry = iSamples[sample]
        if entry[iEntry] == iVal:
            oSamples[sample]=entry    

    return oSamples

def offshell(iSamples,iOffShell):
    oSamples = {}
    tSamples = iSamples.keys()
    for sample in tSamples:
        entry = iSamples[sample]
        if entry[3] > entry[2]*0.5 and iOffShell:
            oSamples[sample]=entry    
        if entry[3] < entry[2]*0.501 and not iOffShell:
            oSamples[sample]=entry    
    return oSamples

#Nearest using Price is right rules (still debating this)
def nearest(iSamples,iEntry,iVal):
    #!!!Note assumes things are sorted by mediator mass
    tSamples = iSamples.keys() 
    baseVal=-1
    #Find nearest Val wit PIR Rules
    for sample in tSamples:
        entry = iSamples[sample]
        if abs(entry[iEntry]-iVal) < abs(baseVal-iVal) or (baseVal-iVal < 0 and entry[iEntry]-iVal > 0) : #2nd bit is POR rules
            baseVal=entry[iEntry]
    return filtered(iSamples,iEntry,baseVal)

def convert(iName):
    #HACK to get name
    if iName.find("MonoW") > -1:
        return 'MonoV_A_10000_1_signal'
    if iName.find("MonoZ") > -1:
        return 'MonoV_A_10000_1_signal'
    lName=iName.replace("Vector"      ,"V")
    lName=lName.replace("Axial"       ,"A")
    lName=lName.replace("Scalar"      ,"S")
    lName=lName.replace("Pseudoscalar","P")
    lName=lName.replace("Mchi-","")
    lName=lName.replace("Mphi-","")
    lName=lName.replace("_0.root_0","")
    return lName+"_signal"

#Find the tree that is kinematic closest before reweighting
def obtainbase(iId,dm,med,proc,hinv):
    #Step 1 Map Get all process with the right decay
    dDecay = filtered(samples,0,iId)
    #Step 2 filter by process
    dProcess = filtered(dDecay,1,proc)
    #Merge Pseudoscalar with Scalar
    if len(dProcess) == 0 and proc == 806:
        dProcess = filtered(dDecay,1,805)
    #Merge Vector/Axial and all flavors with Vector
    if len(dProcess) == 0 and (proc == 801 or proc == 810 or proc == 811 or proc == 820 or proc == 821):
        dProcess = filtered(dDecay,1,800)
    #Just take whatever the hell we have for Mono-V
    if len(dProcess) == 0 and iId > 1:
        print "Mono-V Process missing"
        dProcess = filtered(dDecay,1,800)
    if len(dProcess) == 0:
        print "Process not found!!!!",proc,iId
        output=['H125_Gen.root','ggH125_signal']
        return output
    
    isExact = True
    #Step 3 filter by offshell or on shell
    dMass = offshell(dProcess,(dm > 0.5*med))
    if len(dMass) == 0: 
        isExact = False
    if dm < med and len(dMass) == 0: #Default to onshell if ti fails
        dMass = offshell(dProcess,not (dm > 0.5*med))
        
    #Step 4 find the nearest Mediator
    dMed = filtered(dMass,2,med)
    if len(dMed) == 0: 
        isExact = False
    dMed = nearest(dMass,2,med)
    
    #Step 5 find the nearest DM candidate
    final = nearest(dMed,3,dm)
    if len(final) > 1 : 
        print "Ambiguous options",final

    print "final",final
    output=[final.keys()[0],convert(final.keys()[0])]
    #if isExact and hinv:
    #    output[0]=''
    return output

#parser = OptionParser()
#parser.add_option('--dm'   ,action='store',type='int',dest='dm'    ,default=10,  help='Dark Matter Mass')
#parser.add_option('--med'  ,action='store',type='int',dest='med'   ,default=2000,help='Mediator Mass')
#parser.add_option('--proc' ,action='store',type='int',dest='proc'  ,default=806, help='Process(800=V,801=A,805=S,806=P)')
#(options,args) = parser.parse_args()

#if __name__ == "__main__":
#   dm  =options.dm
#   med =options.med
#   proc=options.proc

#   for i0 in range(0,4):   
#       basetree,trees=obtainbase(i0,dm,med,proc)
#       print "Base:",basetree,"Run Tree",trees
