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
   rparser.add_option('--gq'      ,action='store',type='float',dest='gq'       ,default=0.25,           help='coupling to quarks')
   rparser.add_option('--gdm'     ,action='store',type='float',dest='gdm'      ,default=1,              help='coupling to dark matter')
   rparser.add_option('--label'   ,action='store',type='string',dest='label'   ,default='model',        help='eos label')
   rparser.add_option('--monoW'   ,action='store_true',         dest='monoW'   ,default=False,          help='Run mono W generation') # need a few more options for monoV
   rparser.add_option('--monoZ'   ,action='store_true',         dest='monoZ'   ,default=False,          help='Run mono Z generation') # need a few more options for monoV
   rparser.add_option('--hinv'    ,action='store_true',         dest='hinv'    ,default=False,          help='Run Higgs generation') # need a few more options for monoV
   (options,args) = rparser.parse_args()
   return options


def getXS(iMed,iId,basedir='/afs/cern.ch/user/p/pharris/pharris/public/bacon/prod/CMSSW_7_3_3/src/genproductions/bin/JHUGen/'):
    lFile  = ROOT.TFile(basedir+'/patches/WZXS.root')
    label="ZH"
    if int(iId) == 24:
       label="WH"
    lG     = lFile.Get(label)
    lScale = lFile.Get("scaleUp")
    lBR    = lFile.Get("BRbb")
    if iMed > 500:
       lBR    = lFile.Get("BRtt")
    print lBR,iMed,label,iId
    scale=int(iMed)+91+15 # 15 is an approximation of the extra energy based on matching xsections at 125
    if int(iId) == 24:
       scale=int(iMed)+80+15
    #Correct for the BR to fermions assuming Scalar decays to bosons                                                                                                                                       
    lBaseMass=4.2
    if iMed > 500:
       lBaseMass=172.5
    BRCorr = min(lBR.Eval(iMed)*246.*246./lBaseMass/lBaseMass,1.)
    return lG.Eval(iMed)*lScale.Eval(scale)*BRCorr

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

def reweight(label,DM,Med,Width,gq,gdm,process,basentuple,basename,basecut,basecutReco,iOutputName,iVId=0,iBR=1):
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
   label='MonoJ_%s_%s_%s_%s.root'    % (str(int(Med)),str(int(DM)),str(gq),str(int(process)))
   print label,"!!!!"
   weight1="evtweight*1000*"+basecut+"*"
   weight2="weight*"        +basecutReco
   var1="v_pt"
   var2="genMediatorPt"
   Norm1='(v_pt > 0)'
   Norm2=''
   if iVId > 0:
      var1="v_pt"
      var2="genVBosonPt"
      label=label.replace("MonoJ","MonoV")
      weight1="xs"
      if process < 802:
         weight1=weight1+"2"
      if process > 802:
         weight1=weight1+"*"+str(getXS(Med,iVId))
      weight1=weight1+"*1000*"+basecut.replace("23","23")+"*"
      Norm1='(abs(v_id) == '+str(iVId)+')'
      
   h1=makeHist(label     ,var1,weight1+Norm1,'Events','model',Norm1)
   h2=makeHist(basentuple,var2,weight2+Norm2,basename,'base' ,Norm2)           
   if int(iVId) == 23 and process < 802:
      h1.Scale(1./fixNorm(label,"Events",Norm1))
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

