#! /usr/bin/env python
import commands,sys,os,subprocess,ROOT,numpy
from array import array

eos='/afs/cern.ch/project/eos/installation/cms/bin/eos.select'
basedir ='/afs/cern.ch/user/p/pharris/pharris/public/bacon/prod/CMSSW_5_3_22_patch1/src/MonoX/ModelScan/ntuples'
eosbasedir ='/store/cmst3/user/pharris/monojet13/'
mjcut   ='(v_pt > 0 )'
monojet ='2.11'
#boosted ='2.11*(fjmtrim > 60 && fjmtrim < 112 && fjt2t1 < 0.5 && fjpt > 250)*'+mjcut
boosted ='2.11*(fjm > 60 && fjm < 112 && fjpt > 250)*'+mjcut
#resolved='19.7*mcweight*(60 < mjj && mjj < 112 && ptjj > 160 && dm_pt > 250 && !(fjmtrim > 60 && fjmtrim < 112 && fjt2t1 < 0.5 && fjpt > 250) && jpt_1 > 30 && jpt_2 > 30)'

