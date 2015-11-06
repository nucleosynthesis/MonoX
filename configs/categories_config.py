# Configuration for a simple monojet topology. Use this as a template for your own Run-2 mono-X analysis
# First provide ouput file name in out_file_name field 
out_file_name = 'mono-x.root'

# can define any thing useful here which may be common to several categories, eg binning in MET 
#bins = range(200,1200,200)
bins = [200,250,300,350,400,500,600,1000]
# will expect samples with sample_sys_Up/Down but will skip if not found 
systematics=["Met","FP"]
# Define each of the categories in a dictionary of the following form .. 
#	'name' : the category name 
#	'in_file_name' : input ntuple file for this category 
#	'cutstring': add simple cutrstring, applicable to ALL regions in this category (eg mvamet > 200)
#	'varstring': the main variable to be fit in this category (eg mvamet), must be named as the branch in the ntuples
#	'weightname': name of the weight variable 
#	'bins': binning given as a python list
#	'additionalvars': list additional variables to be histogrammed by the first stage, give as a list of lists, each list element 
#			  as ['variablename',nbins,min,max]
#	'pdfmodel': integer --> N/A  redudant for now unless we move back to parameteric fitting estimates
# 	'samples' : define tree->region/process map given as a dictionary with each entry as follows 
#		TreeName : ['region','process',isMC,isSignal] --> Note isSignal means DM/Higgs etc for signal region but Z-jets/W-jets for the di/single-muon regions !!!

#  OPTIONAL --> 'extra_cuts': additional cuts maybe specific to this control region (eg ptphoton cuts) if this key is missing, the code will not complain   
 
