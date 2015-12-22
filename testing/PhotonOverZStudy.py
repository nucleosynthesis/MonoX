# simple SMP-14-005 study Z/Photon measurement

import ROOT as r
#r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)
import array,sys
#infile = r.TFile.Open("mono-x.root") 
r.gROOT.ProcessLine(".L ../diagonalizer.cc+")
from ROOT import diagonalizer
r.gSystem.Load("libHiggsAnalysisCombinedLimit")

infile = r.TFile.Open("../mono-x.root") 
bins = array.array('d',[200,250,300,350,400,500,600,1000])

phoX = "ptpho"
ZX   = "ptll"

base = r.TH1F("base",";p_{T}^{#mu#mu} or p_{T}^{#gamma}; R Z(#rightarrow#mu#mu)/#gamma",len(bins)-1,bins); base.Sumw2()
one  = r.TH1F("ONE",";p_{T}^{#mu#mu} or p_{T}^{#gamma};  R Z(#rightarrow#mu#mu)/#gamma",1,0,10000); 
for b in range(one.GetNbinsX()): one.SetBinContent(b+1,1)
one.SetLineColor(r.kRed)
one.SetLineWidth(3)

Workspace = infile.Get("category_monojet/wspace_monojet")
diag = diagonalizer(Workspace)

# First grab the data
photon_data = base.Clone(); 
diag.generateTemplate(photon_data,phoX,Workspace.data("photon_data"))

zmm_data = base.Clone();
diag.generateTemplate(zmm_data,ZX,Workspace.data("dimuon_data"))

#MC backgrounds -- Photons fakes 
fPurity = r.TFile.Open("../files/photonPurity_13TeV.root"); ptphopurity = fPurity.Get("data")
photon_background = base.Clone(); photon_background.SetName("photon_gjet_background")
for b in range(ptphopurity.GetNbinsX()): ptphopurity.SetBinContent(b+1,1-ptphopurity.GetBinContent(b+1))  # background is 1-purity
diag.generateWeightedTemplate(photon_background,ptphopurity,"ptpho",phoX,Workspace.data("photon_data"))

# Zmm backgrounds 
top = base.Clone()
dib = base.Clone()
diag.generateTemplate(top,ZX,Workspace.data("dimuon_top"))
diag.generateTemplate(dib,ZX,Workspace.data("dimuon_dibosons"))

photon_data.Add(photon_background,-1)
zmm_data.Add(top,-1)
zmm_data.Add(dib,-1)

zmm_data.Divide(photon_data)
zmm_data.SetMarkerStyle(20); zmm_data.SetMarkerSize(0.8); zmm_data.SetMarkerColor(1); zmm_data.SetLineColor(1)


# Now add theory predictions 
# NLO-1j Photon and NLO-1j Zmm!
fkFactorCentral  = r.TFile.Open("../files/scalefactors.root")

# Central value Photon LO -> NLO, make a dataet 
nlo_pho = fkFactorCentral.Get("anlo1_over_alo/anlo1_over_alo")
diag.generateWeightedDataset("photon_gjet_nlo_QCD",nlo_pho,"weight","genVpt",Workspace,"photon_gjet")
pho_nlo = base.Clone()
diag.generateTemplate(pho_nlo,phoX,Workspace.data("photon_gjet_nlo_QCD"))

nlo_zjt_NLO1j = fkFactorCentral.Get("znlo012_over_znlo1/znlo012_over_znlo1")  # wrong way around so flip it 
for b in range(nlo_zjt_NLO1j.GetNbinsX()): nlo_zjt_NLO1j.SetBinContent(b+1,1./nlo_zjt_NLO1j.GetBinContent(b+1))
diag.generateWeightedDataset("dimuon_zll_nlo1jt_QCD",nlo_zjt_NLO1j,"weight","genVpt",Workspace,"dimuon_zll")
zjt_nlo = base.Clone()
diag.generateTemplate(zjt_nlo,ZX,Workspace.data("dimuon_zll_nlo1jt_QCD"))
zjt_nlo.Divide(pho_nlo); zjt_nlo.SetLineColor(r.kRed); zjt_nlo.SetLineWidth(3)


