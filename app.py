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
# --- استایل ---
# ==============================================================================

st.markdown("""
    <style>
    .stTabs div[role="tablist"] {
        gap: 10px !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        justify-content: center !important;
        display: flex !important;
        padding: 5px 0 !important;
    }
    
    .stTabs [role="tab"] {
        font-size: 22px !important;
        padding: 14px 24px !important;
        border-radius: 10px 10px 0px 0px !important;
        background-color: #f0f2f6 !important;
        color: #1a1a1a !important;
        white-space: nowrap !important;
        min-width: 100px !important;
        text-align: center !important;
        font-weight: 600 !important;
        border: 2px solid #ddd !important;
        border-bottom: none !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: 700 !important;
        border-color: #4CAF50 !important;
    }
    
    @media screen and (max-width: 640px) {
        .stTabs [role="tab"] {
            font-size: 18px !important;
            padding: 10px 16px !important;
            min-width: 70px !important;
        }
    }
    
    .stAppHeader, header[data-testid="stHeader"] {
        display: none !important;
    }
    
    .stDeployButton, .stAppDeployButton, div[data-testid="stAppDeployButton"] {
        display: none !important;
    }
    
    #MainMenu {
        display: none !important;
    }

    footer {
        display: none !important;
    }
    
    .stAppFooter {
        display: none !important;
    }
    
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
        font-weight: 600 !important;
        color: #1a73e8 !important;
        margin-bottom: 5px;
    }

    .app-title {
        text-align: center;
        padding: 5px 0 10px 0;
        margin: 0;
        font-size: 38px;
        font-weight: 700;
        color: #1a1a1a;
        white-space: nowrap;
        overflow: visible;
    }
    
    .app-title .lightning {
        color: #f9a825;
        display: inline-block;
    }

    @media screen and (max-width: 480px) {
        .app-title {
            font-size: 26px !important;
            white-space: normal !important;
            word-break: break-word !important;
            line-height: 1.3 !important;
            padding: 5px 10px !important;
        }
    }

    @media screen and (max-width: 380px) {
        .app-title {
            font-size: 22px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# --- نمایش اسم نرم‌افزار ---
# ==============================================================================

st.markdown("""
    <div class="app-title">
        ElectroCalc <span class="lightning">⚡</span> M&F
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# --- توابع کمکی (اصلاح شده) ---
# ==============================================================================

def get_cable_size(current_a, voltage=380, cos_phi=0.8, max_drop=2, length=50):
    """
    محاسبه سایز کابل مناسب بر اساس جریان با ضریب اطمینان
    ✅ اصلاح: یک پله بالاتر از سایز محاسبه شده پیشنهاد میدهد
    """
    standard_sizes = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300]
    
    current_capacity = {
        1.5: 18, 2.5: 24, 4: 32, 6: 41, 10: 57, 16: 76,
        25: 101, 35: 125, 50: 151, 70: 192, 95: 232,
        120: 269, 150: 300, 185: 341, 240: 400, 300: 460
    }
    
    # ضریب اطمینان ۱.۲۵
    safety_factor = 1.25
    required_current = current_a * safety_factor
    
    # پیدا کردن سایز مناسب
    selected_index = 0
    for i, (size, capacity) in enumerate(current_capacity.items()):
        if capacity >= required_current:
            selected_index = i
            break
    else:
        selected_index = len(standard_sizes) - 1
    
    # ✅ یک پله بالاتر (برای داشتن ضریب اطمینان بیشتر)
    if selected_index < len(standard_sizes) - 1:
        selected_index += 1
    
    selected = standard_sizes[selected_index]
    
    # بررسی افت ولتاژ (برای طول‌های بلند)
    try:
        area_drop = (current_a * length * 1.732 * cos_phi * 100) / (56 * voltage * max_drop)
        if area_drop > selected:
            for size in standard_sizes:
                if size >= area_drop:
                    # ✅ یک پله بالاتر
                    idx = standard_sizes.index(size)
                    if idx < len(standard_sizes) - 1:
                        selected = standard_sizes[idx + 1]
                    else:
                        selected = size
                    break
    except:
        pass
    
    return selected

def get_breaker_size(current_a, load_type="Resistive"):
    """محاسبه سایز کلید محافظ مناسب"""
    if load_type == "Motor":
        multiplier = 1.6
    elif load_type == "Inductive":
        multiplier = 1.4
    else:
        multiplier = 1.25
    
    required = current_a * multiplier
    standard_breakers = [6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630]
    
    for breaker in standard_breakers:
        if breaker >= required:
            return breaker
    return standard_breakers[-1]

# ==============================================================================
# --- توابع اصلی محاسباتی ---
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
            <div class='result-box'>
                <div class='result-text'>⚡ Current: {curr} A</div>
                <div class='result-text' style='color: #1b5e20;'>📏 Standard: {f_size} mm²</div>
                <div class='result-text' style='color: #e65100;'>🚀 Safe Size: {s_size} mm²</div>
                <p style='color: #5f6368;'>Exact Calc: {raw} mm²</p>
            </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# --- تب ۲: UPS ---
# ==============================================================================

