data_path = 'C:\Users\utayv\OneDrive\Desktop\grad\research\data\thz-data\';

%% blank

[~, cond_archive_124] = live_process([data_path '2022_05_12\May12_012.tim'],...
    [data_path '2022_05_12\May12_011.tims'], 0.77);

[~, cond_archive_125] = live_process([data_path '2022_05_13\May13_012.tim'],...
    [data_path '2022_05_13\May13_011.tims'], 0.66);

[~, cond_archive_129] = live_process([data_path '2022_05_14\May14_002.tim'],...
    [data_path '2022_05_14\May14_001.tims'], 0.71);

%% wires
[freq, cond_archive_wires_132] = wires_process([data_path '2022_05_12\May12_015.tims'],...
    [data_path '2022_05_12\May12_016.tim'], 0.89, 0.25);

[~, cond_archive_wires_131] = wires_process([data_path '2022_05_13\May13_007.tims'],...
    [data_path '2022_05_13\May13_008.tim'], 0.86, 0.25);

[~, cond_archive_wires_128] = wires_process([data_path '2022_05_13\May13_015.tims'],...
    [data_path '2022_05_13\May13_016.tim'], 0.84, 0.25);