ewkCorr_pho = fkFactorCentral.Get("a_ewkcorr/a_ewkcorr") 
ewkCorr_zjt = fkFactorCentral.Get("z_ewkcorr/z_ewkcorr") 
diag.generateWeightedDataset("photon_gjet_nlo",ewkCorr_pho,"weight","genVpt",Workspace,"photon_gjet_nlo_QCD")
diag.generateWeightedDataset("dimuon_zll_nlo1jt",ewkCorr_zjt,"weight","genVpt",Workspace,"dimuon_zll_nlo1jt_QCD")



zjt_ewk = base.Clone()
pho_ewk = base.Clone()
diag.generateTemplate(zjt_ewk,ZX,Workspace.data("dimuon_zll_nlo1jt"))
diag.generateTemplate(pho_ewk,phoX,Workspace.data("photon_gjet_nlo"))
zjt_ewk.Divide(pho_ewk)
zjt_ewk.SetLineColor(r.kBlue); zjt_ewk.SetLineWidth(3)


# Now make a bunch of uncertainties ... 
#EWK/updown
genewkphoDown = fkFactorCentral.Get("a_ewkcorr/a_ewkcorrDown_orig")
genewkphoUp   = fkFactorCentral.Get("a_ewkcorr/a_ewkcorrUp_orig")
genewkZDown = fkFactorCentral.Get("z_ewkcorr/z_ewkcorrDown_orig")
genewkZUp   = fkFactorCentral.Get("z_ewkcorr/z_ewkcorrUp_orig")

ewkPhoDown = base.Clone() ; ewkPhoDown.SetName("ewkPhoDown") 
diag.generateWeightedTemplate(ewkPhoDown,genewkphoDown,"genVpt",phoX,Workspace.data("photon_gjet_nlo_QCD"))
ewkPhoUp = base.Clone() ; ewkPhoUp.SetName("ewkPhoUp") 
diag.generateWeightedTemplate(ewkPhoUp,genewkphoUp,"genVpt",phoX,Workspace.data("photon_gjet_nlo_QCD"))
  
ewkDown = base.Clone() ; ewkDown.SetName("photon_weights_s_ewk_Down") 
diag.generateWeightedTemplate(ewkDown,genewkZDown,"genVpt",ZX,Workspace.data("dimuon_zll_nlo1jt_QCD"))
ewkUp = base.Clone() ; ewkUp.SetName("photon_weights_s_ewk_Up") 
diag.generateWeightedTemplate(ewkUp,genewkZUp,"genVpt",ZX,Workspace.data("dimuon_zll_nlo1jt_QCD"))

ewkUp.Divide(ewkPhoUp)
ewkDown.Divide(ewkPhoDown)

# also the scale!!!
# Now look ad delteas and add uncertainty 
uncert = zjt_ewk.Clone(); uncert.SetName("uncertainty"); uncert.SetFillColor(r.kGray)
for b in range(uncert.GetNbinsX()):
  du = abs(ewkUp.GetBinContent(b+1)-zjt_ewk.GetBinContent(b+1))
  dd = abs(ewkDown.GetBinContent(b+1)-zjt_ewk.GetBinContent(b+1))
  uncert.SetBinError(b+1,((max(du,dd))**2+(0.1*zjt_ewk.GetBinContent(b+1))**2)**0.5) 


for d in range(zmm_data.GetNbinsX()): 
  zmm_data.SetBinError(d+1,(zmm_data.GetBinError(d+1)**2+(0.01*zmm_data.GetBinContent(d+1))**2)**0.5)

base.Draw("AXIS")
#one.Draw("histsame")
uncert.Draw("E2same")
zmm_data.Draw("samePEL")
zjt_nlo.Draw("histsame")
zjt_ewk.Draw("histsame")

