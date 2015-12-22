import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining *cmodel*, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
# Second is a list of histos which will addtionally be converted to RooDataHists, leave blank if not needed
model = "zjets"
convertHistograms = []
import sys

def my_W_function(_wspace,_fin,_fOut,nam,diag):

  metname = "mvamet"    # Observable variable name 
  gvptname = "genVpt"    # Weights are in generator pT
  wvarname= "weight"
  target        = _fin.Get("signal_zjets")      # define monimal (MC) of which process this config will model
  
  fkFactorCentral  = r.TFile.Open("files/scalefactors.root")
  # we want to make Z/W ratios ..., use the very best input from the theory 
  nlo_wjt_LO      = fkFactorCentral.Get("wlo/wlo_nominal")
  nlo_wjt_NLO012j = fkFactorCentral.Get("wnlo012/wnlo012_nominal")
  nlo_wjt_NLO012j.Divide(nlo_wjt_LO)
  diag.generateWeightedDataset("signal_wjets_nlo012jt_QCD",nlo_wjt_NLO012j,wvarname,gvptname,_wspace,"signal_wjets")

  ewkCorr_wjt = fkFactorCentral.Get("w_ewkcorr/w_ewkcorr_orig") 
  diag.generateWeightedDataset("signal_wjets_nlo012jt",ewkCorr_wjt,wvarname,gvptname,_wspace,"signal_wjets_nlo012jt_QCD")
  nlo_wjets_FULL = target.Clone(); 
  diag.generateTemplate(nlo_wjets_FULL,metname,_wspace.data("signal_wjets_nlo012jt"));

  # We already have the Z (assuming the other function was called so 
  nlo_zvv_FULL = _fOut.Get("Zvv_met_spec_FULLCorrections")
  WZScales = nlo_zvv_FULL.Clone(); WZScales.SetName("wz_weights_%s"%nam)
  WZScales.Divide(nlo_wjets_FULL);
  _fOut.WriteTObject(WZScales)

  # for each variation, we make Z/Z up/nominal NLO  (this will be our ratio)
  cen   = fkFactorCentral.Get("znlo012_over_wnlo012/znlo012_over_wnlo012")
  mrup  = fkFactorCentral.Get("znlo012_over_wnlo012/znlo012_over_wnlo012_renCorrUp"  ) ; mrup.Divide(cen)
  mrdn  = fkFactorCentral.Get("znlo012_over_wnlo012/znlo012_over_wnlo012_renCorrDown") ; mrdn.Divide(cen)
  mr2up = fkFactorCentral.Get("znlo012_over_wnlo012/znlo012_over_wnlo012_renAcorrUp"  ); mr2up.Divide(cen)
  mr2dn = fkFactorCentral.Get("znlo012_over_wnlo012/znlo012_over_wnlo012_renAcorrDown"); mr2dn.Divide(cen)
  mfup  = fkFactorCentral.Get("znlo012_over_wnlo012/znlo012_over_wnlo012_facAcorrUp"  ); mfup.Divide(cen)
  mfdn  = fkFactorCentral.Get("znlo012_over_wnlo012/znlo012_over_wnlo012_facAcorrDown"); mfdn.Divide(cen)
  mf2up = fkFactorCentral.Get("znlo012_over_wnlo012/znlo012_over_wnlo012_facAcorrUp"  ); mf2up.Divide(cen)
  mf2dn = fkFactorCentral.Get("znlo012_over_wnlo012/znlo012_over_wnlo012_facAcorrDown"); mf2dn.Divide(cen)

  cenY  = fkFactorCentral.Get("znlo012_over_wnlo012/znlo012_over_wnlo012"); 
  pdfup = fkFactorCentral.Get("znlo012_over_wnlo012/znlo012_over_wnlo012_pdfUp"); pdfup.SetName("gen_weights_%s_pdf_Up"%nam)
  pdfdn = fkFactorCentral.Get("znlo012_over_wnlo012/znlo012_over_wnlo012_pdfDown"); pdfdn.SetName("gen_weights_%s_pdf_Down"%nam)
  pdfup.Divide(cenY)
  pdfdn.Divide(cenY)

  # reweight the correct order Z.
  hmrup = target.Clone(); hmrup.SetName("wz_weights_%s_mrW_Up"%nam); 
  diag.generateWeightedTemplate(hmrup,mrup,gvptname,metname,_wspace.data("signal_zjets_nlo012jt"))
  hmrup.Divide(nlo_wjets_FULL)

  hmrdn = target.Clone(); hmrdn.SetName("wz_weights_%s_mrW_Down"%nam)
  diag.generateWeightedTemplate(hmrdn,mrdn,gvptname,metname,_wspace.data("signal_zjets_nlo012jt"))
  hmrdn.Divide(nlo_wjets_FULL)

  hmr2up = target.Clone(); hmr2up.SetName("wz_weights_%s_mr2W_Up"%nam); 
  diag.generateWeightedTemplate(hmr2up,mr2up,gvptname,metname,_wspace.data("signal_zjets_nlo012jt"))
  hmr2up.Divide(nlo_wjets_FULL)

  hmr2dn = target.Clone(); hmr2dn.SetName("wz_weights_%s_mr2W_Down"%nam)
  diag.generateWeightedTemplate(hmr2dn,mr2dn,gvptname,metname,_wspace.data("signal_zjets_nlo012jt"))
  hmr2dn.Divide(nlo_wjets_FULL)
  
  hmfup = target.Clone(); hmfup.SetName("wz_weights_%s_mfW_Up"%nam); 
  diag.generateWeightedTemplate(hmfup,mfup,gvptname,metname,_wspace.data("signal_zjets_nlo012jt"))
  hmfup.Divide(nlo_wjets_FULL)

  hmfdn = target.Clone(); hmfdn.SetName("wz_weights_%s_mfW_Down"%nam)
  diag.generateWeightedTemplate(hmfdn,mfdn,gvptname,metname,_wspace.data("signal_zjets_nlo012jt"))
  hmfdn.Divide(nlo_wjets_FULL)

  hmf2up = target.Clone(); hmf2up.SetName("wz_weights_%s_mf2W_Up"%nam); 
  diag.generateWeightedTemplate(hmf2up,mf2up,gvptname,metname,_wspace.data("signal_zjets_nlo012jt"))
  hmf2up.Divide(nlo_wjets_FULL)

  hmf2dn = target.Clone(); hmf2dn.SetName("wz_weights_%s_mf2W_Down"%nam)
  diag.generateWeightedTemplate(hmf2dn,mf2dn,gvptname,metname,_wspace.data("signal_zjets_nlo012jt"))
  hmf2dn.Divide(nlo_wjets_FULL)
 
  hpdfup = target.Clone(); hpdfup.SetName("wz_weights_%s_pdf_Up"%nam); 
  diag.generateWeightedTemplate(hpdfup,pdfup,gvptname,metname,_wspace.data("signal_zjets_nlo012jt"))
  hpdfup.Divide(nlo_wjets_FULL)

  hpdfdn = target.Clone(); hpdfdn.SetName("wz_weights_%s_pdf_Down"%nam)
  diag.generateWeightedTemplate(hpdfdn,pdfdn,gvptname,metname,_wspace.data("signal_zjets_nlo012jt"))
  hpdfdn.Divide(nlo_wjets_FULL)

  #genewkWDown = fkFactorCentral.Get("w_ewkcorr/w_ewkcorrDown_orig")
  genewkWUp   = fkFactorCentral.Get("w_ewkcorr/w_ewkcorr_orig")
  # For the W therte is no up/down so just square it 
 
  #genewkZDown = fkFactorCentral.Get("z_ewkcorr/z_ewkcorrDown_orig")
  genewkZUp   = fkFactorCentral.Get("z_ewkcorr/z_ewkcorr_orig")

  ewkWDown = target.Clone() ; ewkWDown.SetName("ewkWDown") 
  diag.generateTemplate(ewkWDown,metname,_wspace.data("signal_wjets_nlo012jt_QCD"))
  ewkWUp = target.Clone() ; ewkWUp.SetName("ewkWUp") 
  diag.generateWeightedTemplate(ewkWUp,genewkWUp,gvptname,metname,_wspace.data("signal_wjets_nlo012jt")) # apply twice!
  
  ewkDown = target.Clone() ; ewkDown.SetName("wz_weights_%s_ewk_Down"%nam) 
  diag.generateTemplate(ewkDown,metname,_wspace.data("signal_zjets_nlo1jt_QCD"))
  ewkUp = target.Clone() ; ewkUp.SetName("wz_weights_%s_ewk_Up"%nam) 
  diag.generateWeightedTemplate(ewkUp,genewkZUp,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))

  ewkUp.Divide(ewkWUp)
  ewkDown.Divide(ewkWDown)

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

  for b in range(target.GetNbinsX()):
    ewk_u = WZScales.Clone(); ewk_u.SetName("wz_weights_%s_ewkW_%s_bin%d_Up"%(nam,nam,b))
    ewk_d = WZScales.Clone(); ewk_d.SetName("wz_weights_%s_ewkW_%s_bin%d_Down"%(nam,nam,b))
    for j in range(WZScales.GetNbinsX()):
      if j==b: 
	ewk_u.SetBinContent(j+1,ewkUp.GetBinContent(j+1))
	ewk_d.SetBinContent(j+1,ewkDown.GetBinContent(j+1))
	break
    _fOut.WriteTObject(ewk_u)
    _fOut.WriteTObject(ewk_d)


