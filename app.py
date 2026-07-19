import streamlit as st
import math

# ==============================================================================
# --- Page Configuration ---
# ==============================================================================
st.set_page_config(
    page_title="ElectroCalc ⚡ M&F", 
    page_icon="⚡️", 
    layout="centered"
)

# ==============================================================================
# --- Theme Management in Session State ---
# ==============================================================================

if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

def toggle_theme():
    if st.session_state.theme == 'light':
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'

# Define colors based on theme
if st.session_state.theme == 'light':
    bg_color = "#ffffff"
    text_color = "#000000"
    card_bg = "#f1f3f4"
    border_color = "#3c4043"
    tab_bg = "#f0f2f6"
    tab_active = "#2E7D32"
    button_bg = "#007BFF"
    button_text = "#ffffff"
    result_bg = "#f1f3f4"
    sidebar_bg = "#f0f2f6"
    input_bg = "#ffffff"
    metric_label_color = "#000000"
    metric_value_color = "#1a73e8"
    info_box_bg = "#e8f0fe"
    info_box_border = "#1a73e8"
    info_box_text = "#1a1a1a"
    header_color = "#000000"
    selectbox_bg = "#ffffff"
    selectbox_text = "#000000"
    radio_text = "#000000"
    slider_text = "#000000"
    st_info_bg = "#e3f2fd"
    st_info_text = "#0d47a1"
    st_warning_bg = "#fff3e0"
    st_warning_text = "#bf360c"
    st_success_bg = "#e8f5e9"
    st_success_text = "#1b5e20"
    dual_mode_bg = "#e8f5e9"
    dual_mode_text = "#1b5e20"
    dual_mode_border = "#4CAF50"
    settings_box_bg = "#e3f2fd"
    settings_box_text = "#0d47a1"
    settings_box_border = "#1a73e8"
else:
    bg_color = "#0a0a0a"
    text_color = "#ffffff"
    card_bg = "#1a1a1a"
    border_color = "#666666"
    tab_bg = "#2a2a2a"
    tab_active = "#4CAF50"
    button_bg = "#1E88E5"
    button_text = "#ffffff"
    result_bg = "#1a1a1a"
    sidebar_bg = "#0d0d0d"
    input_bg = "#1f1f1f"
    metric_label_color = "#ffffff"
    metric_value_color = "#64B5F6"
    info_box_bg = "#1a2332"
    info_box_border = "#4FC3F7"
    info_box_text = "#e0e0e0"
    header_color = "#ffffff"
    selectbox_bg = "#1f1f1f"
    selectbox_text = "#ffffff"
    radio_text = "#ffffff"
    slider_text = "#ffffff"
    st_info_bg = "#0d2137"
    st_info_text = "#90CAF9"
    st_warning_bg = "#3e1a00"
    st_warning_text = "#ffab91"
    st_success_bg = "#0d2e1a"
    st_success_text = "#81c784"
    dual_mode_bg = "#0d2137"
    dual_mode_text = "#90CAF9"
    dual_mode_border = "#4FC3F7"
    settings_box_bg = "#0d2137"
    settings_box_text = "#90CAF9"
    settings_box_border = "#4FC3F7"

# ==============================================================================
# --- Styles ---
# ==============================================================================

