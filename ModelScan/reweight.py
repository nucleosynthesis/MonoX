#! /usr/bin/env python
import commands,sys,os,subprocess,ROOT,numpy
from array    import array

from MonoX.ModelScan.generate      import loadmonov,loadmonojet,getWidthXS
from MonoX.ModelScan.ntuple        import makeNtuple,ntuplexs
from MonoX.ModelScan.reweightmap   import obtainbase
from MonoX.ModelScan.config        import *
from MonoX.ModelScan.limittools    import *

from optparse import OptionParser

def parser():
   rparser = OptionParser()
   rparser.add_option('--dm'      ,action='store',type='float',dest='dm'       ,default=1,              help='Dark Matter Mass')
   rparser.add_option('--med'     ,action='store',type='float',dest='med'      ,default=150,            help='Mediator Mass')
   rparser.add_option('--width'   ,action='store',type='float',dest='width'    ,default=1,              help='Width (in Min width units)')
   rparser.add_option('--proc'    ,action='store',type='float',dest='proc'     ,default=805,            help='Process(800=V,801=A,805=S,806=P)')
   rparser.add_option('--gq'      ,action='store',type='float',dest='gq'       ,default=1,              help='coupling to quarks')
   rparser.add_option('--gdm'     ,action='store',type='float',dest='gdm'      ,default=1,              help='coupling to dark matter')
   rparser.add_option('--label'   ,action='store',type='string',dest='label'   ,default='model',        help='eos label')
   rparser.add_option('--monoW'   ,action='store_true',         dest='monoW'   ,default=False,          help='Run mono W generation') # need a few more options for monoV
   rparser.add_option('--monoZ'   ,action='store_true',         dest='monoZ'   ,default=False,          help='Run mono Z generation') # need a few more options for monoV
   rparser.add_option('--hinv'    ,action='store_true',         dest='hinv'    ,default=False,          help='Run Higgs generation') # need a few more options for monoV
   (options,args) = rparser.parse_args()
   return options

def end():
    if __name__ == '__main__':
        rep = ''
        while not rep in [ 'q', 'Q','a',' ' ]:
            rep = raw_input( 'enter "q" to quit: ' )
            if 1 < len(rep):
                rep = rep[0]

def fixNorm(filename,treename,cut):
   lFile = ROOT.TFile(filename)
   lTree = lFile.Get(treename)
   scale=float(lTree.GetEntriesFast())/float(lTree.GetEntries(cut))
   return scale

def makeHist(filename,var,baseweight,treename,label,normalize=''):
   x = array( 'd' )
   y=range(0,1000,25)
   #y=[0.0,100.0,200.0,210.0,220.0,230.0,240.0,250.0 , 260.0 , 270.0 , 280.0 , 290.0 , 300.0 , 310.0 , 320.0 , 330.0,340,360,380,420,710,1200,1500,2000]
   #y=[0.0,100.0,200.0,300,400,500,600,700,800,900,1000,1100,1200]
   for i0  in range(0,len(y)):
      x.append(y[i0])
   if len(filename) != 0:
      print filename
      lFile = ROOT.TFile.Open(filename)
      lTree = lFile.Get(treename)
      lHist = ROOT.TH1F(label,label,len(x)-1,x)
      lTree.Draw(var+'>>'+label,baseweight)
      lHist.SetDirectory(0)
   else:
      lHist = ROOT.TH1F(label,label,len(x)-1,x)
      return lHist
   if normalize != '':
      print "NORM : ",normalize,baseweight
      lHist.Scale(1./lTree.GetEntries(normalize))
   return lHist

