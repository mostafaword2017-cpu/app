
import streamlit as st
import math

# ۱. تنظیمات اولیه صفحه
st.set_page_config(page_title="ElectroCalc M&F", page_icon="⚡️", layout="centered")

# ۲. استایل‌های بهینه برای حذف لینک‌های خارجی و اصلاح فونت موبایل
st.markdown("""
    <style>
 
```css
    / ۱. راست‌چین کردن کل برنامه /
    .main, .stApp { direction: rtl; text-align: right; }

    / ۲. حذف هر چیزی در هدر که لینک است یا دکمه (گربه، فورک، Share و غیره) /
    header div[data-testid="stHeader"] a, 
    header a, 
    div[data-testid="stAppDeployButton"],
    div[data-testid="stHeaderDevelopmentMode"],
    div[data-testid="stHeaderShareButton"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }

    / ۳. اجبار به نمایش منوی سه نقطه و تم /
    header div[data-testid="stHeader"] {
        display: flex !important;
    }
    #MainMenu {
        visibility: visible !important;
        display: block !important;
    }

    / ۴. فیکس کردن فونت موبایل /
    h1 { font-size: 22px !important; white-space: nowrap; }
    @media screen and (max-width: 640px) {
        h1 { font-size: 16px !important; }
        .stTabs [role="tab"] { font-size: 11px !important; padding: 5px !important; }
        .result-text { font-size: 14px !important; }
    }

    / ۵. استایل دکمه‌ها و ورودی‌ها /
    .stButton > button { 
        width: 100%; height: 50px; font-size: 18px !important; 
        border-radius: 12px; background-color: #007BFF !important; color: white !important; 
        font-weight: bold; 
    }
    input { direction: ltr !important; text-align: center !important; }

    / ۶. کادر نتایج /
    .result-box { text-align: center; padding: 15px; border-radius: 15px; background-color: #f8f9fa; border: 1px solid #ddd; }
    .result-text { font-size: 16px !important; font-weight: bold; color: #1a73e8; }
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
        st.markdown(f"""<div class='result-box'><div class='result-text'> جریان تخمینی: {curr} آمپر</div><div class='result-text' style='color: #1b5e20;'>🎯 سایز استاندارد: {f_size} mm²</div><div class='result-text' style='color: #e65100;'>🚀 سایز پیشنهادی (Safe): {s_size} mm²</div><p style='color: #5f6368;'>عدد دقیق محاسباتی: {raw} mm²</p></div>""", unsafe_allow_html=True)
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
