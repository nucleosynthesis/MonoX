
import ROOT 
fi = ROOT.TFile.Open("mlfit_reg.root")
fit_s = fi.Get("fit_s")

errsZ = ROOT.TH1F("errsZ","",4,200,1000)
errsW = ROOT.TH1F("errsW","",4,200,1000)
errsT = ROOT.TH1F("errsT","",4,200,1000)

for b in range(0,4):
  wv =(fit_s.floatParsFinal().find("model_mu_cat_monojet_wjets_bin_%d"%b)).getVal() 
  zv =(fit_s.floatParsFinal().find("model_mu_cat_monojet_zjets_bin_%d"%b)).getVal() 
  we =(fit_s.floatParsFinal().find("model_mu_cat_monojet_wjets_bin_%d"%b)).getError() 
  ze =(fit_s.floatParsFinal().find("model_mu_cat_monojet_zjets_bin_%d"%b)).getError() 
  errsZ.SetBinError(b+1,ze/zv)
  errsW.SetBinError(b+1,we/wv)
  errsT.SetBinError(b+1,((ze**2+we**2)**0.5)/(zv+wv))
  print b, "W = ", wv,we," Z = ",zv,ze

errsT.SetFillColor(ROOT.kPink-4)
errsZ.SetFillColor(ROOT.kBlue-10)
errsW.SetFillColor(ROOT.kGreen-3)

errsT.SetLineColor(1)
errsZ.SetLineColor(1)
errsW.SetLineColor(1)

errsT.SetLineWidth(2)
errsZ.SetLineWidth(2)
errsW.SetLineWidth(2)

errsT.Draw("E2")
#errsW.Draw("E2same")
#errsZ.Draw("E2same")
fout = ROOT.TFile("reg.root","RECREATE")
errsT.SetName("reg")
errsT.Write()

raw_input()
