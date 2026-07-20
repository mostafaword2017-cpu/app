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
    sc_box_bg = "#fff3e0"
    sc_box_text = "#bf360c"
    sc_box_border = "#ff9800"
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
    sc_box_bg = "#2a1500"
    sc_box_text = "#ffab91"
    sc_box_border = "#ff9800"

# ==============================================================================
# --- Styles ---
# ==============================================================================

st.markdown(f"""
    <style>
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

    .stApp, .stApp p, .stApp label, .stApp div, .stApp span, .stApp li {{
        color: {text_color} !important;
    }}

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
        font-size: 18px !important;
        padding: 12px 22px !important;
        border-radius: 14px 14px 0px 0px !important;
        background-color: {tab_bg} !important;
        color: {text_color} !important;
        white-space: nowrap !important;
        min-width: 80px !important;
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
        font-size: 19px !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
    }}
    
    .stTabs [aria-selected="true"]:hover {{
        background-color: #1B5E20 !important;
        transform: translateY(-4px) !important;
        box-shadow: 0 6px 24px rgba(46, 125, 50, 0.5) !important;
        color: #FFFFFF !important;
    }}
    
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
            font-size: 13px !important;
            padding: 8px 12px !important;
            min-width: 55px !important;
            border-radius: 10px 10px 0px 0px !important;
            flex: 0 0 auto !important;
            display: inline-block !important;
            font-weight: 600 !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            font-size: 14px !important;
            transform: translateY(-3px) !important;
            box-shadow: 0 4px 14px rgba(46, 125, 50, 0.35) !important;
            color: #FFFFFF !important;
        }}
    }}

    @media screen and (max-width: 400px) {{
        .stTabs [role="tab"] {{
            font-size: 11px !important;
            padding: 6px 8px !important;
            min-width: 45px !important;
        }}
        .stTabs [aria-selected="true"] {{
            font-size: 12px !important;
            color: #FFFFFF !important;
        }}
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

    footer {{
        display: none !important;
    }}
    
    .stAppFooter {{
        display: none !important;
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

    .sc-box {{
        background-color: {sc_box_bg} !important;
        padding: 12px !important;
        border-radius: 8px !important;
        margin-bottom: 15px !important;
        direction: rtl !important;
        text-align: right !important;
        border-right: 4px solid {sc_box_border} !important;
    }}
    
    .sc-box b {{
        color: {sc_box_text} !important;
    }}
    
    .sc-box, .sc-box p, .sc-box span, .sc-box div {{
        color: {sc_box_text} !important;
    }}

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

    .stHeader, .stSubheader, h1, h2, h3, h4 {{
        color: {header_color} !important;
    }}

    label, .stMarkdown p, .stText, .stCaption {{
        color: {text_color} !important;
    }}

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
        status_text = f"✅ سیستم به توان اسمی ({target_capacity} kW) رسیده است"
        status_color = "test-pass"
    elif percentage >= 80:
        status = "WARNING"
        status_text = f"⚠️ سیستم به توان اسمی نرسیده است ({percentage:.1f}% از {target_capacity} kW)"
        status_color = "test-warning"
    else:
        status = "FAIL"
        status_text = f"❌ سیستم دچار مشکل است ({percentage:.1f}% از {target_capacity} kW)"
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
# --- Short Circuit Calculation Functions ---
# ==============================================================================

def calculate_short_circuit(transformer_kva, uk_percent, voltage=400, 
                            cable_size=240, cable_length=200, num_cables=3,
                            conductor_type="Copper"):
    """
    Calculate short circuit current at transformer terminals and at cable end
    """
    # Calculate rated current
    in_rated = transformer_kva * 1000 / (math.sqrt(3) * voltage)
    
    # Short circuit at transformer terminals
    isc_transformer = in_rated * (100 / uk_percent)
    
    # Transformer impedance
    z_transformer = (uk_percent / 100) * (voltage**2) / (transformer_kva * 1000)
    
    # Cable impedance per km (approximate)
    if conductor_type == "Copper":
        r_per_km = 0.091  # ohm/km for 240mm² copper
        x_per_km = 0.089  # ohm/km (reactance)
    else:
        r_per_km = 0.148  # ohm/km for 240mm² aluminum
        x_per_km = 0.089  # ohm/km (reactance)
    
    # Cable impedance for length
    r_cable = (r_per_km * cable_length / 1000) / num_cables
    x_cable = (x_per_km * cable_length / 1000) / num_cables
    z_cable = math.sqrt(r_cable**2 + x_cable**2)
    
    # Total impedance
    z_total = z_transformer + z_cable
    
    # Short circuit at cable end
    isc_cable_end = voltage / (math.sqrt(3) * z_total)
    
    # Breaker rating check (assuming 10kA standard)
    breaker_rating = 10  # kA standard
    breaker_ok = isc_transformer / 1000 <= breaker_rating
    
    return {
        'rated_current': round(in_rated, 1),
        'isc_transformer': round(isc_transformer / 1000, 2),
        'isc_cable_end': round(isc_cable_end / 1000, 2),
        'z_transformer': round(z_transformer * 1000, 3),
        'z_cable': round(z_cable * 1000, 3),
        'z_total': round(z_total * 1000, 3),
        'breaker_rating': breaker_rating,
        'breaker_ok': breaker_ok,
        'voltage': voltage,
        'uk_percent': uk_percent,
        'transformer_kva': transformer_kva,
        'cable_size': cable_size,
        'cable_length': cable_length,
        'num_cables': num_cables,
        'conductor_type': conductor_type
    }

# ==============================================================================
# --- Tabs (7 tabs) - تعریف تب‌ها ---
# ==============================================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📏 Cable", "🔋 UPS", "⚙️ Motor", "🛡️ Protect", 
    "❄️ HVAC Test", "🔌 Short Circuit", "⚙️ Settings"
])

# ==============================================================================
# --- Tab 1: Cable ---
# ==============================================================================

with tab1:
    st.header("📐 سایزینگ کابل")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            p_in = st.number_input("توان (کیلووات)", value=85.0, step=1.0, key="p_c")
            l_in = st.number_input("طول (متر)", value=90.0, step=5.0, key="l_c")
        with c2:
            s_in = st.number_input("سیگما (هدایت الکتریکی)", value=56.0, step=1.0, key="s_c")
            d_in = st.number_input("افت ولتاژ مجاز (%)", value=2.0, step=0.1, key="d_c")
    
    if st.button("🔍 محاسبه کابل", use_container_width=True):
        curr, f_size, s_size, raw = calculate_cable_fixed(p_in, l_in, s_in, 380, d_in)
        st.latex(r"S = \frac{P \times L \times 100}{\sigma \times V^2 \times \Delta V\%}")
        st.markdown(f"""
            <div class='result-box'>
                <div class='result-text'>⚡ جریان: {curr} آمپر</div>
                <div class='result-text' style='color: #1b5e20;'>📏 سایز استاندارد: {f_size} میلی‌متر مربع</div>
                <div class='result-text' style='color: #e65100;'>🚀 سایز ایمن: {s_size} میلی‌متر مربع</div>
                <p style='color: #5f6368;'>محاسبه دقیق: {raw} میلی‌متر مربع</p>
            </div>
        """, unsafe_allow_html=True)
        
        show_info_box(
            "📋 نتیجه محاسبه کابل",
            [
                'جریان نامی با توجه به توان و ولتاژ ورودی محاسبه شده است',
                'سایز استاندارد: نزدیک‌ترین سایز بالاتر به مقدار محاسبه شده',
                'سایز ایمن با در نظر گرفتن ضریب اطمینان برای طول‌های بالای ۸۰ متر',
                '<span class="highlight">فرمول:</span> S = (P × L × 100) / (σ × V² × ΔV%)'
            ]
        )

# ==============================================================================
# --- Tab 2: UPS ---
# ==============================================================================

with tab2:
    st.header("🔋 سایزینگ UPS با کابل و کلید")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            u_kva = st.number_input("توان UPS (kVA)", value=40.0, step=1.0, key="u_kva")
            u_min = st.number_input("زمان پشتیبانی (دقیقه)", value=15, step=5, key="u_min")
            ups_voltage = st.selectbox("ولتاژ ورودی (V)", [380, 400, 415], index=0, key="ups_voltage")
        with c2:
            u_bat = st.number_input("تعداد باتری‌ها", value=32, step=1, key="u_bat")
            u_volt = st.selectbox("ولتاژ باتری", [12, 24], index=0, key="u_volt")
    
    if st.button("🔍 محاسبه UPS", use_container_width=True):
        res = calculate_ups_fixed(u_kva, u_min, u_bat, u_volt)
        volt_text = "12V" if u_volt == 12 else "24V"
        
        ups_current = u_kva * 1.44
        ups_cable = get_cable_size(ups_current, ups_voltage, 0.8, 2, 50)
        ups_breaker = get_breaker_size(ups_current, "Inductive")
        
        st.latex(r"Ah = \frac{Ah_{Base} \times \frac{kVA}{10} \times 32}{N_{Battery} \times \frac{V_{Battery}}{12}}")
        
        st.markdown(f"""
            <div class='result-box'>
                <div class='result-text'>📦 ظرفیت باتری: {res} آمپر-ساعت</div>
                <div class='result-text' style='color: #0d47a1;'>🔋 تعداد باتری‌های مورد نیاز: {u_bat} عدد</div>
                <div class='result-text' style='color: #e65100;'>⚡ ولتاژ سیستم: {volt_text}</div>
                <div class='result-text' style='color: #1b5e20;'>📏 کابل پیشنهادی: {ups_cable} میلی‌متر مربع</div>
                <div class='result-text' style='color: #d32f2f;'>🛡️ کلید پیشنهادی: {ups_breaker} آمپر</div>
            </div>
        """, unsafe_allow_html=True)
        
        if u_volt == 24:
            st.info("💡 در سیستم ۲۴ ولت، ظرفیت آمپر-ساعت مورد نیاز نصف سیستم ۱۲ ولت است")
        
        st.info(f"💡 برای UPS {u_kva} kVA → جریان = {u_kva} × ۱.۴۴ = **{ups_current:.2f} آمپر** → کابل: **{ups_cable} میلی‌متر مربع** → کلید: **{ups_breaker} آمپر**")
        
        show_info_box(
            "📋 نتیجه محاسبه UPS",
            [
                'ظرفیت باتری بر اساس توان UPS، زمان پشتیبانی و تعداد باتری‌ها محاسبه شده است',
                'سایز کابل با توجه به جریان ورودی UPS و ضریب اطمینان پیشنهاد شده است',
                'کلید محافظ با در نظر گرفتن نوع بار (سلفی) انتخاب شده است',
                '<span class="highlight">فرمول:</span> Ah = (Ah_Base × kVA/10 × 32) / (N_Battery × V_Battery/12)'
            ]
        )

# ==============================================================================
# --- Tab 3: Motor ---
# ==============================================================================

with tab3:
    st.header("⚙️ سایزینگ موتور / ژنراتور با دو حالت محاسبه")
    
    st.markdown(f"""
    <div class="dual-mode-box">
        <b>📌 دو حالت محاسبه:</b><br>
        • <b>حالت توان نامی ژنراتور:</b> محاسبه بر اساس حداکثر توان ژنراتور (مناسب برای طراحی اولیه)<br>
        • <b>حالت بار مصرفی واقعی:</b> محاسبه بر اساس بار واقعی (مناسب برای انتخاب کابل و کلید اقتصادی)
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        st.subheader("🎯 مشخصات ژنراتور")
        
        c1, c2 = st.columns(2)
        with c1:
            gen_kva = st.number_input(
                "حداکثر توان ژنراتور (kVA)", 
                value=150.0, 
                step=5.0, 
                key="gen_kva",
                help="حداکثر توان نامی ژنراتور"
            )
            
            calc_mode = st.selectbox(
                "حالت محاسبه:",
                ["بر اساس حداکثر توان ژنراتور", "بر اساس بار مصرفی واقعی"],
                help="انتخاب کنید که کابل و کلید بر اساس چه توانی محاسبه شود"
            )
            
            if calc_mode == "بر اساس بار مصرفی واقعی":
                actual_load = st.number_input(
                    "بار مصرفی واقعی (kVA)", 
                    value=85.0, 
                    step=1.0, 
                    min_value=1.0,
                    key="actual_load",
                    help="بار مصرفی واقعی (برای انتخاب کابل و کلید اقتصادی)"
                )
            else:
                actual_load = gen_kva
        
        with c2:
            efficiency = st.number_input(
                "راندمان (η)", 
                value=0.85, 
                step=0.01, 
                key="motor_eff_new"
            )
            power_factor = st.number_input(
                "ضریب توان (cos φ)", 
                value=0.8, 
                step=0.01, 
                key="motor_cos_new"
            )
    
    with st.container(border=True):
        st.subheader("🔌 پارامترهای کابل و نصب")
        
        c1, c2 = st.columns(2)
        with c1:
            system_voltage = st.selectbox(
                "ولتاژ سیستم (V)", 
                [380, 400, 415, 480], 
                index=2,
                key="motor_voltage_new"
            )
            cable_length = st.number_input(
                "طول کابل (متر)", 
                value=30.0, 
                step=5.0, 
                min_value=1.0,
                key="cable_length_motor_new",
                help="طول کابل از ژنراتور تا تابلو برق"
            )
        with c2:
            conductor_type = st.selectbox(
                "نوع هادی",
                ["مس", "آلومینیوم"],
                key="conductor_type"
            )
            future_expansion = st.slider(
                "توسعه آینده (%)", 
                min_value=0, 
                max_value=100, 
                value=0, 
                step=10,
                help="درصد افزایش بار احتمالی در آینده"
            )
    
    if st.button("🔍 محاسبه ژنراتور", use_container_width=True):
        gen_current = gen_kva * 1.44
        starting_current = gen_current * 6
        
        actual_current = actual_load * 1.44
        actual_starting_current = actual_current * 6
        
        future_factor = 1 + (future_expansion / 100)
        design_current = actual_current * future_factor
        
        if calc_mode == "بر اساس حداکثر توان ژنراتور":
            base_for_cable = gen_current
            mode_label = "حداکثر توان ژنراتور"
        else:
            base_for_cable = design_current
            mode_label = f"بار واقعی ({actual_load} kVA) + توسعه آینده ({future_expansion}%)"
        
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
        st.subheader("📊 نتایج")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("⚡ جریان حداکثر ژنراتور", f"{gen_current:.2f} A")
            st.metric("⚡ جریان بار واقعی", f"{actual_current:.2f} A")
            st.metric("📐 جریان طراحی", f"{design_current:.2f} A", 
                     delta=f"بر اساس: {mode_label}")
        
        with col2:
            st.metric("🚀 جریان راه‌اندازی", f"{actual_starting_current:.2f} A")
            st.metric("📏 کابل پیشنهادی", f"{cable_size} mm²", 
                     delta=f"هادی: {conductor_type}")
            st.metric("📉 افت ولتاژ", f"{voltage_drop}%",
                     delta="مناسب" if voltage_drop <= 3 else "بالا!")
        
        st.markdown("---")
        
        st.markdown(f"""
            <div class='result-box'>
                <div class='result-text'>🔌 سایزینگ کابل</div>
                <div style='font-size: 16px;'>
                    <b>بر اساس:</b> {mode_label}<br>
                    <b>جریان طراحی:</b> {design_current:.2f} آمپر<br>
                    <b>کابل پیشنهادی:</b> {cable_size} میلی‌متر مربع ({conductor_type})<br>
                    <b>افت ولتاژ:</b> {voltage_drop}% {'✅ قابل قبول' if voltage_drop <= 3 else '⚠️ کابل بزرگ‌تر در نظر گرفته شود'}
                </div>
            </div>
            
            <div class='result-box'>
                <div class='result-text'>🛡️ سایزینگ کلید</div>
                <div style='font-size: 16px;'>
                    <b>کلید نامی:</b> {breaker_size} آمپر<br>
                    <b>کلید راه‌اندازی:</b> {starting_breaker} آمپر<br>
                    <b>نوع بار:</b> موتور (سلفی)
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if voltage_drop > 3:
            st.warning(f"⚠️ افت ولتاژ {voltage_drop}% است که از حد مجاز ۳٪ بیشتر است. کابل را به {get_cable_size(base_for_cable, system_voltage, power_factor, 2, cable_length * 1.5, conductor_type)} میلی‌متر مربع افزایش دهید.")
        
        if calc_mode == "بر اساس بار مصرفی واقعی" and actual_load < gen_kva:
            st.success(f"💡 با طراحی بر اساس بار واقعی ({actual_load} kVA) به جای حداکثر توان ژنراتور ({gen_kva} kVA)، در سایز کابل صرفه‌جویی کرده‌اید.")
        
        show_info_box(
            "📋 نتیجه محاسبه ژنراتور",
            [
                f'حالت محاسبه: {mode_label}',
                f'جریان طراحی: {design_current:.2f} آمپر',
                f'سایز کابل پیشنهادی: {cable_size} میلی‌متر مربع ({conductor_type})',
                f'افت ولتاژ: {voltage_drop}% {"(مناسب)" if voltage_drop <= 3 else "(بیش از حد مجاز)"}',
                f'کلید محافظ: {breaker_size} آمپر (نامی) | {starting_breaker} آمپر (راه‌اندازی)',
                '<span class="highlight">فرمول‌ها:</span> I_gen = kVA × ۱.۴۴ | I_design = I_actual × (۱ + درصد توسعه آینده)'
            ]
        )

# ==============================================================================
# --- Tab 4: Protection ---
# ==============================================================================

with tab4:
    st.header("🛡️ حفاظت و سایزینگ کلید")
    with st.container(border=True):
        p_curr = st.number_input("جریان بار (آمپر)", value=100.0, step=1.0, key="p_curr")
        p_type = st.selectbox("نوع بار", ["مقاومتی", "سلفی", "موتوری"], key="p_type")
        system_voltage = st.selectbox("ولتاژ سیستم (V)", [380, 400, 415], index=0, key="sys_voltage")
    
    if st.button("🔍 محاسبه حفاظت", use_container_width=True):
        # تبدیل نوع بار به انگلیسی برای توابع
        load_type_map = {
            "مقاومتی": "Resistive",
            "سلفی": "Inductive",
            "موتوری": "Motor"
        }
        p_type_en = load_type_map[p_type]
        
        b_size = get_breaker_size(p_curr, p_type_en)
        cable_size = get_cable_size(p_curr, system_voltage, 0.8, 2, 50)
        
        st.markdown(f"""
            <div class='result-box'>
                <div class='result-text'>🛡️ کلید پیشنهادی: {b_size} آمپر</div>
                <div class='result-text' style='color: #1b5e20;'>📏 کابل پیشنهادی: {cable_size} میلی‌متر مربع</div>
                <div class='result-text' style='color: #5f6368;'>📊 نوع بار: {p_type}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.info(f"💡 برای بار {p_curr} آمپر از نوع {p_type} → کابل: **{cable_size} میلی‌متر مربع** → کلید: **{b_size} آمپر**")
        
        show_info_box(
            "📋 نتیجه محاسبه حفاظت",
            [
                'کلید محافظ با توجه به جریان بار و نوع آن انتخاب شده است',
                'سایز کابل بر اساس جریان بار و افت ولتاژ مجاز پیشنهاد شده است',
                'ضریب ایمنی برای بارهای مختلف متفاوت است (مقاومتی: ۱.۲۵، سلفی: ۱.۴، موتوری: ۱.۶)',
                '<span class="highlight">فرمول:</span> I_breaker = I_load × K_safety'
            ]
        )

# ==============================================================================
# --- Tab 5: HVAC ---
# ==============================================================================

with tab5:
    st.header("❄️ تست توان سرمایشی HVAC")

    with st.container(border=True):
        st.subheader("🎯 تنظیم توان هدف")
        
        target_capacity = st.number_input(
            "توان هدف (کیلووات)", 
            value=30.0, 
            step=1.0, 
            min_value=1.0,
            format="%.1f"
        )
    
    with st.container(border=True):
        st.subheader("📊 ورودی‌های اندازه‌گیری")
        
        c1, c2 = st.columns(2)
        with c1:
            air_velocity = st.number_input(
                "سرعت باد (متر بر ثانیه)", 
                value=2.0, 
                step=0.1, 
                format="%.1f"
            )
            
            area_method = st.radio(
                "روش محاسبه سطح مقطع کویل:",
                ["ورود دستی", "محاسبه از روی فن‌ها"]
            )
            
            if area_method == "ورود دستی":
                coil_area = st.number_input(
                    "سطح مقطع کویل (متر مربع)", 
                    value=1.0, 
                    step=0.05, 
                    format="%.2f"
                )
                fan_info = None
            else:
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    num_fans = st.number_input(
                        "تعداد فن‌ها", 
                        value=6, 
                        step=1, 
                        min_value=1
                    )
                with col_f2:
                    fan_diameter = st.number_input(
                        "قطر فن (سانتی‌متر)", 
                        value=30.0, 
                        step=1.0, 
                        min_value=1.0,
                        format="%.1f"
                    )
                
                coil_area = calculate_coil_area_from_fans(num_fans, fan_diameter)
                
                fan_radius = (fan_diameter / 100) / 2
                single_fan_area = math.pi * (fan_radius ** 2)
                
                st.info(f"""
                    **📐 سطح مقطع کویل محاسبه شده از روی فن‌ها:**
                    - تعداد فن‌ها: {num_fans}
                    - قطر فن: {fan_diameter} سانتی‌متر
                    - سطح مقطع هر فن: {single_fan_area:.4f} متر مربع
                    - **سطح مقطع کل کویل: {coil_area:.4f} متر مربع**
                """)
                
                fan_info = {
                    'num_fans': num_fans,
                    'fan_diameter': fan_diameter,
                    'single_fan_area': single_fan_area,
                    'total_area': coil_area
                }
        
        with c2:
            temp_in = st.number_input(
                "دمای هوای ورودی (°C)", 
                value=35.0, 
                step=0.5, 
                format="%.1f"
            )
            temp_out = st.number_input(
                "دمای هوای خروجی (°C)", 
                value=23.0, 
                step=0.5, 
                format="%.1f"
            )
    
    with st.container(border=True):
        st.subheader("⚙️ پارامترهای پیشرفته")
        c1, c2 = st.columns(2)
        with c1:
            air_density = st.number_input(
                "چگالی هوا (kg/m³)", 
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
    
    if st.button("❄️ اجرای تست سرمایشی", use_container_width=True):
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
        st.subheader("📊 نتایج تست")
        
        if fan_info:
            st.markdown(f"""
            <div style='background-color: #f5f5f5; padding: 10px; border-radius: 8px; margin-bottom: 10px; direction: rtl; text-align: right;'>
                <b>🔧 اطلاعات فن‌ها:</b>
                {fan_info['num_fans']} فن با قطر {fan_info['fan_diameter']} سانتی‌متر 
                → سطح مقطع کل: {fan_info['total_area']:.4f} متر مربع
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🌬️ دبی حجمی", f"{result['volume_flow']} m³/s")
            st.metric("🌡️ اختلاف دما (ΔT)", f"{result['delta_t']} °C")
        with col2:
            st.metric("⚖️ دبی جرمی", f"{result['mass_flow']} kg/s")
            st.metric("🎯 توان هدف", f"{result['target']} kW")
        with col3:
            st.metric("❄️ توان سرمایشی", f"{result['capacity']} kW", 
                     delta=f"{result['percentage']}%")
        
        st.markdown("---")
        
        status_class = result['status_color']
        
        st.markdown(f"""
            <div class='result-box {status_class}' style='text-align: center; padding: 20px;'>
                <div style='font-size: 24px; font-weight: 700; margin-bottom: 10px;'>
                    {result['status_text']}
                </div>
                <div style='font-size: 20px; font-weight: 600;'>
                    توان محاسبه شده: <span style='color: #1a73e8;'>{result['capacity']} کیلووات</span>
                    &nbsp;|&nbsp; درصد توان: <span style='color: #1a73e8;'>{result['percentage']}%</span>
                    &nbsp;|&nbsp; وضعیت: <span style='color: #1a73e8;'>{result['status']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📝 جزئیات محاسبات"):
            st.markdown(f"""
            <div style='padding: 10px; direction: rtl; text-align: right;'>
                <b>مراحل محاسبه:</b><br><br>
                ۱. <b>دبی حجمی هوا:</b> Q = سرعت باد × سطح مقطع = {air_velocity} × {coil_area:.4f} = <b>{result['volume_flow']} m³/s</b><br><br>
                ۲. <b>دبی جرمی هوا:</b> ṁ = Q × ρ = {result['volume_flow']} × {air_density} = <b>{result['mass_flow']} kg/s</b><br><br>
                ۳. <b>اختلاف دما:</b> ΔT = T_ورودی - T_خروجی = {temp_in} - {temp_out} = <b>{result['delta_t']} °C</b><br><br>
                ۴. <b>توان سرمایشی:</b> P = ṁ × Cₚ × ΔT = {result['mass_flow']} × {cp} × {result['delta_t']} = <b>{result['capacity']} کیلووات</b>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("💡 پیشنهادات"):
            suggestions = []
            
            if result['capacity'] < target_capacity:
                needed_velocity = (target_capacity * air_velocity) / result['capacity']
                if needed_velocity > air_velocity:
                    suggestions.append(f"🔹 افزایش سرعت باد به حدود **{needed_velocity:.2f} متر بر ثانیه** (از {air_velocity} متر بر ثانیه)")
                
                if fan_info:
                    needed_area = (target_capacity * coil_area) / result['capacity']
                    if needed_area > coil_area:
                        needed_fans = (needed_area / fan_info['single_fan_area'])
                        suggestions.append(f"🔹 افزایش تعداد فن‌ها به حدود **{math.ceil(needed_fans)}** عدد (از {fan_info['num_fans']} عدد)")
                
                needed_delta = (target_capacity * result['delta_t']) / result['capacity']
                if needed_delta > result['delta_t']:
                    needed_temp_out = temp_in - needed_delta
                    suggestions.append(f"🔹 کاهش دمای خروجی به حدود **{needed_temp_out:.1f} درجه سانتی‌گراد** (از {temp_out} درجه سانتی‌گراد)")
                
                if not suggestions:
                    suggestions.append("🔸 سیستم نیاز به بررسی کامل دارد.")
            else:
                suggestions.append(f"✅ سیستم به توان اسمی {target_capacity} کیلووات رسیده است.")
            
            for s in suggestions:
                st.markdown(s)
    
    show_info_box(
        "📋 روش تست توان سرمایشی",
        [
            'تست با استفاده از بادسنج (انیمومتر) - اندازه‌گیری غیرمستقیم',
            'فرمول: P = ṁ × Cₚ × ΔT',
            'پارامترهای پیش‌فرض: چگالی هوا = ۱.۲ kg/m³ | Cₚ = ۱.۰۰۵ kJ/kg·K',
            'توان هدف قابل تنظیم - هر توان سرمایشی را تست کنید',
            '<span class="highlight">تفسیر نتایج:</span> ✅ PASS (≥ ۹۵%) | ⚠️ WARNING (۸۰%-۹۵%) | ❌ FAIL (< ۸۰%)'
        ]
    )
    
    with st.expander("📖 راهنمای انجام تست"):
        st.markdown("""
        ### 🔍 مراحل انجام تست:
        
        1. **تنظیم توان هدف** - توان اسمی سیستم خود را وارد کنید
        
        2. **اندازه‌گیری سرعت باد** با بادسنج در نقاط مختلف کویل و گرفتن میانگین
        
        3. **انتخاب روش محاسبه سطح مقطع:**
           - **ورود دستی:** سطح مقطع را مستقیم وارد کنید
           - **محاسبه از روی فن‌ها:** تعداد و قطر فن‌ها را وارد کنید تا سطح مقطع خودکار محاسبه شود
        
        4. **اندازه‌گیری دمای ورودی و خروجی** هوا با دماسنج دقیق
        
        5. **وارد کردن مقادیر** در فرم بالا و کلیک روی دکمه تست
        
        ---
        
        ### ⚠️ نکات مهم:
        
        - تست باید در **شرایط پایدار** (Steady-State) انجام شود
        - اگر دمای کویل از نقطه شبنم پایین‌تر باشد، رطوبت تبدیل به آب شده و محاسبات دقیق‌تر نیاز به اندازه‌گیری رطوبت دارد
        - برای دقت بیشتر، اندازه‌گیری را در **یک شبکه منظم (Grid)** روی سطح کویل انجام دهید
        """)

# ==============================================================================
# --- Tab 6: Short Circuit ---
# ==============================================================================

with tab6:
    st.header("🔌 محاسبه اتصال کوتاه ترانسفورماتور")
    
    st.markdown(f"""
    <div class="sc-box">
        <b>📌 محاسبه جریان اتصال کوتاه ترانسفورماتور:</b><br>
        • جریان اتصال کوتاه در پایانه‌های ترانس: Isc = In × (100 / Uk%)<br>
        • با افزایش فاصله از ترانس، کابل‌ها وارد مدار شده و جریان اتصال کوتاه کاهش می‌یابد<br>
        • برای انتخاب کلید مناسب، باید قدرت قطع آن از جریان اتصال کوتاه نقطه نصب بیشتر باشد
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        st.subheader("📊 پارامترهای ترانسفورماتور")
        
        c1, c2 = st.columns(2)
        with c1:
            transformer_kva = st.number_input(
                "توان ترانسفورماتور (kVA)", 
                value=1000.0, 
                step=50.0, 
                min_value=50.0,
                key="sc_kva"
            )
            uk_percent = st.number_input(
                "ولتاژ اتصال کوتاه Uk (%)", 
                value=4.7, 
                step=0.1, 
                min_value=1.0,
                max_value=20.0,
                key="sc_uk"
            )
            system_voltage = st.selectbox(
                "ولتاژ سیستم (V)", 
                [400, 415, 480], 
                index=0,
                key="sc_voltage"
            )
        
        with c2:
            st.subheader("🔌 پارامترهای کابل")
            conductor_type = st.selectbox(
                "نوع هادی",
                ["مس", "آلومینیوم"],
                key="sc_conductor"
            )
            cable_size = st.selectbox(
                "سطح مقطع کابل (mm²)",
                [120, 150, 185, 240, 300, 400],
                index=3,
                key="sc_cable_size"
            )
            num_cables = st.number_input(
                "تعداد کابل‌های موازی",
                value=3,
                step=1,
                min_value=1,
                max_value=6,
                key="sc_num_cables"
            )
            cable_length = st.number_input(
                "طول کابل (متر)",
                value=200.0,
                step=10.0,
                min_value=1.0,
                key="sc_cable_length"
            )
    
    if st.button("🔍 محاسبه اتصال کوتاه", use_container_width=True):
        result = calculate_short_circuit(
            transformer_kva=transformer_kva,
            uk_percent=uk_percent,
            voltage=system_voltage,
            cable_size=cable_size,
            cable_length=cable_length,
            num_cables=num_cables,
            conductor_type=conductor_type
        )
        
        st.markdown("---")
        st.subheader("📊 نتایج")
        
        # Display results in columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("⚡ جریان نامی", f"{result['rated_current']:.1f} A")
            st.metric("🔌 امپدانس ترانس", f"{result['z_transformer']:.3f} mΩ")
        with col2:
            st.metric("🔥 جریان اتصال کوتاه در پایانه ترانس", f"{result['isc_transformer']:.2f} kA")
            st.metric("📏 امپدانس کابل", f"{result['z_cable']:.3f} mΩ")
        with col3:
            st.metric("🔽 جریان اتصال کوتاه در انتهای کابل", f"{result['isc_cable_end']:.2f} kA")
            st.metric("📊 امپدانس کل", f"{result['z_total']:.3f} mΩ")
        
        st.markdown("---")
        
        # Breaker check
        breaker_rating = 10  # kA
        isc_ka = result['isc_transformer']
        
        if isc_ka <= breaker_rating:
            st.success(f"✅ کلید ۱۰kA استاندارد برای این نقطه **مناسب** است (Isc = {isc_ka:.2f} kA)")
        else:
            st.error(f"❌ کلید ۱۰kA استاندارد برای این نقطه **مناسب نیست** (Isc = {isc_ka:.2f} kA > ۱۰kA)")
            st.warning(f"⚠️ لطفاً از کلید با قدرت قطع **{math.ceil(isc_ka / 5) * 5:.0f} kA** یا بیشتر استفاده کنید")
        
        st.markdown("---")
        
        # Detailed calculation display
        with st.expander("📝 جزئیات محاسبات"):
            st.markdown(f"""
            <div style='padding: 10px; direction: rtl; text-align: right;'>
                <b>مراحل محاسبه جریان اتصال کوتاه:</b><br><br>
                
                <b>۱. محاسبه جریان نامی ترانسفورماتور:</b><br>
                I_n = S / (√3 × V) = {transformer_kva} × ۱۰۰۰ / (√۳ × {system_voltage}) = <b>{result['rated_current']:.1f} A</b><br><br>
                
                <b>۲. محاسبه جریان اتصال کوتاه در پایانه‌های ترانس:</b><br>
                I_sc = I_n × (۱۰۰ / Uk%) = {result['rated_current']:.1f} × (۱۰۰ / {uk_percent}) = <b>{result['isc_transformer']:.2f} kA</b><br><br>
                
                <b>۳. امپدانس ترانسفورماتور:</b><br>
                Z_T = (Uk% / ۱۰۰) × (V² / S) = ({uk_percent} / ۱۰۰) × ({system_voltage}² / ({transformer_kva} × ۱۰۰۰)) = <b>{result['z_transformer']:.3f} mΩ</b><br><br>
                
                <b>۴. امپدانس کابل‌ها:</b><br>
                {num_cables} رشته کابل {conductor_type} به سطح مقطع {cable_size} mm² به طول {cable_length} متر<br>
                Z_cable ≈ <b>{result['z_cable']:.3f} mΩ</b><br><br>
                
                <b>۵. امپدانس کل:</b><br>
                Z_total = Z_T + Z_cable = {result['z_transformer']:.3f} + {result['z_cable']:.3f} = <b>{result['z_total']:.3f} mΩ</b><br><br>
                
                <b>۶. جریان اتصال کوتاه در انتهای کابل:</b><br>
                I_sc_end = V / (√۳ × Z_total) = {system_voltage} / (√۳ × {result['z_total']:.3f} × ۱۰⁻³) = <b>{result['isc_cable_end']:.2f} kA</b>
            </div>
            """, unsafe_allow_html=True)
        
        # Voltage drop comparison
        with st.expander("💡 تحلیل و توصیه‌ها"):
            reduction_percent = (1 - result['isc_cable_end'] / result['isc_transformer']) * 100
            st.markdown(f"""
            <div style='padding: 10px; direction: rtl; text-align: right;'>
                <b>تحلیل نتایج:</b><br><br>
                
                ✅ جریان اتصال کوتاه در پایانه‌های ترانس: <b>{result['isc_transformer']:.2f} kA</b><br>
                ✅ جریان اتصال کوتاه در انتهای کابل: <b>{result['isc_cable_end']:.2f} kA</b><br>
                ✅ کاهش جریان اتصال کوتاه: <b>{reduction_percent:.1f}%</b><br><br>
                
                <b>توصیه‌ها:</b><br>
                • قدرت قطع کلید باید از جریان اتصال کوتاه نقطه نصب بیشتر باشد<br>
                • برای کلید نصب شده در پایانه ترانس: نیاز به کلید با قدرت قطع حداقل <b>{math.ceil(result['isc_transformer'] / 5) * 5:.0f} kA</b><br>
                • برای کلید نصب شده در انتهای کابل: نیاز به کلید با قدرت قطع حداقل <b>{math.ceil(result['isc_cable_end'] / 5) * 5:.0f} kA</b>
            </div>
            """, unsafe_allow_html=True)
    
    show_info_box(
        "📋 محاسبه جریان اتصال کوتاه ترانسفورماتور",
        [
            'جریان اتصال کوتاه با استفاده از روش امپدانس درصدی محاسبه می‌شود',
            'با افزایش فاصله از ترانس و اضافه شدن کابل‌ها، جریان اتصال کوتاه کاهش می‌یابد',
            'امپدانس کابل‌ها به امپدانس ترانس اضافه شده و جریان اتصال کوتاه را محدود می‌کند',
            'برای انتخاب کلید مناسب، قدرت قطع باید از جریان اتصال کوتاه نقطه نصب بیشتر باشد',
            '<span class="highlight">فرمول:</span> Isc = In × (۱۰۰ / Uk%) | Z_total = Z_T + Z_cable'
        ]
    )

# ==============================================================================
# --- Tab 7: Settings ---
# ==============================================================================

with tab7:
    st.header("⚙️ تنظیمات")
    
    st.markdown(f"""
    <div class="settings-box">
        <b>📋 مدیریت تنظیمات نرم‌افزار</b><br>
        در این بخش می‌توانید تنظیمات ظاهری نرم‌افزار را تغییر دهید.
    </div>
    """, unsafe_allow_html=True)
    
    # ========== Theme Settings ==========
    st.subheader("🌓 تنظیمات تم")
    
    col1, col2 = st.columns(2)
    with col1:
        current_theme = "🌞 روشن" if st.session_state.theme == 'light' else "🌙 تاریک"
        st.info(f"تم فعلی: **{current_theme}**")
    
    with col2:
        theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
        theme_label = "تغییر به حالت تاریک" if st.session_state.theme == 'light' else "تغییر به حالت روشن"
        
        if st.button(f"{theme_icon} {theme_label}", use_container_width=True):
            toggle_theme()
            st.rerun()
    
    st.divider()
    
    # ========== About ==========
    st.subheader("ℹ️ درباره نرم‌افزار")
    st.markdown("""
    **ElectroCalc ⚡ M&F**  
    نسخه: **۲.۱**  
    توسعه یافته برای مهندسی سیستم‌های قدرت  
    
    **استانداردهای مورد استفاده:**
    - IEC 60364 - سایزینگ کابل
    - IEEE 485 - سایزینگ UPS
    - IEC 60034 - محاسبات موتور
    - IEC 60947 - انتخاب کلید
    - IEC 60909 - اتصال کوتاه
    """)
    
    st.divider()
    
    # ========== Status ==========
    st.subheader("🔒 وضعیت")
    st.markdown(f"""
    ✅ **وضعیت نرم‌افزار:** آنلاین  
    ✅ **تم:** {current_theme}  
    ✅ **نسخه:** ۲.۱
    """)
