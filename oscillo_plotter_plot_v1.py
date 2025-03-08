import oscillo_plotter_func_v1 as osc_func
import numpy as np
import matplotlib.pyplot as plt
import sys

#---------------------config----------------------
filename='SDS00368.csv'#ファイル名.
folder_path=r"C:\Users\CSV"#フォルダのパス.
skiprow=12#csvファイルの先頭行数.
x_scale=1e6#横軸のスケール.us->1e6, ms->1e3 etc.

FigSize=[8,6]#グラフのサイズ.

channel=2#対象のチャンネル (1,2,3...).
#-------------------------------------------------

file_path=folder_path+"\\"+filename
matans, channel_num = osc_func.read_csv(file_path,skiprow)#ファイルの読み込み.
if channel_num==-1:
    sys.exit()#ファイルの読み込みに失敗すると終了.
print(fr"channel num = {channel_num}")

#移動平均の例.
move_ave_num=10
v=osc_func.moving_average(matans[channel],move_ave_num)#通常の移動平均.
v2=osc_func.smooth(matans[channel],move_ave_num)#位相特性が直線的な移動平均. 未来の値を使う. あるポイントの両端 int(move_ave_num/2)点数の平均を出す.

#積分の例.
fs=(len(matans[0])-1)/(matans[0][-1]-matans[0][0])#サンプリング周波数.
q=osc_func.integral(matans[channel],fs)
dc_offset=sum(q)/len(q)
q=q-dc_offset

#微分の例.
dy=osc_func.diff(matans[channel],fs)
move_ave_num=100
dy2=osc_func.smooth(dy,move_ave_num)

#---------------------plot------------------------
fig, ax = plt.subplots(nrows=2, ncols=1, squeeze=False, tight_layout=True, figsize=FigSize, sharex = "col")
ax[0,0].plot(matans[0]*x_scale,matans[channel],"k-")
ax[0,0].plot(matans[0]*x_scale,v,"r-")
ax[0,0].plot(matans[0]*x_scale,v2,"g-")
ax[0,0].set_xlabel("time [us]")
ax[0,0].set_xlabel("time [us]")

ax[1,0].plot(matans[0]*x_scale,dy2,"k-")
ax2 = ax[1,0].twinx()#右軸を作る.
ax2.plot(matans[0]*x_scale,q,"r-")
#-------------------------------------------------

plt.show()