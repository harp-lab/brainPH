load("timeseries.Yeo2011.mm316.mat");

for m = 1:316
    subject_mx645 = corrcoef(transpose(subjects(m).mx645));
    subject_mx1400 = corrcoef(transpose(subjects(m).mx1400));
    subject_std2500 = corrcoef(transpose(subjects(m).std2500));
    
    %subject_mx645_f = atanh(subject_mx645);
    %subject_mx1400_f = atanh(subject_mx1400);
    %subject_std2500_f = atanh(subject_std2500);
    
    subject_mx645(24,:) = [];
    subject_mx645(:,24) = [];
    subject_mx1400(24,:) = [];
    subject_mx1400(:,24) = [];
    subject_std2500(24,:) = [];
    subject_std2500(:,24) = [];
    subject_mx645_normalize = sqrt(1 - subject_mx645.*subject_mx645);
    subject_mx1400_normalize = sqrt(1 - subject_mx1400.*subject_mx1400);
    subject_std2500_normalize = sqrt(1 - subject_std2500.*subject_std2500);    
    str_mx645 = "subject_" + m + "_mx645";
    str_mx1400 = "subject_" + m + "_mx1400";
    str_std2500 = "subject_" + m + "_std2500";
    writematrix(subject_mx645_normalize, str_mx645, 'Delimiter', 'tab');
    writematrix(subject_mx1400_normalize, str_mx1400, 'Delimiter', 'tab');
    writematrix(subject_std2500_normalize, str_std2500, 'Delimiter', 'tab');
end