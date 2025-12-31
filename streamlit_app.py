import streamlit as st
from datetime import date

st.set_page_config(page_title="2025 年終計算器", page_icon="🧧")

st.title("🧧 2025 年終獎金計算器")
st.write("輸入資訊後，系統會自動按 2025 年在職比例試算金額。")

# --- 輸入區 ---
salary = st.number_input("月薪 (TWD)", min_value=0, value=50000, step=1000)
months = st.number_input("獎金月數", min_value=0.0, value=2.0, step=0.1)
hire_date = st.date_input("到職日期", value=date(2025, 1, 1))

# --- 計算邏輯 ---
if st.button("點我計算"):
    target_year = 2025
    end_of_year = date(target_year, 12, 31)
    start_of_year = date(target_year, 1, 1)

    # 驗證邏輯
    if hire_date > end_of_year:
        st.warning("⚠️ 到職日期晚於 2025 年底，今年無年終。")
        ratio = 0
        days_worked = 0
    else:
        if hire_date <= start_of_year:
            days_worked = 365
            ratio = 1.0
        else:
            days_worked = (end_of_year - hire_date).days + 1
            ratio = days_worked / 365

        total_bonus = salary * months * ratio

        # --- 結果顯示 ---
        st.balloons() # 撒花特效
        st.divider()
        st.subheader(f"💰 預計年終：${int(total_bonus):,}")
        
        col1, col2 = st.columns(2)
        col1.metric("2025 在職天數", f"{days_worked} 天")
        col2.metric("領取比例", f"{ratio:.2%}")