with tabs[1]:
    st.header("🔋 UPS Sizing with Cable & Breaker")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            u_kva = st.number_input("UPS Power (kVA)", value=40.0, step=1.0, key="u_kva")
            u_min = st.number_input("Backup Time (min)", value=15, step=5, key="u_min")
            ups_voltage = st.selectbox("Input Voltage (V)", [380, 400, 415], index=0, key="ups_voltage")
        with c2:
            u_bat = st.number_input("Number of Batteries", value=32, step=1, key="u_bat")
            u_volt = st.selectbox("Battery Voltage", [12, 24], index=0, key="u_volt")
    
    if st.button("🔍 Calculate UPS", use_container_width=True):
        res = calculate_ups_fixed(u_kva, u_min, u_bat, u_volt)
        volt_text = "12V" if u_volt == 12 else "24V"
        
        ups_current = u_kva * 1.44
        ups_cable = get_cable_size(ups_current, ups_voltage, 0.8, 2, 50)
        ups_breaker = get_breaker_size(ups_current, "Inductive")
        
        st.latex(r"Ah = \frac{Ah_{Base} \times \frac{kVA}{10} \times 32}{N_{Battery} \times \frac{V_{Battery}}{12}}")
        
        st.markdown(f"""
            <div class='result-box'>
                <div class='result-text'>📦 Battery Capacity: {res} Ah</div>
                <div class='result-text' style='color: #0d47a1;'>🔋 Required Batteries: {u_bat} Units</div>
                <div class='result-text' style='color: #e65100;'>⚡ System Voltage: {volt_text}</div>
                <div class='result-text' style='color: #1b5e20;'>📏 Recommended Cable: {ups_cable} mm²</div>
                <div class='result-text' style='color: #d32f2f;'>🛡️ Recommended Breaker: {ups_breaker} A</div>
            </div>
        """, unsafe_allow_html=True)
        
        if u_volt == 24:
            st.info("💡 With 24V system, required Ah is HALF of 12V system")
        
        st.info(f"💡 For {u_kva} kVA UPS → Current = {u_kva} × 1.44 = **{ups_current:.2f} A** → Cable: **{ups_cable} mm²** → Breaker: **{ups_breaker} A**")

# ==============================================================================
# --- تب ۳: موتور / ژنراتور ---
# ==============================================================================

with tabs[2]:
    st.header("⚙️ Motor / Generator Sizing with Cable & Breaker")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            m_kva = st.number_input("Generator Power (kVA)", value=150.0, step=5.0, key="m_kva")
            m_eff = st.number_input("Efficiency (η)", value=0.85, step=0.01, key="m_eff")
            motor_voltage = st.selectbox("System Voltage (V)", [380, 400, 415, 480], index=0, key="motor_voltage")
        with c2:
            m_cos = st.number_input("Power Factor (cos φ)", value=0.8, step=0.01, key="m_cos")
    
    if st.button("🔍 Calculate Generator", use_container_width=True):
        gen_current = m_kva * 1.44
        starting_current = gen_current * 6
        gen_cable = get_cable_size(gen_current, motor_voltage, m_cos, 2, 50)
        gen_breaker = get_breaker_size(gen_current, "Motor")
        starting_breaker = get_breaker_size(starting_current, "Motor")
        
        st.latex(r"I_{gen} = kVA \times 1.44 \quad \text{(Empirical Formula)}")
        
        st.markdown(f"""
            <div class='result-box'>
                <div class='result-text'>⚡ Generator Current: {gen_current:.2f} A</div>
                <div class='result-text' style='color: #e65100;'>🚀 Starting Current: {starting_current:.2f} A</div>
                <div class='result-text' style='color: #1b5e20;'>📏 Recommended Cable: {gen_cable} mm²</div>
                <div class='result-text' style='color: #d32f2f;'>🛡️ Breaker (Rated): {gen_breaker} A</div>
                <div class='result-text' style='color: #e65100;'>⚡ Breaker (Starting): {starting_breaker} A</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.info(f"💡 For {m_kva} kVA Generator → Current = {m_kva} × 1.44 = **{gen_current:.2f} A** → Cable: **{gen_cable} mm²** → Breaker: **{gen_breaker} A**")

# ==============================================================================
# --- تب ۴: حفاظت ---
# ==============================================================================

with tabs[3]:
    st.header("🛡️ Protection & Breaker Sizing")
    with st.container(border=True):
        p_curr = st.number_input("Load Current (A)", value=100.0, step=1.0, key="p_curr")
        p_type = st.selectbox("Load Type", ["Resistive", "Inductive", "Motor"], key="p_type")
        system_voltage = st.selectbox("System Voltage (V)", [380, 400, 415], index=0, key="sys_voltage")
    
    if st.button("🔍 Calculate Protection", use_container_width=True):
        b_size = get_breaker_size(p_curr, p_type)
        cable_size = get_cable_size(p_curr, system_voltage, 0.8, 2, 50)
        
        st.markdown(f"""
            <div class='result-box'>
                <div class='result-text'>🛡️ Suggested Breaker: {b_size} A</div>
                <div class='result-text' style='color: #1b5e20;'>📏 Recommended Cable: {cable_size} mm²</div>
                <div class='result-text' style='color: #5f6368;'>📊 Load Type: {p_type}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.info(f"💡 For {p_curr} A {p_type} load → Cable: **{cable_size} mm²** → Breaker: **{b_size} A**")
