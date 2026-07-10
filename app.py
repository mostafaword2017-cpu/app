
import streamlit as st
import math

# ۱. تنظیمات اولیه صفحه
st.set_page_config(page_title="ElectroCalc M&F", page_icon="⚡️", layout="centered")

# ۲. استایل‌های بهینه برای حذف لینک‌های خارجی و اصلاح فونت موبایل
st.markdown("""
    <style>
    css
    / راست‌چین کردن کلی /
    .main, .stApp, [data-testid="stAppViewContainer"] { 
        direction: rtl !important; 
        text-align: right !important; 
    }

    / حذف گربه و فورک /
    header a, 
    [data-testid="stHeaderDevelopmentMode"], 
    [data-testid="stHeaderShareButton"], 
    div[data-testid="stAppDeployButton"] {
        display: none !important;
    }

    / --- فیکس کردن تب‌ها با اندازه مشابه عنوان --- /
    / این بخش تمام لایه‌های تب را هدف قرار می‌دهد /
    .stTabs [role="tab"], 
    .stTabs button, 
    .stTabs div[data-testid="stHorizontalBlock"] {
        font-size: 14px !important; / اندازه را مشابه عنوان قرار دادم /
        white-space: nowrap !important; 
        padding: 2px 5px !important;
    }

    / حذف حاشیه اضافی تب‌ها برای اینکه در موبایل جا شوند /
    .stTabs [role="tablist"] { 
        gap: 2px !important; 
        direction: rtl !important; 
    }

    / دکمه‌های آبی و گرد /
    .stButton > button { 
        width: 100% !important; 
        height: 50px !important; 
        border-radius: 12px !important; 
        background-color: #007BFF !important; 
        color: white !important; 
        font-weight: bold !important; 
    }

    / ورودی‌ها و نتایج /
    input { direction: ltr !important; text-align: center !important; }
    .result-box { text-align: center; padding: 15px; border-radius: 15px; background-color: #f8f9fa; border: 1px solid #ddd; }
    .result-text { font-size: 16px !important; font-weight: bold; color: #1a73e8; }
    </style>
    """, unsafe_allow_html=True)
# ==============================================================================
# --- توابع محاسباتی (Backend) ---
# ==============================================================================
def calculate_cable_fixed(p_kw, length, sigma, voltage=380, max_drop_percent=2):
    p_watts = p_kw * 1000
    try:
        calculated_area = (p_watts * length * 100) / (sigma * (voltage**2) * max_drop_percent)
    except ZeroDivisionError: return 0, 0, 0, 0
    current = p_watts / (math.sqrt(3) * voltage * 0.8)
    standard_sizes = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300]
    suggested_index = -1
    for i, size in enumerate(standard_sizes):
        if size >= calculated_area:
            suggested_index = i
            break
    if suggested_index == -1: 
        return round(current, 1), "خارج از محدوده", "خارج از محدوده", round(calculated_area, 2)
    final_size = standard_sizes[suggested_index]
    safe_size = standard_sizes[suggested_index + 1] if suggested_index + 1 < len(standard_sizes) else final_size
    return round(current, 1), final_size, safe_size, round(calculated_area, 2)

def calculate_ups_fixed(load_kva, backup_min, num_batteries):
    base_data = {10: 7, 20: 12, 30: 18, 40: 23, 50: 28, 60: 32}
    minutes_list = sorted(base_data.keys())
    if backup_min <= minutes_list[0]: base_ah = base_data[minutes_list[0]]
    elif backup_min >= minutes_list[-1]: base_ah = base_data[60]  (backup_min / 60)
    else:
        for i in range(len(minutes_list)-1):
            m1, m2 = minutes_list[i], minutes_list[i+1]
            if m1 <= backup_min <= m2:
                a1, a2 = base_data[m1], base_data[m2]
                base_ah = a1 + ((a2 - a1) * (backup_min - m1) / (m2 - m1))
                break
    return round((base_ah * (load_kva / 10) * 32) / num_batteries, 1)

def calculate_motor_from_kva(p_kva, eff=0.85, cos_phi=0.8, voltage=380):
    p_kw_out = p_kva * cos_phi
    p_kw_in = p_kw_out / eff
    current = (p_kw_in * 1000) / (math.sqrt(3) * voltage * cos_phi)
    starting_current = current * 6
    return round(current, 2), round(p_kw_in, 2), round(starting_current, 2), round(p_kw_out, 2)
def suggest_breaker(current, type_load="مقاومتی"):
    multiplier = 1.25 if type_load == "مقاومتی" else 1.5 
    required_current = current * multiplier
    standard_breakers = [6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250]
    suggested = min([x for x in standard_breakers if x >= required_current] or [max(standard_breakers)])
    return suggested
