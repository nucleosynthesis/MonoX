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

key_order = ["Z(#rightarrow ll)+jets","Dibosons","QCD","top","W(#rightarrow e#nu)+jets"]
#key_order = ["Z(#rightarrow ll)+jets","Dibosons","top","W(#rightarrow e#nu)+jets"]

backgrounds = { 
		"top":			  	[["secr/top"],		r.kRed+1,   0]
		,"Dibosons":		  	[["secr/dibosons"],	r.kGray,    0]
		,"Z(#rightarrow ll)+jets":	[["secr/zll"],		r.kGreen+3, 0]
		,"W(#rightarrow e#nu)+jets":    [["secr/wle"], 		r.kAzure-3, 0]
		,"QCD":	  		        [["secr/qcd"],		r.kRed+2,   0]

	      }

dataname  = "mono-x.root:category_$CAT/singleelectron_data"
total =  "secr/total_background"
