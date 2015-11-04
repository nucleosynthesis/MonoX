import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining *cmodel*, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
# Second is a list of histos which will addtionally be converted to RooDataHists, leave blank if not needed
model = "zjets"
convertHistograms = []
import sys
# My Function. Just to put all of the complicated part into one function
def my_function(_wspace,_fin,_fOut,nam,diag):

  metname = "mvamet"    # Observable variable name 
  gvptname = "genVpt"    # Weights are in generator pT
  wvarname= "weight"
  target     = _fin.Get("signal_zjets")      # define monimal (MC) of which process this config will model
  controlmc     = _fin.Get("dimuon_zll")  # defines in / out acceptance
  controlmce    = _fin.Get("dielectron_zll")  # defines in / out acceptance

  controlmc_photon   = _fin.Get("photon_gjet")  # defines in / out acceptance
  controlmc_wlv      = _fin.Get("signal_wjets")  # defines in / out acceptance

  # first, easy bit, make the scales for Z->ee 

  ZeeScales = target.Clone(); ZeeScales.SetName("zee_weights_%s"%nam)
  ZeeScales.Divide(controlmce)
  _fOut.WriteTObject(ZeeScales)  # always write out to the directory 


  fkFactorCentral  = r.TFile.Open("files/scalefactors.root")
  fkFactor = r.TFile.Open("files/Photon_Z_NLO_kfactors_w80pcorr.root")

  # Central value Photon LO -> NLO, make a dataet 
  nlo_pho = fkFactorCentral.Get("anlo1_over_alo/anlo1_over_alo")
  diag.generateWeightedDataset("photon_gjet_nlo_QCD",nlo_pho,wvarname,gvptname,_wspace,"photon_gjet")

  # Z+jets MC NLO, make a dataset. 
  nlo_zjt_NLO1j = fkFactorCentral.Get("znlo012_over_znlo1/znlo012_over_znlo1")  # wrong way around so flip it 
  for b in range(nlo_zjt_NLO1j.GetNbinsX()): nlo_zjt_NLO1j.SetBinContent(b+1,1./nlo_zjt_NLO1j.GetBinContent(b+1))
  diag.generateWeightedDataset("signal_zjets_nlo1jt_QCD",nlo_zjt_NLO1j,wvarname,gvptname,_wspace,"signal_zjets")

  # Correct for the Eletroweak corrections ... (uncertainties from OLD files)
  ewkCorr_pho = fkFactorCentral.Get("a_ewkcorr/a_ewkcorr") 
  ewkCorr_zjt = fkFactorCentral.Get("z_ewkcorr/z_ewkcorr") 
  diag.generateWeightedDataset("photon_gjet_nlo",nlo_pho,wvarname,gvptname,_wspace,"photon_gjet_nlo_QCD")
  diag.generateWeightedDataset("signal_zjets_nlo1jt",nlo_zjt_NLO1j,wvarname,gvptname,_wspace,"signal_zjets_nlo1jt_QCD")

  # photon spectrum then ...
  nlo_pho_met = target.Clone(); nlo_pho_met.SetName("photon_weights_denom_%s"%nam); 
  for b in range(nlo_pho_met.GetNbinsX()): nlo_pho_met.SetBinContent(b+1,0)
  diag.generateTemplate(nlo_pho_met,metname,_wspace.data("photon_gjet_nlo"))

  # zjet (NLO 1-jet) spectrum is numerator
  nlo_zjt_met = target.Clone(); nlo_zjt_met.SetName("photon_weights_%s"%nam); 
  for b in range(nlo_zjt_met.GetNbinsX()): nlo_zjt_met.SetBinContent(b+1,0)
  diag.generateTemplate(nlo_zjt_met,metname,_wspace.data("signal_zjets_nlo1jt"))

  # Weights !
  nlo_zjt_met.Divide(nlo_pho_met)

  # for each variation, we make Z/pho up/nominal NLO  (this will be our ratio)
  cen  = fkFactor.Get("Z_pho_NLO")
  mrup = fkFactor.Get("Z_pho_NLO_mrUp")		; mrup.Divide(cen)
  mrdn = fkFactor.Get("Z_pho_NLO_mrDown")	; mrdn.Divide(cen)
  mr2up = fkFactor.Get("Z_pho_NLO_mr2Up")	; mr2up.Divide(cen)
  mr2dn = fkFactor.Get("Z_pho_NLO_mr2Down")	; mr2dn.Divide(cen)
  mfup = fkFactor.Get("Z_pho_NLO_mfUp")		; mfup.Divide(cen)
  mfdn = fkFactor.Get("Z_pho_NLO_mfDown")	; mfdn.Divide(cen)
  mf2up = fkFactor.Get("Z_pho_NLO_mf2Up")	; mf2up.Divide(cen)
  mf2dn = fkFactor.Get("Z_pho_NLO_mf2Down")	; mf2dn.Divide(cen)

  # Get RMS and add to make up/down 
  rmspdf = fkFactor.Get("RMS_NNPDF_Z_Pho_NLO")
  pdfup = cen.Clone(); pdfup.SetName("gen_weights_%s_pdf_Up"%nam)
  pdfdn = cen.Clone(); pdfdn.SetName("gen_weights_%s_pdf_Down"%nam)
  for b in range(rmspdf.GetNbinsX()):
    pdfup.SetBinContent(b+1,1.+(rmspdf.GetBinError(b+1)/rmspdf.GetBinContent(b+1)))
    pdfdn.SetBinContent(b+1,1.-(rmspdf.GetBinError(b+1)/rmspdf.GetBinContent(b+1)))

  # reweight the correct order Z.
  hmrup = target.Clone(); hmrup.SetName("photon_weights_%s_mr_Up"%nam); 
  for b in range(hmrup.GetNbinsX()): hmrup.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(hmrup,mrup,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hmrup.Divide(nlo_pho_met)

  hmrdn = target.Clone(); hmrdn.SetName("photon_weights_%s_mr_Down"%nam)
  for b in range(hmrdn.GetNbinsX()): hmrdn.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(hmrdn,mrdn,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hmrdn.Divide(nlo_pho_met)

  hmr2up = target.Clone(); hmr2up.SetName("photon_weights_%s_mr2_Up"%nam); 
  for b in range(hmr2up.GetNbinsX()): hmr2up.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(hmr2up,mr2up,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hmr2up.Divide(nlo_pho_met)

  hmr2dn = target.Clone(); hmr2dn.SetName("photon_weights_%s_mr2_Down"%nam)
  for b in range(hmr2dn.GetNbinsX()): hmr2dn.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(hmr2dn,mr2dn,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hmr2dn.Divide(nlo_pho_met)
  
  hmfup = target.Clone(); hmfup.SetName("photon_weights_%s_mf_Up"%nam); 
  for b in range(hmfup.GetNbinsX()): hmfup.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(hmfup,mfup,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hmfup.Divide(nlo_pho_met)

  hmfdn = target.Clone(); hmfdn.SetName("photon_weights_%s_mf_Down"%nam)
  for b in range(hmfdn.GetNbinsX()): hmfdn.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(hmfdn,mfdn,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hmfdn.Divide(nlo_pho_met)

  hmf2up = target.Clone(); hmf2up.SetName("photon_weights_%s_mf2_Up"%nam); 
  for b in range(hmf2up.GetNbinsX()): hmf2up.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(hmf2up,mf2up,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hmf2up.Divide(nlo_pho_met)

  hmf2dn = target.Clone(); hmf2dn.SetName("photon_weights_%s_mf2_Down"%nam)
  for b in range(hmf2dn.GetNbinsX()): hmf2dn.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(hmf2dn,mf2dn,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hmf2dn.Divide(nlo_pho_met)
  
  hpdfup = target.Clone(); hpdfup.SetName("photon_weights_%s_pdf_Up"%nam); 
  for b in range(hpdfup.GetNbinsX()): hpdfup.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(hpdfup,pdfup,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hpdfup.Divide(nlo_pho_met)

  hpdfdn = target.Clone(); hpdfdn.SetName("photon_weights_%s_pdf_Down"%nam)
  for b in range(hpdfdn.GetNbinsX()): hpdfdn.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(hpdfdn,pdfdn,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hpdfdn.Divide(nlo_pho_met)

  # Notice that the EWKUp was calculated on the g/Z ratio and Down is its inverse. So need to swap them 
  RatioEwkDown = fkFactor.Get("EWK_Dwon"); 
  for b in range(RatioEwkDown.GetNbinsX()): RatioEwkDown.SetBinContent(b+1,1./RatioEwkDown.GetBinContent(b+1))
  RatioEwkUp   = fkFactor.Get("EWK_Up");   
  for b in range(RatioEwkUp.GetNbinsX()): RatioEwkUp.SetBinContent(b+1,1./RatioEwkUp.GetBinContent(b+1))

  ewkDown = target.Clone(); ewkDown.SetName("photon_weights_%s_ewk_Down"%nam)
  for b in range(ewkDown.GetNbinsX()): ewkDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(ewkDown,RatioEwkDown,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  ewkDown.Divide(nlo_pho_met)

  ewkUp = target.Clone(); ewkUp.SetName("photon_weights_%s_ewk_Up"%nam)
  for b in range(ewkUp.GetNbinsX()): ewkUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(ewkUp,RatioEwkUp,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  ewkUp.Divide(nlo_pho_met)

  # Footprint is a little different now, the dataset is photon_data_FPUp/Down so use relative uncertainty there
  photon_data_nom  = _fin.Get("photon_data")
  photon_data_fpup = _fin.Get("photon_data_FPUp")  ; photon_data_fpup.Divide(photon_data_nom)
  photon_data_fpdn = _fin.Get("photon_data_FPDown"); photon_data_fpdn.Divide(photon_data_nom)
  photon_weight_fpup = nlo_zjt_met.Clone(); photon_weight_fpup.SetName("photon_weights_%s_gamFootPrint_Up"%nam); photon_weight_fpup.Multiply(photon_data_fpup)
  photon_weight_fpdn = nlo_zjt_met.Clone(); photon_weight_fpdn.SetName("photon_weights_%s_gamFootPrint_Down"%nam); photon_weight_fpdn.Multiply(photon_data_fpdn)
  
  # Same for electrons ..
  dielectron_data_nom  = _fin.Get("dielectron_data")
  dielectron_data_fpup = _fin.Get("dielectron_data_FPUp")  ; dielectron_data_fpup.Divide(dielectron_data_nom)
  dielectron_data_fpdn = _fin.Get("dielectron_data_FPDown"); dielectron_data_fpdn.Divide(dielectron_data_nom)
  dielectron_weight_fpup = ZeeScales.Clone(); dielectron_weight_fpup.SetName("zee_weights_%s_eleFootPrint_Up"%nam); dielectron_weight_fpup.Multiply(dielectron_data_fpup)
  dielectron_weight_fpdn = ZeeScales.Clone(); dielectron_weight_fpdn.SetName("zee_weights_%s_eleFootPrint_Down"%nam); dielectron_weight_fpdn.Multiply(dielectron_data_fpdn)
  ##################################################################################################################

  _fOut.WriteTObject( nlo_zjt_met ) # Save weights and variations to file 
  _fOut.WriteTObject( hmrup )
  _fOut.WriteTObject( hmrdn )
  _fOut.WriteTObject( hmr2up )
  _fOut.WriteTObject( hmr2dn )
  _fOut.WriteTObject( hmfup )
  _fOut.WriteTObject( hmfdn )
  _fOut.WriteTObject( hmf2up )
  _fOut.WriteTObject( hmf2dn )
  _fOut.WriteTObject( hpdfup )
  _fOut.WriteTObject( hpdfdn )

  _fOut.WriteTObject( ewkUp )
  _fOut.WriteTObject( ewkDown )

  _fOut.WriteTObject( photon_weight_fpup )
  _fOut.WriteTObject( photon_weight_fpdn )
  
  _fOut.WriteTObject( dielectron_weight_fpup )
  _fOut.WriteTObject( dielectron_weight_fpdn )

  for b in range(target.GetNbinsX()):
    ewk_u = nlo_zjt_met.Clone(); ewk_u.SetName("photon_weights_%s_ewk_%s_bin%d_Up"%(nam,nam,b))
    ewk_d = nlo_zjt_met.Clone(); ewk_d.SetName("photon_weights_%s_ewk_%s_bin%d_Down"%(nam,nam,b))
    for j in range(nlo_zjt_met.GetNbinsX()):
      if j==b: 
	ewk_u.SetBinContent(j+1,ewkUp.GetBinContent(j+1))
	ewk_d.SetBinContent(j+1,ewkDown.GetBinContent(j+1))
	break
    _fOut.WriteTObject(ewk_u)
    _fOut.WriteTObject(ewk_d)

  controlmc_wlv      = _fin.Get("signal_wjets")  # defines in / out acceptance
  WZScales = target.Clone(); WZScales.SetName("wz_weights_%s"%nam)
  WZScales.Divide(controlmc_wlv)
  _fOut.WriteTObject(WZScales)  # always write out to the directory 

  for b in range(target.GetNbinsX()):
    ewk_u = WZScales.Clone(); ewk_u.SetName("wz_weights_%s_ewk_W_%s_bin%d_Up"%(nam,nam,b))
    ewk_d = WZScales.Clone(); ewk_d.SetName("wz_weights_%s_ewk_W_%s_bin%d_Down"%(nam,nam,b))
    for j in range(target.GetNbinsX()):
      if j==b: 
	ewk_u.SetBinContent(j+1,WZScales.GetBinContent(j+1)*1.1)
	ewk_d.SetBinContent(j+1,WZScales.GetBinContent(j+1)*0.9)
	break
    _fOut.WriteTObject(ewk_u)
    _fOut.WriteTObject(ewk_d)

  # finally make a photon background dataset 
  fPurity = r.TFile.Open("files/photonPurity.root")
  ptphopurity = fPurity.Get("data")
  photon_background = target.Clone(); photon_background.SetName("photon_gjet_background")
  for b in range(ptphopurity.GetNbinsX()): 
  	ptphopurity.SetBinContent(b+1,1-ptphopurity.GetBinContent(b+1))  # background is 1-purity
  for b in range(photon_background.GetNbinsX()): 
  	photon_background.SetBinContent(b+1,0)
  ptphopurity.Print()
  diag.generateWeightedTemplate(photon_background,ptphopurity,"ptpho",metname,_wspace.data("photon_data"))
  #photon_background.SetTitle("base") # --> Makes sure this gets converted to RooDataHist laters
  #_fin.WriteTObject(photon_background);
  # store the histogram to be written out later 
  convertHistograms.append(photon_background)

def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  
  # Some setup
  _fin = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)


  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # example below for creating shape systematic for photon which is just every bin up/down 30% 

  metname = "mvamet"    # Observable variable name 
  targetmc     = _fin.Get("signal_zjets")      # define monimal (MC) of which process this config will model
  controlmc    = _fin.Get("dimuon_zll")  # defines in / out acceptance
#  controlmce    = _fin.Get("dielectron_zll")  # defines in / out acceptance

  controlmc_photon   = _fin.Get("photon_gjet")  # defines in / out acceptance
  controlmc_wlv      = _fin.Get("signal_wjets")  # defines in / out acceptance

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  ZmmScales = targetmc.Clone(); ZmmScales.SetName("zmm_weights_%s"%cid)
  ZmmScales.Divide(controlmc)
  _fOut.WriteTObject(ZmmScales)  # always write out to the directory 

  #PhotonScales = targetmc.Clone(); PhotonScales.SetName("photon_weights_%s"%cid)
  #PhotonScales.Divide(controlmc_photon)
  #_fOut.WriteTObject(PhotonScales)  # always write out to the directory 

  WZScales = targetmc.Clone(); WZScales.SetName("wz_weights_%s"%cid)
  WZScales.Divide(controlmc_wlv)
  _fOut.WriteTObject(WZScales)  # always write out to the directory 

  my_function(_wspace,_fin,_fOut,cid,diag)
  PhotonScales = _fOut.Get("photon_weights_%s"%cid)
  ZeeScales = _fOut.Get("zee_weights_%s"%cid)# targetmc.Clone(); ZeeScales.SetName("zee_weights_%s"%cid)

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
   Channel("photon",_wspace,out_ws,cid+'_'+model,PhotonScales) 
  ,Channel("dimuon",_wspace,out_ws,cid+'_'+model,ZmmScales)
  ,Channel("dielectron",_wspace,out_ws,cid+'_'+model,ZeeScales)
  #,Channel("wjetssignal",_wspace,out_ws,cid+'_'+model,WZScales)
  ]


  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)
  CRs[0].add_nuisance_shape("mr",_fOut) 
  CRs[0].add_nuisance_shape("mf",_fOut) 
  CRs[0].add_nuisance_shape("mr2",_fOut) 
  CRs[0].add_nuisance_shape("mf2",_fOut) 
  CRs[0].add_nuisance_shape("pdf",_fOut) 
  CRs[0].add_nuisance_shape("gamFootPrint",_fOut) 
  CRs[0].add_nuisance("PhotonEfficiency",0.01) 
  CRs[1].add_nuisance("CMS_eff_m",0.01)
  CRs[2].add_nuisance("CMS_eff_e",0.01)
  CRs[2].add_nuisance_shape("eleFootPrint",_fOut)

  # Now for each bin in the distribution, we make one EWK uncertainty which is the size of  the Up/Down variation --> Completely uncorrelated between bins
  #for b in range(targetmc.GetNbinsX()):
   # CRs[2].add_nuisance_shape("ewk_W_%s_bin%d"%(cid,b),_fOut)

  # Now for each bin in the distribution, we make one EWK uncertainty which is the size of  the Up/Down variation --> Completely uncorrelated between bins
  for b in range(targetmc.GetNbinsX()):
    CRs[0].add_nuisance_shape("ewk_%s_bin%d"%(cid,b),_fOut)

  # Bin by bin nuisances to cover statistical uncertainties ...
  for b in range(targetmc.GetNbinsX()):
    err = PhotonScales.GetBinError(b+1)
    if not PhotonScales.GetBinContent(b+1)>0: continue 
    relerr = err/PhotonScales.GetBinContent(b+1)
    if relerr<0.01: continue
    byb_u = PhotonScales.Clone(); byb_u.SetName("photon_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"photonCR",b))
    byb_u.SetBinContent(b+1,PhotonScales.GetBinContent(b+1)+err)
    byb_d = PhotonScales.Clone(); byb_d.SetName("photon_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"photonCR",b))
    byb_d.SetBinContent(b+1,PhotonScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[0].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"photonCR",b),_fOut)

  for b in range(targetmc.GetNbinsX()):
    err = ZmmScales.GetBinError(b+1)
    if not ZmmScales.GetBinContent(b+1)>0: continue 
    relerr = err/ZmmScales.GetBinContent(b+1)
    if relerr<0.01: continue
    byb_u = ZmmScales.Clone(); byb_u.SetName("zmm_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"dimuonCR",b))
    byb_u.SetBinContent(b+1,ZmmScales.GetBinContent(b+1)+err)
    byb_d = ZmmScales.Clone(); byb_d.SetName("zmm_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"dimuonCR",b))
    byb_d.SetBinContent(b+1,ZmmScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[1].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"dimuonCR",b),_fOut)

  for b in range(targetmc.GetNbinsX()):
    err = ZeeScales.GetBinError(b+1)
    if not ZeeScales.GetBinContent(b+1)>0: continue 
    relerr = err/ZeeScales.GetBinContent(b+1)
    if relerr<0.01: continue
    byb_u = ZeeScales.Clone(); byb_u.SetName("zee_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"dielectronCR",b))
    byb_u.SetBinContent(b+1,ZeeScales.GetBinContent(b+1)+err)
    byb_d = ZeeScales.Clone(); byb_d.SetName("zee_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"dielectronCR",b))
    byb_d.SetBinContent(b+1,ZeeScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[2].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"dielectronCR",b),_fOut)
  #######################################################################################################


  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,targetmc.GetName(),CRs,diag)
  # Return of course
  #cat.addTarget("photon_gjet_background",-2)# -2 means dont apply any correction # make histogram for this guy?
  return cat