# ==============================================================================
# --- رابط کاربری (UI) ---
# ==============================================================================
st.title("⚡️ ElectroCalc M&F")
tabs = st.tabs(["🔌 کابل", "🔋 UPS", "⚙️ موتور", "🛡️ حفاظتی"])
# --- تب اول: کابل ---
with tabs[0]:
    st.header("📏 محاسبه سطح مقطع (افت ولتاژ)")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            p_in = st.number_input("توان مصرفی (kW)", value=85.0, key="p_c")
            l_in = st.number_input("طول مسیر (متر)", value=90.0, key="l_c")
        with c2:
            s_in = st.number_input("ضریب رسانایی (Sigma)", value=56.0, key="s_c")
            d_in = st.number_input("درصد افت ولتاژ (%)", value=2.0, key="d_c")
    if st.button("شروع محاسبه کابل"):
        curr, f_size, s_size, raw = calculate_cable_fixed(p_in, l_in, s_in, 380, d_in)
        st.latex(r"Area = \frac{P \times L \times 100}{\sigma \times V^2 \times \Delta V\%}")
        st.markdown(f"""<div class='result-box'><div class='result-text'>⚡️ جریان تخمینی: {curr} آمپر</div><div class='result-text' style='color: #1b5e20;'>🎯 سایز استاندارد: {f_size} mm²</div><div class='result-text' style='color: #e65100;'>🚀 سایز پیشنهادی (Safe): {s_size} mm²</div><p style='color: #5f6368;'>عدد دقیق محاسباتی: {raw} mm²</p></div>""", unsafe_allow_html=True)
# --- تب دوم: یو پی اس ---
with tabs[1]:
    st.header("🔋 محاسبه ظرفیت باتری")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            u_kva = st.number_input("توان یو پی اس (kVA)", value=40.0, key="u_kva")
            u_min = st.number_input("زمان (دقیقه)", value=15, key="u_min")
        with c2:
            u_bat = st.number_input("تعداد باتری", value=32, key="u_bat")
    if st.button("محاسبه یو پی اس"):
        res = calculate_ups_fixed(u_kva, u_min, u_bat)
        st.latex(r"Ah_{Final} = \frac{Ah_{Base} \times \frac{kVA}{10} \times 32}{N_{Battery}}")
        st.markdown(f"""<div class='result-box'><div class='result-text'>📦 ظرفیت هر باتری: {res} Ah</div><div class='result-text' style='color: #0d47a1;'>📌 نیاز به {u_bat} عدد باتری</div></div>""", unsafe_allow_html=True)
# --- تب سوم: موتور ---
with tabs[2]:
    st.header("⚙️ محاسبات موتورهای الکتریکی")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            m_kva = st.number_input("توان ظاهری موتور (kVA)", value=150.0, key="m_kva")
            m_eff = st.number_input("راندمان (مثلاً 0.85)", value=0.85, step=0.01, key="m_eff")
        with c2:
            m_cos = st.number_input("ضریب توان (cos φ)", value=0.8, step=0.01, key="m_cos")
            m_vol = st.number_input("ولتاژ (V)", value=380, key="m_vol")
    if st.button("محاسبه مشخصات موتور"):
        curr, p_in, s_curr, p_kw_out = calculate_motor_from_kva(m_kva, m_eff, m_cos, m_vol)
        st.latex(r"P_{kW} = kVA \times \cos\phi \quad \rightarrow \quad I = \frac{P_{kW} \times 1000}{\eta \times \sqrt{3} \times V \times \cos\phi}")
        st.markdown(f"""<div class='result-box'><div class='result-text'>⚡️ جریان نامی: {curr} آمپر</div><div class='result-text' style='color: #D32F2F;'>🚀 جریان استارت (تقریبی): {s_curr} آمپر</div><div class='result-text' style='color: #388E3C;'>📈 توان فعال (خروجی): {p_kw_out} kW</div><div class='result-text' style='color: #1a73e8;'>🔌 توان ورودی واقعی: {p_in} kW</div></div>""", unsafe_allow_html=True)
# --- تب چهارم: حفاظتی ---
with tabs[3]:
    st.header("🛡️ انتخاب تجهیزات حفاظتی")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            b_curr = st.number_input("جریان نامی بار (آمپر)", value=161.0, key="b_curr")
            b_type = st.selectbox("نوع بار", ["مقاومتی", "موتوری/سلفی"], key="b_type")
        with c2:
            st.info("سیستم بر اساس ضریب ایمنی استاندارد (1.25 تا 1.5) محاسبه می‌کند.")
    if st.button("پیشنهاد کلید حفاظتی"):
        suggested_b = suggest_breaker(b_curr, b_type)
        multiplier_text = "1.25" if b_type == "مقاومتی" else "1.5"
        st.latex(f"I_{{breaker}} \geq I_{{load}} \times {multiplier_text}")
        st.markdown(f"""<div class='result-box'><div class='result-text'>🎯 کلید پیشنهادی: {suggested_b} آمپر</div><div class='result-text' style='color: #7B1FA2;'>🛡️ نوع پیشنهادی: MCB / MCCB</div></div>""", unsafe_allow_html=True)
