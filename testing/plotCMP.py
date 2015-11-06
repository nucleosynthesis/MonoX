import ROOT
ROOT.gStyle.SetOptStat(0)

fre = ROOT.TFile.Open("reg.root")
fwe = ROOT.TFile.Open("weird.root")

we = fwe.Get("weird")
re = fre.Get("reg")

re.SetFillColor(ROOT.kBlue-10)
re.GetXaxis().SetTitle("E_{T}^{miss} (GeV)")
re.Draw("E2")
we.Draw("E2same")
raw_input()