st.markdown(f"""
    <style>
    /* ========== Top margin adjustment ========== */
    .main > div {{
        padding-top: 0px !important;
    }}
    
    .stApp {{
        margin-top: 0px !important;
        background-color: {bg_color} !important;
    }}
    
    .block-container {{
        padding-top: 30px !important;
        padding-bottom: 30px !important;
    }}

    /* ========== General text color ========== */
    .stApp, .stApp p, .stApp label, .stApp div, .stApp span, .stApp li {{
        color: {text_color} !important;
    }}

    /* ========== App title ========== */
    .app-title {{
        text-align: center;
        padding: 5px 0 12px 0 !important;
        margin: 0 !important;
        font-size: 60px !important;
        font-weight: 800 !important;
        color: {header_color} !important;
        white-space: nowrap;
        overflow: visible;
        letter-spacing: 1px !important;
        line-height: 1.2 !important;
        border-bottom: 3px solid #888888 !important;
        margin-bottom: 8px !important;
    }}
    
    .app-title .lightning {{
        color: #f9a825;
        display: inline-block;
        margin: 0 6px !important;
        font-size: 68px !important;
    }}

    @media screen and (max-width: 640px) {{
        .block-container {{
            padding-top: 20px !important;
            padding-bottom: 20px !important;
        }}
        .app-title {{
            font-size: 38px !important;
            padding: 0px 0 10px 0 !important;
            white-space: normal !important;
            word-break: break-word !important;
            line-height: 1.3 !important;
        }}
        .app-title .lightning {{
            font-size: 42px !important;
        }}
    }}

    @media screen and (max-width: 400px) {{
        .block-container {{
            padding-top: 15px !important;
            padding-bottom: 15px !important;
        }}
        .app-title {{
            font-size: 30px !important;
            padding: 0px 0 8px 0 !important;
        }}
        .app-title .lightning {{
            font-size: 34px !important;
        }}
    }}

    /* ========== Tabs ========== */
    .stTabs div[role="tablist"] {{
        gap: 8px !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        justify-content: center !important;
        display: flex !important;
        padding: 6px 0 5px 0 !important;
        border-bottom: 3px solid #666666 !important;
        margin-top: 0px !important;
    }}
    
    .stTabs [role="tab"] {{
        font-size: 20px !important;
        padding: 14px 28px !important;
        border-radius: 14px 14px 0px 0px !important;
        background-color: {tab_bg} !important;
        color: {text_color} !important;
        white-space: nowrap !important;
        min-width: 100px !important;
        text-align: center !important;
        font-weight: 600 !important;
        border: 2px solid {border_color} !important;
        border-bottom: none !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        opacity: 0.85 !important;
        margin-bottom: -2px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }}
    
    .stTabs [role="tab"]:hover {{
        background-color: #c8e6c9 !important;
        color: #1b5e20 !important;
        opacity: 1 !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {tab_active} !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border-color: {tab_active} !important;
        border-bottom: 3px solid {tab_active} !important;
        opacity: 1 !important;
        transform: translateY(-4px) !important;
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.4) !important;
        font-size: 21px !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
    }}
    
    .stTabs [aria-selected="true"]:hover {{
        background-color: #1B5E20 !important;
        transform: translateY(-4px) !important;
        box-shadow: 0 6px 24px rgba(46, 125, 50, 0.5) !important;
        color: #FFFFFF !important;
    }}
    
    /* ========== Mobile ========== */
    @media screen and (max-width: 640px) {{
        .stApp {{
            margin-top: 0px !important;
        }}
        
        .stTabs div[role="tablist"] {{
            gap: 4px !important;
            padding: 4px 0 4px 0 !important;
            justify-content: flex-start !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
        }}
        
        .stTabs [role="tab"] {{
            font-size: 15px !important;
            padding: 10px 16px !important;
            min-width: 65px !important;
            border-radius: 10px 10px 0px 0px !important;
            flex: 0 0 auto !important;
            display: inline-block !important;
            font-weight: 600 !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            font-size: 16px !important;
            transform: translateY(-3px) !important;
            box-shadow: 0 4px 14px rgba(46, 125, 50, 0.35) !important;
            color: #FFFFFF !important;
        }}
    }}

    @media screen and (max-width: 400px) {{
        .stTabs [role="tab"] {{
            font-size: 13px !important;
            padding: 8px 12px !important;
            min-width: 55px !important;
        }}
        .stTabs [aria-selected="true"] {{
            font-size: 14px !important;
            color: #FFFFFF !important;
        }}
    }}
    
    /* ========== Hide extra elements ========== */
    .stAppHeader, header[data-testid="stHeader"] {{
        display: none !important;
    }}
    
    .stDeployButton, .stAppDeployButton, div[data-testid="stAppDeployButton"] {{
        display: none !important;
    }}
    
    #MainMenu {{
        display: none !important;
    }}

    footer {{
        display: none !important;
    }}
    
    .stAppFooter {{
        display: none !important;
    }}
    
    /* ========== Result box ========== */
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
    }}

    .test-pass {{
        background-color: #1b5e20 !important;
        border: 3px solid #4CAF50 !important;
        color: #ffffff !important;
    }}
    
    .test-fail {{
        background-color: #b71c1c !important;
        border: 3px solid #f44336 !important;
        color: #ffffff !important;
    }}
    
    .test-warning {{
        background-color: #e65100 !important;
        border: 3px solid #ff9800 !important;
        color: #ffffff !important;
    }}

    /* ========== New info box style ========== */
    .info-box-new {{
        background-color: {info_box_bg} !important;
        padding: 18px 20px !important;
        border-radius: 12px !important;
        margin-top: 20px !important;
        border-right: 5px solid {info_box_border} !important;
        direction: rtl;
        text-align: right;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }}
    
    .info-box-new .info-title {{
        font-size: 18px !important;
        font-weight: 700 !important;
        color: {info_box_border} !important;
        margin-bottom: 12px !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
    }}
    
    .info-box-new .info-title::before {{
        content: "📋";
        font-size: 20px !important;
    }}
    
    .info-box-new .info-item {{
        padding: 6px 0 !important;
        border-bottom: 1px solid rgba(255,255,255,0.05) !important;
        display: flex !important;
        align-items: flex-start !important;
        gap: 10px !important;
        color: {info_box_text} !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
    }}
    
    .info-box-new .info-item:last-child {{
        border-bottom: none !important;
    }}
    
    .info-box-new .info-item .bullet {{
        color: {info_box_border} !important;
        font-weight: 700 !important;
        min-width: 18px !important;
    }}
    
    .info-box-new .info-item .highlight {{
        color: {info_box_border} !important;
        font-weight: 600 !important;
    }}

    /* ========== Dual mode box (Motor tab) ========== */
    .dual-mode-box {{
        background-color: {dual_mode_bg} !important;
        padding: 12px !important;
        border-radius: 8px !important;
        margin-bottom: 15px !important;
        direction: rtl !important;
        text-align: right !important;
        border-right: 4px solid {dual_mode_border} !important;
    }}
    
    .dual-mode-box b {{
        color: {dual_mode_text} !important;
    }}
    
    .dual-mode-box, .dual-mode-box p, .dual-mode-box span, .dual-mode-box div {{
        color: {dual_mode_text} !important;
    }}

    /* ========== Settings box (Settings tab) ========== */
    .settings-box {{
        background-color: {settings_box_bg} !important;
        padding: 15px !important;
        border-radius: 10px !important;
        margin-bottom: 20px !important;
        border-right: 4px solid {settings_box_border} !important;
        direction: rtl !important;
        text-align: right !important;
    }}
    
    .settings-box b {{
        color: {settings_box_text} !important;
    }}
    
    .settings-box, .settings-box p, .settings-box span, .settings-box div {{
        color: {settings_box_text} !important;
    }}

    /* ========== Metric colors ========== */
    div[data-testid="metric-container"] {{
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }}
    
    div[data-testid="metric-container"] label {{
        color: {metric_label_color} !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }}
    
    div[data-testid="metric-container"] .stMetricValue {{
        color: {metric_value_color} !important;
        font-size: 24px !important;
        font-weight: 700 !important;
    }}
    
    div[data-testid="metric-container"] .stMetricDelta {{
        color: {text_color} !important;
    }}

    /* ========== Header colors ========== */
    .stHeader, .stSubheader, h1, h2, h3, h4 {{
        color: {header_color} !important;
    }}

    /* ========== Label colors ========== */
    label, .stMarkdown p, .stText, .stCaption {{
        color: {text_color} !important;
    }}

    /* ========== Input colors ========== */
    .stNumberInput input, .stSelectbox select {{
        color: {text_color} !important;
        background-color: {input_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 6px !important;
    }}

    .stSelectbox div[data-baseweb="select"] {{
        background-color: {selectbox_bg} !important;
        color: {selectbox_text} !important;
    }}
    
    .stSelectbox div[data-baseweb="select"] div {{
        color: {selectbox_text} !important;
    }}

    .stRadio label {{
        color: {radio_text} !important;
    }}
    
    .stRadio div[role="radiogroup"] label {{
        color: {radio_text} !important;
    }}

    .stSlider label {{
        color: {slider_text} !important;
    }}

    .stButton > button {{
        color: {button_text} !important;
        background-color: {button_bg} !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }}

    .stContainer {{
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }}

    .stAlert {{
        background-color: {st_info_bg} !important;
        color: {st_info_text} !important;
    }}
    
    .stAlert p, .stAlert div {{
        color: {st_info_text} !important;
    }}

    .katex, .katex-display {{
        color: {text_color} !important;
    }}
    
    .katex .mathnormal {{
        color: {text_color} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# --- Display App Title ---
# ==============================================================================

st.markdown(f"""
    <div class="app-title">
        ElectroCalc <span class="lightning">⚡</span> M&F
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# --- Function to display info box with new style ---
# ==============================================================================

def show_info_box(title, items):
    items_html = ""
    for item in items:
        items_html += f'<div class="info-item"><span class="bullet">•</span> {item}</div>'
    
    st.markdown(f"""
    <div class="info-box-new">
        <div class="info-title">{title}</div>
        {items_html}
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- Helper Functions ---
# ==============================================================================

def get_cable_size(current_a, voltage=380, cos_phi=0.8, max_drop=2, length=50, conductor="Copper"):
    standard_sizes = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300]
    
    if conductor == "Copper":
        current_capacity = {
            1.5: 18, 2.5: 24, 4: 32, 6: 41, 10: 57, 16: 76,
            25: 101, 35: 125, 50: 151, 70: 192, 95: 232,
            120: 269, 150: 300, 185: 341, 240: 400, 300: 460
        }
        conductivity = 56
    else:
        current_capacity = {
            1.5: 14, 2.5: 18, 4: 25, 6: 32, 10: 44, 16: 60,
            25: 80, 35: 100, 50: 120, 70: 150, 95: 185,
            120: 215, 150: 240, 185: 270, 240: 320, 300: 370
        }
        conductivity = 35
    
    safety_factor = 1.25
    required_current = current_a * safety_factor
    
    selected_index = 0
    for i, (size, capacity) in enumerate(current_capacity.items()):
        if capacity >= required_current:
            selected_index = i
            break
    else:
        selected_index = len(standard_sizes) - 1
    
    if selected_index < len(standard_sizes) - 1:
        selected_index += 1
    
    selected = standard_sizes[selected_index]
    
    try:
        area_drop = (current_a * length * 1.732 * cos_phi * 100) / (conductivity * voltage * max_drop)
        if area_drop > selected:
            for size in standard_sizes:
                if size >= area_drop:
                    idx = standard_sizes.index(size)
                    if idx < len(standard_sizes) - 1:
                        selected = standard_sizes[idx + 1]
                    else:
                        selected = size
                    break
    except:
        pass
    
    return selected

def get_breaker_size(current_a, load_type="Motor"):
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

def calculate_voltage_drop(current_a, length, cable_size, voltage=415, cos_phi=0.8, conductor="Copper"):
    conductivity = 56 if conductor == "Copper" else 35
    try:
        drop = (current_a * length * 1.732 * cos_phi * 100) / (conductivity * voltage * cable_size)
        return round(drop, 2)
    except:
        return 0

def calculate_coil_area_from_fans(num_fans, fan_diameter_cm):
    fan_radius_m = (fan_diameter_cm / 100) / 2
    fan_area = math.pi * (fan_radius_m ** 2)
    total_area = num_fans * fan_area
    return total_area

def calculate_cooling_capacity(air_velocity, coil_area, temp_in, temp_out, 
                               air_density=1.2, cp=1.005, target_capacity=30):
    volume_flow = air_velocity * coil_area
    mass_flow = volume_flow * air_density
    delta_t = temp_in - temp_out
    capacity = mass_flow * cp * delta_t
    percentage = (capacity / target_capacity) * 100
    
    if percentage >= 95:
        status = "PASS"
        status_text = f"✅ System has reached nominal capacity ({target_capacity} kW)"
        status_color = "test-pass"
    elif percentage >= 80:
        status = "WARNING"
        status_text = f"⚠️ System has not reached nominal capacity ({percentage:.1f}% of {target_capacity} kW)"
        status_color = "test-warning"
    else:
        status = "FAIL"
        status_text = f"❌ System has issues ({percentage:.1f}% of {target_capacity} kW)"
        status_color = "test-fail"
    
    return {
        'volume_flow': round(volume_flow, 3),
        'mass_flow': round(mass_flow, 3),
        'delta_t': round(delta_t, 1),
        'capacity': round(capacity, 2),
        'percentage': round(percentage, 1),
        'status': status,
        'status_text': status_text,
        'status_color': status_color,
        'air_velocity': air_velocity,
        'coil_area': coil_area,
        'temp_in': temp_in,
        'temp_out': temp_out,
        'target': target_capacity
    }

# ==============================================================================
# --- Main Functions ---
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
# --- Tabs (6 tabs) ---
# ==============================================================================

tabs = st.tabs(["📏 Cable", "🔋 UPS", "⚙️ Motor", "🛡️ Protect", "❄️ HVAC Test", "⚙️ Settings"])

# ==============================================================================
# --- Tab 1: Cable ---
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
        
        show_info_box(
            "📋 Cable Calculation Result",
            [
                'Rated current calculated based on power and input voltage',
                'Standard size: nearest higher size to the calculated value',
                'Safe size considering safety factor for lengths over 80 meters',
                '<span class="highlight">Formula:</span> S = (P × L × 100) / (σ × V² × ΔV%)'
            ]
        )

# ==============================================================================
# --- Tab 2: UPS ---
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
        
        show_info_box(
            "📋 UPS Calculation Result",
            [
                'Battery capacity calculated based on UPS power, backup time, and number of batteries',
                'Cable size suggested based on UPS input current and safety factor',
                'Protection breaker selected considering load type (inductive)',
                '<span class="highlight">Formula:</span> Ah = (Ah_Base × kVA/10 × 32) / (N_Battery × V_Battery/12)'
            ]
        )

# ==============================================================================
# --- Tab 3: Motor ---
# ==============================================================================

with tabs[2]:
    st.header("⚙️ Motor / Generator Sizing with Dual Mode")
    
    st.markdown(f"""
    <div class="dual-mode-box">
        <b>📌 Two Calculation Modes:</b><br>
        • <b>Generator Nominal Power Mode:</b> Calculation based on maximum generator power (suitable for initial design)<br>
        • <b>Actual Load Mode:</b> Calculation based on actual load (suitable for economical cable and breaker selection)
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        st.subheader("🎯 Generator Specifications")
        
        c1, c2 = st.columns(2)
        with c1:
            gen_kva = st.number_input(
                "Generator Max Power (kVA)", 
                value=150.0, 
                step=5.0, 
                key="gen_kva",
                help="Maximum nominal power of generator"
            )
            
            calc_mode = st.selectbox(
                "Calculation Mode:",
                ["Based on Generator Max Power", "Based on Actual Load"],
                help="Select whether cable and breaker are calculated based on which power"
            )
            
            if calc_mode == "Based on Actual Load":
                actual_load = st.number_input(
                    "Actual Load (kVA)", 
                    value=85.0, 
                    step=1.0, 
                    min_value=1.0,
                    key="actual_load",
                    help="Actual consumed load (for economical cable and breaker selection)"
                )
            else:
                actual_load = gen_kva
        
        with c2:
            efficiency = st.number_input(
                "Efficiency (η)", 
                value=0.85, 
                step=0.01, 
                key="motor_eff_new"
            )
            power_factor = st.number_input(
                "Power Factor (cos φ)", 
                value=0.8, 
                step=0.01, 
                key="motor_cos_new"
            )
    
    with st.container(border=True):
        st.subheader("🔌 Cable & Installation Parameters")
        
        c1, c2 = st.columns(2)
        with c1:
            system_voltage = st.selectbox(
                "System Voltage (V)", 
                [380, 400, 415, 480], 
                index=2,
                key="motor_voltage_new"
            )
            cable_length = st.number_input(
                "Cable Length (m)", 
                value=30.0, 
                step=5.0, 
                min_value=1.0,
                key="cable_length_motor_new",
                help="Cable length from generator to distribution board"
            )
        with c2:
            conductor_type = st.selectbox(
                "Conductor Type",
                ["Copper", "Aluminum"],
                key="conductor_type"
            )
            future_expansion = st.slider(
                "Future Expansion (%)", 
                min_value=0, 
                max_value=100, 
                value=0, 
                step=10,
                help="Percentage of possible future load increase"
            )
    
    if st.button("🔍 Calculate Generator", use_container_width=True):
        gen_current = gen_kva * 1.44
        starting_current = gen_current * 6
        
        actual_current = actual_load * 1.44
        actual_starting_current = actual_current * 6
        
        future_factor = 1 + (future_expansion / 100)
        design_current = actual_current * future_factor
        
        if calc_mode == "Based on Generator Max Power":
            base_for_cable = gen_current
            mode_label = "Generator Max Power"
        else:
            base_for_cable = design_current
            mode_label = f"Actual Load ({actual_load} kVA) + Future Expansion ({future_expansion}%)"
        
        cable_size = get_cable_size(
            base_for_cable, 
            system_voltage, 
            power_factor, 
            2, 
            cable_length,
            conductor_type
        )
        
        voltage_drop = calculate_voltage_drop(
            base_for_cable, 
            cable_length, 
            cable_size, 
            system_voltage, 
            power_factor,
            conductor_type
        )
        
        breaker_size = get_breaker_size(base_for_cable, "Motor")
        starting_breaker = get_breaker_size(actual_starting_current * future_factor, "Motor")
        
        st.markdown("---")
        st.subheader("📊 Results")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("⚡ Generator Max Current", f"{gen_current:.2f} A")
            st.metric("⚡ Actual Load Current", f"{actual_current:.2f} A")
            st.metric("📐 Design Current", f"{design_current:.2f} A", 
                     delta=f"Based on: {mode_label}")
        
        with col2:
            st.metric("🚀 Starting Current", f"{actual_starting_current:.2f} A")
            st.metric("📏 Recommended Cable", f"{cable_size} mm²", 
                     delta=f"Conductor: {conductor_type}")
            st.metric("📉 Voltage Drop", f"{voltage_drop}%",
                     delta="OK" if voltage_drop <= 3 else "High!")
        
        st.markdown("---")
        
        st.markdown(f"""
            <div class='result-box'>
                <div class='result-text'>🔌 Cable Sizing</div>
                <div style='font-size: 16px;'>
                    <b>Based on:</b> {mode_label}<br>
                    <b>Design Current:</b> {design_current:.2f} A<br>
                    <b>Recommended Cable:</b> {cable_size} mm² ({conductor_type})<br>
                    <b>Voltage Drop:</b> {voltage_drop}% {'✅ Acceptable' if voltage_drop <= 3 else '⚠️ Consider larger cable'}
                </div>
            </div>
            
            <div class='result-box'>
                <div class='result-text'>🛡️ Breaker Sizing</div>
                <div style='font-size: 16px;'>
                    <b>Rated Breaker:</b> {breaker_size} A<br>
                    <b>Starting Breaker:</b> {starting_breaker} A<br>
                    <b>Load Type:</b> Motor (Inductive)
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if voltage_drop > 3:
            st.warning(f"⚠️ Voltage drop is {voltage_drop}% which exceeds the recommended 3% limit. Consider increasing cable size to {get_cable_size(base_for_cable, system_voltage, power_factor, 2, cable_length * 1.5, conductor_type)} mm².")
        
        if calc_mode == "Based on Actual Load" and actual_load < gen_kva:
            st.success(f"💡 You saved cable size by designing based on actual load ({actual_load} kVA) instead of generator max power ({gen_kva} kVA).")
        
        show_info_box(
            "📋 Generator Calculation Result",
            [
                f'Calculation mode: {mode_label}',
                f'Design current: {design_current:.2f} A',
                f'Recommended cable size: {cable_size} mm² ({conductor_type})',
                f'Voltage drop: {voltage_drop}% {"(Acceptable)" if voltage_drop <= 3 else "(Exceeds limit)"}',
                f'Protection breaker: {breaker_size} A (Rated) | {starting_breaker} A (Starting)',
                '<span class="highlight">Formulas:</span> I_gen = kVA × 1.44 | I_design = I_actual × (1 + Future Expansion%)'
            ]
        )

# ==============================================================================
# --- Tab 4: Protection ---
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
        
        show_info_box(
            "📋 Protection Calculation Result",
            [
                'Protection breaker selected based on load current and type',
                'Cable size suggested based on load current and allowable voltage drop',
                'Safety factor varies for different loads (Resistive: 1.25, Inductive: 1.4, Motor: 1.6)',
                '<span class="highlight">Formula:</span> I_breaker = I_load × K_safety'
            ]
        )

# ==============================================================================
# --- Tab 5: HVAC ---
# ==============================================================================

with tabs[4]:
    st.header("❄️ HVAC Cooling Capacity Test")

    with st.container(border=True):
        st.subheader("🎯 Target Capacity Setting")
        
        target_capacity = st.number_input(
            "Target Capacity (kW)", 
            value=30.0, 
            step=1.0, 
            min_value=1.0,
            format="%.1f"
        )
    
    with st.container(border=True):
        st.subheader("📊 Measurement Inputs")
        
        c1, c2 = st.columns(2)
        with c1:
            air_velocity = st.number_input(
                "Air Velocity (m/s)", 
                value=2.0, 
                step=0.1, 
                format="%.1f"
            )
            
            area_method = st.radio(
                "Coil Area Calculation Method:",
                ["Manual Entry", "Calculate from Fans"]
            )
            
            if area_method == "Manual Entry":
                coil_area = st.number_input(
                    "Coil Area (m²)", 
                    value=1.0, 
                    step=0.05, 
                    format="%.2f"
                )
                fan_info = None
            else:
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    num_fans = st.number_input(
                        "Number of Fans", 
                        value=6, 
                        step=1, 
                        min_value=1
                    )
                with col_f2:
                    fan_diameter = st.number_input(
                        "Fan Diameter (cm)", 
                        value=30.0, 
                        step=1.0, 
                        min_value=1.0,
                        format="%.1f"
                    )
                
                coil_area = calculate_coil_area_from_fans(num_fans, fan_diameter)
                
                fan_radius = (fan_diameter / 100) / 2
                single_fan_area = math.pi * (fan_radius ** 2)
                
                st.info(f"""
                    **📐 Coil Area Calculated from Fans:**
                    - Number of Fans: {num_fans}
                    - Fan Diameter: {fan_diameter} cm
                    - Single Fan Area: {single_fan_area:.4f} m²
                    - **Total Coil Area: {coil_area:.4f} m²**
                """)
                
                fan_info = {
                    'num_fans': num_fans,
                    'fan_diameter': fan_diameter,
                    'single_fan_area': single_fan_area,
                    'total_area': coil_area
                }
        
        with c2:
            temp_in = st.number_input(
                "Inlet Air Temp (°C)", 
                value=35.0, 
                step=0.5, 
                format="%.1f"
            )
            temp_out = st.number_input(
                "Outlet Air Temp (°C)", 
                value=23.0, 
                step=0.5, 
                format="%.1f"
            )
    
    with st.container(border=True):
        st.subheader("⚙️ Advanced Parameters")
        c1, c2 = st.columns(2)
        with c1:
            air_density = st.number_input(
                "Air Density (kg/m³)", 
                value=1.2, 
                step=0.01, 
                format="%.2f"
            )
        with c2:
            cp = st.number_input(
                "Cₚ (kJ/kg·K)", 
                value=1.005, 
                step=0.001, 
                format="%.3f"
            )
    
    if st.button("❄️ Run Cooling Test", use_container_width=True):
        result = calculate_cooling_capacity(
            air_velocity=air_velocity,
            coil_area=coil_area,
            temp_in=temp_in,
            temp_out=temp_out,
            air_density=air_density,
            cp=cp,
            target_capacity=target_capacity
        )
        
        st.markdown("---")
        st.subheader("📊 Test Results")
        
        if fan_info:
            st.markdown(f"""
            <div style='background-color: #f5f5f5; padding: 10px; border-radius: 8px; margin-bottom: 10px; direction: rtl; text-align: right;'>
                <b>🔧 Fan Information:</b>
                {fan_info['num_fans']} fans with diameter {fan_info['fan_diameter']} cm 
                → Total cross-section: {fan_info['total_area']:.4f} m²
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🌬️ Volume Flow", f"{result['volume_flow']} m³/s")
            st.metric("🌡️ Temperature Diff (ΔT)", f"{result['delta_t']} °C")
        with col2:
            st.metric("⚖️ Mass Flow", f"{result['mass_flow']} kg/s")
            st.metric("🎯 Target Capacity", f"{result['target']} kW")
        with col3:
            st.metric("❄️ Cooling Capacity", f"{result['capacity']} kW", 
                     delta=f"{result['percentage']}%")
        
        st.markdown("---")
        
        status_class = result['status_color']
        
        st.markdown(f"""
            <div class='result-box {status_class}' style='text-align: center; padding: 20px;'>
                <div style='font-size: 24px; font-weight: 700; margin-bottom: 10px;'>
                    {result['status_text']}
                </div>
                <div style='font-size: 20px; font-weight: 600;'>
                    Calculated Power: <span style='color: #1a73e8;'>{result['capacity']} kW</span>
                    &nbsp;|&nbsp; Power Percentage: <span style='color: #1a73e8;'>{result['percentage']}%</span>
                    &nbsp;|&nbsp; Status: <span style='color: #1a73e8;'>{result['status']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📝 Calculation Details"):
            st.markdown(f"""
            <div style='padding: 10px; direction: rtl; text-align: right;'>
                <b>Calculation Steps:</b><br><br>
                1. <b>Air Volume Flow:</b> Q = Air Velocity × Cross Section = {air_velocity} × {coil_area:.4f} = <b>{result['volume_flow']} m³/s</b><br><br>
                2. <b>Air Mass Flow:</b> ṁ = Q × ρ = {result['volume_flow']} × {air_density} = <b>{result['mass_flow']} kg/s</b><br><br>
                3. <b>Temperature Difference:</b> ΔT = T_inlet - T_outlet = {temp_in} - {temp_out} = <b>{result['delta_t']} °C</b><br><br>
                4. <b>Cooling Power:</b> P = ṁ × Cₚ × ΔT = {result['mass_flow']} × {cp} × {result['delta_t']} = <b>{result['capacity']} kW</b>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("💡 Recommendations"):
            suggestions = []
            
            if result['capacity'] < target_capacity:
                needed_velocity = (target_capacity * air_velocity) / result['capacity']
                if needed_velocity > air_velocity:
                    suggestions.append(f"🔹 Increase air velocity to approximately **{needed_velocity:.2f} m/s** (from {air_velocity} m/s)")
                
                if fan_info:
                    needed_area = (target_capacity * coil_area) / result['capacity']
                    if needed_area > coil_area:
                        needed_fans = (needed_area / fan_info['single_fan_area'])
                        suggestions.append(f"🔹 Increase number of fans to approximately **{math.ceil(needed_fans)}** units (from {fan_info['num_fans']} units)")
                
                needed_delta = (target_capacity * result['delta_t']) / result['capacity']
                if needed_delta > result['delta_t']:
                    needed_temp_out = temp_in - needed_delta
                    suggestions.append(f"🔹 Reduce outlet temperature to approximately **{needed_temp_out:.1f} °C** (from {temp_out} °C)")
                
                if not suggestions:
                    suggestions.append("🔸 System requires complete review.")
            else:
                suggestions.append(f"✅ System has reached nominal capacity of {target_capacity} kW.")
            
            for s in suggestions:
                st.markdown(s)
    
    show_info_box(
        "📋 Cooling Capacity Test Method",
        [
            'Test using anemometer - indirect measurement',
            'Formula: P = ṁ × Cₚ × ΔT',
            'Default parameters: Air density = 1.2 kg/m³ | Cₚ = 1.005 kJ/kg·K',
            'Target power adjustable - test any cooling capacity',
            '<span class="highlight">Result Interpretation:</span> ✅ PASS (≥ 95%) | ⚠️ WARNING (80%-95%) | ❌ FAIL (< 80%)'
        ]
    )
    
    with st.expander("📖 Test Procedure Guide"):
        st.markdown("""
        ### 🔍 Test Steps:
        
        1. **Set Target Capacity** - Enter your system's nominal cooling capacity
        
        2. **Measure Air Velocity** with an anemometer at multiple points on the coil and take the average
        
        3. **Select Coil Area Calculation Method:**
           - **Manual Entry:** Enter the coil area directly
           - **Calculate from Fans:** Enter number and diameter of fans for automatic area calculation
        
        4. **Measure Inlet and Outlet Air Temperatures** with a precise thermometer
        
        5. **Enter values** in the form above and click the test button
        
        ---
        
        ### ⚠️ Important Notes:
        
        - Test should be performed in **steady-state** conditions
        - If coil temperature is below the dew point, moisture condenses and calculations require humidity measurement for accuracy
        - For better accuracy, take measurements in a **regular grid pattern** across the coil surface
        """)

# ==============================================================================
# --- Tab 6: Settings ---
# ==============================================================================

with tabs[5]:
    st.header("⚙️ Settings")
    
    st.markdown(f"""
    <div class="settings-box">
        <b>📋 Application Settings Management</b><br>
        In this section you can change the application's appearance settings.
    </div>
    """, unsafe_allow_html=True)
    
    # ========== Theme Settings ==========
    st.subheader("🌓 Theme Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        current_theme = "🌞 Light" if st.session_state.theme == 'light' else "🌙 Dark"
        st.info(f"Current Theme: **{current_theme}**")
    
    with col2:
        theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
        theme_label = "Switch to Dark Mode" if st.session_state.theme == 'light' else "Switch to Light Mode"
        
        if st.button(f"{theme_icon} {theme_label}", use_container_width=True):
            toggle_theme()
            st.rerun()
    
    st.divider()
    
    # ========== About ==========
    st.subheader("ℹ️ About")
    st.markdown("""
    **ElectroCalc ⚡ M&F**  
    Version: **2.0**  
    Developed for Power Systems Engineering  
    
    **Standards Used:**
    - IEC 60364 - Cable Sizing
    - IEEE 485 - UPS Sizing
    - IEC 60034 - Motor Calculations
    - IEC 60947 - Breaker Selection
    - IEC 60909 - Short Circuit
    """)
    
    st.divider()
    
    # ========== Status ==========
    st.subheader("🔒 Status")
    st.markdown(f"""
    ✅ **Application Status:** Online  
    ✅ **Theme:** {current_theme}  
    ✅ **Version:** 2.0
    """)