leg = r.TLegend(0.6,0.6,0.89,0.89)
leg.SetFillColor(0)
leg.SetTextFont(42)
leg.AddEntry(zmm_data,"Data #pm (stat + exp syst)","pel")
leg.AddEntry(zjt_nlo,"NLO QCD 1jet + PS","L")
leg.AddEntry(zjt_ewk,"NLO QCD 1jet + PS + NLO EWK","L")
leg.AddEntry(uncert,"Theory (EWK+QCD scales)#pm 1#sigma","F")
leg.Draw()


raw_input()


# OLD CODE IS HERE!!!!!
photon_d = base.Clone(); photon_d.SetName("photon_data")
photon_d.Sumw2()
diag.generateWeightedTemplate(photon_d,one,"mvamet",phoX,Workspace.data("photon_data"))
photon_b =   photon_d.Clone(); photon_b.SetName("photon_bkg")
for b in range(photon_b.GetNbinsX()): photon_b.SetBinContent(b+1,0)
diag.generateWeightedTemplate(photon_b,one,"mvamet",ZX,Workspace.data("photon_gjet_backgrounds"))

#photon_b.Scale(0.03)

zmm_d = base.Clone(); zmm_d.SetName("zmm_data")
zmm_d.Sumw2()
diag.generateWeightedTemplate(zmm_d,one,"mvamet",ZX,Workspace.data("dimuon_data"))
zmm_b = base.Clone(); zmm_b.SetName("zmm_bkg")
diag.generateWeightedTemplate(zmm_b,one,"mvamet",ZX,Workspace.data("dimuon_all_background"))

# Add 1% muoneff/pho eff uncerts to datapoints
# Add 1% also for photon backgrounds
for b in range(photon_d.GetNbinsX()):
  pi = photon_d.GetBinContent(b+1);
  zi = zmm_d.GetBinContent(b+1);
  photon_d.SetBinError(b+1, ( (photon_d.GetBinError(b+1))**2 + (pi*0.01)**2 + (pi*0.01)**2 )**0.5)
  zmm_d.SetBinError(b+1, ( (zmm_d.GetBinError(b+1))**2 + (zi*0.01)**2 )**0.5)

# Add the FP also (I think its done on the Z) ?


#photon_d.Add(photon_b,-1)
#zmm_d.Add(zmm_b,-1)

# Photon to Z ratio in data -> Easy !
zmm_d.Divide(photon_d)
zmm_d.SetLineColor(1)
zmm_d.SetLineWidth(3)

# Now we do the same in MC BUT we have to correct the photon peice
diag.generateWeightedDataset("photon_gjet_nlo"		,nlo_pho,"weight","genVpt",Workspace,"photon_gjet")
diag.generateWeightedDataset("dimuon_zll_nlo"           ,nlo_zjt,"weight","genVpt",Workspace,"dimuon_zll")
diag.generateWeightedDataset("dimuon_zll_nlo_ewk"     	,nlo_ewkDn,"weight","genVpt",Workspace,"dimuon_zll_nlo")  # Down and Up are actually reversed!
diag.generateWeightedDataset("dimuon_zll_nlo_ewk2"      ,nlo_ewkDn,"weight","genVpt",Workspace,"dimuon_zll_nlo_ewk")  # this says, apply twice!!

# Correction QCD 
photon_mc = base.Clone(); photon_mc.SetName("photon_mc")
diag.generateWeightedTemplate(photon_mc,one,"genVpt",phoX,Workspace.data("photon_gjet_nlo"))

photon_mc_lo = base.Clone(); photon_mc_lo.SetName("photon_mc_RAW")
diag.generateWeightedTemplate(photon_mc_lo,one,"genVpt",phoX,Workspace.data("photon_gjet"))

zmm_mc_lo = base.Clone(); zmm_mc_lo.SetName("zmm_mc_RAW")
diag.generateWeightedTemplate(zmm_mc_lo,one,"genVpt",ZX,Workspace.data("dimuon_zll"))

