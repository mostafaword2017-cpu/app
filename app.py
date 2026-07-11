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
# --- مدیریت تم (Theme) ---
# ==============================================================================

if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

if st.session_state.theme == 'light':
    bg_color = "#ffffff"
    text_color = "#1a1a1a"
    card_bg = "#f1f3f4"
    border_color = "#3c4043"
    tab_bg = "#f0f2f6"
    tab_active = "#4CAF50"
    button_bg = "#007BFF"
    button_text = "#ffffff"
    result_bg = "#f1f3f4"
    sidebar_bg = "#f0f2f6"
    input_bg = "#ffffff"
    theme_icon = "🌙"
    theme_label = "Dark Mode"
else:
    bg_color = "#1a1a1a"
    text_color = "#f0f0f0"
    card_bg = "#2d2d2d"
    border_color = "#555555"
    tab_bg = "#333333"
    tab_active = "#4CAF50"
    button_bg = "#0d6efd"
    button_text = "#ffffff"
    result_bg = "#2d2d2d"
    sidebar_bg = "#252525"
    input_bg = "#333333"
    theme_icon = "☀️"
    theme_label = "Light Mode"

# ==============================================================================
# --- استایل با اسم در بالای صفحه ---
# ==============================================================================

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color} !important;
    }}
    
    .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label {{
        color: {text_color} !important;
    }}

    .stAppHeader, header[data-testid="stHeader"] {{
        display: none !important;
    }}
    
    .stDeployButton, .stAppDeployButton, div[data-testid="stAppDeployButton"] {{
        display: none !important;
    }}
    
    #MainMenu {{
        display: none !important;
    }}

    footer, .stAppFooter {{
        display: none !important;
    }}

    /* ========== بردن اسم به بالای صفحه ========== */
    .stApp h1 {{
        font-size: 49.5px !important;
        text-align: center !important;
        white-space: nowrap !important;
        font-weight: 700 !important;
        color: {text_color} !important;
        padding: 0px 0 0px 0 !important;
        margin-top: -25px !important;
        margin-bottom: -12px !important;
    }}

    @media screen and (max-width: 640px) {{
        .stApp h1 {{
            font-size: 36px !important;
            letter-spacing: -0.5px !important;
            margin-top: -15px !important;
            margin-bottom: -8px !important;
        }}
    }}

    /* ========== تب‌ها با فاصله کم از عنوان ========== */
    .stTabs div[role="tablist"] {{ 
        gap: 5px !important; 
        flex-wrap: nowrap !important; 
        overflow-x: auto !important;
        justify-content: center !important;
        display: flex !important;
        padding-top: 0px !important;
        margin-top: -5px !important;
    }}
    
    .stTabs [role="tab"] {{
        font-size: 19.5px !important;
        padding: 10px 18px !important;
        border-radius: 8px 8px 0px 0px !important;
        background-color: {tab_bg} !important;
        color: {text_color} !important;
        white-space: nowrap !important;
        min-width: 90px !important;
        text-align: center !important;
        font-weight: 500 !important;
        border: 1px solid {border_color} !important;
        border-bottom: none !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {tab_active} !important; 
        color: white !important;
        font-weight: 700 !important;
        border-color: {tab_active} !important;
    }}

    @media screen and (max-width: 640px) {{
        .stTabs [role="tab"] {{
            font-size: 16.5px !important;
            padding: 8px 12px !important;
            min-width: 75px !important;
        }}
        .stTabs div[role="tablist"] {{
            margin-top: -3px !important;
        }}
    }}

    /* ========== بقیه استایل‌ها ========== */
    label, .stMarkdown p {{
        font-size: 14px !important;
        color: {text_color} !important;
    }}
    
    @media screen and (max-width: 640px) {{
        label, .stMarkdown p {{
            font-size: 12px !important;
        }}
    }}

    .stButton > button {{
        width: 100% !important;
        height: 45px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        background-color: {button_bg} !important;
        color: {button_text} !important;
        border: none !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }}

    .stButton > button:hover {{
        opacity: 0.85 !important;
        transform: scale(1.02) !important;
    }}

    @media screen and (max-width: 640px) {{
        .stButton > button {{
            height: 38px !important;
            font-size: 14px !important;
        }}
    }}

    .result-box {{
        text-align: center;
        padding: 15px;
        border-radius: 15px;
        background-color: {result_bg} !important;
        border: 2px solid {border_color};
        margin: 15px 0;
    }}
    
    .result-text {{
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #1a73e8 !important;
        margin-bottom: 5px;
        word-wrap: break-word;
    }}

    @media screen and (max-width: 640px) {{
        .result-text {{
            font-size: 14px !important;
        }}
    }}

    .cable-box {{
        text-align: center;
        padding: 12px;
        border-radius: 12px;
        background-color: {card_bg} !important;
        border: 2px solid #4CAF50;
        margin: 10px 0;
    }}
    
    .cable-text {{
        font-size: 17px !important;
        font-weight: 600 !important;
        color: #1b5e20 !important;
        margin-bottom: 3px;
        word-wrap: break-word;
    }}

    @media screen and (max-width: 640px) {{
        .cable-text {{
            font-size: 13px !important;
        }}
    }}

    .css-1d391kg, .css-12oz5g7 {{
        background-color: {sidebar_bg} !important;
    }}

    .stNumberInput input, .stSelectbox select {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
        border-radius: 6px !important;
    }}

    .stNumberInput input:focus, .stSelectbox select:focus {{
        border-color: {tab_active} !important;
    }}

    .stHeader {{
        font-size: 18px !important;
        color: {text_color} !important;
    }}

    .stNumberInput, .stSelectbox {{
        margin-bottom: 8px !important;
    }}

    .katex-display {{
        text-align: center !important;
        margin: 10px 0 !important;
        font-size: 16px !important;
        color: {text_color} !important;
    }}

    @media screen and (max-width: 640px) {{
        .katex-display {{
            font-size: 13px !important;
        }}
    }}

    .stContainer {{
        background-color: {card_bg} !important;
        border-radius: 12px !important;
        padding: 10px !important;
        border: 1px solid {border_color} !important;
    }}
    </style>
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


