# sptmsfmri

## Referenced Work
This repository holds the preprocessing and QC code for the publication **Concurrent single-pulse (sp) TMS/fMRI to reveal the causal connectome in healthy and patient populations** Find the preprint here: [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.09.25.614833v1)

## Contributers
Cameron C Glick, Niharika Gajawelli, Yinming Sun, Faizan Badami, Manish Saggar, Amit Etkin

## Abstract
Neuroimaging and cognitive neuroscience studies have identified neural circuits linked to anxiety, mood, and trauma-related symptoms and focused on their interaction with the medial prefrontal default mode circuitry. Despite these advances, developing new neuromodulatory treatments based on neurocircuitry remains challenging. It remains unclear which nodes within and controlling these circuits are affected and how their impairment is connected to psychiatric symptoms. Concurrent single-pulse (sp) TMS/fMRI offers a promising approach to probing and mapping the integrity of these circuits. In this study, we present concurrent sp-TMS/fMRI data along with structural MRI scans from 152 participants, including both healthy and depressed individuals. The sp-TMS was administered to 11 different cortical sites, providing a dataset that allows researchers to investigate how brain circuits are modulated by spTMS.

## Overview
- minimally preproccess data using mriqc: [mriqc_individual_ng.sh](https://github.com/braindynamicslab/sptmsfmri/blob/main/mriqc_individual_ng.sh), [mri_qc_group_ng.sh](https://github.com/braindynamicslab/sptmsfmri/blob/main/mriqc_group_ng.sh)
- generate plots [generate_plots_cg.py](https://github.com/braindynamicslab/sptmsfmri/blob/main/generate_plots_cg.py)
- compute stats [stat_test_ms.m](https://github.com/braindynamicslab/sptmsfmri/blob/main/stat_test_ms.m)
- data for generating plots [data](https://github.com/braindynamicslab/sptmsfmri/tree/main/data)

## Having Issues?

Email Cameron Glick: camglick@stanford.edu
