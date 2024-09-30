#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9, 2024
@author: camglick@stanford.edu
purpose: To generate plots for sptms/fmri paper
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Specify Subjects Included
subs_included =(1001,1003,1009,1015,1016,1019,1021,1022,1023,1024,1026,1027,1028,
                1029,1032,1035,1036,1037,1038,1039,1040,1043,1047,1049,1050,1052,
                1053,1055,1056,1057,1061,1062,1064,1065,1066,1068,1073,1075,1097,
                1098,1099,1101,1102,1105,1107,1108,2001,2002,2010,2022,2026,2040,
                2043,2044,2047,2048,2053,2062,2064,2066,2069,2070,2074,2075,2076,
                2079,2083,2090,2093,2096,2102,2103,2104,2105,2108,3006,3019,3020,
                3022,3023,3026,3029,3031,3037,3045,3046,3051,3053,3055,3056,3058,
                3065,3072,3074,3077,3079,3083,3084,3086,3088,3089,3090,3091,3093,
                3094,3095,3096,3097,3098,3099,3101,3102,3103,3107,3108,3109,3115,
                3116,4025,4039,4042,4044,4048,4049,4050,4052,4056,4068,4072,4077,
                4088,4089,4096,4105,4113,4117,4120,4121,4127,4135,4136,4147,4161,
                4166,4167,4175,4177,4178,4182,4199,4203,4206)

# Load Data                                                                                                                                                                            #
group_bold = pd.read_csv("path to tsv", sep = '\t').iloc[:,1:]
group_bold_unaltered = group_bold.copy()

group_bold_unaltered['group'] = pd.read_csv("path to sptmsfmri-bold.tsv", sep = '\t').iloc[:,0].str.split("-", expand = True).iloc[:,1].str.split("_", expand = True).iloc[:,0].str.slice(0, -4)
group_bold_unaltered['subject'] = pd.read_csv("path to sptmsfmri-bold.tsv", sep = '\t').iloc[:,0].str.split("-", expand = True).iloc[:,1].str.split("_", expand = True).iloc[:,0].str.slice(-4)
group_bold_unaltered['task'] = pd.read_csv("path to sptmsfmri-bold.tsv", sep = '\t').iloc[:,0].str.split("-", expand = True).iloc[:,3].str.split("_", expand = True).iloc[:,0]
group_bold_unaltered['sub_full_name'] = pd.read_csv("path to sptmsfmri-bold.tsv", sep = '\t').iloc[:,0].str.split("-", expand = True).iloc[:,1].str.split("_", expand = True).iloc[:,0]
group_bold_unaltered = group_bold_unaltered.loc[group_bold_unaltered['subject'].astype(int).isin(subs_included)]
unique_subjs = group_bold_unaltered['subject'].unique()
subs_info = pd.read_excel("path to age_gender_edu.xlsx")
subs_info.index = subs_info["cc_post_intake_id"].astype('str')


#Generate descriptive Tags for data
replace_dict = {"stimLxFpxEEG": "L-FP",
                "stimRxFEFxDAN":"R-FEF",
                "stimRxFpxEEG":"R-FP",
                "stimRxIFJxDAN":"R-IFJ",
                "stimRxIPL":"R-IPL",
                "stimRxM1xAnat":"R-M1",
                "stimRxoPreSMA":"R-preSMA",
                "stimRxSaliencexICA":"R-aMFG",
                "stimRxECNxICA":"R-pMFG",
                "stimLxECNxICA":"L-pMFG",
                "stimLxSaliencexICA":"L-aMFG",
                "Resting":"resting"
                }

group_bold_unaltered = group_bold_unaltered.join(subs_info, on = 'subject', how = 'left' ).replace(replace_dict)

