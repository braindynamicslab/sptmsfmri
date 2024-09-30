%WGGGG
%
%
%
% aim - ttest for sptms paper
% author - saggar@stanford.edu
% date - Sep 23, 2024

%%
cd <current directory>

fnames = dir('*.csv');
fnames = {fnames.name};

data = struct();
for f = 1:1:length(fnames)
    tmp = readtable(fnames{f});

    data.(strrep(fnames{f},'.csv','')) = tmp;
    

end

%%
[p,s,st]=anova1(data.SUDS.value, data.SUDS.variable)
multcompare(st)

[p,s,st]=anova1(data.stim_snr.value, data.stim_snr.group)
multcompare(st)
[p,s,st]=anova1(data.rest_fd.value, data.rest_fd.group)
multcompare(st)
[p,s,st]=anova1(data.stim_fd.value, data.stim_fd.group)
multcompare(st)

[p,s,st]=anova1(data.tsnr_comparison.tsnr, data.tsnr_comparison.task)
multcompare(st)


[p,s,st]=anova1(data.efc_comparison.efc, data.efc_comparison.task)
multcompare(st)

[p,s,st]=anova1(data.fber_comparison.fber, data.fber_comparison.task)
multcompare(st)

[p,s,st]=anova1(data.snr_comparison.fber, data.snr_comparison.task)

[p,s,st]=anova1(data.snr_comparison.snr, data.snr_comparison.task)
multcompare(st)
[p,s,st]=anova1(data.dvars_std_comparison.dvars_std, data.dvars_std_comparison.task)
multcompare(st)
[p,s,st]=anova1(data.dvars_vstd_comparison.dvars_vstd, data.dvars_vstd_comparison.task), multcompare(st)

[p,s,st]=anova1(data.dvars_vstd_comparison.dvars_vstd, data.dvars_vstd_comparison.task)
multcompare(st)
[p,s,st]=anova1(data.gcor_comparison.gcor, data.gcor_comparison.task)
multcompare(st)
[p,s,st]=anova1(data.tsnr_comparison.tsnr, data.tsnr_comparison.task)
multcompare(st)
[p,s,st]=anova1(data.fd_mean_comparison.fd_mean, data.fd_mean_comparison.task)
multcompare(st)
[p,s,st]=anova1(data.gsr_x_comparison.gsr_x, data.gsr_x_comparison.task)
multcompare(st)
[p,s,st]=anova1(data.gsr_x_comparison.gsr_y, data.gsr_y_comparison.task)
[p,s,st]=anova1(data.gsr_y_comparison.gsr_y, data.gsr_y_comparison.task)
multcompare(st)
[p,s,st]=anova1(data.aor_comparison.aor, data.aor_comparison.task)
multcompare(st)
[p,s,st]=anova1(data.aqi_comparison.aqi, data.aqi_comparison.task)
multcompare(st)
