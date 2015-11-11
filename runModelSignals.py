#########################################################################################
# Setup the basics ----> USER DEFINED SECTION HERE ------------------------------------//
fOutName = "signals.root"  # --> Output file
fName    = "mono-x-signals.root"  # --> input file (all the signals use here 
categories = ["monojet"] # --> Should be labeled as in original config 
#--------------------------------------------------------------------------------------//
#########################################################################################

# Leave the following alone!
# Headers 
#from combineControlRegions import *
from pullPlot import pullPlot
from counting_experiment import *
from convert import * 

import ROOT as r 
r.gROOT.SetBatch(1)

_fOut 	   = r.TFile(fOutName,"RECREATE") 
_f 	   = r.TFile.Open(fName) 
out_ws 	   = r.RooWorkspace("combinedws") 
out_ws._import = getattr(out_ws,"import")

convertToCombineWorkspace(out_ws,_f,categories,[],[])  # use the same converter tool, but no need for fancy stuff
_fOut.WriteTObject(out_ws)

print "Produced Signals Models in --> ", _fOut.GetName()