#Get comparisom mriqc data
comparison_bold = pd.read_csv("path to comparison-bold.csv").iloc[:,3:63].drop(['_id.$oid', '_updated.$date', 'bids_meta.EchoTime', 'bids_meta.FlipAngle', 'bids_meta.MagneticFieldStrength', 'bids_meta.ManufacturersModelName', 'bids_meta.RepetitionTime', 'bids_meta.TaskName', 'bids_meta.modality', 'bids_meta.subject_id', 'bids_meta.task_id', 'provenance.md5sum', 'provenance.settings.fd_thres', 'provenance.settings.hmc_fsl', 'provenance.version', 'provenance.software'], axis = 1)                                                                                                                                                             
group_bold_unaltered['compare'] = 'TMS-fMRI'  
comparison_bold['compare'] = 'mriqc'

#Clean Comparison Bold Data
Q1 = comparison_bold.quantile(0.25)
Q3 = comparison_bold.quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - 5 * IQR
upper_bound = Q3 + 5 * IQR

comparison_bold = comparison_bold[~((comparison_bold < lower_bound) | (comparison_bold > upper_bound)).any(axis=1)]

bold_plot = comparison_bold.append(group_bold_unaltered, ignore_index = True).reset_index(drop = True)
bold_plot = bold_plot.replace(np.nan, 'test')

# Define color palettes

group_palette = {'TMS-fMRI': '#92DCE5', 'mriqc': '#7C7C7C'} #{"TIS":"#7C7C7C", "TEHC":"#EB7B00", "NTS": "#92DCE5", "NTHC": "#0062EB"} 

tasks_palette = {"L-FP":"#B26321",
                "R-FEF":"#64A5A5",
                "R-FP":"#1255B8",
                "R-IFJ":"#AD813F",
                "R-IPL":"#21378B",
                "R-M1":"#AAA856",
                "R-preSMA":"#83C86D",
                "R-aMFG":"#3F7CC2",
                "R-pMFG":"#5796A0",
                "L-pMFG": "#751713",
                "L-aMFG": "#8E3B20",
                "resting": "#7C7C7C"
                }

# Reformat data
unique_tasks = group_bold_unaltered['task'].value_counts().reset_index(drop = False).iloc[[0,4,5,7,8,9,10,11,13,14,15,16],:]
unique_tasks_lst = list(unique_tasks['index'])

tasks_numbers = group_bold_unaltered[['task', 'group']].loc[group_bold_unaltered['task'].isin(unique_tasks_lst)].value_counts().reset_index(drop = False)



    

# Make Table with unique Tasks
plt.figure(figsize = (10, 20))
ax = sns.barplot(data = unique_tasks, x = 'task', y = 'index', color = '#7C7C7C', palette=group_palette)
plt.axvline(x=len(group_bold_unaltered['subject'].unique()), color='black', linestyle='--', linewidth = 2)
sns.despine()
ax.set_xlabel("Count", fontsize=30, fontweight='bold')
ax.tick_params(which='major', labelsize=12, length = 3, width = 2)
ax.set_ylabel("Task", fontsize=30, fontweight='bold')
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
plt.rcParams['figure.dpi'] = 300


# Make plot comparing TSR and meanFD between groups
group_wise_comparison_fd = group_bold_unaltered[group_bold_unaltered['task'].isin(unique_tasks_lst)].melt(id_vars = 'group', value_vars = ['fd_mean'])
plt.figure(figsize = (8, 20))
ax = sns.boxplot(group_wise_comparison_fd, x='group', y='value', hue = 'group',fliersize=0, palette = group_palette, linewidth=2, fill = True, width=0.4)
sns.stripplot(group_wise_comparison_fd, x='group', y='value', hue = 'group', jitter = 0.2, size=7, palette = group_palette, alpha = 0.4,edgecolor=None)
sns.despine(bottom = True)
ax.set_xlabel("", fontsize=40, fontweight='bold')
ax.tick_params(which='major', labelsize=24, length = 3, width = 2)
ax.set_ylabel("Mean FD", fontsize=30, fontweight='bold')
ax.spines['left'].set_linewidth(2)
ax.tick_params(bottom = False, labelsize=24, length = 0, width = 0)
ax.set_ylim(0,1.2)
plt.rcParams['figure.dpi'] = 300


