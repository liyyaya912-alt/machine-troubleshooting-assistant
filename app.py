import re

import streamlit as st


MANUFACTURING_KEYWORDS = [
    "機台",
    "產線",
    "設備",
    "輸送帶",
    "馬達",
    "伺服",
    "壓力",
    "氣缸",
    "感應器",
    "sensor",
    "plc",
    "cnc",
    "沖床",
    "射出",
    "包裝",
    "貼標",
    "焊接",
    "烘箱",
    "泵浦",
    "閥",
    "軸承",
    "皮帶",
    "治具",
    "夾具",
    "robot",
    "robot arm",
    "機械手",
]

NON_MANUFACTURING_KEYWORDS = [
    "excel",
    "word",
    "powerpoint",
    "網頁",
    "網站",
    "手機",
    "app",
    "電腦",
    "筆電",
    "印表機",
    "wifi",
    "路由器",
    "財務系統",
    "erp",
    "email",
    "信箱",
    "windows",
    "browser",
    "chrome",
]

MECHANICAL_KEYWORDS = [
    "卡料",
    "異音",
    "震動",
    "皮帶",
    "軸承",
    "磨損",
    "堵塞",
    "偏移",
    "鬆動",
    "斷裂",
    "夾料",
    "刮傷",
    "機構",
    "輸送",
]

ELECTRICAL_KEYWORDS = [
    "sensor",
    "感應器",
    "伺服",
    "馬達",
    "過載",
    "過熱",
    "電流",
    "電壓",
    "plc",
    "io",
    "i/o",
    "訊號",
    "斷線",
    "短路",
    "變頻器",
    "driver",
    "alarm",
    "警報",
]

OPERATION_KEYWORDS = [
    "參數",
    "設定",
    "未歸零",
    "歸零",
    "配方",
    "recipe",
    "操作",
    "模式",
    "手動",
    "自動",
    "數值",
    "超出",
    "未啟動",
    "未復歸",
]


def normalize_text(*values: str) -> str:
    """將使用者輸入合併並轉小寫，方便後續關鍵字判斷。"""
    return " ".join(value.strip().lower() for value in values if value)


def has_keyword(text: str, keywords: list[str]) -> bool:
    """檢查輸入內容是否命中任一關鍵字。"""
    return any(keyword.lower() in text for keyword in keywords)


def validate_trigger(machine_name: str, error_code: str, abnormal_desc: str) -> tuple[bool, str]:
    """觸發檢查：確認必填欄位與製造業實體機台情境。"""
    if not machine_name.strip() or not error_code.strip():
        return False, "請至少輸入「機台名稱/類型」與「錯誤代碼」，才能啟動排查流程。"

    combined_text = normalize_text(machine_name, error_code, abnormal_desc)

    if has_keyword(combined_text, NON_MANUFACTURING_KEYWORDS):
        return False, "此工具僅支援製造業實體機台異常排查，不處理軟體、手機、網頁或辦公系統問題。"

    if not has_keyword(combined_text, MANUFACTURING_KEYWORDS):
        return False, "請確認輸入內容包含製造業機台或產線設備資訊，例如：輸送帶、馬達、CNC、PLC、感應器等。"

    return True, ""


def classify_issue(machine_name: str, error_code: str, abnormal_desc: str) -> str:
    """分類：依錯誤代碼與異常現象自動判斷故障可能類別。"""
    combined_text = normalize_text(machine_name, error_code, abnormal_desc)

    scores = {
        "機械問題": sum(keyword.lower() in combined_text for keyword in MECHANICAL_KEYWORDS),
        "電氣控制問題": sum(keyword.lower() in combined_text for keyword in ELECTRICAL_KEYWORDS),
        "人為操作問題": sum(keyword.lower() in combined_text for keyword in OPERATION_KEYWORDS),
    }

    error_code_upper = error_code.strip().upper()
    if re.search(r"(M|MECH|BELT|JAM|LOAD)", error_code_upper):
        scores["機械問題"] += 2
    if re.search(r"(E|ELEC|SV|SERVO|PLC|IO|OL|OC|OH)", error_code_upper):
        scores["電氣控制問題"] += 2
    if re.search(r"(P|PARA|SET|ZERO|OP|MODE)", error_code_upper):
        scores["人為操作問題"] += 2

    return max(scores, key=scores.get)


def build_safety_checks(issue_type: str) -> list[str]:
    """引導式安全檢查：在復歸前提供現場安全確認動作。"""
    common_check = "確認現場人員已離開可動機構範圍，必要時執行 LOTO 上鎖掛牌，並確認急停按鈕狀態。"

    checks_by_type = {
        "機械問題": [
            common_check,
            "確認輸送路徑、治具與防護門內無卡料、掉料或異物，且安全護罩已正確關閉。",
        ],
        "電氣控制問題": [
            common_check,
            "確認主電源、控制電源與氣源壓力在允收範圍內，並檢查安全光柵或門鎖訊號是否正常。",
        ],
        "人為操作問題": [
            common_check,
            "確認目前機台模式、產品配方與參數版本正確，且原點復歸條件已滿足。",
        ],
    }

    return checks_by_type[issue_type]


