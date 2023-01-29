load("timeseries.Yeo2011.mm316.mat");
output_dir = "full_data_linear_downsample";
mkdir(output_dir);
count = 0;
for m = 1:316
    subject_mx645_original = subjects(m).mx645;
    subject_mx1400_original = subjects(m).mx1400;
    subject_std2500_original = subjects(m).std2500;
    [mx_645_rows, mx_645_columns] = size(subject_mx645_original);
    [mx_1400_rows, mx_1400_columns] = size(subject_mx1400_original);
    [std_2500_rows, std_2500_columns] = size(subject_std2500_original);
    ratio_mx645_std2500 = floor(mx_645_columns / std_2500_columns);
    ratio_mx1400_std2500 = floor(mx_1400_columns / std_2500_columns);
    subject_mx645_down = subject_mx645_original(:, 1:ratio_mx645_std2500:end);
    subject_mx645_down = subject_mx645_down(:, 1:std_2500_columns);
    subject_mx1400_down = subject_mx1400_original(:, 1:ratio_mx1400_std2500:end);
    subject_mx1400_down = subject_mx1400_down(:, 1:std_2500_columns);
    subject_mx645 = corrcoef(transpose(subject_mx645_down));
    subject_mx1400 = corrcoef(transpose(subject_mx1400_down));
    subject_std2500 = corrcoef(transpose(subject_std2500_original));
    subject_mx645(24,:) = [];
    subject_mx645(:,24) = [];
    subject_mx1400(24,:) = [];
    subject_mx1400(:,24) = [];
    subject_std2500(24,:) = [];
    subject_std2500(:,24) = [];
    subject_mx645_normalize = 1 - subject_mx645;
    subject_mx1400_normalize = 1 - subject_mx1400;
    subject_std2500_normalize = 1 - subject_std2500;
    str_mx645 = output_dir + "/subject_" + m + "_mx645";
    str_mx1400 = output_dir + "/subject_" + m + "_mx1400";
    str_std2500 = output_dir + "/subject_" + m + "_std2500";
    writematrix(subject_mx645_normalize, str_mx645, 'Delimiter', 'tab');
    writematrix(subject_mx1400_normalize, str_mx1400, 'Delimiter', 'tab');
    writematrix(subject_std2500_normalize, str_std2500, 'Delimiter', 'tab');
    count = count + 1;
end
count = count * 3;
disp("Done generating "+count+" files");