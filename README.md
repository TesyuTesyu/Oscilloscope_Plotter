# 概要
オシロスコープのCSVデータを読んでグラフを作るプログラム。  
いくつかの機能を関数化しているので手軽に使うことができる。  
できること：  
  
1. 時間軸のデータのプロット、微分、積分  
![スクリーンショット 2025-03-08 205535](https://github.com/user-attachments/assets/d1a6c300-bd35-4be5-bd68-382806b7ebd5)
  
2. FFT  
![スクリーンショット 2025-03-08 205327](https://github.com/user-attachments/assets/71b0bd59-3412-4cea-b339-73f99ac780b8)
  
3. スペクトログラム  
![スクリーンショット 2025-03-08 205153](https://github.com/user-attachments/assets/25009463-b1a5-4834-97de-0fcf63576d03)
  
# 動作環境：  
VS code (matplotlibのGUIが優秀)  
  
# 使い方：  
全てのプログラムファイルを同じフォルダに入れて実行する。関数は"oscillo_plotter_func_v1.py"にまとめられている。  
  
# 補足：  
"CSV_example"内の"SDS00365_downsampled.csv"を読み込み、例えば以下のように左軸にCH1を、右軸にCH2をplotしてみる。  
```
fig, ax = plt.subplots(nrows=1, ncols=1, squeeze=False, tight_layout=True, figsize=FigSize, sharex = "col")
ax[0,0].plot(matans[0]*x_scale,matans[2],"k-")
ax2 = ax[0,0].twinx()#右軸を作る.
ax2.plot(matans[0]*x_scale,matans[1],"r-")
```