def reweightNtuple(iFile,iTreeName,iHistName,iOTreeName,iClass,iMonoV,iHiggsPt=False,histlabel='model'):
   print iFile,iTreeName,iHistName,iOTreeName,iMonoV
   lHFile = ROOT.TFile('%s' % (iHistName))
   h1     = lHFile.Get(histlabel)
   #If Tree is empty put in a dummy branch and scale it down to nothing 
   baseweight=1
   
   #Now reweight the ntuple
   lFile  = ROOT.TFile('%s' % iFile)
   lTree  = lFile.Get(iTreeName)
   lOFile = ROOT.TFile('tmpRWTree%s' % (iHistName),'RECREATE')
   lFTree = lTree.CopyTree(iClass)
   lOTree = lFTree.CloneTree(0)
   lOTree.SetTitle(iOTreeName)
   lOTree.SetName(iOTreeName)
   w1 = numpy.zeros(1, dtype=float)
   w2 = numpy.zeros(1, dtype=float)
   lOTree.Branch("oldweight",w2,"w2/D")
   lOTree.SetBranchAddress("weight",w1)
   for i0 in range(lFTree.GetEntriesFast()):
      lFTree.GetEntry(i0)
      #if iMonoV:
      #   genpt = lTree.genvpt
      #else:
      genpt = lFTree.genMediatorPt
      w1[0] = 1
      w2[0] = lFTree.weight
      w1[0] = h1.GetBinContent(h1.FindBin(genpt))*baseweight
      w1[0] = w1[0] * w2[0]
      lOTree.Fill()
   lOTree.Write()
   lOFile.Close()
   return iTreeName

def treeName(proc,med,dm,gq,iId):
   Name='V'
   if proc == 801:
      Name='A'
   if proc == 805:
      Name='S'
   if proc == 806:
      Name='P'
   if iId == 24:
      Name="MonoW_"+Name
   if iId == 23:
      Name="MonoZ_"+Name
   Name="%s_%s_%s_%s_signal" % (Name,int(med),int(dm),str(gq))
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
   cuts=[monojet,boosted]
   cutsReco=[monojetReco,boostedReco]
   monoV = False
   if gq == 1:
      gq = int(gq)

   if options.monoW:
      baseid=24
      cut=boosted+"*(abs(v_id) == 24)"
      monoV =  True

   if options.monoZ:
      baseid=23
      cut=boosted+"*(abs(v_id) == 23)"
      monoV =  True
   
   if not monoV:
      cuts[1]     = monojet
      cutsReco[1] = monojetReco

   #Determine the sample to use reweighting by scanning
   basetree,trees=obtainbase(baseid,dm,med,proc,options.hinv)
   basetreegen=basetree
   os.system('cmsStage %s/%s .' % (eosbasedir,basetree))
   treesgen=trees
   #List them
   print "Ntuples : ",basetree,"-- using",trees,label,trees,gq

   os.system('rm *ggHRWmonojet.root')
   for i0 in range(0,len(cuts)):
      #Loop through the categories and build the weight hitograms as listed in rwfile
      xsGG=reweight(label,dm,med,width,gq,gdm,proc,basetreegen,treesgen,cuts[i0],cutsReco[i0],'ggHRWmonojet.root',baseid,BRGG)
      idcut='(id=='+str(i0+1)+')'
      #Build ntuples with modified weights => if blank re-assign
      reweightNtuple(basetree,trees,'ggHRWmonojet.root',treeName(proc,med,dm,gq,baseid),idcut,monoV)
      if i0 > 0:
         os.system('hadd tmp2TreeggHRWmonojet.root RWTreeggHRWmonojet.root tmpRWTreeggHRWmonojet.root')
         os.system('mv tmp2TreeggHRWmonojet.root tmpRWTreeggHRWmonojet.root')
      os.system('mv tmpRWTreeggHRWmonojet.root RWTreeggHRWmonojet.root')

   name='MonoJ_%s_%s_%s_%s.root' % (int(med),int(dm),str(gq),int(proc))
   if options.monoZ:
      name=name.replace('MonoJ','MonoZ')
   if options.monoW:
      name=name.replace('MonoJ','MonoW')
   os.system('%s rm  eos/cms/store/cmst3/group/monojet/mc/model4/%s' % (eos,name))
   os.system('cmsStage RWTreeggHRWmonojet.root /store/cmst3/group/monojet/mc/model4/%s' % name)
   
