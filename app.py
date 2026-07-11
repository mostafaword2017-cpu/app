import streamlit as st
import math
import numpy as np
import pandas as pd

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

def toggle_theme():
    if st.session_state.theme == 'light':
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'

if st.session_state.theme == 'light':
    bg_color = "#ffffff"
    text_color = "#1a1a1a"
    card_bg = "#f8f9fa"
    border_color = "#e0e0e0"
    tab_bg = "#f0f2f6"
    tab_active = "#4CAF50"
    button_bg = "#007BFF"
    button_text = "#ffffff"
    metric_bg = "#f8f9fa"
    input_bg = "#ffffff"
    expander_bg = "#f8f9fa"
else:
    bg_color = "#1a1a1a"
    text_color = "#f0f0f0"
    card_bg = "#2d2d2d"
    border_color = "#404040"
    tab_bg = "#333333"
    tab_active = "#4CAF50"
    button_bg = "#0d6efd"
    button_text = "#ffffff"
    metric_bg = "#2d2d2d"
    input_bg = "#333333"
    expander_bg = "#2d2d2d"

# ==============================================================================
# --- استایل ---
# ==============================================================================

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color} !important;
    }}
    
    .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label {{
        color: {text_color} !important;
    }}
    
    header div[data-testid="stHeader"] a, 
    div[data-testid="stAppDeployButton"], 
    #MainMenu {{
        display: none !important;
    }}
    
    .theme-button-container {{
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 9999;
    }}
    
    .theme-button {{
        background-color: {tab_bg};
        color: {text_color};
        border: 1px solid {border_color};
        border-radius: 50%;
        width: 40px;
        height: 40px;
        font-size: 20px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }}
    
    .theme-button:hover {{
        transform: scale(1.1);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}
    
    .stApp h1 {{
        font-size: 34px !important;
        text-align: center !important;
        white-space: nowrap !important;
        letter-spacing: 0px !important;
        font-weight: 700 !important;
        padding: 10px 0 !important;
        margin: 0 auto !important;
        display: block !important;
        width: 100% !important;
        color: {text_color} !important;
    }}
    
    @media screen and (max-width: 480px) {{
        .stApp h1 {{
            font-size: 26px !important;
            letter-spacing: -0.3px !important;
        }}
        .theme-button {{
            width: 32px;
            height: 32px;
            font-size: 16px;
        }}
    }}

    .stTabs div[role="tablist"] {{ 
        gap: 5px !important; 
        flex-wrap: nowrap !important; 
        overflow-x: auto !important;
        padding: 2px 0 !important;
        justify-content: center !important;
        display: flex !important;
    }}
    
    .stTabs [role="tab"] {{
        font-size: 16px !important;
        padding: 10px 18px !important;
        border-radius: 8px 8px 0px 0px !important;
        background-color: {tab_bg} !important;
        color: {text_color} !important;
        white-space: nowrap !important;
        min-width: 80px !important;
        text-align: center !important;
        flex: 0 0 auto !important;
        border: 1px solid {border_color} !important;
        border-bottom: none !important;
    }}
    
    @media screen and (max-width: 480px) {{
        .stTabs div[role="tablist"] {{
            gap: 3px !important;
            justify-content: center !important;
        }}
        .stTabs [role="tab"] {{
            font-size: 13px !important;
            padding: 6px 10px !important;
            min-width: 55px !important;
        }}
    }}

    .stTabs [aria-selected="true"] {{
        background-color: {tab_active} !important; 
        color: white !important;
        font-weight: 600 !important;
    }}

    label, .stMarkdown p, .stText, .stNumberInput label {{
        font-size: 13px !important;
        margin-bottom: 2px !important;
        color: {text_color} !important;
    }}
    
    @media screen and (max-width: 480px) {{
        label, .stMarkdown p, .stText, .stNumberInput label {{
            font-size: 11px !important;
        }}
    }}

    .stButton > button {{
        width: 100% !important;
        height: 42px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        background-color: {button_bg} !important;
        color: {button_text} !important;
        padding: 0 10px !important;
        border: none !important;
    }}
    
    @media screen and (max-width: 480px) {{
        .stButton > button {{
            height: 36px !important;
            font-size: 12px !important;
        }}
    }}

    div[data-testid="metric-container"] {{
        padding: 8px !important;
        background-color: {metric_bg} !important;
        border-radius: 10px !important;
        border: 1px solid {border_color} !important;
    }}
    
    div[data-testid="metric-container"] label {{
        font-size: 11px !important;
        color: {text_color} !important;
    }}
    
    div[data-testid="metric-container"] .stMetricValue {{
        font-size: 17px !important;
        font-weight: 700 !important;
        color: {text_color} !important;
    }}
    
    @media screen and (max-width: 480px) {{
        div[data-testid="metric-container"] label {{
            font-size: 9px !important;
        }}
        div[data-testid="metric-container"] .stMetricValue {{
            font-size: 14px !important;
        }}
    }}

    .stNumberInput input, .stSelectbox select {{
        font-size: 13px !important;
        padding: 4px 8px !important;
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
        border-radius: 6px !important;
    }}
    
    @media screen and (max-width: 480px) {{
        .stNumberInput input, .stSelectbox select {{
            font-size: 11px !important;
            padding: 3px 6px !important;
        }}
    }}

    .streamlit-expanderHeader {{
        font-size: 13px !important;
        font-weight: 600 !important;
        padding: 6px 10px !important;
        background-color: {expander_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
        border-radius: 8px !important;
    }}
    
    @media screen and (max-width: 480px) {{
        .streamlit-expanderHeader {{
            font-size: 11px !important;
            padding: 4px 8px !important;
        }}
    }}

    .katex, .katex-display {{
        font-size: 14px !important;
        color: {text_color} !important;
    }}
    
    @media screen and (max-width: 480px) {{
        .katex, .katex-display {{
            font-size: 11px !important;
        }}
    }}

    .stApp h1 .lightning {{
        color: #f9a825 !important;
        display: inline-block !important;
        margin: 0 4px !important;
    }}
    
    .main {{
        overflow-x: hidden !important;
    }}
    
    .stHeader {{
        background-color: {bg_color} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# --- دکمه تغییر تم ---
# ==============================================================================

theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
theme_tooltip = "Switch to Dark Mode" if st.session_state.theme == 'light' else "Switch to Light Mode"

st.markdown(f"""
    <div class="theme-button-container">
        <button class="theme-button" onclick="location.href='?theme=toggle'" title="{theme_tooltip}">
            {theme_icon}
        </button>
    </div>
""", unsafe_allow_html=True)

import urllib.parse
query_params = st.query_params
if 'theme' in query_params and query_params['theme'] == 'toggle':
    toggle_theme()
    st.query_params.clear()
    st.rerun()

# ==============================================================================
# --- کلاس محاسباتی اصلی ---
# ==============================================================================

class PowerSystemCalculator:
    SQRT3 = math.sqrt(3)
    
    STANDARD_CABLE_SIZES = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300]
    
    CABLE_CURRENT_CAPACITY = {
        1.5: 18, 2.5: 24, 4: 32, 6: 41, 10: 57, 16: 76,
        25: 101, 35: 125, 50: 151, 70: 192, 95: 232,
        120: 269, 150: 300, 185: 341, 240: 400, 300: 460
    }
    
    STANDARD_BREAKERS = [6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630]
    
    @classmethod
    def calculate_cable(cls, power_kw: float, length_m: float, 
                       voltage: float = 380, cos_phi: float = 0.8,
                       max_drop_percent: float = 2.0, conductivity: float = 56.0) -> dict:
        current = (power_kw * 1000) / (cls.SQRT3 * voltage * cos_phi)
        area_voltage_drop = (power_kw * 1000 * length_m * 100) / (conductivity * (voltage ** 2) * max_drop_percent)
        min_area_for_current = 1.5
        for size, max_current in cls.CABLE_CURRENT_CAPACITY.items():
            if current <= max_current:
                min_area_for_current = size
                break
        else:
            min_area_for_current = max(cls.CABLE_CURRENT_CAPACITY.keys())
        required_area = max(area_voltage_drop, min_area_for_current)
        standard_size = cls._round_to_standard(required_area)
        if length_m > 80:
            idx = cls.STANDARD_CABLE_SIZES.index(standard_size)
            safe_size = cls.STANDARD_CABLE_SIZES[min(idx + 1, len(cls.STANDARD_CABLE_SIZES) - 1)]
        else:
            safe_size = standard_size
        actual_drop = (power_kw * 1000 * length_m * 100) / (conductivity * (voltage ** 2) * standard_size)
        return {
            'current': round(current, 2), 'standard_size': standard_size,
            'safe_size': safe_size, 'required_area': round(required_area, 3),
            'voltage_drop': round(actual_drop, 2), 'is_ok': actual_drop <= max_drop_percent
        }
    
    @classmethod
    def _round_to_standard(cls, area: float) -> float:
        for size in cls.STANDARD_CABLE_SIZES:
            if size >= area:
                return size
        return cls.STANDARD_CABLE_SIZES[-1]
    
    @classmethod
    def calculate_ups(cls, load_kva: float, backup_min: float, num_batteries: int,
                     battery_voltage: float = 12.0, inverter_efficiency: float = 0.9,
                     depth_of_discharge: float = 0.8) -> dict:
        load_kw = load_kva * 0.8
        total_dc_voltage = num_batteries * battery_voltage
        dc_current = (load_kw * 1000) / (total_dc_voltage * inverter_efficiency)
        ah_required = (dc_current * backup_min) / (60 * depth_of_discharge)
        standard_ahs = [7, 12, 18, 26, 40, 55, 65, 80, 100, 120, 150, 200, 250]
        standard_ah = 7
        for std_ah in standard_ahs:
            if std_ah >= ah_required:
                standard_ah = std_ah
                break
        return {
            'ah_required': round(ah_required, 1), 'ah_standard': standard_ah,
            'dc_current': round(dc_current, 2), 'dc_voltage': round(total_dc_voltage, 1),
            'load_kw': round(load_kw, 2)
        }
    
    @classmethod
    def calculate_motor(cls, power_kva: float, efficiency: float = 0.85,
                       cos_phi: float = 0.8, voltage: float = 380,
                       starting_factor: float = 6.5) -> dict:
        power_out_kw = power_kva * cos_phi
        power_in_kw = power_out_kw / efficiency
        rated_current = (power_in_kw * 1000) / (cls.SQRT3 * voltage * cos_phi)
        starting_current = rated_current * starting_factor
        torque_nm = (power_out_kw * 9550) / 1500
        return {
            'rated_current': round(rated_current, 2), 'starting_current': round(starting_current, 2),
            'power_in': round(power_in_kw, 2), 'power_out': round(power_out_kw, 2),
            'torque': round(torque_nm, 2), 'efficiency': round(efficiency * 100, 1)
        }
    
    @classmethod
    def suggest_breaker(cls, current: float, load_type: str = "Resistive",
                       motor_starting: bool = False) -> dict:
        if load_type == "Motor":
            multiplier = 1.6
            if motor_starting:
                required = current * 6.5 * 0.8
            else:
                required = current * multiplier
        elif load_type == "Inductive":
            multiplier = 1.4
            required = current * multiplier
        else:
            multiplier = 1.2
            required = current * multiplier
        suggested = min([b for b in cls.STANDARD_BREAKERS if b >= required], default=max(cls.STANDARD_BREAKERS))
        return {
            'suggested_breaker': suggested, 'required_current': round(required, 2),
            'multiplier': multiplier, 'load_type': load_type
        }

# ==============================================================================
# --- عنوان و تب‌ها ---
# ==============================================================================

st.markdown(f"""
    <h1 style='
        text-align: center; 
        font-size: 34px; 
        font-weight: 700; 
        margin: 0; 
        padding: 10px 0;
        letter-spacing: 0px;
        color: {text_color};
    '>
    ElectroCalc <span style='color: #f9a825; display: inline-block; margin: 0 4px;'>⚡</span> M&F
    </h1>
""", unsafe_allow_html=True)

tabs = st.tabs(["📏 Cable", "🔋 UPS", "⚙️ Motor", "🛡️ Protect"])

# ==============================================================================
# --- تب ۱: کابل ---
# ==============================================================================

with tabs[0]:
    st.header("📐 Cable Sizing")
    with st.expander("⚙️ Parameters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            power = st.number_input("Power (kW)", value=85.0, step=1.0, key="cable_power")
            length = st.number_input("Length (m)", value=90.0, step=5.0, key="cable_length")
            voltage = st.selectbox("Voltage (V)", [380, 400, 415, 480], index=0, key="cable_voltage")
        with col2:
            cos_phi = st.slider("cos φ", 0.7, 1.0, 0.8, 0.01, key="cable_cosphi")
            drop_limit = st.slider("Max Drop %", 1.0, 5.0, 2.0, 0.5, key="cable_drop")
            conductor = st.selectbox("Conductor", ["Copper", "Aluminum"], index=0, key="cable_conductor")
    if st.button("🔍 Calculate", use_container_width=True, key="cable_btn"):
        sigma = 56.0 if conductor == "Copper" else 35.0
        result = PowerSystemCalculator.calculate_cable(power, length, voltage, cos_phi, drop_limit, sigma)
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Current", f"{result['current']} A")
        with col2: st.metric("Std Size", f"{result['standard_size']} mm²")
        with col3: st.metric("Safe Size", f"{result['safe_size']} mm²")
        with st.expander("📊 Details"):
            st.write(f"**Required Area:** {result['required_area']} mm²")
            st.write(f"**Voltage Drop:** {result['voltage_drop']}%")
            st.write(f"**Status:** {'✅ PASS' if result['is_ok'] else '❌ FAIL'}")
            st.latex(r"S = \frac{P \times L \times 100}{\sigma \times V^2 \times \Delta V\%}")

# ==============================================================================
# --- تب ۲: UPS ---
# ==============================================================================

with tabs[1]:
    st.header("🔋 Battery Sizing")
    with st.expander("⚙️ Parameters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            ups_kva = st.number_input("UPS (kVA)", value=40.0, step=1.0, key="ups_kva")
            backup_time = st.number_input("Time (min)", value=15, step=5, key="ups_time")
        with col2:
            num_batteries = st.number_input("Batteries", value=32, step=1, key="ups_bat")
            battery_voltage = st.selectbox("Bat Voltage", [12, 6, 2], index=0, key="ups_volt")
    if st.button("🔍 Calculate", use_container_width=True, key="ups_btn"):
        result = PowerSystemCalculator.calculate_ups(ups_kva, backup_time, num_batteries, float(battery_voltage))
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Capacity", f"{result['ah_standard']} Ah")
        with col2: st.metric("DC Volt", f"{result['dc_voltage']} V")
        with col3: st.metric("DC Curr", f"{result['dc_current']} A")
        with st.expander("📊 Details"):
            st.write(f"**Required Ah:** {result['ah_required']} Ah")
            st.write(f"**Load Power:** {result['load_kw']} kW")
            st.latex(r"Ah = \frac{P_{kW} \times 1000 \times T_{min}}{V_{DC} \times \eta \times 60 \times DOD}")

# ==============================================================================
# --- تب ۳: موتور ---
# ==============================================================================

with tabs[2]:
    st.header("⚙️ Motor Calc")
    with st.expander("⚙️ Parameters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            motor_kva = st.number_input("Power (kVA)", value=150.0, step=5.0, key="motor_kva")
            efficiency = st.slider("Eff %", 70, 98, 85, 1, key="motor_eff") / 100
        with col2:
            motor_cos = st.slider("cos φ", 0.7, 0.95, 0.8, 0.01, key="motor_cos")
            start_factor = st.slider("Start Factor", 4.0, 10.0, 6.5, 0.5, key="motor_start")
    if st.button("🔍 Calculate", use_container_width=True, key="motor_btn"):
        result = PowerSystemCalculator.calculate_motor(motor_kva, efficiency, motor_cos, 380, start_factor)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rated Curr", f"{result['rated_current']} A")
            st.metric("Start Curr", f"{result['starting_current']} A")
        with col2:
            st.metric("Input P", f"{result['power_in']} kW")
            st.metric("Output P", f"{result['power_out']} kW")
        with st.expander("📊 Details"):
            st.write(f"**Torque:** {result['torque']} Nm")
            st.write(f"**Efficiency:** {result['efficiency']}%")
            st.latex(r"I_{rated} = \frac{P_{kW} \times 1000}{\eta \times \sqrt{3} \times V \times \cos\phi}")

# ==============================================================================
# --- تب ۴: حفاظت ---
# ==============================================================================

with tabs[3]:
    st.header("🛡️ Breaker Sizing")
    with st.expander("⚙️ Parameters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            load_current = st.number_input("Load (A)", value=100.0, step=1.0, key="protect_curr")
            load_type = st.selectbox("Load Type", ["Resistive", "Inductive", "Motor"], key="protect_type")
        with col2:
            consider_starting = st.checkbox("Starting?", value=False, key="protect_start")
    if st.button("🔍 Calculate", use_container_width=True, key="protect_btn"):
        result = PowerSystemCalculator.suggest_breaker(load_current, load_type, consider_starting)
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("🛡️ Breaker", f"{result['suggested_breaker']} A")
        with col2: st.metric("Required", f"{result['required_current']} A")
        with col3: st.metric("Safety Factor", f"{result['multiplier']}")
        with st.expander("📊 Details"):
            st.write(f"**Load Type:** {result['load_type']}")
            st.write(f"**Required Current:** {result['required_current']} A")
            st.write(f"**Safety Factor:** {result['multiplier']}")
            st.latex(r"I_{breaker} = I_{load} \times K_{safety}")

# ==============================================================================
# --- سایدبار ---
# ==============================================================================

with st.sidebar:
    st.header("📚 Standards")
    st.markdown("""
    **IEC 60364** - Cable Sizing  
    **IEEE 485** - UPS Sizing  
    **IEC 60034** - Motor Calculations  
    **IEC 60947** - Breaker Selection  
    
    ---
    **Assumptions:**  
    • 3-Phase AC System  
    • Copper Conductors (σ=56)  
    • Ambient Temp: 30°C  
    • Power Factor: 0.8 (default)
    """)
    
    st.divider()
    st.caption("v2.0 ⚡ ElectroCalc M&F")
    st.caption("Developed for Power Systems Engineering")
