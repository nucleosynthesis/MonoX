import ROOT as r
directory = "shapes_fit_b"

signals = {
 	   #"Higgs #rightarrow inv, m_{H}=125 GeV":[
	   #	["mono-x-vtagged.root:category_$CAT/signal_ggH"
	#	,"mono-x-vtagged.root:category_$CAT/signal_vbf"
        #        ,"mono-x-vtagged.root:category_$CAT/signal_wh"
	
         #       ,"mono-x-vtagged.root:category_$CAT/signal_zh"
	#	] ,r.kOrange	,0],
 	   #"#splitline{Scalar Mediator}{m_{MED}=925 GeV, m_{DM}=10 GeV}":[
	   #	["card_$CAT.root:signal_ggH"
	   
	   #] ,r.kAzure+10	,0,1000]
	   }

key_order = ["Fakes","#gamma+jet"]

backgrounds = { 
		"#gamma+jet":		  	[["pcr/gjet"],		r.kGreen+1,    0]
		,"Fakes":	  		[["pcr/non_prompt"],		r.kRed+2,   0]

	      }

dataname  = "mono-x.root:category_$CAT/photon_data"
total =  "pcr/total_background"
