#! /usr/bin/env python
import commands,sys,os,subprocess,ROOT,numpy
from array    import array
from optparse import OptionParser
from MonoX.ModelScan.generate      import loadmonov,loadmonojet,getWidthXS
from MonoX.ModelScan.ntuple        import makeNtuple,ntuplexs
from MonoX.ModelScan.reweightmap   import obtainbase
from MonoX.ModelScan.config        import *
from MonoX.ModelScan.limittools    import *

parser = OptionParser()
parser.add_option('--dm'      ,action='store',type='float',dest='dm'       ,default=1,              help='Dark Matter Mass')
parser.add_option('--med'     ,action='store',type='float',dest='med'      ,default=150,            help='Mediator Mass')
parser.add_option('--width'   ,action='store',type='float',dest='width'    ,default=1,              help='Width (in Min width units)')
parser.add_option('--proc'    ,action='store',type='float',dest='proc'     ,default=805,            help='Process(800=V,801=A,805=S,806=P)')
parser.add_option('--gq'      ,action='store',type='float',dest='gq'       ,default=1,              help='coupling to quarks')
parser.add_option('--gdm'     ,action='store',type='float',dest='gdm'      ,default=1,              help='coupling to dark matter')
parser.add_option('--label'   ,action='store',type='string',dest='label'   ,default='model',        help='eos label')
parser.add_option('--monoV'   ,action='store_true',         dest='monov'   ,default=False,          help='Run mono V generation') # need a few more options for monoV
parser.add_option('--hinv'    ,action='store_true',         dest='hinv'    ,default=False,          help='Higgs Invisible') # need a few more options for monoV
parser.add_option('--monoJ'   ,action='store_true',         dest='monoJ'   ,default=False,          help='Just Monojet') # need a few more options for monoV
parser.add_option('--override',action='store_true',         dest='override',default=False,          help='Use Specified Ntuples') 
parser.add_option('--mj'      ,action='store',              dest='mj'      ,default='ggH125_signal',help='Monojet Base') 
parser.add_option('--zh'      ,action='store',              dest='zh'      ,default='ZH125_signal', help='ZH Base') 
parser.add_option('--wh'      ,action='store',              dest='wh'      ,default='WH125_signal', help='WH Base') 

(options,args) = parser.parse_args()

def fixNorm(filename,treename,cut):
   lFile = ROOT.TFile(filename)
   lTree = lFile.Get(treename)
   scale=float(lTree.GetEntriesFast())/float(lTree.GetEntries(cut))
   return scale

def makeHist(filename,var,baseweight,treename,label,normalize=False):
   x = array( 'd' )
   y=[0.0,100.0,200.0,210.0,220.0,230.0,240.0,250.0 , 260.0 , 270.0 , 280.0 , 290.0 , 300.0 , 310.0 , 320.0 , 330.0,340,360,380,420,710,1200,1500]
   for i0  in range(0,len(y)):
      x.append(y[i0])
   if len(filename) != 0:
      print filename
      lFile = ROOT.TFile.Open(filename)
      lTree = lFile.Get(treename)
      lHist = ROOT.TH1F(label,label,len(x)-1,x)
      print "weight",baseweight
      lTree.Draw(var+'>>'+label,baseweight)
      lHist.SetDirectory(0)
   else:
      lHist = ROOT.TH1F(label,label,len(x)-1,x)
      return lHist
   if normalize:
      lHist.Scale(1./lTree.GetEntriesFast())
   return lHist

