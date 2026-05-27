# 智慧產線稼動率與異常排查看板

這是一個以 Streamlit 製作的工業工程（IE）作業二作品，主題為「智慧產線稼動率與異常排查」。

## 功能特色

- 寬螢幕工廠戰情室 Dashboard 版面
- 機台型號與 Alarm Code 下拉選單
- 計劃運轉時間與故障停機時間滑桿
- 自動計算時間稼動率
- Plotly 圓餅圖呈現實際運轉時間與停機時間比例
- AI Skill 風格異常排查與處置報告
- 包含 TPM 預防性維護建議

## 本機執行方式

```bash
pip install -r requirements.txt
streamlit run app.py
```

啟動後開啟：

```text
http://localhost:8501
```

## 主要檔案

- `app.py`：Streamlit 主程式
- `requirements.txt`：部署與安裝所需套件
- `README.md`：專案說明
