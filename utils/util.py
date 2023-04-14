# helper functions

import pandas as pd
import matplotlib.pyplot as plt 
import sys
import numpy
import statistics

#NAME=sys.argv[1]

def load_data(NAME):
    # Load data
    df = pd.read_csv('processed/'+str(NAME)+'.csv')
    # Remove empty spaces in column names.
    df.columns = [col.replace(" ", "") for col in df.columns]
    # Print few values of data.
    print(NAME)
    print(f"Max number of frames {df.frame.max()}", f"\nTotal shape of dataframe {df.shape}")
    return df

def calibration_data(vid_names):
    '''
    @Param <vid_names>  : array of 5 strings 
        where each string is the name of a generated CSV in '../processed/'
        to be plotted on the same graph
        [Q1 Q2 Q3 Q4 CC]
    '''
    d_cal = {}
    for name in vid_names:
        d_cal[name] = pd.read_csv('processed/'+str(name)+'.csv')
    return d_cal
        
def plot_calibration_data(d_cal, tag, eye_pos="0"):
    '''
    @Param <d_cal>      : dictionary of dataframes
        where key=NAME, value=df_${NAME}
    @Param <eye_pos>         : int
        default value 0. Represents location of eye landmark according to 
        https://github.com/TadasBaltrusaitis/OpenFace/wiki/Output-Format
    @Param <tag>        : str
        to distinguish outputs with a unique name
    '''

    title = "Gaze Clustering: Positive Control"
    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(projection='3d')
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Y coordinate')
    ax.set_zlabel('Z coordinate')
    
    i=0
    colour=['red','orange','yellow','green','blue']
    marker=['o','*','s','p','+']
    for name in d_cal:
        ax.scatter(d_cal[name]['gaze_'+eye_pos+'_x'], d_cal[name]['gaze_'+eye_pos+'_y'], d_cal[name]['gaze_'+eye_pos+'_z'], color=colour[i], marker=marker[i], label=name)
        i+=1
    ax.legend(loc="upper left")
    title = title+" ("+eye_pos+")"
    ax.set_title(title)

    path='figs/'+tag+'.jpg'
    plt.savefig(path)
    return path

def compute_stats(d_cal, eye_pos="0"):
    '''
    @Param <d_cal>      : dictionary of dataframes
        where key=NAME, value=df_${NAME}
    @Param <eye_pos>    : int
        default value 0. Represents location of eye landmark according to
        https://github.com/TadasBaltrusaitis/OpenFace/wiki/Output-Format
    '''
    d_stats={}
    for name in d_cal:
        d_stats[name] = d_cal[name][['gaze_'+eye_pos+'_x','gaze_'+eye_pos+'_y','gaze_'+eye_pos+'_z']].quantile([0.01, 0.25, 0.5, 0.75, 0.99])
        d_stats[name].loc['avg'] = [statistics.mean(d_cal[name]['gaze_'+eye_pos+'_x']), statistics.mean(d_cal[name]['gaze_'+eye_pos+'_y']), statistics.mean(d_cal[name]['gaze_'+eye_pos+'_z'])]
        d_stats[name].loc['stdev'] = [statistics.stdev(d_cal[name]['gaze_'+eye_pos+'_x']), statistics.stdev(d_cal[name]['gaze_'+eye_pos+'_y']), statistics.stdev(d_cal[name]['gaze_'+eye_pos+'_z'])]
    return d_stats

def find_zscore(d_stats, x):
    '''
    @Param <d_stats>    : dictionary of dataframes
        where key=NAME, value=df with quantile/avg/stdev vector
    @Param <x>          : vector with x,y,z gaze vector coordinate
    '''
    conf_x = {}
    error = {}
    for name in d_stats:
        zscore = (x-d_stats[name].loc['avg'])/d_stats[name].loc['stdev']
        zscore_abs = [abs(z) for z in zscore]
        SSE=0
        for z_abs in zscore_abs:
            SSE += z_abs**2
        conf_x[name] = zscore_abs
        error[name] = SSE
    return conf_x, error
