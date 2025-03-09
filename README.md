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
"CSV_example"内の"SDS00365_downsampled.csv"を読み込み、例えば以下のように左軸にCH1を、右軸にCH2をplotしてみます。  
```
fig, ax = plt.subplots(nrows=1, ncols=1, squeeze=False, tight_layout=True, figsize=FigSize, sharex = "col")
ax[0,0].plot(matans[0]*x_scale,matans[2],"k-")
ax2 = ax[0,0].twinx()#右軸を作る.
ax2.plot(matans[0]*x_scale,matans[1],"r-")
```
すると、  
<img width="602" alt="image" src="https://github.com/user-attachments/assets/b679f73e-a261-4052-8e57-321c4c7f6cc2" />
左右の軸は独立しているので、上図のようにゼロの位置が合わないことがあります。これは軸の上限と下限を設定すれば解決されますが面倒です。そこでここでは、matplotlibの機能で修正してみます。まず、以下の図の青矢印のボタンを押すと、このようなウィンドウが出ます。  
<img width="600" alt="image" src="https://github.com/user-attachments/assets/a8a78076-9811-4fdf-88bd-982c49309006" />
ここでどの軸を編集するかを選択できます。右軸を選択し（どっちが右がわかりませんが）、  
<img width="592" alt="image" src="https://github.com/user-attachments/assets/171d735f-aa5c-43d2-9d6b-cb53ac9a863b" />
"Y-Axis"のMin, Max を設定できます。例えばこの例では-150, 150とすると、  
<img width="602" alt="image" src="https://github.com/user-attachments/assets/72d5b1b8-8a6e-4cc0-8900-9eb94bbfe52f" />
見やすくなりました。GUIで設定できるのは便利！  
  
バグ・質問などあればTwitterにて報告ください。とくにFFTは数値の確かさに関して自信がありません。：@Testes_int
