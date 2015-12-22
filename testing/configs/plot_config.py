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

key_order = ["Z(#rightarrow ll)+jets","QCD","Dibosons","top","W(#rightarrow l#nu)+jets","Z(#rightarrow #nu#nu)+jets"]

backgrounds = { 
		"top":			  	[["sr/top"],		r.kRed+1,   0]
		,"Dibosons":		  	[["sr/dibosons"],	r.kGray,    0]
		,"Z(#rightarrow ll)+jets":	[["sr/zll"],		r.kGreen+3, 0]
		,"W(#rightarrow l#nu)+jets":    [["sr/wjets"], 		r.kAzure-3, 0]
		,"Z(#rightarrow #nu#nu)+jets":  [["sr/zjets"],		r.kBlue-9,   0]
		,"QCD":	  		        [["sr/qcd"],		r.kRed+2,   0]

	      }
# take the background from some histogram, not the stack!, useful for histograms 
total =  "sr/total_background"
dataname  = "mono-x.root:category_$CAT/signal_data"
