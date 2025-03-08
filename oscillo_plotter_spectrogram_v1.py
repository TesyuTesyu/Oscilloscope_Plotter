import oscillo_plotter_func_v1 as osc_func
import numpy as np
import matplotlib.pyplot as plt
import sys

#---------------------config----------------------
filename='SDS00365'
folder_path=r"C:\Users\CSV"
skiprow=12
x_scale=1e6

FigSize=[8,6]

channel=1#対象のチャンネル (1,2,3...).

window_name="hanning"
f_min=10e3
spectro_division_num=100
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
matt_for_spectrogram, matf_for_spectrogram, Spec_dB = osc_func.f_spectrogram(v, t, window_name, fs, f_min, spectro_division_num, dB_min)

fig, ax = plt.subplots(nrows=1, ncols=1, squeeze=False, tight_layout=True, figsize=FigSize, sharex = "col")
plt.pcolormesh((matt_for_spectrogram + t[0])*x_scale, matf_for_spectrogram*1e-3, Spec_dB, cmap="Greys")
plt.ylabel('Frequency [kHz]')
plt.xlabel('Time [usec]')
cbar = plt.colorbar()

fig, ax = plt.subplots(nrows=1, ncols=1, squeeze=False, tight_layout=True, figsize=FigSize, sharex = "col")
ax[0,0].plot(t*x_scale,v,"k-")
plt.show()