# REST TSNR
group_wise_comparison_fd = group_bold_unaltered[group_bold_unaltered['task'] == 'resting'].melt(id_vars = 'group', value_vars = ['tsnr'])
plt.figure(figsize = (8, 20))
ax = sns.boxplot(group_wise_comparison_fd.sort_values(by = 'group', ascending = False), x='group', y='value', hue = 'group',fliersize=0, palette = group_palette, linewidth=2, width=0.4, order = group_wise_comparison_fd['group'])
ax.set_title("Resting", fontsize=30, fontweight='bold')
sns.stripplot(group_wise_comparison_fd, x='group', y='value', hue = 'group', jitter = 0.2, size=7, palette = group_palette, alpha = 0.4, edgecolor=None)
plt.axhline(y = group_bold_unaltered[group_bold_unaltered['task'] == 'resting']['tsnr'].mean(), color = 'black', linewidth=2, linestyle="--")
sns.despine(bottom = True)
ax.set_xlabel("", fontsize=40, fontweight='bold')
ax.tick_params(which='major', labelsize=24, length = 3, width = 2)
ax.set_ylabel("TSNR", fontsize=30, fontweight='bold')
ax.spines['left'].set_linewidth(2)
ax.tick_params(bottom = False, labelsize=24, length = 0, width = 0)
ax.set_ylim(0,120)
plt.rcParams['figure.dpi'] = 300

# STIM TSNR
group_wise_comparison_fd = group_bold_unaltered[group_bold_unaltered['task'].isin(unique_tasks_lst[1:])].melt(id_vars = 'group', value_vars = ['tsnr'])
plt.figure(figsize = (8, 20))
ax = sns.boxplot(group_wise_comparison_fd.sort_values(by = 'group', ascending = False), x='group', y='value', hue = 'group',fliersize=0, palette = group_palette, linewidth=2, width=0.4, order = group_wise_comparison_fd['group'])
ax.set_title("Stimulation", fontsize=30, fontweight='bold')
sns.stripplot(group_wise_comparison_fd, x='group', y='value', hue = 'group', jitter = 0.2, size=7, palette = group_palette, alpha = 0.4, edgecolor=None)
plt.axhline(y = group_bold_unaltered[group_bold_unaltered['task'].isin(unique_tasks_lst[1:])]['tsnr'].mean(), color = 'black', linewidth=2, linestyle="--")
sns.despine(bottom = True)
ax.set_xlabel("", fontsize=40, fontweight='bold')
ax.set_yticks([])
ax.tick_params(which='major', labelsize=0, length = 3, width = 2)
ax.set_ylabel("", fontsize=30, fontweight='bold')
ax.spines['left'].set_linewidth(2)
ax.tick_params(bottom = False, labelsize=24, length = 0, width = 0)
ax.set_ylim(0,120)
plt.rcParams['figure.dpi'] = 300

# REST FD
group_wise_comparison_fd = group_bold_unaltered[group_bold_unaltered['task'] == 'resting'].melt(id_vars = 'group', value_vars = ['fd_mean'])
plt.figure(figsize = (8, 20))
ax = sns.boxplot(group_wise_comparison_fd.sort_values(by = 'group', ascending = False), x='group', y='value', hue = 'group',fliersize=0, palette = group_palette, linewidth=2, width=0.4, order = group_wise_comparison_fd['group'])
ax.set_title("Resting", fontsize=30, fontweight='bold')
sns.stripplot(group_wise_comparison_fd, x='group', y='value', hue = 'group', jitter = 0.2, size=7, palette = group_palette, alpha = 0.4, edgecolor=None)
plt.axhline(y = group_bold_unaltered[group_bold_unaltered['task'] == 'resting']['fd_mean'].mean(), color = 'black', linewidth=2, linestyle="--")
sns.despine(bottom = True)
ax.set_xlabel("", fontsize=40, fontweight='bold')
ax.tick_params(which='major', labelsize=24, length = 3, width = 2)
ax.set_ylabel("Mean FD", fontsize=30, fontweight='bold')
ax.spines['left'].set_linewidth(2)
ax.tick_params(bottom = False, labelsize=24, length = 0, width = 0)
ax.set_ylim(0,1.2)
plt.rcParams['figure.dpi'] = 300

