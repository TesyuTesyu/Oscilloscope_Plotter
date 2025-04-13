import numpy as np
import csv
import os
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
#LTspiceの波形データのサンプリング間隔が一定でないので、補間して一定のサンプリング周波数で書き出すやつ.
#オシロのplotterで読むためにヘッダー行を適当に入れれるようにしている.

#CSVデータを読む関数.
def read_csv(file_path,skiprow):
    if not os.path.isfile(file_path):#指定したパスがファイルかどうかを確認する
        print("this is not file pass")
        return -1,-1
    elif not os.path.exists(file_path):#指定したパスがファイルかどうかを確認する
        print("no such file")
        return -1,-1
    else:
        with open(file_path, encoding='utf8', newline='') as f:
            csvreader = csv.reader(f, delimiter='\t')
            matans=[]
            i=0
            for row in csvreader:
                if i>skiprow-1:
                    ans_num=[float(x) for x in row]
                    matans.append(ans_num)
                else:
                    print(row)
                i+=1
        matans=np.array(matans)#読まれたデータのlistをnumpy 行列に変換.

        matans=np.transpose(matans)#転置すると扱いやすくなる.
        channel_num=len(matans)-1#チャンネル数.
    return matans, channel_num

#----------------------config----------------------
folder_path=r"C:\Users"
file_name="TLine_PTS_v2_150kHz.txt"
file_name_write="TLine_PTS_v2_interp_150kHz.csv"
skiprow=12#書き出すcsvファイルのヘッダー行数.
Fs=5e6#サンプリング周波数.

x_scale=1e6#plot時のスケール.
FigSize=[8,6]#グラフのサイズ.
#--------------------------------------------------

file_path=folder_path+"\\"+file_name
matans, channel_num = read_csv(file_path,1)

timespan=matans[0][-1]-matans[0][0]
data_num=int(timespan*Fs)
time=np.linspace(matans[0][0],matans[0][-1],data_num)
y=[]
for i in range(channel_num):
    y.append(griddata(matans[0], matans[i+1], time, method='linear'))

file_pass_csv_write=folder_path+"\\"+file_name_write
with open(file_pass_csv_write, 'w', newline='') as fil:
    writer = csv.writer(fil)
    writer.writerow([fr"From LTspice. Original file : {file_name}"])
    writer.writerow([fr"fs={Fs}"])
    for i in range(skiprow-2):
        writer.writerow(["a"])
    i=0
    for i in range(data_num):
        y2=[]
        y2.append(time[i])
        for i2 in range(channel_num):
            y2.append(y[i2][i])
        writer.writerow(y2)

fig, ax = plt.subplots(nrows=channel_num, ncols=1, squeeze=False, tight_layout=True, figsize=FigSize, sharex = "col")
ax[0,0].plot(matans[0]*x_scale,matans[1],"k-")
ax[0,0].plot(time*x_scale,y[0],"r-")
if channel_num>1:
    ax[1,0].plot(matans[0]*x_scale,matans[2],"k-")
    ax[1,0].plot(time*x_scale,y[1],"r-")
if channel_num>2:
    ax[2,0].plot(matans[0]*x_scale,matans[3],"k-")
    ax[2,0].plot(time*x_scale,y[2],"r-")
if channel_num>3:
    ax[3,0].plot(matans[0]*x_scale,matans[4],"k-")
    ax[3,0].plot(time*x_scale,y[3],"r-")
if channel_num>4:
    ax[4,0].plot(matans[0]*x_scale,matans[5],"k-")
    ax[4,0].plot(time*x_scale,y[4],"r-")
plt.show()