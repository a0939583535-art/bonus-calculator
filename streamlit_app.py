import streamlit as st
from datetime import date
import calendar

st.set_page_config(page_title="通用年終獎金計算器", page_icon="💰")

st.title("💰 通用年終獎金計算器")
st.write("不限年份，輸入資訊即可自動試算在職比例與獎金。")

# --- 輸入區 ---
with st.sidebar:
    st.header("參數設定")
    salary = st.number_input("您的月薪 (TWD)", min_value=0, value=50000, step=1000)
    months = st.number_input("獎金月數", min_value=0.0, value=2.0, step=0.1)
    
st.subheader("日期設定")
col_d1, col_d2 = st.columns(2)

with col_d1:
    hire_date = st.date_input("到職日期", value=date(2025, 1, 1))

# 自動抓取到職日的那一年作為結算年
calc_year = hire_date.year
default_end_date = date(calc_year, 12, 31)

with col_d2:
    end_date = st.date_input("獎金結算截止日", value=default_end_date)

# --- 計算邏輯 ---
if st.button("開始試算金額"):
    if hire_date > end_date:
        st.error("❌ 錯誤：到職日期不能晚於結算日期！")
    else:
        # 計算當年總天數 (考慮閏年)
        is_leap = calendar.isleap(end_date.year)
        total_days_in_year = 366 if is_leap else 365
        
        # 判斷是否為當年到職
        start_of_year = date(end_date.year, 1, 1)
        
        if hire_date < start_of_year:
            # 結算年以前就到職了 -> 滿職，領全額
            days_worked = total_days_in_year
            ratio = 1.0
        else:
            # 結算年才到職 -> 按比例
            days_worked = (end_date - hire_date).days + 1
            ratio = days_worked / total_days_in_year

        # 最終計算
        total_bonus = salary * months * ratio

        # --- 結果顯示 ---
        st.divider()
        st.balloons()
        
        st.success(f"### 預計領取金額： ${int(total_bonus):,}")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("結算年度", f"{end_date.year} 年")
        c2.metric("在職天數", f"{days_worked} 天")
        c3.metric("發放比例", f"{ratio:.2%}")
        
        st.info(f"💡 計算基準：{end_date.year} 年總天數為 {total_days_in_year} 天")