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
# --- مدیریت تم در Session State ---
# ==============================================================================

if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

def toggle_theme():
    if st.session_state.theme == 'light':
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'

# تعیین رنگ‌ها بر اساس تم
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
# --- استایل ---
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
# --- نمایش اسم نرم‌افزار ---
# ==============================================================================

st.markdown(f"""
    <div class="app-title">
        ElectroCalc <span class="lightning">⚡</span> M&F
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# --- تابع برای نمایش جعبه اطلاعات ---
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
# --- توابع کمکی ---
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
# --- تب‌ها (7 تب) ---
# ==============================================================================

tabs = st.tabs(["📏 Cable", "🔋 UPS", "⚙️ Motor", "🛡️ Protect", "❄️ HVAC Test", "⚡ Short Circuit", "⚙️ Settings"])

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
# --- تب ۳: موتور ---
# ==============================================================================

with tabs[2]:
    st.header("⚙️ Motor / Generator Sizing with Dual Mode")
    
    st.markdown(f"""
    <div class="dual-mode-box">
        <b>📌 دو حالت محاسبه:</b><br>
        • <b>حالت توان نامی موتور:</b> محاسبه بر اساس حداکثر توان ژنراتور (مناسب برای طراحی اولیه)<br>
        • <b>حالت توان بار مصرفی:</b> محاسبه بر اساس بار واقعی (مناسب برای انتخاب کابل و کلید اقتصادی)
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
                help="حداکثر توان نامی ژنراتور"
            )
            
            calc_mode = st.selectbox(
                "Calculation Mode:",
                ["Based on Generator Max Power", "Based on Actual Load"],
                help="انتخاب کنید که کابل و کلید بر اساس چه توانی محاسبه شود"
            )
            
            if calc_mode == "Based on Actual Load":
                actual_load = st.number_input(
                    "Actual Load (kVA)", 
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
                help="طول کابل از ژنراتور تا تابلو برق"
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
                help="درصد افزایش بار احتمالی در آینده"
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
            "📋 نتیجه محاسبه ژنراتور",
            [
                f'حالت محاسبه: {mode_label}',
                f'جریان طراحی: {design_current:.2f} آمپر',
                f'سایز کابل پیشنهادی: {cable_size} میلی‌متر مربع ({conductor_type})',
                f'افت ولتاژ: {voltage_drop}% {"(مناسب)" if voltage_drop <= 3 else "(بیش از حد مجاز)"}',
                f'کلید محافظ: {breaker_size} آمپر (نامی) | {starting_breaker} آمپر (راه‌اندازی)',
                '<span class="highlight">فرمول‌ها:</span> I_gen = kVA × 1.44 | I_design = I_actual × (1 + Future Expansion%)'
            ]
        )

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
# --- تب ۵: HVAC ---
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
                <b>🔧 اطلاعات فن‌ها:</b>
                {fan_info['num_fans']} فن با قطر {fan_info['fan_diameter']} سانتی‌متر 
                → سطح مقطع کل: {fan_info['total_area']:.4f} متر مربع
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
    
    with st.expander("📖 Test Procedure Guide (راهنمای انجام تست)"):
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
# --- تب ۶: اتصال کوتاه (Short Circuit) - اصلاح شده ---
# ==============================================================================

