import numpy as np
import csv
from scipy.signal import ShortTimeFFT
import os

def make_window_func(window_name, segment_size):
    #今のところnumpy のみ.scipy.signalを使えばもっとある.
    if window_name=='bartlett':
        window=np.bartlett(segment_size)
    elif window_name=='blackman':
        window=np.blackman(segment_size)
    elif window_name=='hamming':
        window=np.hamming(segment_size)
    elif window_name=='hanning':
        window=np.hanning(segment_size)
    elif window_name=='kaiser':
        window=np.kaiser(segment_size)
    elif window_name=='square':
        window=np.ones(segment_size)

    return window

#一部の時間領域を切り取ってfftするやつ.
def f_fft(y, time, window_name, fs, t_start, t_end, dB_min):
    #y : 対象の電圧, time : 時間, window : 窓(長さはt_end-t_start)
    #t_start = np.nan もしくは t_end = np.nan なら初めの時間からもしくは最後の時間までをfftする.
    if np.isnan(t_start):
        n_start=0
    else:
        n_start=int((t_start-time[0])*fs)

    if np.isnan(t_end):
        n_end=int(len(y))
    else:
        n_end=int((t_end-time[0])*fs)

    segment_V = y[n_start:n_end]
    segment_size = n_end-n_start
    freq_min = 1/(segment_size/fs)#周波数の刻み幅.
    final_freq = fs/2
    fin_num_plt = int(final_freq/freq_min)#plotするときのポイント数.
    freq_segment = np.fft.fftfreq(segment_size, d=1/fs)[0:fin_num_plt]#周波数軸のmatrix.
    window = make_window_func(window_name, segment_size)#窓関数.
    windowed_segment_V = segment_V * window
    FV_segment = np.fft.fft(windowed_segment_V) / (segment_size / 2)
    FV_segment=np.abs(FV_segment)
    FV_segment = 20*np.log10(np.fmax(FV_segment[0:fin_num_plt], dB_min))

    return freq_segment, FV_segment#=x, y

#scipy.signalのスペクトログラム.
def f_spectrogram(y, time, window_name, fs, f_min, spectro_division_num, dB_min):
    #spectro_division_num : 時間軸の分割数.
    #dB_min : 答えの最小値（logにするから）.
    hop_time=(time[-1]-time[0])/spectro_division_num
    hop_length=int(hop_time*fs)
    t_period=1/f_min
    fft_num=int(t_period*fs)
    window = make_window_func(window_name, fft_num)
    SFT = ShortTimeFFT(window, hop=hop_length, fs=fs, mfft=fft_num, scale_to='magnitude')
    Sxx = SFT.spectrogram(y)
    N_t = np.arange(Sxx.shape[1])
    matt_for_spectrogram = SFT.delta_t * N_t
    matf_for_spectrogram = SFT.f

    Spec_dB = 20*np.log10(np.fmax(Sxx, dB_min))

    return matt_for_spectrogram, matf_for_spectrogram, Spec_dB#=x, y, z

#CSVデータを読む.
def read_csv(file_path,skiprow):
    if not os.path.isfile(file_path):#指定したパスがファイルかどうかを確認する
        print("this is not file pass")
        return -1,-1
    elif not os.path.exists(file_path):#指定したパスがファイルかどうかを確認する
        print("no such file")
        return -1,-1
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
        matans=np.array(matans)#読まれたデータのlistをnumpy 行列に変換.

        matans=np.transpose(matans)#転置すると扱いやすくなる.
        channel_num=len(matans)-1#チャンネル数.
    return matans, channel_num

#移動平均.
def moving_average(y,move_ave_num):
    if move_ave_num>1:
        size_y=len(y)
        y=np.concatenate([y[0]*np.ones(move_ave_num),y])
        y_new=[]
        for i2 in range(size_y):
            y_new.append(np.sum(y[i2:i2+move_ave_num+1])/(move_ave_num+1))
    else:
        y_new=y
    return y_new

#位相特性が直線的な移動平均 (未来の値を使う。あるポイントの両端int(move_ave_num/2)点数の平均を出す).
def smooth(y,move_ave_num):
    if move_ave_num>1:
        half_move_ave_num=int(move_ave_num/2)
        size_y=len(y)
        y=np.concatenate([y[0]*np.ones(half_move_ave_num),y,y[-1]*np.ones(half_move_ave_num)])
        y_new=[]
        for i2 in range(size_y):
            y_new.append(np.sum(y[i2:i2+move_ave_num+1])/(move_ave_num+1))
    else:
        y_new=y
    return y_new

#不定積分.
def integral(y,fs):
    y0=np.ones(len(y))
    q=np.convolve(y, y0, mode = 'full')[:len(y)]/fs
    return q

#数値微分（差分）.
def diff(y,fs):
    dy=[]
    y_pst=y[0]
    for y0 in y:
        dy.append((y0-y_pst)*fs)
        y_pst=y0
    return dy