def reweight(label,DM,Med,Width,gq,gdm,process,basentuple,basename,basecut,iOutputName,monoV=False,iBR=1):
   xs = [1,1]
   scale = 1
   h1=makeHist('','',basecut,'Events','model')
   h2=makeHist('','',basecut,'Events','base')
   for i0 in range(0,h1.GetNbinsX()+1):
      h1.SetBinContent(i0,1)
      h2.SetBinContent(i0,1)
   #MonoJet
   if basentuple == '':
      return
   if not monoV :
      loadmonojet(DM,Med,Width,process,gq,gdm)
   else :
      loadmonow(DM,Med,Width,process,gq,gdm)
   label='MonoJ_%s_%s_%s_%s.root'    % (str(int(Med)),str(int(DM)),str(int(Width)),str(int(process))))
   if monoV:
      label=label.replace("MonoJ","MonoV")

   #h1=makeHist(('MonoJ_%s_%s_%s_%s_mcfm.root'    % (str(int(Med)),str(int(DM)),str(int(Width)),str(int(process)))),'v_pt',"xs2*"+basecut,'Events','model',True)     
   h1=makeHist(label,'v_pt',"evtweight*1000.*"+basecut,'Events','model',True)
   h2=makeHist(basentuple,'genVpt',"weight",basename,'base',False)           
      #h1.Scale(iBR/1000.)
   print h1.Integral(),h2.Integral()
   h1.Divide(h2)
   lOFile = ROOT.TFile(iOutputName,'RECREATE')
   h1.Write()
   lOFile.Close()
   return xs

def reweightNtuple(iFile,iTreeName,iHistName,iOTreeName,iHiggsPt=False,histlabel='model'):
   lHFile = ROOT.TFile('%s' % (iHistName))
   h1     = lHFile.Get(histlabel)
   #If Tree is empty put in a dummy branch and scale it down to nothing 
   baseweight=1
   
   #Now reweight the ntuple
   lFile  = ROOT.TFile('%s' % iFile)
   lTree  = lFile.Get(iTreeName)
   lOFile = ROOT.TFile('RWTree%s' % (iHistName),'UPDATE')
   lOTree = lTree.CloneTree(0)
   lOTree.SetTitle(iOTreeName)
   lOTree.SetName(iOTreeName)
   w1 = numpy.zeros(1, dtype=float)
   w2 = numpy.zeros(1, dtype=float)
   lOTree.Branch("oldweight",w2,"w2/D")
   lOTree.SetBranchAddress("weight",w1)
   for i0 in range(lTree.GetEntriesFast()):
      lTree.GetEntry(i0)
      genpt = lTree.genVpt
      w2[0] = lTree.weight
      w1[0] = 1
      w1[0] = h1.GetBinContent(h1.FindBin(genpt))*baseweight
      w1[0] = w1[0] * lTree.weight
      lOTree.Fill()
   lOTree.Write()
   lOFile.Close()
   return iTreeName

def treeName(proc,med,dm):
   Name='V'
   if proc == 801:
      Name='A'
   if proc == 805:
      Name='S'
   if proc == 806:
      Name='P'
   Name="%s_%s_%s_signal" % (Name,int(med),int(dm))
   print Name,"!!!"
   return Name
      
if __name__ == "__main__":
   label=options.label
   dm=options.dm
   med=options.med
   width=options.width
   gq=options.gq
   gdm=options.gdm
   proc=options.proc
   BRGG=1
   baseid=0
   cut=monojet
   if options.monoV:
      baseid=1
      cut=monow

   #Determine the sample to use reweighting by scanning
   basetree,trees=obtainbase(baseid,dm,med,proc,options.hinv)
   os.system('cmsStage %s/%s .' % (eosbasedir,basetree))
   #List them
   print "Ntuples : ",basetree,"-- using",trees
   
   #Loop through the categories and build the weight hitograms as listed in rwfile
   xsGG=reweight(label,dm,med,width,gq,gdm,proc,basetree,trees,cut,'ggHRWmonojet.root',False,BRGG)

   #Build ntuples with modified weights => if blank re-assign
   reweightNtuple(basetree,trees,'ggHRWmonojet.root',treeName(proc,med,dm))
   os.system('%s rm  eos/cms/store/cmst3/group/monojet/mc/model4/MonoJ_%s_%s_%s_%s.root' % (eos,int(med),int(dm),int(width),int(proc)))
   os.system('cmsStage RWTreeggHRWmonojet.root /store/cmst3/group/monojet/mc/model4/MonoJ_%s_%s_%s_%s.root' % (int(med),int(dm),int(width),int(proc)))
