# 產線機台異常排查與復歸智慧助理

這是一個使用 Streamlit 製作的製造業現場機台異常排查工具，協助操作員、設備工程師或生管人員在產線發生 Alarm、停機、卡料、馬達過載、感應器異常等狀況時，依照工業管理實務快速完成初步判斷、安全確認與復歸 SOP。

## 專案目標

本工具以 Industrial Management、Troubleshooting、TPM 與 Lean Management 的現場實務為基礎，將機台異常處理流程標準化，降低排查時的資訊落差與復歸風險。

## 主要功能

- 輸入機台名稱、錯誤代碼與現場異常現象
- 自動攔截非製造業或非實體機台問題
- 自動分類異常類型：
  - 機械問題
  - 電氣控制問題
  - 人為操作問題
- 先輸出現場安全確認動作
- 產生 3 步驟標準復歸 SOP
- 提供 Lean / TPM 預防性維護建議

## 使用情境

適合用於以下製造現場情境：

- 輸送帶卡料
- 馬達過載或過熱
- 感應器訊號異常
- PLC / I/O Alarm
- 機台未歸零
- 參數或配方設定錯誤
- 包裝機、CNC、射出機、貼標機、機械手等設備異常

## 線上使用方式

部署到 Streamlit Community Cloud 後，使用者只要開啟公開網址即可使用。

操作步驟：

1. 輸入機台名稱或類型，例如：`A03 輸送帶`
2. 輸入錯誤代碼，例如：`E-214`
3. 輸入現場異常現象，例如：`輸送帶卡料後停機，HMI 顯示馬達過載`
4. 點擊「開始智慧排查診斷」
5. 系統會產生「機台異常排查與處置報告」

## 本機執行方式

先安裝套件：

```bash
pip install -r requirements.txt
```

啟動 Streamlit：

```bash
streamlit run app.py
```

開啟瀏覽器：

```text
http://localhost:8501
```

## Streamlit Cloud 部署設定

部署時請使用以下設定：

```text
Repository: 你的 GitHub repository
Branch: main
Main file path: app.py
```

## 測試範例

可以使用以下資料測試：

```text
機台名稱 / 類型：A03 輸送帶
錯誤代碼：E-214
現場異常現象：輸送帶卡料後停機，HMI 顯示馬達過載，現場有異音。
```

預期系統會判斷為機械或電氣控制相關異常，並輸出安全檢查、復歸 SOP 與 TPM 預防建議。

## 專案檔案

```text
app.py            Streamlit 主程式
requirements.txt  Python 套件需求
README.md         GitHub 專案說明文件
```

## 注意事項

本工具提供現場初步排查與標準化復歸建議，不取代合格設備工程師、電控人員或廠內安全規範。若涉及高壓、高溫、旋轉機構、安全迴路或人員危害風險，請依公司 EHS 與 LOTO 規範處理。