def build_sop(issue_type: str) -> list[str]:
    """復歸 SOP：依分類輸出 3 個標準復歸步驟。"""
    sop_by_type = {
        "機械問題": [
            "停機並確認能量隔離後，清除卡料或異物，檢查皮帶、治具、軸承與限位機構是否鬆動或磨損。",
            "關閉安全門與護罩，解除急停，於 HMI 清除警報並執行單動或寸動確認機構動作順暢。",
            "切換低速試運轉 3-5 分鐘，確認無異音、無偏移、無再次卡料後，再恢復自動生產。",
        ],
        "電氣控制問題": [
            "停機後確認電控箱無異味、焦痕或異常高溫，檢查感應器、線束、端子與伺服/變頻器警報狀態。",
            "排除鬆脫或遮擋問題後，復歸安全迴路，於 HMI 或控制器清除 Alarm，必要時重新原點復歸。",
            "以手動模式測試 I/O、馬達與感應器訊號，再以低速自動循環確認警報不再發生。",
        ],
        "人為操作問題": [
            "確認產品型號、工單、配方與參數版本是否一致，將超出合理範圍的設定值調回標準值。",
            "依機台作業標準書重新執行原點復歸、模式切換與啟動前點檢，並清除 HMI 警報。",
            "先執行首件確認或短循環試產，確認尺寸、節拍與良率穩定後，再交回量產。",
        ],
    }

    return sop_by_type[issue_type]


def build_preventive_action(issue_type: str) -> str:
    """預防建議：提供符合 Lean 或 TPM 的維護管理建議。"""
    actions_by_type = {
        "機械問題": "將易卡料點、皮帶張力、治具定位與軸承異音納入 TPM 每日自主保養點檢表，並用目視化標準標示正常範圍。",
        "電氣控制問題": "建立感應器清潔、線束固定、端子鬆動與伺服警報履歷的週期性 PM 檢查，並用 Pareto 分析追蹤高頻 Alarm。",
        "人為操作問題": "將配方切換與參數確認設計成首件前 Check Sheet，並用防呆欄位限制超規參數輸入，降低換線失誤。",
    }

    return actions_by_type[issue_type]


def format_report(machine_name: str, error_code: str, abnormal_desc: str, issue_type: str) -> str:
    """格式化輸出：組成機台異常排查與處置報告。"""
    safety_checks = build_safety_checks(issue_type)
    sop_steps = build_sop(issue_type)
    preventive_action = build_preventive_action(issue_type)
    description = abnormal_desc.strip() or "未提供，請現場人員補充異音、燈號、停機位置或 HMI 訊息。"

    return f"""
# 🚨 【機台異常排查與處置報告】

## 一、 異常現況與初步分類
* **通報機台/代碼**：{machine_name.strip()} / {error_code.strip()}
* **現場異常現象**：{description}
* **故障可能類別**：{issue_type}

## 二、 現場引導檢查確認（請依序確認）
1. 🛠️ **步驟一**：{safety_checks[0]}
2. 🛠️ **步驟二**：{safety_checks[1]}

## 三、 排除復歸步驟 (SOP)
* **復歸程序**：
  1. {sop_steps[0]}
  2. {sop_steps[1]}
  3. {sop_steps[2]}
* **💡 預防性維護建議**：{preventive_action}
"""


st.set_page_config(
    page_title="產線機台異常排查與復歸智慧助理",
    page_icon="🚨",
    layout="centered",
)

st.title("🚨 產線機台異常排查與復歸智慧助理")
st.caption("Industrial Management / Troubleshooting / TPM Recovery Assistant")

with st.container(border=True):
    st.subheader("異常通報資訊")
    machine_name = st.text_input(
        "機台名稱 / 類型",
        placeholder="例：A03 輸送帶、CNC-02、包裝機、PLC 控制站",
    )
    error_code = st.text_input(
        "錯誤代碼（Error Code）",
        placeholder="例：E-214、SV-OL、JAM-01、P-ZERO",
    )
    abnormal_desc = st.text_area(
        "現場異常現象簡述",
        placeholder="例：輸送帶卡料後停機，HMI 顯示馬達過載，現場有異音。",
        height=130,
    )

if st.button("開始智慧排查診斷", type="primary", use_container_width=True):
    is_valid, error_message = validate_trigger(machine_name, error_code, abnormal_desc)

    if not is_valid:
        st.error(error_message)
    else:
        issue_type = classify_issue(machine_name, error_code, abnormal_desc)
        report = format_report(machine_name, error_code, abnormal_desc, issue_type)
        st.markdown(report)
        st.info("提醒：若涉及高壓、高溫、旋轉機構或安全迴路異常，請由合格設備工程師或電控人員執行復歸。")