# STIM FD
group_wise_comparison_fd = group_bold_unaltered[group_bold_unaltered['task'].isin(unique_tasks_lst[1:])].melt(id_vars = 'group', value_vars = ['fd_mean'])
plt.figure(figsize = (8, 20))
ax = sns.boxplot(group_wise_comparison_fd.sort_values(by = 'group', ascending = False), x='group', y='value', hue = 'group',fliersize=0, palette = group_palette, linewidth=2, width=0.4, order = group_wise_comparison_fd['group'])
ax.set_title("Stimulation", fontsize=30, fontweight='bold')
sns.stripplot(group_wise_comparison_fd, x='group', y='value', hue = 'group', jitter = 0.2, size=7, palette = group_palette, alpha = 0.4, edgecolor=None)
plt.axhline(y = group_bold_unaltered[group_bold_unaltered['task'].isin(unique_tasks_lst[1:])]['fd_mean'].mean(), color = 'black', linewidth=2, linestyle="--")
sns.despine(bottom = True)
ax.set_xlabel("", fontsize=40, fontweight='bold')
ax.set_yticks([])
ax.tick_params(which='major', labelsize=0, length = 3, width = 2)
ax.set_ylabel("", fontsize=30, fontweight='bold')
ax.spines['left'].set_linewidth(2)
ax.tick_params(bottom = False, labelsize=24, length = 0, width = 0)
ax.set_ylim(0,1.2)
plt.rcParams['figure.dpi'] = 300

# REST SNR
group_wise_comparison_fd = group_bold_unaltered[group_bold_unaltered['task'] == 'resting'].melt(id_vars = 'group', value_vars = ['snr'])
plt.figure(figsize = (8, 20))
ax = sns.boxplot(group_wise_comparison_fd.sort_values(by = 'group', ascending = False), x='group', y='value', hue = 'group',fliersize=0, palette = group_palette, linewidth=2, width=0.4, order = group_wise_comparison_fd['group'])
ax.set_title("Resting", fontsize=30, fontweight='bold')
sns.stripplot(group_wise_comparison_fd, x='group', y='value', hue = 'group', jitter = 0.2, size=7, palette = group_palette, alpha = 0.4, edgecolor=None)
plt.axhline(y = group_bold_unaltered[group_bold_unaltered['task'] == 'resting']['snr'].mean(), color = 'black', linewidth=2, linestyle="--")
sns.despine(bottom = True)
ax.set_xlabel("", fontsize=40, fontweight='bold')
ax.tick_params(which='major', labelsize=24, length = 3, width = 2)
ax.set_ylabel("SNR", fontsize=30, fontweight='bold')
ax.spines['left'].set_linewidth(2)
ax.tick_params(bottom = False, labelsize=24, length = 0, width = 0)
ax.set_ylim(0,7)
plt.rcParams['figure.dpi'] = 300

# STIM SNR
group_wise_comparison_fd = group_bold_unaltered[group_bold_unaltered['task'].isin(unique_tasks_lst[1:])].melt(id_vars = 'group', value_vars = ['snr'])
plt.figure(figsize = (8, 20))
ax = sns.boxplot(group_wise_comparison_fd.sort_values(by = 'group', ascending = False), x='group', y='value', hue = 'group',fliersize=0, palette = group_palette, linewidth=2, width=0.4, order = group_wise_comparison_fd['group'])
ax.set_title("Stimulation", fontsize=30, fontweight='bold')
sns.stripplot(group_wise_comparison_fd, x='group', y='value', hue = 'group', jitter = 0.2, size=7, palette = group_palette, alpha = 0.4, edgecolor=None)
plt.axhline(y = group_bold_unaltered[group_bold_unaltered['task'].isin(unique_tasks_lst[1:])]['snr'].mean(), color = 'black', linewidth=2, linestyle="--")
sns.despine(bottom = True)
ax.set_xlabel("", fontsize=40, fontweight='bold')
ax.set_yticks([])
ax.tick_params(which='major', labelsize=0, length = 3, width = 2)
ax.set_ylabel("", fontsize=30, fontweight='bold')
ax.spines['left'].set_linewidth(2)
ax.tick_params(bottom = False, labelsize=24, length = 0, width = 0)
ax.set_ylim(2,7)
plt.rcParams['figure.dpi'] = 300