def calculate_cable_from_current(current, length=100, sigma=56, voltage=380, max_drop_percent=2):
    cos_phi = 0.8
    p_watts = current * math.sqrt(3) * voltage * cos_phi
    p_kw = p_watts / 1000
    return calculate_cable_fixed(p_kw, length, sigma, voltage, max_drop_percent)


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


def show_cable_size(current, label="Load"):
    cable_curr, cable_std, cable_safe, cable_raw = calculate_cable_from_current(current)
    
    st.markdown(f"""
        <div class='cable-box'>
            <div class='cable-text'>🔌 Cable Sizing for {label}</div>
            <div class='cable-text' style='font-size: 15px; color: #1a73e8;'>
                Current: {cable_curr} A
            </div>
            <div class='cable-text' style='font-size: 15px; color: #1b5e20;'>
                📏 Standard Size: {cable_std} mm²
            </div>
            <div class='cable-text' style='font-size: 15px; color: #e65100;'>
                🚀 Safe Size: {cable_safe} mm²
            </div>
            <p style='color: #5f6368; font-size: 13px; margin: 0;'>
                Exact Calc: {cable_raw} mm²
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    return cable_curr, cable_std, cable_safe, cable_raw

# ==============================================================================
# --- رابط کاربری ---
# ==============================================================================

st.title("ElectroCalc ⚡ M&F")

# سایدبار
with st.sidebar:
    st.header("⚙️ Settings")
    
    if st.button(f"{theme_icon} {theme_label}", use_container_width=True):
        if st.session_state.theme == 'light':
            st.session_state.theme = 'dark'
        else:
            st.session_state.theme = 'light'
        st.rerun()
    
    st.divider()
    st.header("📚 Standards")
    st.markdown("""
    **IEC 60364** - Cable Sizing  
    **IEEE 485** - UPS Sizing  
    **IEC 60034** - Motor Calculations  
    **IEC 60947** - Breaker Selection  
    """)
    st.divider()
    st.caption("⚡ ElectroCalc M&F v2.0")
    st.caption("📱 Optimized for Mobile")

# تب‌ها
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
            <div class='result-box'>
                <div class='result-text'>📦 Battery Capacity: {res} Ah</div>
                <div class='result-text' style='color: #0d47a1;'>🔋 Required: {u_bat} Batteries</div>
                <div class='result-text' style='color: #e65100;'>⚡ System Voltage: {volt_text}</div>
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
            <div class='result-box'>
                <div class='result-text'>⚡ Rated Current: {curr} A</div>
                <div class='result-text' style='color: #e65100;'>🚀 Start Current: {s_curr} A</div>
                <div class='result-text' style='color: #1a73e8;'>🔌 Input Power: {p_in} kW</div>
                <div class='result-text' style='color: #1b5e20;'>🎯 Output Power: {p_kw_out} kW</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.subheader("🔌 Recommended Cable Size")
        show_cable_size(curr, "Motor Rated Current")
        
        with st.expander("ℹ️ About Cable Sizing for Motors"):
            st.markdown("""
            **Cable Sizing Guidelines for Motors:**
            
            - **Rated Current:** Use for normal operation
            - **Starting Current:** 6× rated current (for direct-on-line starting)
            - **Recommendation:** For motors, increase cable size by 1-2 levels above standard
            - **Voltage Drop:** Max 2% for motor circuits
            """)

# ==============================================================================
# --- تب ۴: حفاظت ---
# ==============================================================================

with tabs[3]:
    st.header("🛡️ Breaker & Cable Sizing")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            p_curr = st.number_input("Load Current (A)", value=100.0, step=1.0, key="p_curr")
            p_type = st.selectbox("Load Type", ["Resistive", "Inductive", "Motor"], key="p_type")
        with c2:
            cable_length = st.number_input("Cable Length (m)", value=50.0, step=5.0, key="p_cable_len")
            conductor_type = st.selectbox("Conductor", ["Copper", "Aluminum"], key="p_conductor")
    
    if st.button("🔍 Suggest Breaker & Cable", use_container_width=True):
        b_size = suggest_breaker(p_curr, p_type)
        sigma = 56.0 if conductor_type == "Copper" else 35.0
        cable_curr, cable_std, cable_safe, cable_raw = calculate_cable_from_current(
            p_curr, length=cable_length, sigma=sigma
        )
        
        st.markdown("### 🛡️ Breaker Selection")
        st.markdown(f"""
            <div class='result-box'>
                <div class='result-text'>🛡️ Suggested Breaker: {b_size} A</div>
                <div class='result-text' style='color: #0d47a1;'>⚡ Load Type: {p_type}</div>
                <div class='result-text' style='color: #5f6368; font-size: 15px;'>Load Current: {p_curr} A</div>
                <p style='color: #5f6368;'>Based on IEC 60947 standard</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔌 Cable Sizing")
        st.markdown(f"""
            <div class='cable-box'>
                <div class='cable-text'>📏 Standard Size: {cable_std} mm²</div>
                <div class='cable-text' style='color: #e65100;'>🚀 Safe Size: {cable_safe} mm²</div>
                <div class='cable-text' style='color: #1a73e8; font-size: 15px;'>⚡ Current: {cable_curr} A</div>
                <p style='color: #5f6368; font-size: 13px; margin: 0;'>
                    Length: {cable_length}m | {conductor_type} | Exact: {cable_raw} mm²
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        if p_type == "Motor":
            st.info("💡 For motor circuits, it's recommended to use the 'Safe Size' or one size larger due to starting current")
        elif p_type == "Inductive":
            st.info("💡 Inductive loads may require larger cable due to inrush current")
        else:
            st.success("✅ Cable size is suitable for this resistive load")
