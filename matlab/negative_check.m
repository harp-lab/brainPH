load("timeseries.Yeo2011.mm316.mat");
disp(size(subjects));
is_negative = 0;
for m = 1:316
    subject_mx645 = subjects(m).mx645;
    subject_mx1400 = subjects(m).mx1400;
    subject_std2500 = subjects(m).std2500;

    [rows, columns] = size(subject_mx645);
    count_negative = 0;
    for i = 1:rows
        for j=1:columns
            x = subject_mx645(i, j);
            if x < 0
                subject_mx645(i, j) = 0;
                count_negative = count_negative + 1;
                is_negative = 1;
            end
        end
    end
    if count_negative > 0
        disp("Subject "+m+ "_subject_mx645: "+ count_negative);
    end

    [rows, columns] = size(subject_mx1400);
    count_negative = 0;
    for i = 1:rows
        for j=1:columns
            x = subject_mx1400(i, j);
            if x < 0
                subject_mx1400(i, j) = 0;
                count_negative = count_negative + 1;
                is_negative = 1;
            end
        end
    end
    if count_negative > 0
        disp("Subject "+m+ "_subject_mx1400: "+ count_negative);
    end

    [rows, columns] = size(subject_std2500);
    count_negative = 0;
    for i = 1:rows
        for j=1:columns
            x = subject_std2500(i, j);
            if x < 0
                subject_std2500(i, j) = 0;
                count_negative = count_negative + 1;
                is_negative = 1;
            end
        end
    end
    if count_negative > 0
        disp("Subject "+m+ "_std2500_negative: "+ count_negative);
    end
end
disp(is_negative);