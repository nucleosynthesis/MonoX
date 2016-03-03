#! /usr/bin/env python
import commands,sys,os,subprocess,ROOT,numpy
from array import array

eos='/afs/cern.ch/project/eos/installation/cms/bin/eos.select'
basedir ='/afs/cern.ch/user/p/pharris/pharris/public/bacon/prod/CMSSW_7_4_12_patch1/src/MonoX/ModelScan'
#eosbasedir ='/store/user/rgerosa/MONOJET_ANALYSIS/GenTreeForInterpolation/'
eosbasedir ='/store/cmst3/user/pharris/monojet13/reweight'
mjcut   ='(v_pt > 0 )'
monojet     ='2.26'#*(jpt_1 > 100)*(fjm < 60 || fjm > 112 || fjpt < 250)'
boosted     ='2.26*(fjm > 60 && fjm < 112 && fjpt > 250 && fjt2t1 < 0.6)*'+mjcut
monojetReco ='1.'#*(genAK4JetPt > 100)*(genAK8JetMass < 60 || genAK8JetMass > 112 || genAK8JetPt < 250)'
boostedReco ='1.*(genAK8JetMass > 60 && genAK8JetMass < 112 && genAK8JetPt > 250 && genAK8JetTau2Tau1 < 0.6)'

mvrbins = [250,300,350,400,500,600,1000]
mvgbins = [100.,150.,200.,250,300,350,400,500,600,1000]
mvrcut  = "pfMetPt>250 && pfMetPt < 10000 && id==2"
mjrbins = [200., 230., 260.0, 290.0, 320.0, 350.0, 390.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1250.0]
mjgbins = [100.,150.,180.,200., 230., 260.0, 290.0, 320.0, 350.0, 390.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1250.0]
mjrcut  = "pfMetPt>200 && pfMetPt < 10000 && id==1"

#boosted ='2.11*(fjmtrim > 60 && fjmtrim < 112 && fjt2t1 < 0.5 && fjpt > 250)*'+mjcut
#resolved='19.7*mcweight*(60 < mjj && mjj < 112 && ptjj > 160 && dm_pt > 250 && !(fjmtrim > 60 && fjmtrim < 112 && fjt2t1 < 0.5 && fjpt > 250) && jpt_1 > 30 && jpt_2 > 30)'