with tabs[5]:
    st.header("⚡ محاسبه اتصال کوتاه (Short Circuit)")
    st.info("محاسبه جریان اتصال کوتاه برای ترانسفورماتور و ژنراتور بر اساس IEC 60909", icon="ℹ️")
    
    # ========== انتخاب منبع ==========
    source_type = st.radio(
        "نوع منبع:",
        ["🔴 ترانسفورماتور", "🟢 ژنراتور", "🔵 ترکیبی (ترانس + ژنراتور)"],
        horizontal=True
    )
    
    st.markdown("---")
    
    # ==========================================
    # بخش ۱: ترانسفورماتور
    # ==========================================
    if source_type in ["🔴 ترانسفورماتور", "🔵 ترکیبی (ترانس + ژنراتور)"]:
        st.subheader("🔴 مشخصات ترانسفورماتور")
        
        col1, col2 = st.columns(2)
        with col1:
            S_nom_tr = st.number_input(
                "توان نامی ترانسفورماتور (kVA)", 
                value=1000.0, 
                step=50.0, 
                min_value=10.0,
                format="%.1f",
                key="tr_s"
            )
            V_sec_tr = st.number_input(
                "ولتاژ ثانویه (V)", 
                value=400.0, 
                step=50.0, 
                min_value=100.0,
                format="%.0f",
                key="tr_v"
            )
            Uk_percent = st.number_input(
                "ولتاژ اتصال کوتاه Uk%", 
                value=4.7, 
                step=0.1, 
                min_value=0.1, 
                max_value=30.0,
                format="%.1f",
                key="tr_uk",
                help="معمولاً بین ۴ تا ۱۲ درصد - میتواند هر عددی باشد"
            )
        
        with col2:
            P_k_tr = st.number_input(
                "تلفات اتصال کوتاه (kW)", 
                value=10.0, 
                step=1.0, 
                min_value=0.0,
                format="%.1f",
                key="tr_pk",
                help="اختیاری - برای محاسبه دقیق مقاومت"
            )
            X_over_R_tr = st.number_input(
                "نسبت X/R", 
                value=5.0, 
                step=0.5, 
                min_value=0.1,
                format="%.1f",
                key="tr_xr",
                help="اختیاری - اگر تلفات وارد نشده باشد"
            )
            V_pri_tr = st.number_input(
                "ولتاژ اولیه (kV)", 
                value=20.0, 
                step=1.0, 
                min_value=0.4,
                format="%.1f",
                key="tr_vp"
            )
    
    # ==========================================
    # بخش ۲: ژنراتور
    # ==========================================
    if source_type in ["🟢 ژنراتور", "🔵 ترکیبی (ترانس + ژنراتور)"]:
        if source_type == "🔵 ترکیبی (ترانس + ژنراتور)":
            st.markdown("---")
        
        st.subheader("🟢 مشخصات ژنراتور")
        
        col1, col2 = st.columns(2)
        with col1:
            S_nom_gen = st.number_input(
                "توان نامی ژنراتور (kVA)", 
                value=1500.0, 
                step=50.0, 
                min_value=10.0,
                format="%.1f",
                key="gen_s"
            )
            V_nom_gen = st.number_input(
                "ولتاژ نامی (V)", 
                value=400.0, 
                step=50.0, 
                min_value=100.0,
                format="%.0f",
                key="gen_v"
            )
            Xd_percent = st.number_input(
                "راکتانس زیرگذرا Xd″%", 
                value=15.0, 
                step=0.5, 
                min_value=1.0,
                max_value=30.0,
                format="%.1f",
                key="gen_xd",
                help="معمولاً بین ۱۲ تا ۲۰ درصد"
            )
        
        with col2:
            X_over_R_gen = st.number_input(
                "نسبت Xd″/R", 
                value=10.0, 
                step=1.0, 
                min_value=1.0,
                format="%.1f",
                key="gen_xr",
                help="معمولاً بین ۵ تا ۳۰"
            )
            Xd_prime = st.number_input(
                "راکتانس گذرا Xd′% (اختیاری)", 
                value=25.0, 
                step=0.5, 
                min_value=0.0,
                format="%.1f",
                key="gen_xdp",
                help="برای محاسبه جریان گذرا"
            )
            Xd_steady = st.number_input(
                "راکتانس ماندگار Xd% (اختیاری)", 
                value=100.0, 
                step=5.0, 
                min_value=0.0,
                format="%.1f",
                key="gen_xds",
                help="برای محاسبه جریان ماندگار"
            )
    
    # ==========================================
    # بخش ۳: کابلها
    # ==========================================
    st.markdown("---")
    st.subheader("📏 مشخصات کابلها (برای محاسبه در انتهای مسیر)")
    
    with st.expander("🔧 تنظیمات کابل", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            cable_length = st.number_input(
                "طول مسیر (m)", 
                value=200.0, 
                step=10.0, 
                min_value=0.0,
                format="%.0f",
                key="cable_len"
            )
            cable_area = st.number_input(
                "سطح مقطع هر رشته (mm²)", 
                value=240.0, 
                step=10.0, 
                min_value=1.0,
                format="%.0f",
                key="cable_area"
            )
        
        with col2:
            cable_count = st.number_input(
                "تعداد رشتههای موازی", 
                value=3, 
                step=1, 
                min_value=1,
                key="cable_count"
            )
            conductor_type = st.selectbox(
                "جنس هادی",
                ["مس", "آلومینیوم"],
                key="conductor_type_sc"
            )
        
        with col3:
            cable_temp = st.number_input(
                "دمای کابل (°C)", 
                value=40.0, 
                step=5.0, 
                min_value=20.0,
                format="%.0f",
                key="cable_temp"
            )
            include_cable = st.checkbox(
                "✔️ در نظر گرفتن کابل در محاسبه", 
                value=True,
                key="include_cable"
            )
    
    # ==========================================
    # دکمه محاسبه
    # ==========================================
    st.markdown("---")
    
    if st.button("⚡ محاسبه جریان اتصال کوتاه", type="primary", use_container_width=True):
        
        results = {}
        error_message = None
        
        try:
            # ===== ترانسفورماتور =====
            if source_type in ["🔴 ترانسفورماتور", "🔵 ترکیبی (ترانس + ژنراتور)"]:
                
                I_nom_tr = (S_nom_tr * 1000) / (math.sqrt(3) * V_sec_tr)
                Z_tr = (Uk_percent / 100) * (V_sec_tr**2 / (S_nom_tr * 1000))
                
                if P_k_tr > 0:
                    R_tr = (P_k_tr * 1000 * V_sec_tr**2) / (S_nom_tr * 1000)**2
                    X_tr = math.sqrt(max(0, Z_tr**2 - R_tr**2))
                else:
                    if X_over_R_tr > 0:
                        X_over_R_use = X_over_R_tr
                    else:
                        if Uk_percent <= 4:
                            X_over_R_use = 3
                        elif Uk_percent <= 6:
                            X_over_R_use = 5
                        elif Uk_percent <= 8:
                            X_over_R_use = 8
                        elif Uk_percent <= 12:
                            X_over_R_use = 12
                        else:
                            X_over_R_use = 15
                    
                    R_tr = Z_tr / math.sqrt(1 + X_over_R_use**2)
                    X_tr = R_tr * X_over_R_use
                
                I_sc_tr = (V_sec_tr / math.sqrt(3)) / Z_tr
                I_sc_simple = I_nom_tr * (100 / Uk_percent)
                kappa_tr = 1.02 + 0.98 * math.exp(-3 * (X_tr / R_tr)) if R_tr > 0 else 1.8
                I_peak_tr = kappa_tr * math.sqrt(2) * I_sc_tr
                S_sc_tr = math.sqrt(3) * V_sec_tr * I_sc_tr / 1000
                
                results['transformer'] = {
                    'I_nom': I_nom_tr,
                    'Z_tr': Z_tr,
                    'R_tr': R_tr,
                    'X_tr': X_tr,
                    'X_over_R': X_tr / R_tr if R_tr > 0 else 0,
                    'I_sc': I_sc_tr,
                    'I_sc_simple': I_sc_simple,
                    'S_sc': S_sc_tr,
                    'kappa': kappa_tr,
                    'I_peak': I_peak_tr
                }
            
            # ===== ژنراتور =====
            if source_type in ["🟢 ژنراتور", "🔵 ترکیبی (ترانس + ژنراتور)"]:
                
                I_nom_gen = (S_nom_gen * 1000) / (math.sqrt(3) * V_nom_gen)
                Xd = (Xd_percent / 100) * (V_nom_gen**2 / (S_nom_gen * 1000))
                
                if X_over_R_gen > 0:
                    R_gen = Xd / X_over_R_gen
                else:
                    R_gen = Xd / 10
                
                Z_gen = math.sqrt(R_gen**2 + Xd**2)
                I_sc_sub = (V_nom_gen / math.sqrt(3)) / Xd
                
                if Xd_prime > 0:
                    Xd_p = (Xd_prime / 100) * (V_nom_gen**2 / (S_nom_gen * 1000))
                    I_sc_trans = (V_nom_gen / math.sqrt(3)) / Xd_p
                else:
                    I_sc_trans = None
                
                if Xd_steady > 0:
                    Xd_s = (Xd_steady / 100) * (V_nom_gen**2 / (S_nom_gen * 1000))
                    I_sc_steady = (V_nom_gen / math.sqrt(3)) / Xd_s
                else:
                    I_sc_steady = None
                
                kappa_gen = 1.02 + 0.98 * math.exp(-3 * (Xd / R_gen)) if R_gen > 0 else 1.8
                I_peak_gen = kappa_gen * math.sqrt(2) * I_sc_sub
                I_asym_gen = I_sc_sub * math.sqrt(1 + 2 * (kappa_gen - 1)**2)
                
                results['generator'] = {
                    'I_nom': I_nom_gen,
                    'Xd': Xd,
                    'R_gen': R_gen,
                    'Z_gen': Z_gen,
                    'X_over_R': Xd / R_gen if R_gen > 0 else 0,
                    'I_sc_sub': I_sc_sub,
                    'I_sc_trans': I_sc_trans,
                    'I_sc_steady': I_sc_steady,
                    'kappa': kappa_gen,
                    'I_peak': I_peak_gen,
                    'I_asym': I_asym_gen
                }
            
            # ===== کابلها =====
            if include_cable and cable_length > 0:
                
                if conductor_type == "مس":
                    rho_20 = 0.01724
                    alpha = 0.00393
                else:
                    rho_20 = 0.02826
                    alpha = 0.00403
                
                rho = rho_20 * (1 + alpha * (cable_temp - 20))
                R_single = rho * cable_length / cable_area
                R_cable = R_single / cable_count
                
                if cable_area <= 16:
                    X_per_km = 0.085
                elif cable_area <= 35:
                    X_per_km = 0.075
                elif cable_area <= 70:
                    X_per_km = 0.065
                elif cable_area <= 120:
                    X_per_km = 0.055
                elif cable_area <= 185:
                    X_per_km = 0.045
                else:
                    X_per_km = 0.038
                
                X_cable = X_per_km * cable_length / 1000 / cable_count
                Z_cable = math.sqrt(R_cable**2 + X_cable**2)
                
                results['cable'] = {
                    'R_cable': R_cable,
                    'X_cable': X_cable,
                    'Z_cable': Z_cable
                }
            
            # ===== نمایش نتایج =====
            st.markdown("---")
            st.subheader("📊 نتایج محاسبه")
            
            # --- نتایج ترانسفورماتور ---
            if 'transformer' in results:
                tr = results['transformer']
                st.markdown("### 🔴 نتایج ترانسفورماتور")
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("جریان نامی", f"{tr['I_nom']:.1f} A")
                    st.metric("امپدانس Z_tr", f"{tr['Z_tr']:.4f} Ω")
                    st.metric("نسبت X/R", f"{tr['X_over_R']:.2f}")
                with c2:
                    st.metric("جریان اتصال کوتاه", f"{tr['I_sc']/1000:.2f} kA")
                    st.metric("مقاومت R_tr", f"{tr['R_tr']:.4f} Ω")
                    st.metric("ضریب پیک κ", f"{tr['kappa']:.3f}")
                with c3:
                    st.metric("توان اتصال کوتاه", f"{tr['S_sc']:.1f} MVA")
                    st.metric("راکتانس X_tr", f"{tr['X_tr']:.4f} Ω")
                    st.metric("جریان پیک I_peak", f"{tr['I_peak']/1000:.2f} kA")
            
            # --- نتایج ژنراتور ---
            if 'generator' in results:
                gen = results['generator']
                st.markdown("### 🟢 نتایج ژنراتور")
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("جریان نامی", f"{gen['I_nom']:.1f} A")
                    st.metric("راکتانس Xd″", f"{gen['Xd']:.4f} Ω")
                    st.metric("نسبت X/R", f"{gen['X_over_R']:.2f}")
                with c2:
                    st.metric("جریان زیرگذرا", f"{gen['I_sc_sub']/1000:.2f} kA")
                    if gen['I_sc_trans']:
                        st.metric("جریان گذرا", f"{gen['I_sc_trans']/1000:.2f} kA")
                    if gen['I_sc_steady']:
                        st.metric("جریان ماندگار", f"{gen['I_sc_steady']/1000:.2f} kA")
                with c3:
                    st.metric("ضریب پیک κ", f"{gen['kappa']:.3f}")
                    st.metric("جریان پیک I_peak", f"{gen['I_peak']/1000:.2f} kA")
                    st.metric("جریان نامتقارن", f"{gen['I_asym']/1000:.2f} kA")
            
            # --- نتایج کابل ---
            if 'cable' in results and include_cable and cable_length > 0:
                cab = results['cable']
                st.markdown("### 📏 نتایج کابلها")
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("مقاومت کل R_cable", f"{cab['R_cable']:.6f} Ω")
                    st.metric("امپدانس Z_cable", f"{cab['Z_cable']:.6f} Ω")
                with c2:
                    st.metric("راکتانس X_cable", f"{cab['X_cable']:.6f} Ω")
                
                if 'transformer' in results:
                    tr = results['transformer']
                    R_total = tr['R_tr'] + cab['R_cable']
                    X_total = tr['X_tr'] + cab['X_cable']
                    Z_total = math.sqrt(R_total**2 + X_total**2)
                    I_sc_end = (V_sec_tr / math.sqrt(3)) / Z_total
                    reduction = ((tr['I_sc'] - I_sc_end) / tr['I_sc']) * 100
                    
                    with c3:
                        st.metric("جریان در انتهای کابل", f"{I_sc_end/1000:.2f} kA")
                        st.metric("کاهش جریان", f"{reduction:.1f}%")
                    
                    st.info(f"""
                    **امپدانس کل مسیر (ترانس + کابل):**
                    - R_total = {R_total:.6f} Ω
                    - X_total = {X_total:.6f} Ω
                    - Z_total = {Z_total:.6f} Ω
                    """)
            
            # --- انتخاب کلید مناسب ---
            st.markdown("---")
            st.subheader("🛡️ انتخاب کلید مناسب")
            
            sc_values = []
            if 'transformer' in results:
                sc_values.append(('ترمینال ترانس', results['transformer']['I_sc']))
                if 'cable' in results and include_cable and cable_length > 0:
                    sc_values.append(('انتهای کابل', I_sc_end))
            if 'generator' in results:
                sc_values.append(('ژنراتور', results['generator']['I_sc_sub']))
            
            for location, current in sc_values:
                recommended = math.ceil(current / 1000) * 1000
                st.markdown(f"""
                **📍 {location}:** جریان اتصال کوتاه = **{current/1000:.2f} kA**  
                ✅ کلید پیشنهادی: **≥ {recommended} A**  
                """)
            
            # --- نمایش فرمولها ---
            with st.expander("📐 مشاهده فرمولهای محاسبه"):
                st.markdown("""
                **فرمولهای ترانسفورماتور:**
                
