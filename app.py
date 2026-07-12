import streamlit as st
import math

# ==============================================================================
# --- تنظیمات صفحه ---
# ==============================================================================
st.set_page_config(
    page_title="ElectroCalc ⚡ M&F", 
    page_icon="⚡️", 
    layout="centered"
)

# ==============================================================================
# --- نمایش اسم نرم‌افزار با روش ساده و مطمئن ---
# ==============================================================================

# ✅ این روش ۱۰۰٪ کار میکنه
st.markdown("""
    <div style='text-align: center; padding: 10px 0;'>
        <h1 style='font-size: 40px; font-weight: 700; margin: 0; color: #1a1a1a;'>
            ElectroCalc <span style='color: #f9a825;'>⚡</span> M&F
        </h1>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# --- توابع محاسباتی ---
# ==============================================================================

def calculate_cable_fixed(p_kw, length, sigma, voltage=380, max_drop_percent=2):
    p_watts = p_kw * 1000
    cos_phi = 0.8 
    current = p_watts / (math.sqrt(3) * voltage * cos_phi)
    
    try:
        area_voltage_drop = (p_watts * length * 100) / (sigma * (voltage**2) * max_drop_percent)
    except ZeroDivisionError: 
        return 0, "Error", "Error", 0

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
        min_area_for_current = 120

    final_calc = max(area_voltage_drop, min_area_for_current)

    standard_sizes = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300]
    
    suggested_index = -1
    for i, size in enumerate(standard_sizes):
        if size >= final_calc:
            suggested_index = i
            break
    
    if suggested_index == -1: 
        return round(current, 1), "Out of Range", "Out of Range", round(final_calc, 2)
    
    standard_size = standard_sizes[suggested_index]
    
    if length <= 80:
        suggested_size = standard_size
    else:
        if suggested_index + 1 < len(standard_sizes):
            suggested_size = standard_sizes[suggested_index + 1]
        else:
            suggested_size = standard_size

    return round(current, 1), standard_size, suggested_size, round(final_calc, 2)


def calculate_ups_fixed(load_kva, backup_min, num_batteries, battery_voltage=12):
    base_data = {10: 7, 20: 12, 30: 18, 40: 23, 50: 28, 60: 32}
    minutes_list = sorted(base_data.keys())
    
    if backup_min <= minutes_list[0]:
        base_ah = base_data[minutes_list[0]]
    elif backup_min >= minutes_list[-1]:
        base_ah = base_data[60]
    else:
        for i in range(len(minutes_list)-1):
            m1, m2 = minutes_list[i], minutes_list[i+1]
            if m1 <= backup_min <= m2:
                a1, a2 = base_data[m1], base_data[m2]
                base_ah = a1 + ((a2 - a1) * (backup_min - m1) / (m2 - m1))
                break
    
    voltage_factor = battery_voltage / 12
    result = (base_ah * (load_kva / 10) * 32) / (num_batteries * voltage_factor)
    return round(result, 1)


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
# --- تب‌ها ---
# ==============================================================================

tabs = st.tabs(["📏 Cable", "🔋 UPS", "⚙️ Motor", "🛡️ Protect"])

# ==============================================================================
# --- تب ۱: کابل ---
# ==============================================================================

with tabs[0]:
    st.header("📐 Cable Sizing")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            p_in = st.number_input("Power (kW)", value=85.0, step=1.0, key="p_c")
            l_in = st.number_input("Length (m)", value=90.0, step=5.0, key="l_c")
        with c2:
            s_in = st.number_input("Sigma (Conductivity)", value=56.0, step=1.0, key="s_c")
            d_in = st.number_input("Voltage Drop (%)", value=2.0, step=0.1, key="d_c")
    
    if st.button("🔍 Calculate Cable", use_container_width=True):
        curr, f_size, s_size, raw = calculate_cable_fixed(p_in, l_in, s_in, 380, d_in)
        st.latex(r"S = \frac{P \times L \times 100}{\sigma \times V^2 \times \Delta V\%}")
        st.markdown(f"""
            <div style='text-align: center; padding: 15px; border-radius: 15px; background-color: #f1f3f4; border: 2px solid #3c4043; margin: 15px 0;'>
                <div style='font-size: 18px; font-weight: 600; color: #1a73e8; margin-bottom: 5px;'>⚡ Current: {curr} A</div>
                <div style='font-size: 18px; font-weight: 600; color: #1b5e20; margin-bottom: 5px;'>📏 Standard: {f_size} mm²</div>
                <div style='font-size: 18px; font-weight: 600; color: #e65100; margin-bottom: 5px;'>🚀 Safe Size: {s_size} mm²</div>
                <p style='color: #5f6368;'>Exact Calc: {raw} mm²</p>
            </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# --- تب ۲: UPS ---
# ==============================================================================

with tabs[1]:
    st.header("🔋 Battery Sizing")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            u_kva = st.number_input("UPS Power (kVA)", value=40.0, step=1.0, key="u_kva")
            u_min = st.number_input("Time (min)", value=15, step=5, key="u_min")
        with c2:
            u_bat = st.number_input("Number of Batteries", value=32, step=1, key="u_bat")
            u_volt = st.selectbox("Battery Voltage", [12, 24], index=0, key="u_volt")
    
    if st.button("🔍 Calculate UPS", use_container_width=True):
        res = calculate_ups_fixed(u_kva, u_min, u_bat, u_volt)
        volt_text = "12V" if u_volt == 12 else "24V"
        st.latex(r"Ah = \frac{Ah_{Base} \times \frac{kVA}{10} \times 32}{N_{Battery} \times \frac{V_{Battery}}{12}}")
        st.markdown(f"""
            <div style='text-align: center; padding: 15px; border-radius: 15px; background-color: #f1f3f4; border: 2px solid #3c4043; margin: 15px 0;'>
                <div style='font-size: 18px; font-weight: 600; color: #1a73e8; margin-bottom: 5px;'>📦 Battery Capacity: {res} Ah</div>
                <div style='font-size: 18px; font-weight: 600; color: #0d47a1; margin-bottom: 5px;'>🔋 Required: {u_bat} Batteries</div>
                <div style='font-size: 18px; font-weight: 600; color: #e65100;'>⚡ System Voltage: {volt_text}</div>
            </div>
        """, unsafe_allow_html=True)
        if u_volt == 24:
            st.info("💡 With 24V system, required Ah is HALF of 12V system")

# ==============================================================================
# --- تب ۳: موتور ---
# ==============================================================================

with tabs[2]:
    st.header("⚙️ Motor Calculations")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            m_kva = st.number_input("Power (kVA)", value=150.0, step=5.0, key="m_kva")
            m_eff = st.number_input("Efficiency", value=0.85, step=0.01, key="m_eff")
        with c2:
            m_cos = st.number_input("Power Factor (cos φ)", value=0.8, step=0.01, key="m_cos")
            m_vol = st.number_input("Voltage (V)", value=380, step=10, key="m_vol")
    
    if st.button("🔍 Calculate Motor", use_container_width=True):
        curr, p_in, s_curr, p_kw_out = calculate_motor_from_kva(m_kva, m_eff, m_cos, m_vol)
        st.latex(r"I = \frac{P_{kW} \times 1000}{\eta \times \sqrt{3} \times V \times \cos\phi}")
        st.markdown(f"""
            <div style='text-align: center; padding: 15px; border-radius: 15px; background-color: #f1f3f4; border: 2px solid #3c4043; margin: 15px 0;'>
                <div style='font-size: 18px; font-weight: 600; color: #1a73e8; margin-bottom: 5px;'>⚡ Rated Current: {curr} A</div>
                <div style='font-size: 18px; font-weight: 600; color: #e65100; margin-bottom: 5px;'>🚀 Start Current: {s_curr} A</div>
                <div style='font-size: 18px; font-weight: 600; color: #1a73e8; margin-bottom: 5px;'>🔌 Input Power: {p_in} kW</div>
                <div style='font-size: 18px; font-weight: 600; color: #1b5e20;'>🎯 Output Power: {p_kw_out} kW</div>
            </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# --- تب ۴: حفاظت ---
# ==============================================================================

with tabs[3]:
    st.header("🛡️ Breaker Sizing")
    with st.container(border=True):
        p_curr = st.number_input("Load Current (A)", value=100.0, step=1.0, key="p_curr")
        p_type = st.selectbox("Load Type", ["Resistive", "Inductive"], key="p_type")
    
    if st.button("🔍 Suggest Breaker", use_container_width=True):
        b_size = suggest_breaker(p_curr, p_type)
        st.markdown(f"""
            <div style='text-align: center; padding: 15px; border-radius: 15px; background-color: #f1f3f4; border: 2px solid #3c4043; margin: 15px 0;'>
                <div style='font-size: 18px; font-weight: 600; color: #1a73e8; margin-bottom: 5px;'>🛡️ Suggested Breaker: {b_size} A</div>
                <p style='color: #5f6368;'>Based on IEC 60947 standard</p>
            </div>
        """, unsafe_allow_html=True)
