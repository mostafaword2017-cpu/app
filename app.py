import streamlit as st
import math
import numpy as np
from typing import Tuple, Optional

# ==============================================================================
# --- تنظیمات صفحه ---
# ==============================================================================
st.set_page_config(
    page_title="ElectroCalc ⚡ M&F", 
    page_icon="⚡️", 
    layout="centered"
)

# ==============================================================================
# --- استایل بهینه برای موبایل ---
# ==============================================================================
st.markdown("""
    <style>
    /* حذف المان‌های اضافی Streamlit */
    header div[data-testid="stHeader"] a, 
    div[data-testid="stAppDeployButton"], 
    #MainMenu {
        display: none !important;
    }

    /* ========== بهینه‌سازی تایتل اصلی ========== */
    .stApp h1 {
        font-size: 30px !important;  /* دو درجه بزرگتر (از 26 به 30) */
        text-align: center !important;
        white-space: nowrap !important;
        letter-spacing: 0px !important;
        font-weight: 700 !important;
        padding: 10px 0 !important;
        margin: 0 auto !important;
        display: block !important;
        width: 100% !important;
        color: #1a1a1a !important;
    }
    
    /* تایتل در موبایل */
    @media screen and (max-width: 480px) {
        .stApp h1 {
            font-size: 23px !important;  /* دو درجه بزرگتر (از 20 به 23) */
            letter-spacing: -0.3px !important;
        }
    }

    /* ========== بهینه‌سازی هدر تب‌ها (وسط‌چین) ========== */
    .stTabs div[role="tablist"] { 
        gap: 5px !important; 
        flex-wrap: nowrap !important; 
        overflow-x: auto !important;
        padding: 2px 0 !important;
        justify-content: center !important;
        display: flex !important;
    }
    
    .stTabs [role="tab"] {
        font-size: 16px !important;  /* دو درجه بزرگتر (از 13 به 16) */
        padding: 10px 18px !important;
        border-radius: 8px 8px 0px 0px !important;
        background-color: #f0f2f6 !important;
        white-space: nowrap !important;
        min-width: 80px !important;
        text-align: center !important;
        flex: 0 0 auto !important;
    }
    
    @media screen and (max-width: 480px) {
        .stTabs div[role="tablist"] {
            gap: 3px !important;
            justify-content: center !important;
        }
        .stTabs [role="tab"] {
            font-size: 13px !important;  /* دو درجه بزرگتر (از 10 به 13) */
            padding: 6px 10px !important;
            min-width: 55px !important;
        }
    }

    /* تب فعال */
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50 !important; 
        color: white !important;
        font-weight: 600 !important;
    }

    /* ========== لیبل‌ها ========== */
    label, .stMarkdown p, .stText, .stNumberInput label {
        font-size: 13px !important;
        margin-bottom: 2px !important;
    }
    
    @media screen and (max-width: 480px) {
        label, .stMarkdown p, .stText, .stNumberInput label {
            font-size: 11px !important;
        }
    }

    /* ========== دکمه‌ها ========== */
    .stButton > button {
        width: 100% !important;
        height: 42px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        background-color: #007BFF !important;
        color: white !important;
        padding: 0 10px !important;
    }
    
    @media screen and (max-width: 480px) {
        .stButton > button {
            height: 36px !important;
            font-size: 12px !important;
        }
    }

    /* ========== متریک‌ها ========== */
    div[data-testid="metric-container"] {
        padding: 8px !important;
        background-color: #f8f9fa !important;
        border-radius: 10px !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    div[data-testid="metric-container"] label {
        font-size: 11px !important;
    }
    
    div[data-testid="metric-container"] .stMetricValue {
        font-size: 17px !important;
        font-weight: 700 !important;
    }
    
    @media screen and (max-width: 480px) {
        div[data-testid="metric-container"] label {
            font-size: 9px !important;
        }
        div[data-testid="metric-container"] .stMetricValue {
            font-size: 14px !important;
        }
    }

    /* ========== ورودی‌ها ========== */
    .stNumberInput input, .stSelectbox select {
        font-size: 13px !important;
        padding: 4px 8px !important;
    }
    
    @media screen and (max-width: 480px) {
        .stNumberInput input, .stSelectbox select {
            font-size: 11px !important;
            padding: 3px 6px !important;
        }
    }

    /* ========== اکسپندر ========== */
    .streamlit-expanderHeader {
        font-size: 13px !important;
        font-weight: 600 !important;
        padding: 6px 10px !important;
    }
    
    @media screen and (max-width: 480px) {
        .streamlit-expanderHeader {
            font-size: 11px !important;
            padding: 4px 8px !important;
        }
    }

    /* ========== لاتکس ========== */
    .katex, .katex-display {
        font-size: 14px !important;
    }
    
    @media screen and (max-width: 480px) {
        .katex, .katex-display {
            font-size: 11px !important;
        }
    }

    /* ========== تب‌ها در یک خط ========== */
    .stTabs div[role="tablist"] { 
        gap: 3px !important; 
        flex-wrap: nowrap !important; 
        overflow-x: auto !important;
        padding: 2px 0 !important;
        justify-content: center !important;
        display: flex !important;
    }
    
    .main {
        overflow-x: hidden !important;
    }
    
    /* ========== علامت برق در تایتل ========== */
    .stApp h1 .lightning {
        color: #f9a825 !important;
        display: inline-block !important;
        margin: 0 4px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- هسته محاسباتی با فرمول صحیح کابل ---
# ==============================================================================

class PowerSystemCalculator:
    """
    کلاس اصلی محاسبات برق قدرت با دقت صنعتی
    تمام محاسبات با فرمولهای استاندارد IEEE و IEC
    """
    
    # ثابتهای جهانی
    SQRT3 = math.sqrt(3)
    
    # جدول استاندارد سطح مقطع کابل (mm²)
    STANDARD_CABLE_SIZES = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300]
    
    # جریان مجاز برای کابل مسی (دمای ۳۰°C، نصب در هوا)
    CABLE_CURRENT_CAPACITY = {
        1.5: 18, 2.5: 24, 4: 32, 6: 41, 10: 57, 16: 76,
        25: 101, 35: 125, 50: 151, 70: 192, 95: 232,
        120: 269, 150: 300, 185: 341, 240: 400, 300: 460
    }
    
    # استاندارد کلیدهای محافظ (IEC)
    STANDARD_BREAKERS = [6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630]
    
    @classmethod
    def calculate_cable(cls, power_kw: float, length_m: float, 
                       voltage: float = 380, 
                       cos_phi: float = 0.8,
                       max_drop_percent: float = 2.0,
                       conductivity: float = 56.0) -> dict:
        """
        محاسبه دقیق سطح مقطع کابل بر اساس استاندارد IEC 60364
        
        ✅ فرمول صحیح:
        S = (P × L × 100) / (σ × V² × ΔV%)
        """
        # ۱. محاسبه جریان نامی (فرمول صحیح سهفاز)
        current = (power_kw * 1000) / (cls.SQRT3 * voltage * cos_phi)
        
        # ۲. محاسبه سطح مقطع بر اساس افت ولتاژ
        area_voltage_drop = (power_kw * 1000 * length_m * 100) / (
            conductivity * (voltage ** 2) * max_drop_percent
        )
        
        # ۳. محاسبه بر اساس جریان مجاز (حرارتی)
        min_area_for_current = 1.5
        for size, max_current in cls.CABLE_CURRENT_CAPACITY.items():
            if current <= max_current:
                min_area_for_current = size
                break
        else:
            min_area_for_current = max(cls.CABLE_CURRENT_CAPACITY.keys())
        
        # ۴. انتخاب بزرگترین سطح مقطع برای ایمنی
        required_area = max(area_voltage_drop, min_area_for_current)
        
        # ۵. تطبیق با سایزهای استاندارد
        standard_size = cls._round_to_standard(required_area)
        
        # ۶. بررسی شرط طول (افزایش یک سایز برای طولهای بلند)
        if length_m > 80:
            idx = cls.STANDARD_CABLE_SIZES.index(standard_size)
            safe_size = cls.STANDARD_CABLE_SIZES[min(idx + 1, len(cls.STANDARD_CABLE_SIZES) - 1)]
        else:
            safe_size = standard_size
        
        # ۷. محاسبه افت ولتاژ واقعی با سایز انتخابی
        actual_drop = cls._calculate_voltage_drop(power_kw, length_m, standard_size, voltage, conductivity)
        
        return {
            'current': round(current, 2),
            'standard_size': standard_size,
            'safe_size': safe_size,
            'required_area': round(required_area, 3),
            'voltage_drop': round(actual_drop, 2),
            'is_ok': actual_drop <= max_drop_percent
        }
    
    @classmethod
    def _round_to_standard(cls, area: float) -> float:
        """گرد کردن به نزدیکترین سایز استاندارد بالاتر"""
        for size in cls.STANDARD_CABLE_SIZES:
            if size >= area:
                return size
        return cls.STANDARD_CABLE_SIZES[-1]
    
    @classmethod
    def _calculate_voltage_drop(cls, power_kw: float, length_m: float, 
                                size: float, voltage: float, 
                                conductivity: float) -> float:
        """
        محاسبه دقیق افت ولتاژ بر حسب درصد
        ✅ فرمول صحیح: ΔV% = (P × L × 100) / (σ × V² × S)
        """
        drop = (power_kw * 1000 * length_m * 100) / (
            conductivity * (voltage ** 2) * size
        )
        return drop
    
    @classmethod
    def calculate_ups(cls, load_kva: float, backup_min: float, 
                     num_batteries: int, battery_voltage: float = 12.0,
                     inverter_efficiency: float = 0.9,
                     depth_of_discharge: float = 0.8) -> dict:
        """
        محاسبه دقیق ظرفیت باتری UPS بر اساس استاندارد IEEE 485
        """
        load_kw = load_kva * 0.8
        total_dc_voltage = num_batteries * battery_voltage
        dc_current = (load_kw * 1000) / (total_dc_voltage * inverter_efficiency)
        ah_required = (dc_current * backup_min) / (60 * depth_of_discharge)
        standard_ah = cls._round_battery_ah(ah_required)
        
        return {
            'ah_required': round(ah_required, 1),
            'ah_standard': standard_ah,
            'dc_current': round(dc_current, 2),
            'dc_voltage': round(total_dc_voltage, 1),
            'load_kw': round(load_kw, 2)
        }
    
    @classmethod
    def _round_battery_ah(cls, ah: float) -> int:
        """گرد کردن به سایز استاندارد باتری"""
        standard_ahs = [7, 12, 18, 26, 40, 55, 65, 80, 100, 120, 150, 200, 250]
        for std_ah in standard_ahs:
            if std_ah >= ah:
                return std_ah
        return standard_ahs[-1]
    
    @classmethod
    def calculate_motor(cls, power_kva: float, efficiency: float = 0.85,
                       cos_phi: float = 0.8, voltage: float = 380,
                       starting_factor: float = 6.5) -> dict:
        """
        محاسبه پارامترهای موتور الکتریکی
        """
        power_out_kw = power_kva * cos_phi
        power_in_kw = power_out_kw / efficiency
        rated_current = (power_in_kw * 1000) / (cls.SQRT3 * voltage * cos_phi)
        starting_current = rated_current * starting_factor
        torque_nm = (power_out_kw * 9550) / 1500
        
        return {
            'rated_current': round(rated_current, 2),
            'starting_current': round(starting_current, 2),
            'power_in': round(power_in_kw, 2),
            'power_out': round(power_out_kw, 2),
            'torque': round(torque_nm, 2),
            'efficiency': round(efficiency * 100, 1)
        }
    
    @classmethod
    def suggest_breaker(cls, current: float, load_type: str = "Resistive",
                       motor_starting: bool = False) -> dict:
        """
        انتخاب کلید محافظ بر اساس استاندارد IEC 60947
        """
        if load_type == "Motor":
            multiplier = 1.6
            if motor_starting:
                required = current * 6.5 * 0.8
            else:
                required = current * multiplier
        elif load_type == "Inductive":
            multiplier = 1.4
            required = current * multiplier
        else:  # Resistive
            multiplier = 1.2
            required = current * multiplier
        
        suggested = min([b for b in cls.STANDARD_BREAKERS if b >= required], 
                       default=max(cls.STANDARD_BREAKERS))
        
        return {
            'suggested_breaker': suggested,
            'required_current': round(required, 2),
            'multiplier': multiplier,
            'load_type': load_type
        }

# ==============================================================================
# --- رابط کاربری (UI) با اسم بزرگتر و تبهای وسطچین ---
# ==============================================================================

# ✅ عنوان با علامت برق در وسط و فونت بزرگتر
st.markdown("""
    <h1 style='
        text-align: center; 
        font-size: 30px; 
        font-weight: 700; 
        margin: 0; 
        padding: 10px 0;
        letter-spacing: 0px;
        color: #1a1a1a;
    '>
    ElectroCalc <span style='color: #f9a825; display: inline-block; margin: 0 4px;'>⚡</span> M&F
    </h1>
""", unsafe_allow_html=True)

# تب‌ها با وسط‌چین
tabs = st.tabs(["📏 Cable", "🔋 UPS", "⚙️ Motor", "🛡️ Protect"])

# --- تب ۱: کابل ---
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
        result = PowerSystemCalculator.calculate_cable(
            power, length, voltage, cos_phi, drop_limit, sigma
        )
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Current", f"{result['current']} A")
        with col2:
            st.metric("Std Size", f"{result['standard_size']} mm²")
        with col3:
            st.metric("Safe Size", f"{result['safe_size']} mm²")
        
        with st.expander("📊 Details"):
            st.write(f"**Required Area:** {result['required_area']} mm²")
            st.write(f"**Voltage Drop:** {result['voltage_drop']}%")
            st.write(f"**Status:** {'✅ PASS' if result['is_ok'] else '❌ FAIL'}")
            st.latex(r"""
            S = \frac{P \times L \times 100}{\sigma \times V^2 \times \Delta V\%}
            """)
            # ✅ متن فارسی حذف شد

# --- تب ۲: UPS ---
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
        result = PowerSystemCalculator.calculate_ups(
            ups_kva, backup_time, num_batteries, float(battery_voltage)
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Capacity", f"{result['ah_standard']} Ah")
        with col2:
            st.metric("DC Volt", f"{result['dc_voltage']} V")
        with col3:
            st.metric("DC Curr", f"{result['dc_current']} A")
        
        with st.expander("📊 Details"):
            st.write(f"**Required Ah:** {result['ah_required']} Ah")
            st.write(f"**Load Power:** {result['load_kw']} kW")
            st.latex(r"""
            Ah = \frac{P_{kW} \times 1000 \times T_{min}}{V_{DC} \times \eta \times 60 \times DOD}
            """)

# --- تب ۳: موتور ---
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
        result = PowerSystemCalculator.calculate_motor(
            motor_kva, efficiency, motor_cos, 380, start_factor
        )
        
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
            st.latex(r"""
            I_{rated} = \frac{P_{kW} \times 1000}{\eta \times \sqrt{3} \times V \times \cos\phi}
            """)

# --- تب ۴: حفاظت ---
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
        result = PowerSystemCalculator.suggest_breaker(
            load_current, load_type, consider_starting
        )
        
        st.metric("🛡️ Breaker", f"{result['suggested_breaker']} A")
        
        with st.expander("📊 Details"):
            st.write(f"**Required:** {result['required_current']} A")
            st.write(f"**Safety Factor:** {result['multiplier']}")
            st.write(f"**Load Type:** {result['load_type']}")
            st.latex(r"""
            I_{breaker} = I_{load} \times K_{safety}
            """)

# --- سایدبار ---
with st.sidebar:
    st.header("📚 Standards")
    st.markdown("""
    **IEC 60364** - Cable  
    **IEEE 485** - UPS  
    **IEC 60034** - Motor  
    **IEC 60947** - Breaker
    
    ---
    **Assumptions:**  
    • 3-Phase AC  
    • Copper (σ=56)  
    • Temp: 30°C  
    • PF: 0.8 (default)
    """)
    
    st.divider()
    st.caption("v2.0 ⚡")