# Compare stim and nonstim
group_wise_comparison_fd = group_bold_unaltered[group_bold_unaltered['task'].isin(unique_tasks_lst)].loc[(group_bold_unaltered['task'] == 'stimRxFEFxDAN') | (group_bold_unaltered['task'] == 'resting')]#.melt(id_vars = 'group', value_vars = ['fd_mean'])
plt.figure(figsize = (10, 20))
ax = sns.boxplot(group_wise_comparison_fd, x='task', y='fd_mean', hue = 'task', fliersize=0, palette = {'stimRxFEFxDAN': '#92DCE5', 'resting': '#7C7C7C'})
sns.stripplot(group_wise_comparison_fd, x='task', y='fd_mean', hue = 'task', jitter = 0.4, size=7, alpha = 0.6, edgecolor=None, palette = {'stimRxFEFxDAN': '#92DCE5', 'resting': '#7C7C7C'})
sns.despine(bottom = True)
ax.set_xlabel("", fontsize=40, fontweight='bold')
ax.tick_params(which='major', labelsize=24, length = 3, width = 2)
ax.set_ylabel("Mean FD", fontsize=30, fontweight='bold')
ax.spines['left'].set_linewidth(2)
ax.tick_params(bottom = False, labelsize=24, length = 0, width = 0)
plt.rcParams['figure.dpi'] = 300

# Compare stim and nonstim
group_wise_comparison_fd = group_bold_unaltered[group_bold_unaltered['task'].isin(unique_tasks_lst)].loc[(group_bold_unaltered['task'] == 'stimRxFEFxDAN') | (group_bold_unaltered['task'] == 'resting')]#.melt(id_vars = 'group', value_vars = ['fd_mean'])
plt.figure(figsize = (10, 20))
ax = sns.boxplot(group_wise_comparison_fd, x='task', y='tsnr', hue = 'task', fliersize=0, palette = {'stimRxFEFxDAN': '#92DCE5', 'resting': '#7C7C7C'})
sns.stripplot(group_wise_comparison_fd, x='task', y='tsnr', hue = 'task', jitter = 0.4, size=7, alpha = 0.6, edgecolor=None, palette = {'stimRxFEFxDAN': '#92DCE5', 'resting': '#7C7C7C'})
sns.despine(bottom = True)
ax.set_xlabel("", fontsize=40, fontweight='bold')
ax.tick_params(which='major', labelsize=24, length = 3, width = 2)
ax.set_ylabel("TSNR", fontsize=30, fontweight='bold')
ax.spines['left'].set_linewidth(2)
ax.tick_params(bottom = False, labelsize=24, length = 0, width = 0)
plt.rcParams['figure.dpi'] = 300

# Subject plots
subj_breakdown = group_bold_unaltered[group_bold_unaltered['task'].isin(unique_tasks_lst)].groupby('group').nunique('subject')['subject'].reset_index(drop = False)
plt.figure(figsize = (20, 10))
ax = sns.barplot(subj_breakdown, x='subject', y='group', hue = 'group', palette=group_palette)
sns.despine(bottom = True)
ax.set_xlabel("Count", fontsize=30, fontweight='bold')
ax.tick_params(which='major', labelsize=24, length = 3, width = 2)
ax.set_ylabel("", fontsize=30, fontweight='bold')
ax.spines['left'].set_linewidth(2)
plt.rcParams['figure.dpi'] = 300