zmm_mc = base.Clone(); zmm_mc.SetName("zmm_mc")
diag.generateWeightedTemplate(zmm_mc,one,"genVpt",ZX,Workspace.data("dimuon_zll_nlo_ewk")) #    - Nominal 

zmm_mc_e_u = base.Clone(); zmm_mc_e_u.SetName("zmm_mc_e_u")
diag.generateWeightedTemplate(zmm_mc_e_u,one,"genVpt",ZX,Workspace.data("dimuon_zll_nlo_ewk2"))	  # EWK U 
zmm_mc_e_d = base.Clone(); zmm_mc_e_d.SetName("zmm_mc_e_d")
diag.generateWeightedTemplate(zmm_mc_e_d,one,"genVpt",ZX,Workspace.data("dimuon_zll_nlo")) # EWK D


# we also make QCD mr, mf scale + pdf uncertainties 
diag.generateWeightedDataset("dimuon_zll_EWK_only"     	,nlo_ewkDn,"weight","genVpt",Workspace,"dimuon_zll")

photon_mc_mrup = base.Clone(); photon_mc_mrup.SetName("photon_mc_mrup")
photon_mc_mrdn = base.Clone(); photon_mc_mrdn.SetName("photon_mc_mrdn")
photon_mc_mfup = base.Clone(); photon_mc_mfup.SetName("photon_mc_mfup")
photon_mc_mfdn = base.Clone(); photon_mc_mfdn.SetName("photon_mc_mfdn")
diag.generateWeightedTemplate(photon_mc_mrup,nlo_pho_mrUp,"genVpt",phoX,Workspace.data("photon_gjet"))  
diag.generateWeightedTemplate(photon_mc_mrdn,nlo_pho_mrDown,"genVpt",phoX,Workspace.data("photon_gjet")) 
diag.generateWeightedTemplate(photon_mc_mfup,nlo_pho_mfUp,"genVpt",phoX,Workspace.data("photon_gjet")) 
diag.generateWeightedTemplate(photon_mc_mfdn,nlo_pho_mfDown,"genVpt",phoX,Workspace.data("photon_gjet")) 

photon_mc_mrup2 = base.Clone(); photon_mc_mrup2.SetName("photon_mc_mrup2")
photon_mc_mrdn2 = base.Clone(); photon_mc_mrdn2.SetName("photon_mc_mrdn2")
photon_mc_mfup2 = base.Clone(); photon_mc_mfup2.SetName("photon_mc_mfup2")
photon_mc_mfdn2 = base.Clone(); photon_mc_mfdn2.SetName("photon_mc_mfdn2")
diag.generateWeightedTemplate(photon_mc_mrup2,nlo_pho_mrUp2,"genVpt",phoX,Workspace.data("photon_gjet"))  
diag.generateWeightedTemplate(photon_mc_mrdn2,nlo_pho_mrDown2,"genVpt",phoX,Workspace.data("photon_gjet")) 
diag.generateWeightedTemplate(photon_mc_mfup2,nlo_pho_mfUp2,"genVpt",phoX,Workspace.data("photon_gjet")) 
diag.generateWeightedTemplate(photon_mc_mfdn2,nlo_pho_mfDown2,"genVpt",phoX,Workspace.data("photon_gjet")) 

