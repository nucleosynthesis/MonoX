import ROOT

ROOT.gStyle.SetOptStat(0)

fin = ROOT.TFile.Open("../combined_model.root") 
fout = ROOT.TFile("scale-factors.root","RECREATE")

sfactors = {
	   "Z_constraints_category_monojet/photon_weights_monojet": "R^{#gamma}"
	   ,"Z_constraints_category_monojet/zee_weights_monojet"   : "R^{Z#rightarrow ee}"
	   ,"Z_constraints_category_monojet/zmm_weights_monojet"   : "R^{Z#rightarrow #mu#mu}"
	   ,"Z_constraints_category_monojet/wz_weights_monojet"	  : "R^{W/Z}"
	   ,"W_DEP_constraints_category_monojet/wen_weights_monojet": "R^{W#rightarrow e#nu}"
	   ,"W_DEP_constraints_category_monojet/wmn_weights_monojet": "R^{W#rightarrow #mu#nu}"
	   }

for sf in sfactors.keys(): 


 tc = ROOT.TCanvas("%s"%((sf.split("/"))[-1]),"",800,600)
 
 sfC = fin.Get(sf)
 sfC.SetTitle("")
 sfC.GetXaxis().SetTitle("Recoil (GeV)")
 sfC.GetYaxis().SetTitle(sfactors[sf])
 sfC.SetMarkerSize(1.0)
 sfC.SetMarkerColor(1)
 sfC.SetLineColor(1)
 sfC.SetLineWidth(2)
 sfC.SetMarkerStyle(20)

 sfE = fin.Get("%s_uncert"%sf)
 sfE.SetFillColor(ROOT.kGreen-5)

 sfC.Draw("axis")
 sfE.Draw("pe2")
 sfC.Draw("pelsame")
 tc.RedrawAxis()

 tLeg = ROOT.TLegend(0.46,0.7,0.89,0.89)
 tLeg.SetTextFont(42)
 tLeg.SetBorderSize(0)
 tLeg.SetFillColor(0)
 tLeg.AddEntry(sfC,"%s Transfer Factor #pm MC Stat"%sfactors[sf],"PEL")
 tLeg.AddEntry(sfE,"#pm MC Stat #pm Systematics","F")
 tLeg.Draw()

 fout.cd()
 tc.Write()
print "scale factors saved in ", fout.GetName() 
