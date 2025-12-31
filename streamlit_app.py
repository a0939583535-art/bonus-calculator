import streamlit as st
from datetime import date
import calendar

st.set_page_config(page_title="通用年終獎金計算器", page_icon="🧧")

st.title("🧧 通用年終獎金計算器")
st.write("輸入資訊後，可自由選擇是否扣除二代健保與預扣所得稅。")

# --- 側邊欄：基本參數 ---
with st.sidebar:
    st.header("⚙️ 基本參數")
    salary = st.number_input("您的月薪 (TWD)", min_value=0, value=50000, step=1000)
    months = st.number_input("獎金月數", min_value=0.0, value=2.0, step=0.1)
    
    st.divider()
    st.header("📝 扣款選項")
    # 加入勾選框
    use_nhi = st.checkbox("扣除二代健保 (2.11%)", value=False, help="單次給付超過 2 萬元時需扣除")
    use_tax = st.checkbox("預扣所得稅 (5%)", value=False, help="單次給付超過 88,501 元時通常會預扣")

# --- 主畫面：日期設定 ---
st.subheader("📅 日期設定")
col_d1, col_d2 = st.columns(2)

with col_d1:
    hire_date = st.date_input("到職日期", value=date(2025, 1, 1))

# 預設結算日為到職當年的 12/31
calc_year = hire_date.year
with col_d2:
    end_date = st.date_input("獎金結算截止日", value=date(calc_year, 12, 31))

# --- 計算邏輯 ---
if st.button("🚀 開始試算金額"):
    if hire_date > end_date:
        st.error("❌ 錯誤：到職日期不能晚於結算日期！")
    else:
        # 1. 計算在職比例
        is_leap = calendar.isleap(end_date.year)
        total_days_in_year = 366 if is_leap else 365
        start_of_year = date(end_date.year, 1, 1)
        
        if hire_date < start_of_year:
            days_worked = total_days_in_year
            ratio = 1.0
        else:
            days_worked = (end_date - hire_date).days + 1
            ratio = days_worked / total_days_in_year

        # 2. 計算總額 (應發獎金)
        gross_bonus = salary * months * ratio
        
        # 3. 處理扣項
        nhi_fee = 0
        tax_fee = 0
        
        # 二代健保：單次領取需大於 20,000 才扣 (依照法規)
        if use_nhi and gross_bonus >= 20000:
            nhi_fee = gross_bonus * 0.0211
            
        # 預扣所得稅：單次領取需大於 88,501 才扣 (依照 2025 標準)
        if use_tax and gross_bonus > 88501:
            tax_fee = gross_bonus * 0.05
            
        net_bonus = gross_bonus - nhi_fee - tax_fee

        # --- 結果顯示 ---
        st.divider()
        st.balloons()
        
        st.success(f"### 預估實領金額： ${int(net_bonus):,}")
        
        # 使用欄位顯示詳細拆解
        c1, c2, c3 = st.columns(3)
        c1.metric("應發總額", f"${int(gross_bonus):,}")
        c2.metric("在職天數", f"{days_worked} 天")
        c3.metric("在職比例", f"{ratio:.2%}")
        
        # 如果有扣款，顯示扣款明細
        if nhi_fee > 0 or tax_fee > 0:
            st.info(f"📋 **扣款明細：**\n"
                    f"- 二代健保 (2.11%): -${int(nhi_fee):,}\n"
                    f"- 預扣所得稅 (5%): -${int(tax_fee):,}")
        else:
            st.caption("註：目前未扣除任何稅費，此為稅前總額。")