# My Function. Just to put all of the complicated part into one function
def my_function(_wspace,_fin,_fOut,nam,diag):

  metname = "mvamet"    # Observable variable name 
  gvptname = "genVpt"    # Weights are in generator pT
  wvarname= "weight"
  target        = _fin.Get("signal_zjets")      # define monimal (MC) of which process this config will model

  # first, easy bit, make the scales for Z->ee 

  fkFactorCentral  = r.TFile.Open("files/scalefactors.root")
  #fkFactor = r.TFile.Open("files/Photon_Z_NLO_kfactors_w80pcorr.root")

  # Central value Photon LO -> NLO, make a dataet 
  nlo_pho = fkFactorCentral.Get("anlo1_over_alo/anlo1_over_alo")
  diag.generateWeightedDataset("photon_gjet_nlo_QCD",nlo_pho,wvarname,gvptname,_wspace,"photon_gjet")

  # Z+jets MC NLO, make a dataset. # NOTE THAT we need to just take the 012 why not! 
  nlo_zjt_NLO1j = fkFactorCentral.Get("znlo012/znlo012_nominal")
  nlo_zjt_LO    = fkFactorCentral.Get("zlo/zlo_nominal")
  nlo_zjt_NLO1j.Divide(nlo_zjt_LO)
  diag.generateWeightedDataset("signal_zjets_nlo1jt_QCD",nlo_zjt_NLO1j,wvarname,gvptname,_wspace,"signal_zjets")  # cheating, here this is really th eZ 0,1,2

  # Correct for the Eletroweak corrections ... (uncertainties from OLD files)
  ewkCorr_pho = fkFactorCentral.Get("a_ewkcorr/a_ewkcorr_orig") 
  ewkCorr_zjt = fkFactorCentral.Get("z_ewkcorr/z_ewkcorr_orig") 
  diag.generateWeightedDataset("photon_gjet_nlo",ewkCorr_pho,wvarname,gvptname,_wspace,"photon_gjet_nlo_QCD")
  diag.generateWeightedDataset("signal_zjets_nlo1jt",ewkCorr_zjt,wvarname,gvptname,_wspace,"signal_zjets_nlo1jt_QCD")
  
  # Also make a nice Z+jets 0,1,2 + EWK for use with Z->ee/Z->mm scales
  nlo_zjt_NLO012j =  fkFactorCentral.Get("znlo012/znlo012_nominal")
  nlo_zjt_NLO012j.Divide(nlo_zjt_LO)

  diag.generateWeightedDataset("signal_zjets_nlo012jt_QCD",nlo_zjt_NLO012j,wvarname,gvptname,_wspace,"signal_zjets")
  diag.generateWeightedDataset("signal_zjets_nlo012jt",ewkCorr_zjt,wvarname,gvptname,_wspace,"signal_zjets_nlo012jt_QCD")
  nlo_zvv_FULL = target.Clone(); nlo_zvv_FULL.SetName("Zvv_met_spec_FULLCorrections");
  diag.generateTemplate(nlo_zvv_FULL,metname,_wspace.data("signal_zjets_nlo012jt"));

  # Also need templates for Z->ee, Z->mm 
  diag.generateWeightedDataset("dimuon_zll_nlo012jt_QCD",nlo_zjt_NLO012j,wvarname,gvptname,_wspace,"dimuon_zll")
  diag.generateWeightedDataset("dimuon_zll_nlo012jt",ewkCorr_zjt,wvarname,gvptname,_wspace,"dimuon_zll_nlo012jt_QCD")
  nlo_zmm_FULL = target.Clone();
  diag.generateTemplate(nlo_zmm_FULL,metname,_wspace.data("dimuon_zll_nlo012jt"))

  diag.generateWeightedDataset("dielectron_zll_nlo012jt_QCD",nlo_zjt_NLO012j,wvarname,gvptname,_wspace,"dielectron_zll")
  diag.generateWeightedDataset("dielectron_zll_nlo012jt",ewkCorr_zjt,wvarname,gvptname,_wspace,"dielectron_zll_nlo012jt_QCD")
  nlo_zee_FULL = target.Clone();
  diag.generateTemplate(nlo_zee_FULL,metname,_wspace.data("dielectron_zll_nlo012jt"))


  ZeeWeights = nlo_zvv_FULL.Clone(); ZeeWeights.SetName("zee_weights_%s"%nam)
  ZmmWeights = nlo_zvv_FULL.Clone(); ZmmWeights.SetName("zmm_weights_%s"%nam)
  ZeeWeights.Divide(nlo_zee_FULL);
  ZmmWeights.Divide(nlo_zmm_FULL);

  _fOut.WriteTObject(ZmmWeights)
  _fOut.WriteTObject(ZeeWeights)
  _fOut.WriteTObject(nlo_zvv_FULL)


  # Now the photons/Z ratios .... 
  nlo_pho_met = target.Clone(); nlo_pho_met.SetName("photon_weights_denom_%s"%nam); 
  for b in range(nlo_pho_met.GetNbinsX()): nlo_pho_met.SetBinContent(b+1,0)
  diag.generateTemplate(nlo_pho_met,metname,_wspace.data("photon_gjet_nlo"))

  # zjet (NLO 1-jet) spectrum is numerator
  nlo_zjt_met = target.Clone(); nlo_zjt_met.SetName("photon_weights_%s"%nam); 
  for b in range(nlo_zjt_met.GetNbinsX()): nlo_zjt_met.SetBinContent(b+1,0)
  diag.generateTemplate(nlo_zjt_met,metname,_wspace.data("signal_zjets_nlo1jt"))

  # Keep this safe
  nlo_zjt_metSpec = nlo_zjt_met.Clone(); nlo_zjt_metSpec.SetName("nlo1j_zjet_spectrum_met_%s"%nam); 

  # Weights Z/gamma! #####################
  nlo_zjt_met.Divide(nlo_pho_met)
  #########################################

  # for each variation, we make Z/pho up/nominal NLO  (this will be our ratio)
  cen   = fkFactorCentral.Get("znlo1_over_anlo1/znlo1_over_anlo1")
  mrup  = fkFactorCentral.Get("znlo1_over_anlo1/znlo1_over_anlo1_renCorrUp"  ) ; mrup.Divide(cen)
  mrdn  = fkFactorCentral.Get("znlo1_over_anlo1/znlo1_over_anlo1_renCorrDown") ; mrdn.Divide(cen)
  mr2up = fkFactorCentral.Get("znlo1_over_anlo1/znlo1_over_anlo1_renAcorrUp"  ); mr2up.Divide(cen)
  mr2dn = fkFactorCentral.Get("znlo1_over_anlo1/znlo1_over_anlo1_renAcorrDown"); mr2dn.Divide(cen)
  mfup  = fkFactorCentral.Get("znlo1_over_anlo1/znlo1_over_anlo1_facCorrUp"  ); mfup.Divide(cen)
  mfdn  = fkFactorCentral.Get("znlo1_over_anlo1/znlo1_over_anlo1_facCorrDown"); mfdn.Divide(cen)
  mf2up = fkFactorCentral.Get("znlo1_over_anlo1/znlo1_over_anlo1_facAcorrUp"  ); mf2up.Divide(cen)
  mf2dn = fkFactorCentral.Get("znlo1_over_anlo1/znlo1_over_anlo1_facAcorrDown"); mf2dn.Divide(cen)

  # Get RMS and add to make up/down 
  #rmspdf = fkFactor.Get("RMS_NNPDF_Z_Pho_NLO")

  cenY  = fkFactorCentral.Get("znlo1_over_anlo1/znlo1_over_anlo1"); 
  pdfup = fkFactorCentral.Get("znlo1_over_anlo1/znlo1_over_anlo1_pdfUp"); pdfup.SetName("gen_weights_%s_pdf_Up"%nam)
  pdfdn = fkFactorCentral.Get("znlo1_over_anlo1/znlo1_over_anlo1_pdfDown"); pdfdn.SetName("gen_weights_%s_pdf_Down"%nam)
  pdfup.Divide(cenY)
  pdfdn.Divide(cenY)

  # reweight the correct order Z.
  hmrup = target.Clone(); hmrup.SetName("photon_weights_%s_mr_Up"%nam); 
  diag.generateWeightedTemplate(hmrup,mrup,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hmrup.Divide(nlo_pho_met)

  hmrdn = target.Clone(); hmrdn.SetName("photon_weights_%s_mr_Down"%nam)
  diag.generateWeightedTemplate(hmrdn,mrdn,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hmrdn.Divide(nlo_pho_met)

  hmr2up = target.Clone(); hmr2up.SetName("photon_weights_%s_mr2_Up"%nam); 
  diag.generateWeightedTemplate(hmr2up,mr2up,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hmr2up.Divide(nlo_pho_met)

  hmr2dn = target.Clone(); hmr2dn.SetName("photon_weights_%s_mr2_Down"%nam)
  diag.generateWeightedTemplate(hmr2dn,mr2dn,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hmr2dn.Divide(nlo_pho_met)
  
  hmfup = target.Clone(); hmfup.SetName("photon_weights_%s_mf_Up"%nam); 
  diag.generateWeightedTemplate(hmfup,mfup,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hmfup.Divide(nlo_pho_met)

  hmfdn = target.Clone(); hmfdn.SetName("photon_weights_%s_mf_Down"%nam)
  diag.generateWeightedTemplate(hmfdn,mfdn,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hmfdn.Divide(nlo_pho_met)

  hmf2up = target.Clone(); hmf2up.SetName("photon_weights_%s_mf2_Up"%nam); 
  diag.generateWeightedTemplate(hmf2up,mf2up,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hmf2up.Divide(nlo_pho_met)

  hmf2dn = target.Clone(); hmf2dn.SetName("photon_weights_%s_mf2_Down"%nam)
  diag.generateWeightedTemplate(hmf2dn,mf2dn,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hmf2dn.Divide(nlo_pho_met)
 
  hpdfup = target.Clone(); hpdfup.SetName("photon_weights_%s_pdf_Up"%nam); 
  diag.generateWeightedTemplate(hpdfup,pdfup,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hpdfup.Divide(nlo_pho_met)

  hpdfdn = target.Clone(); hpdfdn.SetName("photon_weights_%s_pdf_Down"%nam)
  diag.generateWeightedTemplate(hpdfdn,pdfdn,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))
  hpdfdn.Divide(nlo_pho_met)

  #genewkphoDown = fkFactorCentral.Get("a_ewkcorr/a_ewkcorrDown_orig")
  genewkphoUp   = fkFactorCentral.Get("a_ewkcorr/a_ewkcorrUp_orig")
  #genewkZDown = fkFactorCentral.Get("z_ewkcorr/z_ewkcorrDown_orig")
  genewkZUp   = fkFactorCentral.Get("z_ewkcorr/z_ewkcorrUp_orig")

  ewkPhoDown = target.Clone() ; ewkPhoDown.SetName("ewkPhoDown") 
  diag.generateTemplate(ewkPhoDown,metname,_wspace.data("photon_gjet_nlo_QCD"))
  ewkPhoUp = target.Clone() ; ewkPhoUp.SetName("ewkPhoUp") 
  diag.generateWeightedTemplate(ewkPhoUp,genewkphoUp,gvptname,metname,_wspace.data("photon_gjet_nlo"))
  
  ewkDown = target.Clone() ; ewkDown.SetName("photon_weights_%s_ewk_Down"%nam) 
  diag.generateTemplate(ewkDown,metname,_wspace.data("signal_zjets_nlo1jt_QCD"))
  ewkUp = target.Clone() ; ewkUp.SetName("photon_weights_%s_ewk_Up"%nam) 
  diag.generateWeightedTemplate(ewkUp,genewkZUp,gvptname,metname,_wspace.data("signal_zjets_nlo1jt"))

  ewkUp.Divide(ewkPhoUp)
  ewkDown.Divide(ewkPhoDown)

  FootPrintUnc = r.TFile.Open("files/FP_v2.root")
  FPup = FootPrintUnc.Get("FP_Up")
  FPdn = FootPrintUnc.Get("FP_Down")
  
  photon_weight_fpupD = nlo_zjt_met.Clone(); photon_weight_fpupD.SetName("photon_weights_denom_%s_gamFootPrint_Up"%nam); 
  for b in range(photon_weight_fpupD.GetNbinsX()): photon_weight_fpupD.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(photon_weight_fpupD,FPup,"ptpho",metname,_wspace.data("photon_gjet_nlo"))
  photon_weight_fpup = nlo_zjt_metSpec.Clone(); photon_weight_fpup.SetName("photon_weights_%s_gamFootPrint_Up"%nam)
  photon_weight_fpup.Divide(photon_weight_fpupD)
  
  photon_weight_fpdnD = nlo_zjt_met.Clone(); photon_weight_fpdnD.SetName("photon_weights_denom_%s_gamFootPrint_Down"%nam); 
  for b in range(photon_weight_fpdnD.GetNbinsX()): photon_weight_fpdnD.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(photon_weight_fpdnD,FPdn,"ptpho",metname,_wspace.data("photon_gjet_nlo"))
  photon_weight_fpdn = nlo_zjt_metSpec.Clone(); photon_weight_fpdn.SetName("photon_weights_%s_gamFootPrint_Down"%nam)
  photon_weight_fpdn.Divide(photon_weight_fpdnD)
  
  dielectron_weight_fpupD = nlo_zvv_FULL.Clone(); dielectron_weight_fpupD.SetName("zee_weights_denom_%s_eleFootPrint_Up"%nam); 
  for b in range(dielectron_weight_fpupD.GetNbinsX()): dielectron_weight_fpupD.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(dielectron_weight_fpupD,FPup,"ptll",metname,_wspace.data("dielectron_zll_nlo012jt"))
  dielectron_weight_fpup = target.Clone(); dielectron_weight_fpup.SetName("zee_weights_%s_eleFootPrint_Up"%nam)
  dielectron_weight_fpup.Divide(dielectron_weight_fpupD)
  
  dielectron_weight_fpdnD = nlo_zvv_FULL.Clone(); dielectron_weight_fpdnD.SetName("zee_weights_denom_%s_eleFootPrint_Down"%nam); 
  for b in range(dielectron_weight_fpdnD.GetNbinsX()): dielectron_weight_fpdnD.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(dielectron_weight_fpdnD,FPdn,"ptll",metname,_wspace.data("dielectron_zll_nlo012jt"))
  dielectron_weight_fpdn = target.Clone(); dielectron_weight_fpdn.SetName("zee_weights_%s_eleFootPrint_Down"%nam)
  dielectron_weight_fpdn.Divide(dielectron_weight_fpdnD)
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

  # finally make a photon background dataset 
  fPurity = r.TFile.Open("files/photonPurity_13TeV.root")
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


  my_function(_wspace,_fin,_fOut,cid,diag)
  my_W_function(_wspace,_fin,_fOut,cid,diag)
  PhotonScales = _fOut.Get("photon_weights_%s"%cid)
  ZeeScales = _fOut.Get("zee_weights_%s"%cid)
  ZmmScales = _fOut.Get("zmm_weights_%s"%cid)
  WZScales  = _fOut.Get("wz_weights_%s"%cid)

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
  ,Channel("wjetssignal",_wspace,out_ws,cid+'_'+model,WZScales)
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
  CRs[3].add_nuisance_shape("mrW",_fOut) 
  CRs[3].add_nuisance_shape("mfW",_fOut) 
  CRs[3].add_nuisance_shape("mr2W",_fOut) 
  CRs[3].add_nuisance_shape("mf2W",_fOut) 
  CRs[3].add_nuisance_shape("pdf",_fOut) # correlate pdf effects

  # Now for each bin in the distribution, we make one EWK uncertainty which is the size of  the Up/Down variation --> Completely uncorrelated between bins
  #for b in range(targetmc.GetNbinsX()):
   # CRs[2].add_nuisance_shape("ewk_W_%s_bin%d"%(cid,b),_fOut)

  # Now for each bin in the distribution, we make one EWK uncertainty which is the size of  the Up/Down variation --> Completely uncorrelated between bins
  for b in range(targetmc.GetNbinsX()):
    CRs[0].add_nuisance_shape("ewk_%s_bin%d"%(cid,b),_fOut)
    CRs[3].add_nuisance_shape("ewkW_%s_bin%d"%(cid,b),_fOut)

  # Bin by bin nuisances to cover statistical uncertainties ...
  for b in range(targetmc.GetNbinsX()):
    err = PhotonScales.GetBinError(b+1)
    if not PhotonScales.GetBinContent(b+1)>0: relerr = 1.#continue 
    else: relerr = err/PhotonScales.GetBinContent(b+1)
    #if relerr<0.01: continue
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
    if not ZmmScales.GetBinContent(b+1)>0: relerr=1. #continue 
    else: relerr = err/ZmmScales.GetBinContent(b+1)
    #if relerr<0.01: continue
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
    if not ZeeScales.GetBinContent(b+1)>0: relerr = 1. #continue 
    else: relerr = err/ZeeScales.GetBinContent(b+1)
    #if relerr<0.01: continue
    byb_u = ZeeScales.Clone(); byb_u.SetName("zee_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"dielectronCR",b))
    byb_u.SetBinContent(b+1,ZeeScales.GetBinContent(b+1)+err)
    byb_d = ZeeScales.Clone(); byb_d.SetName("zee_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"dielectronCR",b))
    byb_d.SetBinContent(b+1,ZeeScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[2].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"dielectronCR",b),_fOut)
  #######################################################################################################


  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,"signal_zjets_nlo012jt",CRs,diag)  # start from NLO 012 + EWK corrected Z also 
  # Return of course
  #cat.addTarget("photon_gjet_background",-2)# -2 means dont apply any correction # make histogram for this guy?
  return cat

