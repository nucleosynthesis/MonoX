#!/bin/bash 
python makePlot.py mlfit.root plot_config                -c monojet -x "E_{T}^{miss} (GeV)" -b -o monojet -t "Signal Region" -g
python makePlot.py mlfit.root plot_config_dimuon         -c monojet -x "|U| (GeV)" -b -o monojet -t "Di-muon Control Region"	
python makePlot.py mlfit.root plot_config_singlemuon     -c monojet -x "|U| (GeV)" -b -o monojet -t "Single-muon Control Region"		
python makePlot.py mlfit.root plot_config_photon         -c monojet -x "|U| (GeV)" -b -o monojet -t "Photon Control Region"              
python makePlot.py mlfit.root plot_config_dielectron     -c monojet -x "|U| (GeV)" -b -o monojet -t "Di-electron Control Region"    	
python makePlot.py mlfit.root plot_config_singleelectron -c monojet -x "|U| (GeV)" -b -o monojet -t "Single-electron Control Region"

python makePlot.py mlfit.root plot_config                -c monojet -x "E_{T}^{miss} (GeV)" -b -o monojet_prefit -t "Signal Region" -g      -d shapes_prefit
python makePlot.py mlfit.root plot_config_dimuon         -c monojet -x "|U| (GeV)" -b -o monojet_prefit -t "Di-muon Control Region"	     -d shapes_prefit
python makePlot.py mlfit.root plot_config_singlemuon     -c monojet -x "|U| (GeV)" -b -o monojet_prefit -t "Single-muon Control Region"     -d shapes_prefit		
python makePlot.py mlfit.root plot_config_photon         -c monojet -x "|U| (GeV)" -b -o monojet_prefit -t "Photon Control Region"          -d shapes_prefit         
python makePlot.py mlfit.root plot_config_dielectron     -c monojet -x "|U| (GeV)" -b -o monojet_prefit -t "Di-electron Control Region"     -d shapes_prefit	
python makePlot.py mlfit.root plot_config_singleelectron -c monojet -x "|U| (GeV)" -b -o monojet_prefit -t "Single-electron Control Region" -d shapes_prefit

#python makePlot.py mlfit.root plot_config -c boosted -x "E_{T}^{miss} (GeV)" -b -o boosted
#python makePlot.py mlfit.root plot_config_dimuon -c boosted -x "E_{T}^{miss} (GeV)" -b -o boosted
#python makePlot.py mlfit.root plot_config_singlemuon -c boosted -x "E_{T}^{miss} (GeV)" -b -o boosted
#python makePlot.py mlfit.root plot_config_photon -c boosted -x "E_{T}^{miss} (GeV)" -b -o boosted

#python makePlot.py mlfit.root plot_config -c resolved -x "E_{T}^{miss} (GeV)" -b -o resolved
#python makePlot.py mlfit.root plot_config_dimuon -c resolved -x "E_{T}^{miss} (GeV)" -b -o resolved
#python makePlot.py mlfit.root plot_config_singlemuon -c resolved -x "E_{T}^{miss} (GeV)" -b -o resolved
#python makePlot.py mlfit.root plot_config_photon -c resolved -x "E_{T}^{miss} (GeV)" -b -o resolved