plt.figure(figsize = (20, 10))
gender_breakdown = group_bold_unaltered[group_bold_unaltered['task'].isin(unique_tasks_lst)].groupby(['group', 'gender']).count().reset_index(drop = False)
ax = sns.barplot(gender_breakdown, x='subject', y='gender', hue = 'gender')

# mriqc comparison
for data_type in ['aor', 'aqi', 'dvars_std', 'dvars_vstd', 'efc', 'fber', 'fd_mean', 'gcor', 'gsr_x', 'gsr_y', 'snr', 'tsnr']:
    
    data = bold_plot[['compare', data_type, 'task']]
    data = data.loc[(data['task'] == 'resting') | (data['task'].isin(unique_tasks_lst[1:])) | (data['task'] == 'test')]
    data['task'].replace('\w-\w*', 'stimulation', regex = True, inplace = True)
    data['task'].replace('test', 'mriqc', regex = True, inplace = True)
    data['data type'] = data_type
    
    data.to_csv(f'{data_type}_comparison.csv')
    plt.figure(figsize = (4,20))
    
    ax = sns.violinplot(data = data, 
                     x = 'task', 
                     y = data_type, 
                     hue = 'task',
                     palette = {'mriqc': '#F0F0F0', 'resting': '#bdbdbd', 'stimulation': '#636363'}, inner = 'quart')
    sns.despine(bottom = True)
    ax.set_xlabel("", fontsize=30, fontweight='bold')
    ax.tick_params(which='major', labelsize=24, length = 3, width = 2)
    ax.set_ylabel(data_type, fontsize=40, fontweight='bold')
    ax.spines['left'].set_linewidth(2)
    ax.tick_params(bottom = False, labelsize=24, length = 0, width = 0)
    plt.xticks([])
    plt.rcParams['figure.dpi'] = 300



# Redcap Data
redcap_data = pd.read_excel("path to spTMS-fMRI Metadata.xlsx")
redcap_data = redcap_data[redcap_data['REPORTED DATA'] == 1]
redcap_data = redcap_data[redcap_data['Redcap ID'].isin(subs_included)]

subjs_to_report = redcap_data['MRI ID'].astype(int)

subjs_sex = redcap_data[['Group','Sex']]
subjs_male = subjs_sex.loc[subjs_sex['Sex'] == 1].groupby('Group').count().reset_index().sort_values(by = 'Group', ascending = True)
subjs_all = subjs_sex.groupby('Group').count().reset_index().sort_values(by = 'Group', ascending = True)

plt.figure(figsize = (20, 10))
ax = sns.barplot(data = subjs_all, x = 'Sex', y = 'Group', color = '#7C7C7C', palette=group_palette, alpha = 0.5, order = subjs_all['Group'])
ax = sns.barplot(data = subjs_male, x = 'Sex', y = 'Group', color = '#7C7C7C', palette=group_palette, order = subjs_male['Group'])
sns.despine(left = True)
ax.set_xlabel("Count", fontsize=30, fontweight='bold')
ax.tick_params(which='major', labelsize=20, length = 3, width = 2)

ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
plt.yticks([])
plt.rcParams['figure.dpi'] = 300

plt.figure(figsize = (20, 10))
subjs_age = redcap_data[['Group','Age']].sort_values('Group')
ax = sns.boxplot(subjs_age, x='Age', y='Group', hue = 'Group', fliersize=0, palette = group_palette)
sns.stripplot(subjs_age, x='Age', y='Group', hue = 'Group', jitter = 0.4, size=7, alpha = 0.6, edgecolor='white', linewidth=0.5,palette = group_palette)
sns.despine(left=True)
ax.set_xlabel("Age", fontsize=40, fontweight='bold')
ax.tick_params(which='major', labelsize=24)
plt.yticks([])
ax.set_ylabel("", fontsize=30, fontweight='bold')
ax.spines['left'].set_linewidth(2)
ax.tick_params(bottom = False, labelsize=24)
plt.rcParams['figure.dpi'] = 300
subjs_unique_targets = redcap_data.iloc[:,14:40].loc[redcap_data['MRI ID'].isin(unique_subjs.astype(int))].sum().sort_values(ascending=False)

