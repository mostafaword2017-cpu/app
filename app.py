import streamlit as st
import math
import numpy as np
from typing import Tuple, Optional

# ==============================================================================
# --- تنظیمات صفحه (بدون تغییر) ---
# ==============================================================================
st.set_page_config(page_title="ElectroCalc M&F Pro", page_icon="⚡️", layout="centered")

# استایلهای شما (بدون تغییر)
st.markdown("""...""", unsafe_allow_html=True)

# ==============================================================================
# --- هسته محاسباتی اصلاحشده (Industrial Grade) ---
# ==============================================================================

class PowerSystemCalculator:
    """
    کلاس اصلی محاسبات برق قدرت با دقت صنعتی
    تمام محاسبات با فرمولهای استاندارد IEEE و IEC
    """
    
    # ثابتهای جهانی
    SQRT3 = math.sqrt(3)
    VOLTAGE_380 = 380
    VOLTAGE_400 = 400
    
    # جدول استاندارد سطح مقطع کابل (mm²)
    STANDARD_CABLE_SIZES = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300]
    
    # جریان مجاز برای کابل مسی (با فرض دمای ۳۰°C، نصب در هوا)
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
                       conductivity: float = 56.0,
                       ambient_temp: float = 30.0) -> dict:
        """
        محاسبه دقیق سطح مقطع کابل بر اساس استاندارد IEC 60364
        
        Args:
            power_kw: توان بر حسب کیلووات
            length_m: طول کابل بر حسب متر
            voltage: ولتاژ خط (ولت)
            cos_phi: ضریب توان
            max_drop_percent: حداکثر افت ولتاژ مجاز (درصد)
            conductivity: هدایت الکتریکی (مس=۵۶، آلومینیوم=۳۵)
            ambient_temp: دمای محیط (درجه سانتی‌گراد)
            
        Returns:
            dict: شامل جریان، سطح مقطع استاندارد، پیشنهادی و محاسبات دقیق
        """
        
        # ۱. محاسبه جریان نامی (فرمول صحیح سهفاز)
        current = (power_kw * 1000) / (cls.SQRT3 * voltage * cos_phi)
        
        # ۲. محاسبه سطح مقطع بر اساس افت ولتاژ
        # فرمول دقیق: S = (P * L) / (σ * V^2 * ΔV% * cos^2φ * 100)
        area_voltage_drop = (power_kw * 1000 * length_m * 100) / (
            conductivity * (voltage ** 2) * max_drop_percent * (cos_phi ** 2)
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
            # افزایش یک سایز برای افت ولتاژ بیشتر
            idx = cls.STANDARD_CABLE_SIZES.index(standard_size)
            safe_size = cls.STANDARD_CABLE_SIZES[min(idx + 1, len(cls.STANDARD_CABLE_SIZES) - 1)]
        else:
            safe_size = standard_size
        
        # ۷. محاسبه افت ولتاژ واقعی با سایز انتخابی
        actual_drop = cls._calculate_voltage_drop(power_kw, length_m, standard_size, voltage, cos_phi, conductivity)
        
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
                                cos_phi: float, conductivity: float) -> float:
        """
        محاسبه دقیق افت ولتاژ بر حسب درصد
        فرمول: ΔV% = (P * L * 100) / (σ * V^2 * S * cos^2φ)
        """
        drop = (power_kw * 1000 * length_m * 100) / (
            conductivity * (voltage ** 2) * size * (cos_phi ** 2)
        )
        return drop
    
    @classmethod
    def calculate_ups(cls, load_kva: float, backup_min: float, 
                     num_batteries: int, battery_voltage: float = 12.0,
                     inverter_efficiency: float = 0.9,
                     depth_of_discharge: float = 0.8) -> dict:
        """
        محاسبه دقیق ظرفیت باتری UPS بر اساس استاندارد IEEE 485
        
        Args:
            load_kva: توان UPS بر حسب کیلوولت-آمپر
            backup_min: زمان پشتیبانی بر حسب دقیقه
            num_batteries: تعداد باتریها
            battery_voltage: ولتاژ هر باتری (ولت)
            inverter_efficiency: راندمان اینورتر
            depth_of_discharge: عمق تخلیه مجاز (معمولاً ۰.۸)
            
        Returns:
            dict: شامل ظرفیت باتری، جریان DC و سایر پارامترها
        """
        # ۱. محاسبه توان واقعی بار (با در نظر گرفتن ضریب توان)
        load_kw = load_kva * 0.8  # فرض ضریب توان ۰.۸
        
        # ۲. محاسبه ولتاژ DC کل
        total_dc_voltage = num_batteries * battery_voltage
        
        # ۳. محاسبه جریان DC مورد نیاز
        dc_current = (load_kw * 1000) / (total_dc_voltage * inverter_efficiency)
        
        # ۴. محاسبه ظرفیت باتری بر حسب آمپر-ساعت
        ah_required = (dc_current * backup_min) / (60 * depth_of_discharge)
        
        # ۵. گرد کردن به سایز استاندارد باتری
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
        
        Args:
            power_kva: توان ظاهری (kVA)
            efficiency: راندمان
            cos_phi: ضریب توان
            voltage: ولتاژ خط
            starting_factor: ضریب جریان راهاندازی (معمولاً ۶ تا ۸)
        """
        # ۱. توان خروجی مکانیکی
        power_out_kw = power_kva * cos_phi
        
        # ۲. توان ورودی الکتریکی
        power_in_kw = power_out_kw / efficiency
        
        # ۳. جریان نامی
        rated_current = (power_in_kw * 1000) / (cls.SQRT3 * voltage * cos_phi)
        
        # ۴. جریان راهاندازی
        starting_current = rated_current * starting_factor
        
        # ۵. گشتاور نامی (تخمینی)
        torque_nm = (power_out_kw * 9550) / 1500  # فرض سرعت ۱۵۰۰ RPM
        
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
        
        Args:
            current: جریان بار (آمپر)
            load_type: نوع بار ("Resistive", "Inductive", "Motor")
            motor_starting: آیا جریان راهاندازی موتور در نظر گرفته شود؟
        """
        if load_type == "Motor":
            multiplier = 1.6  # ضریب ایمنی برای موتور
            if motor_starting:
                # کلید باید جریان راهاندازی را تحمل کند
                required = current * 6.5 * 0.8  # ۰.۸ برای فاکتور زمان
            else:
                required = current * multiplier
        elif load_type == "Inductive":
            multiplier = 1.4
            required = current * multiplier
        else:  # Resistive
            multiplier = 1.2
            required = current * multiplier
        
        # انتخاب نزدیکترین سایز استاندارد بالاتر
        suggested = min([b for b in cls.STANDARD_BREAKERS if b >= required], 
                       default=max(cls.STANDARD_BREAKERS))
        
        return {
            'suggested_breaker': suggested,
            'required_current': round(required, 2),
            'multiplier': multiplier,
            'load_type': load_type
        }

