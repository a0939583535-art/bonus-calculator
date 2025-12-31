import streamlit as st
from datetime import date
import calendar

st.set_page_config(page_title="通用年終獎金計算器", page_icon="🧧")

st.title("🧧 通用年終獎金計算器")

# --- 側邊欄變更點：加入勾選按鈕 ---
with st.sidebar:
    st.header("⚙️ 基本參數")
    salary = st.number_input("您的月薪 (TWD)", min_value=0, value=50000, step=1000)
    months = st.number_input("獎金月數", min_value=0.0, value=2.0, step=0.1)
    
    st.divider()
    st.header("📝 扣款選項 (新增)")
    # 【變更點 1：使用者勾選介面】
    use_nhi = st.checkbox("扣除二代健保 (2.11%)", value=False)
    use_tax = st.checkbox("預扣所得稅 (5%)", value=False)

# --- 主畫面 ---
st.subheader("📅 日期設定")
col_d1, col_d2 = st.columns(2)
with col_d1:
    hire_date = st.date_input("到職日期", value=date(2025, 1, 1))
with col_d2:
    end_date = st.date_input("獎金結算截止日", value=date(hire_date.year, 12, 31))

if st.button("🚀 開始試算金額"):
    if hire_date > end_date:
        st.error("❌ 錯誤：到職日期不能晚於結算日期！")
    else:
        # 計算比例
        is_leap = calendar.isleap(end_date.year)
        total_days_in_year = 366 if is_leap else 365
        start_of_year = date(end_date.year, 1, 1)
        days_worked = (end_date - max(hire_date, start_of_year)).days + 1
        ratio = min(days_worked / total_days_in_year, 1.0)

        # 【變更點 2：扣款計算邏輯】
        gross_bonus = salary * months * ratio
        nhi_fee = 0
        tax_fee = 0
        
        # 判定是否達到扣款門檻 (2025標準)
        if use_nhi and gross_bonus >= 20000:
            nhi_fee = gross_bonus * 0.0211
        if use_tax and gross_bonus > 88501:
            tax_fee = gross_bonus * 0.05
            
        final_bonus = gross_bonus - nhi_fee - tax_fee

        # --- 結果顯示 ---
        st.divider()
        st.success(f"### 預估實領金額： ${int(final_bonus):,}")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("應發總額 (稅前)", f"${int(gross_bonus):,}")
        c2.metric("在職比例", f"{ratio:.2%}")
        c3.metric("總扣除額", f"-${int(nhi_fee + tax_fee):,}")

        if nhi_fee > 0 or tax_fee > 0:
            st.warning(f"明細：二代健保 -${int(nhi_fee):,} / 所得稅 -${int(tax_fee):,}")