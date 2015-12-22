#!/bin/bash
combineCards.py dmcr=monojet_hinv_dimuon_control.txt pcr=monojet_hinv_photon_control.txt smcr=monojet_hinv_singlemuon_control.txt sr=monojet_sr.txt decr=monojet_hinv_dielectron_control.txt secr=monojet_hinv_singleelectron_control.txt > monojet_combined.txt
combineCards.py dmcr=monojet_hinv_dimuon_control.txt pcr=monojet_hinv_photon_control.txt smcr=monojet_hinv_singlemuon_control.txt decr=monojet_hinv_dielectron_control.txt secr=monojet_hinv_singleelectron_control.txt > monojet_combined_cronly.txt
text2workspace.py monojet_combined_cronly.txt --X-allow-no-signal
combineCards.py dmcr=monojet_hinv_dimuon_control.txt pcr=monojet_hinv_photon_control.txt smcr=monojet_hinv_singlemuon_control.txt sr=monojet_sr.txt > monojet_combined_noele.txt