# ==============================================================================
# --- رابط کاربری (UI) با بهبودها ---
# ==============================================================================

st.title("⚡️ ElectroCalc M&F Pro")

tabs = st.tabs(["📏 Cable", "🔋 UPS", "⚙️ Motor", "🛡️ Protect"])

# --- تب ۱: کابل (Cable) ---
with tabs[0]:
    st.header("📐 Cable Sizing (IEC 60364)")
    
    with st.expander("⚙️ Input Parameters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            power = st.number_input("Power (kW)", value=85.0, step=1.0)
            length = st.number_input("Cable Length (m)", value=90.0, step=5.0)
            voltage = st.selectbox("System Voltage (V)", [380, 400, 415, 480], index=0)
            
        with col2:
            cos_phi = st.slider("Power Factor (cos φ)", 0.7, 1.0, 0.8, 0.01)
            drop_limit = st.slider("Max Drop (%)", 1.0, 5.0, 2.0, 0.5)
            conductor = st.selectbox("Conductor Type", ["Copper (σ=56)", "Aluminum (σ=35)"], index=0)
    
    if st.button("🔍 Calculate Cable", use_container_width=True):
        sigma = 56.0 if "Copper" in conductor else 35.0
        result = PowerSystemCalculator.calculate_cable(
            power, length, voltage, cos_phi, drop_limit, sigma
        )
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("⚡️ Current", f"{result['current']} A")
        with col2:
            st.metric("📏 Standard Size", f"{result['standard_size']} mm²", 
                     delta="Recommended")
        with col3:
            st.metric("🚀 Safe Size", f"{result['safe_size']} mm²", 
                     delta="+1 Size" if result['safe_size'] > result['standard_size'] else "OK")
        
        # نمایش دقیق محاسبات
        with st.expander("📊 Detailed Calculations"):
            st.write(f"**Required Area:** {result['required_area']} mm²")
            st.write(f"**Actual Voltage Drop:** {result['voltage_drop']}%")
            st.write(f"**Status:** {'✅ PASS' if result['is_ok'] else '❌ FAIL'}")
            
            # نمایش فرمول
            st.latex(r"""
            S = \frac{P \times L \times 100}{\sigma \times V^2 \times \Delta V\% \times \cos^2\phi}
            """)

# --- تب ۲: UPS (با بهبود) ---
with tabs[1]:
    st.header("🔋 UPS Battery Sizing (IEEE 485)")
    
    with st.expander("⚙️ Input Parameters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            ups_kva = st.number_input("UPS Power (kVA)", value=40.0, step=1.0)
            backup_time = st.number_input("Backup Time (min)", value=15, step=5)
        with col2:
            num_batteries = st.number_input("Number of Batteries", value=32, step=1)
            battery_voltage = st.selectbox("Battery Voltage (V)", [12, 6, 2], index=0)
    
    if st.button("🔍 Calculate UPS", use_container_width=True):
        result = PowerSystemCalculator.calculate_ups(
            ups_kva, backup_time, num_batteries, float(battery_voltage)
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📦 Battery Capacity", f"{result['ah_standard']} Ah")
        with col2:
            st.metric("🔋 DC Voltage", f"{result['dc_voltage']} V")
        with col3:
            st.metric("⚡️ DC Current", f"{result['dc_current']} A")
        
        with st.expander("📊 Detailed Calculations"):
            st.write(f"**Required Ah:** {result['ah_required']} Ah")
            st.write(f"**Load Power:** {result['load_kw']} kW")
            st.latex(r"""
            Ah = \frac{P_{kW} \times 1000 \times T_{min}}{V_{DC} \times \eta \times 60 \times DOD}
            """)

# --- تب ۳: موتور (Motor) ---
with tabs[2]:
    st.header("⚙️ Motor Calculations (IEC 60034)")
    
    with st.expander("⚙️ Input Parameters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            motor_kva = st.number_input("Apparent Power (kVA)", value=150.0, step=5.0)
            efficiency = st.slider("Efficiency (%)", 70, 98, 85, 1) / 100
        with col2:
            motor_cos = st.slider("Power Factor (cos φ)", 0.7, 0.95, 0.8, 0.01)
            start_factor = st.slider("Starting Current Factor", 4.0, 10.0, 6.5, 0.5)
    
    if st.button("🔍 Calculate Motor", use_container_width=True):
        result = PowerSystemCalculator.calculate_motor(
            motor_kva, efficiency, motor_cos, 380, start_factor
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("⚡️ Rated Current", f"{result['rated_current']} A")
            st.metric("🚀 Starting Current", f"{result['starting_current']} A")
        with col2:
            st.metric("🔌 Input Power", f"{result['power_in']} kW")
            st.metric("🎯 Output Power", f"{result['power_out']} kW")
        
        with st.expander("📊 Additional Parameters"):
            st.write(f"**Torque:** {result['torque']} Nm")
            st.write(f"**Efficiency:** {result['efficiency']}%")
            st.latex(r"""
            I_{rated} = \frac{P_{kW} \times 1000}{\eta \times \sqrt{3} \times V \times \cos\phi}
            """)

# --- تب ۴: حفاظت (Protection) ---
with tabs[3]:
    st.header("🛡️ Circuit Breaker Sizing (IEC 60947)")
    
    with st.expander("⚙️ Input Parameters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            load_current = st.number_input("Load Current (A)", value=100.0, step=1.0)
            load_type = st.selectbox("Load Type", ["Resistive", "Inductive", "Motor"])
        with col2:
            consider_starting = st.checkbox("Consider Motor Starting", value=False)
    
    if st.button("🔍 Suggest Breaker", use_container_width=True):
        result = PowerSystemCalculator.suggest_breaker(
            load_current, load_type, consider_starting
        )
        
        st.metric("🛡️ Suggested Breaker", f"{result['suggested_breaker']} A")
        
        with st.expander("📊 Calculation Details"):
            st.write(f"**Required Current:** {result['required_current']} A")
            st.write(f"**Safety Factor:** {result['multiplier']}")
            st.write(f"**Load Type:** {result['load_type']}")
            st.latex(r"""
            I_{breaker} = I_{load} \times K_{safety}
            """)

# --- بخش اطلاعات فنی ---
with st.sidebar:
    st.header("📚 Technical Reference")
    st.markdown("""
    **Standards Used:**
    - IEC 60364 (Cable Sizing)
    - IEEE 485 (UPS Sizing)
    - IEC 60034 (Motor)
    - IEC 60947 (Breakers)
    
    **Assumptions:**
    - 3-Phase AC System
    - Copper Conductors (σ=56)
    - Ambient Temp: 30°C
    - Power Factor: 0.8 (Default)
    """)
    
    st.divider()
    st.caption("Version 2.0 - Industrial Grade")
    st.caption("Developed with ♥ for Power Systems")
