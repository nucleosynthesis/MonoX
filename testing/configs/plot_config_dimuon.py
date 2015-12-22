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

key_order = ["Dibosons","top","Z(#rightarrow #mu#mu)+jets"]

backgrounds = { 
		"top":			  	[["dmcr/top"],		r.kRed+1,   0]
		,"Dibosons":		  	[["dmcr/dibosons"],		r.kGray,    0]
		,"Z(#rightarrow #mu#mu)+jets":	[["dmcr/zmm"],		r.kGreen+3, 0]

	      }

dataname  = "mono-x.root:category_$CAT/dimuon_data"
total =  "dmcr/total_background"