zmm_mc_mrup = base.Clone(); zmm_mc_mrup.SetName("zmm_mc_mrup")
zmm_mc_mrdn = base.Clone(); zmm_mc_mrdn.SetName("zmm_mc_mrdn")
zmm_mc_mfup = base.Clone(); zmm_mc_mfup.SetName("zmm_mc_mfup")
zmm_mc_mfdn = base.Clone(); zmm_mc_mfdn.SetName("zmm_mc_mfdn")
zmm_mc_mrup2 = base.Clone(); zmm_mc_mrup2.SetName("zmm_mc_mrup2")
zmm_mc_mrdn2 = base.Clone(); zmm_mc_mrdn2.SetName("zmm_mc_mrdn2")
zmm_mc_mfup2 = base.Clone(); zmm_mc_mfup2.SetName("zmm_mc_mfup2")
zmm_mc_mfdn2 = base.Clone(); zmm_mc_mfdn2.SetName("zmm_mc_mfdn2")
zmm_mc_pdfup = base.Clone(); zmm_mc_pdfup.SetName("zmm_mc_pdfUP")
zmm_mc_pdfdn = base.Clone(); zmm_mc_pdfdn.SetName("zmm_mc_pdfDN")

diag.generateWeightedTemplate(zmm_mc_mrup,nlo_zjt_mrUp,"genVpt",ZX,Workspace.data("dimuon_zll_EWK_only")) 
diag.generateWeightedTemplate(zmm_mc_mrdn,nlo_zjt_mrDown,"genVpt",ZX,Workspace.data("dimuon_zll_EWK_only")) 
diag.generateWeightedTemplate(zmm_mc_mfup,nlo_zjt_mfUp  ,"genVpt",ZX,Workspace.data("dimuon_zll_EWK_only")) 
diag.generateWeightedTemplate(zmm_mc_mfdn,nlo_zjt_mfDown,"genVpt",ZX,Workspace.data("dimuon_zll_EWK_only")) 
diag.generateWeightedTemplate(zmm_mc_mrup2,nlo_zjt_mrUp2,"genVpt",ZX,Workspace.data("dimuon_zll_EWK_only")) 
diag.generateWeightedTemplate(zmm_mc_mrdn2,nlo_zjt_mrDown2,"genVpt",ZX,Workspace.data("dimuon_zll_EWK_only")) 
diag.generateWeightedTemplate(zmm_mc_mfup2,nlo_zjt_mfUp2  ,"genVpt",ZX,Workspace.data("dimuon_zll_EWK_only")) 
diag.generateWeightedTemplate(zmm_mc_mfdn2,nlo_zjt_mfDown2,"genVpt",ZX,Workspace.data("dimuon_zll_EWK_only")) 
#diag.generateWeightedTemplate(zmm_mc_pdfup,nlo_zjt_pdfUp  ,"genVpt",ZX,Workspace.data("dimuon_zll_EWK_only")) 
#diag.generateWeightedTemplate(zmm_mc_pdfdn,nlo_zjt_pdfDown,"genVpt",ZX,Workspace.data("dimuon_zll_EWK_only")) 
diag.generateWeightedTemplate(zmm_mc_pdfup,nlo_zjt_pdfUp  ,"genVpt",ZX,Workspace.data("dimuon_zll_EWK_only")) 
diag.generateWeightedTemplate(zmm_mc_pdfdn,nlo_zjt_pdfDown,"genVpt",ZX,Workspace.data("dimuon_zll_EWK_only")) 
                                                                                                 
zmm_mc_mrup.Divide(photon_mc_mrup)
zmm_mc_mrdn.Divide(photon_mc_mrdn)
zmm_mc_mfup.Divide(photon_mc_mfup)
zmm_mc_mfdn.Divide(photon_mc_mfdn)
zmm_mc_mrup2.Divide(photon_mc_mrup2)
zmm_mc_mrdn2.Divide(photon_mc_mrdn2)
zmm_mc_mfup2.Divide(photon_mc_mfup2)
zmm_mc_mfdn2.Divide(photon_mc_mfdn2)
zmm_mc_pdfup.Divide(photon_mc)
zmm_mc_pdfdn.Divide(photon_mc)


# Footprint correction
Zvv_FPDown = base.Clone(); Zvv_FPDown.SetName("photon_weights_fp_Down")
diag.generateWeightedTemplate(Zvv_FPDown,nlo_FPDown,"genVpt",ZX,Workspace.data("dimuon_zll"))

