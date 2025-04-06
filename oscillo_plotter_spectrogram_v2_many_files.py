import oscillo_plotter_func_v1 as osc_func
import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib.colors as mcolors

#いくつものファイルを読み込み、それらのスペクトログラムを一つのグラフにplotする.
#---------------------config----------------------

mat_filename=['TLine_PTS_v2_interp_50k.csv'
              ,'TLine_PTS_v2_interp_100k.csv'
              ,'TLine_PTS_v2_interp_200k.csv'
              ,'TLine_PTS_v2_interp_250k.csv'
              ,'TLine_PTS_v2_interp_300k.csv']

folder_path=r"C:\Users\CSV"
skiprow=12
x_scale=1e3

FigSize=[8,6]

channel=1#対象のチャンネル (1,2,3...).

window_name="hanning"#窓関数.
f_min=2e3#周波数の最小値.
spectro_division_num=500#時間軸の刻み数.
dB_min=1e-12#答えの最小値 [dB].

num_colors=64#色の解像度(64 etc.).
cm_name = 'jet'#それぞれのファイルにおける色を決める、カラーマップの種類.
alpha_max=1#透明度の最大値.
dash_offset=2#破線の長さ.int, 1, 2, 3, ...
#-------------------------------------------------

file_num=len(mat_filename)
fig, ax = plt.subplots(nrows=1, ncols=1, squeeze=False, tight_layout=True, figsize=FigSize, sharex = "col")
cm = plt.get_cmap(cm_name, file_num)#cm(i)[0:3]でRGBを取得できる.
k=0
for filename in mat_filename:
    end_color_rgb=cm(k)[0:4]
    rgb_colormap = np.linspace([1, 1, 1, 0], end_color_rgb, num_colors)

    #値が小さいほど透明度を高くする.
    alpha_values=np.linspace(0.0, alpha_max, len(rgb_colormap))  # 透明度を設定.
    for i in range(len(rgb_colormap)):
        rgb_colormap[i][-1] = alpha_values[i]  # RGBAの最後の値（アルファ）を更新
    custom_cmap = mcolors.ListedColormap(rgb_colormap)

    file_path=folder_path+"\\"+filename
    matans, channel_num = osc_func.read_csv(file_path,skiprow)
    if channel_num==-1:
        sys.exit()#ファイルの読み込みに失敗すると終了.
    print(fr"channel num = {channel_num}")

    v=matans[channel]#対象の電圧.
    t=matans[0]#時間.

    fs=(len(t)+1)/(t[-1]-t[0])#サンプリング周波数.
    matt_for_spectrogram, matf_for_spectrogram, Spec_dB = osc_func.f_spectrogram(v, t, window_name, fs, f_min, spectro_division_num, dB_min)

    #破線にして、重なっても判別できるようにする.
    j2=k*dash_offset
    j=0
    while j<spectro_division_num:
        if j2==(file_num-1)*dash_offset:
            j2=0
            j+=dash_offset
        else:
            Spec_dB[:,j]=np.nan
            j2+=1
            j+=1
    
    pcolormesh_plot = ax[0,0].pcolormesh((matt_for_spectrogram + t[0])*x_scale, matf_for_spectrogram*1e-3, Spec_dB, cmap=custom_cmap)
    #ax[1,0].plot(t*x_scale,v,"k-")
    k+=1

ax[0,0].set_ylabel('Frequency [kHz]')
#ax[1,0].set_ylabel('Voltage [V]')
ax[0,0].set_xlabel('Time [m sec]')
#cbar = plt.colorbar(pcolormesh_plot, ax=ax[0,0])
#cbar2 = plt.colorbar(pcolormesh_plot, ax=ax[1,0])
plt.show()