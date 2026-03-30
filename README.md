
這是一個使用 Python `tkinter` 與 `serial` 撰寫的圖形化介面程式。透過序列埠接收來自 Arduino 的資料，即時監控 6 組電池的電壓，並計算 EPS（Electrical Power System）的總電壓。

同時顯示 6 組電池的即時電壓狀態。
電壓上升：數值變為紅色。
電壓下降：數值變為綠色。
電池安全警報:
當電壓 < 3.0V 時，顯示 ` Low` 警告。
當電壓 > 4.25V 時，顯示 ` High` 警告。
EPS 總電壓監控:
自動加總 Battery 4、5、6 的電壓作為 EPS 總電壓。
總電壓 < 24.0V 顯示 ` Undervoltage` (欠壓)。
總電壓 > 26.0V 顯示 ` Overvoltage` (過壓)。

