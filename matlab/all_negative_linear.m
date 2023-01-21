load("timeseries.Yeo2011.mm316.mat");
output_dir = "full_data_negative_linear";
mkdir(output_dir);
total_positive = 0;
for m = 1:316
    subject_mx645 = corrcoef(transpose(subjects(m).mx645));
    subject_mx1400 = corrcoef(transpose(subjects(m).mx1400));
    subject_std2500 = corrcoef(transpose(subjects(m).std2500));
    
    subject_mx645(24,:) = [];
    subject_mx645(:,24) = [];
    subject_mx1400(24,:) = [];
    subject_mx1400(:,24) = [];
    subject_std2500(24,:) = [];
    subject_std2500(:,24) = [];
    [rows, columns] = size(subject_mx645);
    count_positive = 0;
    for i = 1:rows
        for j=1:columns
            x = subject_mx645(i, j);
            if x > 0
                subject_mx645(i, j) = 0;
                count_positive = count_positive + 1;
            end
        end
    end
    total_positive = total_positive + count_positive;

    [rows, columns] = size(subject_mx1400);
    count_positive = 0;
    for i = 1:rows
        for j=1:columns
            x = subject_mx1400(i, j);
            if x > 0
                subject_mx1400(i, j) = 0;
                count_positive = count_positive + 1;
            end
        end
    end
    total_positive = total_positive + count_positive;

    [rows, columns] = size(subject_std2500);
    count_positive = 0;
    for i = 1:rows
        for j=1:columns
            x = subject_std2500(i, j);
            if x > 0
                subject_std2500(i, j) = 0;
                count_positive = count_positive + 1;
            end
        end
    end
    total_positive = total_positive + count_positive;

    subject_mx645_normalize = 1 - subject_mx645;
    subject_mx1400_normalize = 1 - subject_mx1400;
    subject_std2500_normalize = 1 - subject_std2500;
    str_mx645 = output_dir + "/subject_" + m + "_mx645";
    str_mx1400 = output_dir + "/subject_" + m + "_mx1400";
    str_std2500 = output_dir + "/subject_" + m + "_std2500";
    writematrix(subject_mx645_normalize, str_mx645, 'Delimiter', 'tab');
    writematrix(subject_mx1400_normalize, str_mx1400, 'Delimiter', 'tab');
    writematrix(subject_std2500_normalize, str_std2500, 'Delimiter', 'tab');
end
disp("Total positive: " + total_positive);