Zvv_FPUp   = base.Clone(); Zvv_FPUp   .SetName("photon_weights_fp_Up")
diag.generateWeightedTemplate(Zvv_FPUp,nlo_FPUp,"genVpt",ZX,Workspace.data("dimuon_zll"))

Zvv_FPUp.Divide(photon_mc)
Zvv_FPDown.Divide(photon_mc)
#########################################################################################################

zmm_mc_lo.Divide(photon_mc_lo)
zmm_mc.Divide(photon_mc)

zmm_mc_e_u.Divide(photon_mc)
zmm_mc_e_d.Divide(photon_mc)

zmm_mc.SetLineWidth(3)
zmm_mc_lo.SetLineWidth(3)
zmm_mc_e_u.SetLineWidth(3)
zmm_mc_e_d.SetLineWidth(3)

errs = zmm_mc.Clone()

for b in range(zmm_mc.GetNbinsX()):

	cv = zmm_mc.GetBinContent(b+1)
        diffu = abs(zmm_mc_e_u.GetBinContent(b+1)- cv )
        diffd = abs(zmm_mc_e_d.GetBinContent(b+1)- cv)

	errT = (max(diffu,diffd))**2

	# add in quad from the others 
	diffmc_mr_u = zmm_mc_mrup.GetBinContent(b+1) - cv
	diffmc_mr_d = zmm_mc_mrdn.GetBinContent(b+1) - cv
	diffmc_mf_u = zmm_mc_mfup.GetBinContent(b+1) - cv
	diffmc_mf_d = zmm_mc_mfdn.GetBinContent(b+1) - cv

	diffmc_mr_u2 = zmm_mc_mrup2.GetBinContent(b+1) - cv
	diffmc_mr_d2 = zmm_mc_mrdn2.GetBinContent(b+1) - cv
	diffmc_mf_u2 = zmm_mc_mfup2.GetBinContent(b+1) - cv
	diffmc_mf_d2 = zmm_mc_mfdn2.GetBinContent(b+1) - cv

	diffmc_pdf_u = zmm_mc_pdfup.GetBinContent(b+1) - cv
	diffmc_pdf_d = zmm_mc_pdfdn.GetBinContent(b+1) - cv

	derr_mr = 0.5*(abs(diffmc_mr_u)+abs(diffmc_mr_d))
	derr_mf = 0.5*(abs(diffmc_mf_u)+abs(diffmc_mf_d))
	derr_mr2 = 0.5*(abs(diffmc_mr_u2)+abs(diffmc_mr_d2))
	derr_mf2 = 0.5*(abs(diffmc_mf_u2)+abs(diffmc_mf_d2))
	derr_pdf = 0.5*(abs(diffmc_pdf_u)+abs(diffmc_pdf_d))

	
	errT+=derr_mr**2
	errT+=derr_mf**2
	errT+=derr_mr2**2
	errT+=derr_mf2**2
	errT+=derr_pdf**2

	errs.SetBinError(b+1,errT**0.5)


zmm_mc_lo.SetLineColor(r.kOrange)
zmm_mc.SetLineColor(4)
errs.SetFillColor(r.kGray)

zmm_d.SetMarkerSize(1.2)
zmm_d.SetMarkerStyle(20)
zmm_d.GetXaxis().SetName("fake E_{T}^{miss}")
cv = r.TCanvas()

zmm_d.Draw("pel")
errs.Draw("sameE2")
zmm_mc.Draw("samehist")
zmm_mc_lo.Draw("samehist")
zmm_d.Draw("pelsame")

leg = r.TLegend(0.6,0.6,0.89,0.89)
leg.SetFillColor(0)
leg.SetTextFont(42)
leg.AddEntry(zmm_d,"Data #pm (stat + exp syst)","pel")
leg.AddEntry(zmm_mc_lo,"Madgraph Raw","L")
leg.AddEntry(zmm_mc,"NLO corrected, Theory #pm 1#sigma","LF")
leg.Draw()
cv.SaveAs("Closure.root")
#raw_input()

