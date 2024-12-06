import os
from typing import Union, Optional
import matplotlib
matplotlib.use('Agg')  # For non-GUI environments
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from simba.utils.checks import check_if_dir_exists, check_all_file_names_are_represented_in_video_log, check_float
from simba.utils.read_write import find_files_of_filetypes_in_directory, read_df, read_video_info_csv, get_fn_ext, read_video_info
from simba.utils.data import detect_bouts

GROUP_COLORS = {'CNO': 'orchid', 'SALINE': 'cadetblue'}

def frequency_grapher(data_dir: Union[str, os.PathLike],
                      video_info_path: Union[str, os.PathLike],
                      start_times_path: Union[str, os.PathLike],
                      save_path: Union[str, os.PathLike],
                      min_bout: float,
                      clf: str,
                      bin_size: Optional[int] = 55) -> None:

    """
    :param Union[str, os.PathLike] data_dir: Path to directory holding machine learning results.
    :param Union[str, os.PathLike] video_info_path: Path to CSV holding video sample rate (fps).
    :param Union[str, os.PathLike] start_times_path: Path to CSV holding the CNO onset times.
    :param Union[str, os.PathLike] save_path: Where to save th image.
    :param float min_bout: The minimum bout to plot in seconds.
    :param str clf: The name of the classifier.
    :param Optional[int] bin_size: The size of each plotted bar in frames.

    :example:
    >>> _ frequency_grapher(data_dir=r'D:\troubleshooting\mitra\project_folder\logs\grooming_data',
    >>>                     clf='grooming',
    >>>                     video_info_path=r"D:\troubleshooting\mitra\project_folder\logs\video_info.csv",
    >>>                     start_times_path=r"D:\troubleshooting\mitra\Start_annotations_Simon_Hallie.csv",
    >>>                     min_bout=2.5,
    >>>                     bin_size=55,
    >>>                     save_path=r"C:\Users\sroni\OneDrive\Desktop\grooming.png")
    """

    data_paths = find_files_of_filetypes_in_directory(directory=data_dir, extensions=['.csv'])
    video_info_df = read_video_info_csv(file_path=video_info_path)
    check_all_file_names_are_represented_in_video_log(video_info_df=video_info_df, data_paths=data_paths)
    start_times = pd.read_csv(start_times_path, index_col=0)
    check_float(name='min_bout', value=min_bout, min_value=10e-7)
    check_if_dir_exists(in_dir=os.path.dirname(save_path))
    results = []
    for file_cnt, file_path in enumerate(data_paths):
        video_name = get_fn_ext(filepath=file_path)[1]
        group = 'SALINE'
        if 'CNO' in video_name:
            group = 'CNO'
        df = read_df(file_path=file_path, file_type='csv', usecols=[clf])
        _, _, fps = read_video_info(video_name=video_name, video_info_df=video_info_df)
        start_frm_number = start_times[start_times['VIDEO'] == video_name]['CNO onset (frame)'].values[0]
        start_frm = max(0, start_frm_number - int(fps * 120))
        end_frm = start_frm_number + int((fps * 60) * 10)
        df = df.loc[start_frm:end_frm, :].reset_index(drop=True)
        bouts = detect_bouts(data_df=df, target_lst=[clf], fps=fps)
        bouts = bouts[bouts['Start_frame'] >= start_frm]
        bouts = bouts[bouts['Bout_time'] >= min_bout]
        bouts = list(bouts[bouts['Start_frame'] <= end_frm]['Start_frame'])
        video_results = pd.DataFrame()
        video_results['start'] = bouts
        video_results['duration'] = bin_size
        video_results['group'] = group
        video_results['event'] = clf
        results.append(video_results)
    results = pd.concat(results, axis=0)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.set_style("whitegrid")
    plt.xlim(0, 21601)

    for idx, row in results.iterrows():
        plt.barh(y=row['event'], width=row['duration'], left=row['start'], color=GROUP_COLORS[row['group']], edgecolor=None, height=0.8)

    plt.xlabel('frame')
    plt.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=GROUP_COLORS['CNO']), plt.Rectangle((0, 0), 1, 1, color=GROUP_COLORS['SALINE'])], labels=['CNO', 'SALINE'], title='Groups')
    plt.savefig(save_path, format='png', dpi=1200, bbox_inches='tight')




#
# frequency_grapher(data_dir=r'D:\troubleshooting\mitra\project_folder\logs\grooming_data',
#                   clf='grooming',
#                   video_info_path=r"D:\troubleshooting\mitra\project_folder\logs\video_info.csv",
#                   start_times_path=r"D:\troubleshooting\mitra\Start_annotations_Simon_Hallie.csv",
#                   min_bout=2.5,
#                   bin_size=55,
#                   save_path=r"C:\Users\sroni\OneDrive\Desktop\grooming.png")