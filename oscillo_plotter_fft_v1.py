import oscillo_plotter_func_v1 as osc_func
import numpy as np
import matplotlib.pyplot as plt
import sys

#---------------------config----------------------
filename='SDS00365_downsampled.csv'
folder_path=r"C:\Users\CSV"
skiprow=12
x_scale=1e6

FigSize=[8,6]

channel=1#対象のチャンネル (1,2,3...).

window_name="hanning"#窓関数.
dB_min=1e-6#答えの最小値.
#-------------------------------------------------

file_path=folder_path+"\\"+filename
matans, channel_num = osc_func.read_csv(file_path,skiprow)
if channel_num==-1:
    sys.exit()#ファイルの読み込みに失敗すると終了.
print(fr"channel num = {channel_num}")

v=matans[channel]#対象の電圧.
t=matans[0]#時間.

fs=(len(t)+1)/(t[-1]-t[0])#サンプリング周波数.
freq_segment, FV_segment=osc_func.f_fft(v, t, window_name, fs, np.nan, np.nan, dB_min)

fig, ax = plt.subplots(nrows=1, ncols=1, squeeze=False, tight_layout=True, figsize=FigSize, sharex = "col")
ax[0,0].plot(freq_segment,FV_segment,"k-")

fig, ax = plt.subplots(nrows=1, ncols=1, squeeze=False, tight_layout=True, figsize=FigSize, sharex = "col")
ax[0,0].plot(t*x_scale,v,"k-")
plt.show()