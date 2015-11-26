from ROOT import *
import ROOT as r
import re, array, sys, numpy, os

gROOT.ProcessLine(
    "struct eff_t {\
     Double_t         eff;\
    }" )


def categoryWeight(iName,iSetup):
  weight=1
  if iName.find("data") > -1:
    return weight
  if iName.find("photon_control") > -1:
    weight*=iSetup["photonsSF"]
  if iName.find("single_muon_control") > -1:
    weight*=iSetup["muonsSF"]
  if iName.find("di_muon_control") > -1:
    weight*=iSetup["muonsSF"]
  if iName.find("single_electron_control") > -1:
    weight*=iSetup["electronsSF"]
  if iName.find("di_electron_control") > -1:
    weight*=iSetup["electronsSF"]
  return weight

def correctNtuple(iFile,iSample,iFileName,iScale):
    lNtuple  = iFile.Get(iSample)
    if lNtuple == 0:
      print "missing :",iSample
      return
    addTrigger = False
    addEleTrigger = False
    if  lNtuple.GetName().find("Zll_di_muon_control") > -1:
      addTrigger = True
      print "Met Trigger"
    if  lNtuple.GetName().find("Znunu_signal") > -1:
      addTrigger = True
      print "Met Trigger"
    if  lNtuple.GetName().find("single_electron") > -1 and  lNtuple.GetName().find("data") == -1 :
      addEleTrigger = True
      print "Ele Trigger"
      
    lFile  = r.TFile(iFileName+'Eff','UPDATE')
    lTree = lNtuple.CloneTree(0)
    lTree.SetName (lNtuple.GetName() )
    lTree.SetTitle(lNtuple.GetTitle())
    lEff=eff_t()
    lTree.SetBranchAddress( 'weight',    AddressOf(lEff,"eff"))
    for i0 in range(0,lNtuple.GetEntriesFast()):
        lNtuple.GetEntry(i0)
        lEff.eff      = lNtuple.weight*iScale
        #correct the photon data to have additional SF to match MET turn on
        if addEleTrigger:
           lEff.eff      =  lEff.eff*0.955
        if addTrigger:
          pMet = lNtuple.mvamet
          #pMet = lNtuple.metRaw
          #pEff = lTriggerData.Eval(pMet)/lTriggerMC.Eval(pMet)
          pEff = (0.975+(pMet-200)*0.025*0.025)
          if pMet > 240:
            pEff = 1.
          lEff.eff  = lNtuple.weight*iScale*pEff
        lTree.Fill()
    lTree.Write()

sys.path.append("configs")
x = __import__(sys.argv[1]) 
cat=x.categories[0]
print cat
lBaseFile  = r.TFile.Open(cat['in_file_name'])
for sample in lBaseFile.GetListOfKeys():
    print "Sample :",sample.ReadObj().GetName()
    pTree = lBaseFile.Get(sample.ReadObj().GetName())
    sampleName = sample.ReadObj().GetName()
    pScale = categoryWeight(sampleName,cat)
    print "Sample :",sampleName,pScale
    correctNtuple(lBaseFile,sampleName,cat['in_file_name'],pScale)

os.system('cp %s    %s_old' % (cat['in_file_name'],cat['in_file_name']))
os.system('mv %sEff %s    ' % (cat['in_file_name'],cat['in_file_name']))