monojet_category = {
	    'name':"monojet"
	   #,'in_file_name':"/afs/cern.ch/user/p/pharris/pharris/public/bacon/prod/CMSSW_7_4_12_patch1/src/MonoX/../BaconAnalyzer/MJSelection/skim/monojet-combo-electron.root"  # Without recoil corrections
	   ,'in_file_name':"/afs/cern.ch/user/p/pharris/pharris/public/bacon/prod/CMSSW_7_4_12_patch1/src/MonoX/monojet-combo-electron.root_recoil"
	   ,"cutstring":"mvamet>200 && mvamet<1000"
	   ,"varstring":["mvamet",200,1000]
	   ,"weightname":"weight"
	   ,"bins":bins[:]
	   #,"bins":[200.0 , 210.0 , 220.0 , 230.0 , 240.0 , 250.0 , 260.0 , 270.0 , 280.0 , 290.0 , 300.0 , 310.0 , 320.0 , 330.0,340,360,380,420,510,1000]
  	   ,"additionalvars":[['jet1pt',25,150,1000]]
	   ,"pdfmodel":0
	   #,"extra_cuts":[["singleelectron","rmet>40"],["photon","ptpho>200"]]
	   ,"extra_cuts":[["singleelectron","rmet>40"]]
	   ,"samples":
	   	{  
		  # Signal Region
		   "Znunu_signal"  	           :['signal','zjets',1,0]
                   ,"Zll_signal"	           :['signal','zll',1,0]
 		  ,"Wjets_signal"  	           :['signal','wjets',1,0]
		  ,"WW_signal"  	           :['signal','dibosons',1,0]
		  ,"WZ_signal"  	           :['signal','dibosons',1,0]
		  ,"ZZ_signal"  	           :['signal','dibosons',1,0]
		  ,"ttbar_signal"   	           :['signal','top',1,0]
		  ,"SingleTop_signal"              :['signal','top',1,0]
		  ,"QCD_signal"		   	   :['signal','qcd',1,0]
		  ,"data_signal"	           :['signal','data',0,0]

		  # some signals 
		  ,"P_200_150_signal"		   :['signal','pseudoscalar_200150',1,1]
		  ,"P_200_100_signal"		   :['signal','pseudoscalar_200100',1,1]
		  ,"P_200_10_signal"		   :['signal','pseudoscalar_200010',1,1]
		  ,"P_200_1_signal"		   :['signal','pseudoscalar_200001',1,1]

		  #,"A_2000_150_g025_signal"		   :['signal','axialvector_2000150',1,1]
		  #,"A_2000_100_g025_signal"		   :['signal','axialvector_2000100',1,1]
		  #,"A_2000_10_g025_signal"		   :['signal','axialvector_2000010',1,1]
		  ,"A_2000_1_g025_signal"		   :['signal','axialvector_2000001',1,1]

		  # Di muon-Control
		  ,"Zll_di_muon_control"	   :['dimuon','zll',1,1]
		  ,"Wjets_di_muon_control"  	   :['dimuon','wjets',1,0]
		  ,"WW_di_muon_control"  	   :['dimuon','dibosons',1,0]
		  ,"WZ_di_muon_control"  	   :['dimuon','dibosons',1,0]
		  ,"ZZ_di_muon_control"  	   :['dimuon','dibosons',1,0]
		  ,"ttbar_di_muon_control"         :['dimuon','top',1,0]
		  ,"SingleTop_di_muon_control"     :['dimuon','top',1,0]
		  ,"data_di_muon_control"	   :['dimuon','data',0,0]

		  # Single muon control
		  ,"Zll_single_muon_control"	   :['singlemuon','zll',1,0]
		  ,"Wjets_single_muon_control"     :['singlemuon','wjets',1,1]
		  ,"ZZ_single_muon_control"        :['singlemuon','dibosons',1,0]
		  ,"WW_single_muon_control"        :['singlemuon','dibosons',1,0]
		  ,"WZ_single_muon_control"        :['singlemuon','dibosons',1,0]
		  ,"SingleTop_single_muon_control" :['singlemuon','top',1,0]
		  ,"ttbar_single_muon_control"     :['singlemuon','top',1,0]
		  ,"QCD_single_muon_control"	   :['singlemuon','qcd',1,0]
		  ,"data_single_muon_control"	   :['singlemuon','data',0,0]

		  # Photon control region
		  ,"data_photon_control"	   :['photon','data',0,0]
		  ,"Photon_photon_control"	   :['photon','gjet',1,1]
                  ,"QCD_photon_control"	   	   :['photon','qcd',1,0]

		  # Di electron-Control
		  ,"Zll_di_electron_control"	   :['dielectron','zll',1,1]
		  ,"Wjets_di_electron_control"     :['dielectron','wjets',1,0]
		  ,"WW_di_electron_control"  	   :['dielectron','dibosons',1,0]
		  ,"WZ_di_electron_control"  	   :['dielectron','dibosons',1,0]
		  ,"ZZ_di_electron_control"  	   :['dielectron','dibosons',1,0]
		  ,"ttbar_di_electron_control"      :['dielectron','top',1,0]
		  ,"SingleTop_di_electron_control"  :['dielectron','top',1,0]
		  ,"data_di_electron_control"	   :['dielectron','data',0,0]

		  # Single electron control
		  ,"Zll_single_electron_control"       :['singleelectron','zll',1,0]
		  ,"Wjets_single_electron_control"     :['singleelectron','wjets',1,1]
		  ,"ZZ_single_electron_control"        :['singleelectron','dibosons',1,0]
		  ,"WW_single_electron_control"        :['singleelectron','dibosons',1,0]
		  ,"WZ_single_electron_control"        :['singleelectron','dibosons',1,0]
		  ,"SingleTop_single_electron_control" :['singleelectron','top',1,0]
		  ,"ttbar_single_electron_control"     :['singleelectron','top',1,0]
		  ,"QCD_single_electron_control"       :['singleelectron','qcd',1,0]
		  ,"data_single_electron_control"      :['singleelectron','data',0,0]
	   	},
}
categories = [monojet_category]
