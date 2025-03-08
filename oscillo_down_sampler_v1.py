import oscillo_plotter_func_v1 as osc_func
import numpy as np
import matplotlib.pyplot as plt
import sys
import csv
import os

#サンプリング周波数を下げて別名で保存する.
#---------------------config----------------------
filename='SDS00365.csv'#ファイル名.
filename_write='SDS00365_downsampled.csv'#ダウンサンプリング後のファイル名.
folder_path=r"C:\Users\CSV"#フォルダのパス.
skiprow=12#csvファイルの先頭行数.
x_scale=1e6#横軸のスケール.us->1e6, ms->1e3 etc.

FigSize=[8,6]#グラフのサイズ.
down_sample=10#>1
#-------------------------------------------------

if down_sample<2:
    print("down_sample must be larger than 1")
    sys.exit()
file_path=folder_path+"\\"+filename
if not os.path.isfile(file_path):#指定したパスがファイルかどうかを確認する
    print("this is not file pass")
    sys.exit()
elif not os.path.exists(file_path):#指定したパスがファイルかどうかを確認する
    print("no such file")
    sys.exit()
else:
    with open(file_path, encoding='utf8', newline='') as f:
        csvreader = csv.reader(f, delimiter=',')
        matans=[]
        i=0
        for row in csvreader:
            if i>skiprow-1:
                ans_num=[float(x) for x in row]
                matans.append(ans_num)
            else:
                print(row)
            i+=1

time_ini=matans[0][0]
time_end=matans[-1][0]
num=len(matans)
fs=(num-1)/(time_end-time_ini)

file_pass_csv_write=folder_path+"\\"+filename_write
with open(file_pass_csv_write, 'w', newline='') as fil:
    writer = csv.writer(fil)
    writer.writerow([fr"original file : {filename}"])
    writer.writerow([fr"fs={fs/down_sample}"])
    for i in range(skiprow-2):
        writer.writerow(["a"])
    i=0
    while i<num:
        writer.writerow(matans[i])
        i+=down_sample
