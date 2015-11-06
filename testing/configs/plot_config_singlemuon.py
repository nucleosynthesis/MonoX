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

key_order = ["Z(#rightarrow ll)+jets","QCD","Dibosons","top","W(#rightarrow #mu#nu)+jets"]

backgrounds = { 
		"top":			  	[["smcr/top"],		r.kRed+1,   0]
		,"Dibosons":		  	[["smcr/dibosons"],	r.kGray,    0]
		,"Z(#rightarrow ll)+jets":	[["smcr/zll"],		r.kGreen+3, 0]
		,"W(#rightarrow #mu#nu)+jets":  [["smcr/wlm"], 		r.kAzure-3, 0]
		,"QCD":	  		        [["smcr/qcd"],		r.kRed+2,   0]

	      }

dataname  = "mono-x.root:category_$CAT/singlemuon_data"
total =  "smcr/total_background"