# Plot Tasks
plt.figure(figsize = (36, 10))
ax = sns.barplot(data = tasks_numbers.sort_values(by = ['task', 'group'], ascending = True), x = 'task', y = 0, hue = 'group', palette=group_palette, legend = False,  edgecolor = 'black', gap = 0.1)
plt.setp(ax.patches, linewidth=1)
sns.despine(bottom = True)
ax.set_xlabel("", fontsize=30, fontweight='bold')
ax.set_ylabel("", fontsize=30, fontweight='bold')
ax.spines['left'].set_linewidth(1.5)
ax.tick_params(which='major', labelsize=20, length = 3, width = 2)
ax.tick_params(length  = 0, width = 0)
plt.legend()
plt.rcParams['figure.dpi'] = 300

# PLOT SUD
SUDS = redcap_data.iloc[:,25:]
SUDS.columns = redcap_data.iloc[:,14:25].columns

SUDS_replace_dict = {"LFp": "L-FP",
                "RFEF":"R-FEF",
                "RFp":"R-FP",
                "RIFJ":"R-IFJ",
                "RIPL":"R-IPL",
                "RM1":"R-M1",
                "RpreSMA":"R-preSMA",
                "RAMFG":"R-aMFG",
                "RpMFG":"R-pMFG",
                "LpMFG":"L-pMFG",
                "LAMFG":"L-aMFG",
                "Resting":"resting"
                }

SUDS = SUDS.melt().replace(SUDS_replace_dict)

plt.figure(figsize = (15, 20))
ax = sns.boxplot(SUDS, x='variable', y='value', hue = 'variable',fliersize=0, palette = tasks_palette, linewidth =3)
sns.despine(bottom=True)
ax.set_xlabel("", fontsize=40, fontweight='bold')
ax.tick_params(which='major', labelsize=24)
ax.set_ylabel("", fontsize=30, fontweight='bold')
ax.spines['left'].set_linewidth(2)
ax.tick_params(bottom = False, labelsize=20)
plt.rcParams['figure.dpi'] = 300


# Plot MT
MT = redcap_data.iloc[:,11]

plt.figure(figsize = (1.3, 20))
ax = sns.boxplot(MT,fliersize=0, color='#F0F0F0', linewidth =3, linecolor = 'black')
sns.despine(bottom=True)
ax.set_xlabel("", fontsize=40, fontweight='bold')
ax.tick_params(which='major', labelsize=24)
ax.set_ylabel("", fontsize=30, fontweight='bold')
ax.spines['left'].set_linewidth(2)
ax.tick_params(bottom = False, labelsize=20)
plt.rcParams['figure.dpi'] = 300

# Plot percent
perc = redcap_data.iloc[:,12]
perc = perc[perc < 101]

plt.figure(figsize = (1.3, 20))
ax = sns.boxplot(perc,fliersize=0, color='#F0F0F0', linewidth =3, linecolor = 'black')
sns.despine(bottom=True)
ax.set_xlabel("", fontsize=40, fontweight='bold')
ax.tick_params(which='major', labelsize=24)
ax.set_ylabel("", fontsize=30, fontweight='bold')
ax.spines['left'].set_linewidth(2)
ax.tick_params(bottom = False, labelsize=20)
plt.rcParams['figure.dpi'] = 300


# Find completion %
n_subs_NTHC = tasks_numbers[tasks_numbers['group'] == 'NTHC'][0].sum()/(51 *12) * 100 
n_subs_NTS = tasks_numbers[tasks_numbers['group'] == 'NTS'][0].sum()/(60 *12) * 100 
n_subs_TIS = tasks_numbers[tasks_numbers['group'] == 'TIS'][0].sum()/(45 *12) * 100 
n_subs_TEHC = tasks_numbers[tasks_numbers['group'] == 'TEHC'][0].sum()/(50 *12) * 100