def reweight(label,DM,Med,Width,gq,gdm,process,basentuple,basename,basecut,iOutputName,iVId=0,iBR=1):
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
      loadmonov(DM,Med,Width,process,gq,gdm)
   label='MonoJ_%s_%s_%s_%s.root'    % (str(int(Med)),str(int(DM)),str(int(Width)),str(int(process)))
   weight1="evtweight*1000*"+basecut+"*"
   weight2="weight*"        +basecut
   var1="v_pt"
   var2="genVpt"
   Norm1='(v_pt > 0)'
   Norm2=''
   if iVId > 0:
      label=label.replace("MonoJ","MonoV")
      weight1="xs2*"+basecut.replace("23","23")+"*"
      weight2="xs*"+basecut.replace("23","24")+"*"
      Norm1='(abs(v_id) == '+str(iVId)+')'
      #Norm2='(abs(v_id) == '+str(iVId)+')'
      Norm2='(abs(v_id) == 24)'
      var1="v_pt"
      var2="v_pt"
      
   h1=makeHist(label     ,var1,weight1+Norm1,'Events','model',Norm1)
   h2=makeHist(basentuple,var2,weight2+Norm2,basename,'base' ,Norm2)           
   print h1.Integral(),h2.Integral()
   can= ROOT.TCanvas("C","C",800,600)
   h1.Draw()
   h2.SetLineColor(ROOT.kRed)
   h2.Draw("sames")
   #end()
   h1.Divide(h2)
   lOFile = ROOT.TFile(iOutputName,'RECREATE')
   h1.Write()
   lOFile.Close()
   return xs

def reweightNtuple(iFile,iTreeName,iHistName,iOTreeName,iMonoV,iHiggsPt=False,histlabel='model'):
   print iFile,iTreeName,iHistName,iOTreeName,iMonoV
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
      #if iMonoV:
      #   genpt = lTree.genvpt
      #else:
      genpt = lTree.genVpt
      w1[0] = 1
      w2[0] = lTree.weight
      w1[0] = h1.GetBinContent(h1.FindBin(genpt))*baseweight
      w1[0] = w1[0] * w2[0]
      lOTree.Fill()
   lOTree.Write()
   lOFile.Close()
   return iTreeName

def treeName(proc,med,dm,iId):
   if iId > 0:
      return 'Events'
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
   options = parser()
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
   monoV = False
   if options.monoW:
      baseid=24
      cut=boosted+"*(abs(v_id) == 24)"
      monoV =  True

   if options.monoZ:
      baseid=23
      cut=boosted+"*(abs(v_id) == 23)"
      monoV =  True

   #Determine the sample to use reweighting by scanning
   basetree,trees=obtainbase(baseid,dm,med,proc,options.hinv)
   basetree=basetree.replace('MonoZ','MonoW')
   trees   =trees.replace('MonoZ','MonoW')
   basetreegen=basetree
   os.system('cmsStage %s/%s .' % (eosbasedir,basetree))
   treesgen=trees
   if options.monoW or options.monoZ:
      basetreegen=basetree.replace(".root_0","_Gen.root")
      os.system('cmsStage %s/%s .' % (eosbasedir,basetreegen))
      treesgen='Events'
   #List them
   print "Ntuples : ",basetree,"-- using",trees,label,trees
   
   #Loop through the categories and build the weight hitograms as listed in rwfile
   xsGG=reweight(label,dm,med,width,gq,gdm,proc,basetreegen,treesgen,cut,'ggHRWmonojet.root',baseid,BRGG)

   #Build ntuples with modified weights => if blank re-assign
   reweightNtuple(basetree,trees,'ggHRWmonojet.root',treeName(proc,med,dm,baseid),monoV)
   name='MonoJ_%s_%s_%s_%s.root' % (int(med),int(dm),int(width),int(proc))
   if options.monoZ:
      name=name.replace('MonoJ','MonoZ')
   if options.monoW:
      name=name.replace('MonoJ','MonoW')
   os.system('%s rm  eos/cms/store/cmst3/group/monojet/mc/model4/%s' % (eos,name))
   os.system('cmsStage RWTreeggHRWmonojet.root /store/cmst3/group/monojet/mc/model4/%s' % name)
   
