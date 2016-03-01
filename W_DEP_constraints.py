import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining cmodel provide, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "wjets"
convertHistograms = []
def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  
  # Some setup
  _fin = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)


  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # but for now this is just kept simple 
  processName = "WJets" # Give a name of the process being modelled
  metname = "mvamet"    # Observable variable name 
  targetmc     = _fin.Get("signal_wjets")      # define monimal (MC) of which process this config will model
  genVpt = "genVpt"

  # correct with NLO weights 
  fkFactorCentral  = r.TFile.Open("files/scalefactors.root")
  nlo_W = fkFactorCentral.Get("wnlo012_over_wlo/wnlo012_over_wlo")
  diag.generateWeightedDataset("signal_wjets_nlo012jt_QCD",nlo_W,"weight",genVpt,_wspace,"signal_wjets")
  ewkCorr_wjt = fkFactorCentral.Get("w_ewkcorr/w_ewkcorr_orig") 
  diag.generateWeightedDataset("signal_wjets_nlo012jt",ewkCorr_wjt,"weight",genVpt,_wspace,"signal_wjets_nlo012jt_QCD")

  diag.generateWeightedDataset("singlemuon_wjets_nlo_QCD",nlo_W,"weight",genVpt,_wspace,"singlemuon_wjets")
  diag.generateWeightedDataset("singleelectron_wjets_nlo_QCD",nlo_W,"weight",genVpt,_wspace,"singleelectron_wjets")

  diag.generateWeightedDataset("singleelectron_wjets_nlo",ewkCorr_wjt,"weight",genVpt,_wspace,"singleelectron_wjets_nlo_QCD")
  diag.generateWeightedDataset("singlemuon_wjets_nlo",ewkCorr_wjt,"weight",genVpt,_wspace,"singlemuon_wjets_nlo_QCD")

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  WScalesD = targetmc.Clone(); WScalesD.SetName("wmn_weights_den_%s"%cid)
  diag.generateTemplate(WScalesD,metname,_wspace.data("singlemuon_wjets_nlo"))

  WScaleseD = targetmc.Clone(); WScaleseD.SetName("wen_weights_den_%s"%cid)
  diag.generateTemplate(WScaleseD,metname,_wspace.data("singleelectron_wjets_nlo"))

  
  WScales = targetmc.Clone(); WScales.SetName("wmn_weights_%s"%cid)
  diag.generateTemplate(WScales,metname,_wspace.data("signal_wjets_nlo012jt"))
  WScalese = WScales.Clone(); WScalese.SetName("wen_weights_%s"%cid)

  WScales.Divide(WScalesD)
  _fOut.WriteTObject(WScales)  # always write out to the directory 

  WScalese.Divide(WScaleseD)
  _fOut.WriteTObject(WScalese)  # always write out to the directory 
  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(targetmc.GetNbinsX()+1):
    _bins.append(targetmc.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg WScales

  CRs = [
   Channel("singlemuon",_wspace,out_ws,cid+'_'+model,WScales)
  ,Channel("singleelectron",_wspace,out_ws,cid+'_'+model,WScalese)
  ]


  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)
  CRs[0].add_nuisance("pdf_CT10",0.006)
  CRs[0].add_nuisance("CMS_eff_m",0.01)
  CRs[1].add_nuisance("pdf_CT10",0.006)
  CRs[1].add_nuisance("CMS_eff_e",0.01)

  # Statistical uncertainties too!, one per bin 
  for b in range(targetmc.GetNbinsX()):
    err = WScales.GetBinError(b+1)
    if not WScales.GetBinContent(b+1)>0: relerr=1.#continue 
    else: relerr = err/WScales.GetBinContent(b+1)
    #if relerr<0.01: continue
    byb_u = WScales.Clone(); byb_u.SetName("wmn_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"singlemuonCR",b))
    byb_u.SetBinContent(b+1,WScales.GetBinContent(b+1)+err)
    byb_d = WScales.Clone(); byb_d.SetName("wmn_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"singlemuonCR",b))
    byb_d.SetBinContent(b+1,WScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[0].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"singlemuonCR",b),_fOut)
  
  for b in range(targetmc.GetNbinsX()):
    err = WScalese.GetBinError(b+1)
    if not WScalese.GetBinContent(b+1)>0: relerr=1. #continue 
    else: relerr = err/WScalese.GetBinContent(b+1)
    #if relerr<0.01: continue
    byb_u = WScalese.Clone(); byb_u.SetName("wen_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"singleelectronCR",b))
    byb_u.SetBinContent(b+1,WScalese.GetBinContent(b+1)+err)
    byb_d = WScalese.Clone(); byb_d.SetName("wen_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"singleelectronCR",b))
    byb_d.SetBinContent(b+1,WScalese.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[1].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"singleelectronCR",b),_fOut)
  #######################################################################################################


  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,"signal_wjets_nlo012jt",CRs,diag)
  cat.setDependant("zjets","wjetssignal")  # Can use this to state that the "BASE" of this is already dependant on another process
  # EG if the W->lv in signal is dependant on the Z->vv and then the W->mv is depenant on W->lv, then 
  # give the arguments model,channel name from the config which defines the Z->vv => W->lv map! 
  # Return of course
  return cat
