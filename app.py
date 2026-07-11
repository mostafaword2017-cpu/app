
import streamlit as st
import math

# 1. Page Configuration
st.set_page_config(page_title="ElectroCalc M&F", page_icon="⚡️", layout="centered")

# 2. Optimized Styles for Mobile & English Tabs
st.markdown("""
    <style>
    / وسط چین کردن تیترها و اسم نرم افزار /
    h1, h2, h3 {
        text-align: center !important;
    }

    / وسط چین کردن دکمه‌های تب‌ها /
    .stTabs {
        display: flex !important;
        justify-content: center !important;
    }
    div[data-testid="stTabs"] {
        display: flex !important;
        justify-content: center !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)


    <style>
    / Hide Streamlit header elements /
    header div[data-testid="stHeader"] a, 
    div[data-testid="stAppDeployButton"], 
    #MainMenu {
        display: none !important;
    }

    / Optimize Title for Mobile /
css
    / استایل پیش‌فرض برای لپ‌تاپ و تبلت /
    .stApp h1 {
        font-size: 16px !important; 
        text-align: center !important;
        white-space: nowrap !important;
    }

    / استایل مخصوص گوشی‌های موبایل (صفحات زیر 640 پیکسل) /
    @media screen and (max-width: 640px) {
        .stApp h1 {
            font-size: 10px !important; / اندازه فونت در موبایل خیلی کوچک شد تا نشکند /
            letter-spacing: -1px !important;
        }
    }
    / Label and Markdown fonts /
    label, .stMarkdown p {
        font-size: 14px !important;
    }
    @media screen and (max-width: 640px) {
        label, .stMarkdown p {
            font-size: 12px !important;
        }
    }

    / TABS STYLE - Forced to be English & Compact /
    .stTabs div[role="tablist"] { 
        gap: 5px !important; 
        flex-wrap: nowrap !important; 
        overflow-x: auto !important;
    }
    .stTabs [role="tab"] {
        font-size: 13px !important;
        padding: 8px 10px !important;
        border-radius: 8px 8px 0px 0px !important;
        background-color: #f0f2f6 !important;
        white-space: nowrap !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50 !important; 
        color: white !important;
    }

    / Buttons Styling /
    .stButton > button {
        width: 100% !important;
        height: 50px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        background-color: #007BFF !important;
        color: white !important;
    }

    / Result Boxes /
    .result-box {
        text-align: center;
        padding: 15px;
        border-radius: 15px;
        background-color: #f1f3f4;
        border: 2px solid #3c4043;
        margin: 15px 0;
    }
    .result-text {
        font-size: 18px !important;
        font-weight: bold !important;
        color: #1a73e8;
        margin-bottom: 5px;
        word-wrap: break-word;
    }
    @media screen and (max-width: 640px) {
        .result-text {
            font-size: 15px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- Backend Calculation Functions ---
# ==============================================================================


import math

def calculate_cable_fixed(p_kw, length, sigma, voltage=380, max_drop_percent=2):
    # ۱. تبدیل توان به وات و محاسبه جریان نامی (با فرض بهره ۰.۸)
    p_watts = p_kw * 1000
    cos_phi = 0.8 
    current = p_watts / (math.sqrt(3) * voltage * cos_phi)
    
    # ۲. محاسبه سطح مقطع بر اساس افت ولتاژ
    try:
        # فرمول: Area = (P * L * 100) / (sigma * V^2 * deltaV%)
        area_voltage_drop = (p_watts * length * 100) / (sigma * (voltage**2) * max_drop_percent)
    except ZeroDivisionError: 
        return 0, "Error", "Error", 0

    # ۳. تعیین حداقل سطح مقطع بر اساس تحمل جریان (برای جلوگیری از ذوب شدن کابل)
    # جدول: (حداکثر جریان مجاز -> سایز کابل)
    current_capacity_table = [
        (15, 1.5), (22, 2.5), (32, 4), (45, 6), 
        (65, 10), (100, 16), (150, 25), (200, 35), 
        (260, 50), (320, 70), (380, 95), (450, 120)
    ]
    
    min_area_for_current = 1.5
    for limit, size in current_capacity_table:
        if current <= limit:
            min_area_for_current = size
            break
    else: 
        min_area_for_current = 120 # برای جریان‌های بسیار بالا

    # ۴. انتخاب مقدار بزرگتر بین «افت ولتاژ» و «تحمل جریان» برای ایمنی
    final_calc = max(area_voltage_drop, min_area_for_current)

    # ۵. تطبیق با سایزهای استاندارد بازار
    standard_sizes = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300]
    
    suggested_index = -1
    for i, size in enumerate(standard_sizes):
        if size >= final_calc:
            suggested_index = i
            break
    
    if suggested_index == -1: 
        return round(current, 1), "Out of Range", "Out of Range", round(final_calc, 2)
    
    standard_size = standard_sizes[suggested_index]
    
    # ۶. اعمال شرط مسافت ۸۰ متری شما
    if length <= 80:
        # زیر ۸۰ متر: سایز پیشنهادی همان سایز استاندارد است (تغییری نمی‌کند)
        suggested_size = standard_size
    else:
        # بالای ۸۰ متر: سایز پیشنهادی یک پله بالاتر از استاندارد می‌رود
        if suggested_index + 1 < len(standard_sizes):
            suggested_size = standard_sizes[suggested_index + 1]
        else:
            suggested_size = standard_size

    return round(current, 1), standard_size, suggested_size, round(final_calc, 2)
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

def suggest_breaker(current, type_load="Resistive"):
    multiplier = 1.25 if type_load == "Resistive" else 1.5 
    required_current = current * multiplier
    standard_breakers = [6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250]
    suggested = min([x for x in standard_breakers if x >= required_current] or [max(standard_breakers)])
    return suggested
# ==============================================================================
# --- User Interface (UI) ---
# ==============================================================================
st.title("⚡️ ElectroCalc M&F")
# English names for tabs to ensure a clean look on mobile
tabs = st.tabs(["📏 Cable", "🔋 UPS", "⚙️ Motor", "🛡️ Protect"])
# --- Tab 1: Cable ---
with tabs[0]:
    st.header("Cable Section Calculation")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            p_in = st.number_input("Power (kW)", value=85.0, key="p_c")
            l_in = st.number_input("Length (m)", value=90.0, key="l_c")
        with c2:
            s_in = st.number_input("Sigma (Conductivity)", value=56.0, key="s_c")
            d_in = st.number_input("Voltage Drop (%)", value=2.0, key="d_c")
    if st.button("Calculate Cable"):
        curr, f_size, s_size, raw = calculate_cable_fixed(p_in, l_in, s_in, 380, d_in)
        st.latex(r"Area = \frac{P \times L \times 100}{\sigma \times V^2 \times \Delta V\%}")
        st.markdown(f"""<div class='result-box'><div class='result-text'>⚡️ Current: {curr} A</div><div class='result-text' style='color: #1b5e20;'>🎯 Std Size: {f_size} mm²</div><div class='result-text' style='color: #e65100;'>🚀 Safe Size: {s_size} mm²</div><p style='color: #5f6368;'>Exact Calc: {raw} mm²</p></div>""", unsafe_allow_html=True)
# --- Tab 2: UPS ---
with tabs[1]:
    st.header("Battery Capacity Calculation")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            u_kva = st.number_input("UPS Power (kVA)", value=40.0, key="u_kva")
            u_min = st.number_input("Time (min)", value=15, key="u_min")
        with c2:
            u_bat = st.number_input("Number of Batteries", value=32, key="u_bat")
    if st.button("Calculate UPS"):
        res =calculate_ups_fixed(u_kva, u_min, u_bat)
        st.latex(r"Ah_{Final} = \frac{Ah_{Base} \times \frac{kVA}{10} \times 32}{N_{Battery}}")
        st.markdown(f"""<div class='result-box'><div class='result-text'>📦 Battery Cap: {res} Ah</div><div class='result-text' style='color: #0d47a1;'>📌 Required: {u_bat} Units</div></div>""", unsafe_allow_html=True)
# --- Tab 3: Motor ---
with tabs[2]:
    st.header("Electric Motor Calculations")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            m_kva = st.number_input("Apparent Power (kVA)", value=150.0, key="m_kva")
            m_eff = st.number_input("Efficiency (e.g. 0.85)", value=0.85, step=0.01, key="m_eff")
        with c2:
            m_cos = st.number_input("Power Factor (cos φ)", value=0.8, step=0.01, key="m_cos")
            m_vol = st.number_input("Voltage (V)", value=380, key="m_vol")
    if st.button("Calculate Motor"):
        curr, p_in, s_curr, p_kw_out = calculate_motor_from_kva(m_kva, m_eff, m_cos, m_vol)
        st.latex(r"P_{kW} = kVA \times \cos\phi \quad \rightarrow \quad I = \frac{P_{kW} \times 1000}{\eta \times \sqrt{3} \times V \times \cos\phi}")
        st.markdown(f"""<div class='result-box'><div class='result-text'>⚡️ Rated Current: {curr} A</div><div class='result-text'>🚀 Start Current: {s_curr} A</div><div class='result-text' style='color: #1a73e8;'>🔌 Input Power: {p_in} kW</div><div class='result-text'>🎯 Output Power: {p_kw_out} kW</div></div>""", unsafe_allow_html=True)
# --- Tab 4: Protection ---
with tabs[3]:
    st.header("Protection & Breakers")
    with st.container(border=True):
        p_curr = st.number_input("Load Current (A)", value=100.0, key="p_curr")
        p_type = st.selectbox("Load Type", ["Resistive", "Inductive"], key="p_type")
    if st.button("Suggest Breaker"):
        b_size = suggest_breaker(p_curr, p_type)
        st.markdown(f"""<div class='result-box'><div class='result-text'>🛡️ Suggested Breaker: {b_size} A</div><p style='color: #5f6368;'>Based on standard IEC sizing</p></div>""", unsafe_allow_html=True)
