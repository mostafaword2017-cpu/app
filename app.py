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
# --- استایل با اسم بزرگتر و فاصله از تب‌ها ---
# ==============================================================================

st.markdown("""
    <style>
    /* ========== اسم نرم‌افزار (3 درجه بزرگتر + فاصله از تب‌ها) ========== */
    .app-title {
        text-align: center;
        padding: 15px 0 25px 0 !important;  /* افزایش padding پایین برای فاصله از تب‌ها */
        margin: 0 !important;
        font-size: 60px !important;  /* 3 درجه بزرگتر (از 46 به 60) */
        font-weight: 800 !important;
        color: #1a1a1a;
        white-space: nowrap;
        overflow: visible;
        letter-spacing: 1px !important;
        line-height: 1.2 !important;
        border-bottom: 3px solid #e8e8e8 !important;  /* خط جداکننده */
        margin-bottom: 15px !important;
    }
    
    .app-title .lightning {
        color: #f9a825;
        display: inline-block;
        margin: 0 6px !important;
        font-size: 68px !important;  /* علامت برق هم بزرگتر */
    }

    @media screen and (max-width: 640px) {
        .app-title {
            font-size: 38px !important;
            padding: 10px 0 20px 0 !important;
            white-space: normal !important;
            word-break: break-word !important;
            line-height: 1.3 !important;
        }
        .app-title .lightning {
            font-size: 42px !important;
        }
    }

    @media screen and (max-width: 400px) {
        .app-title {
            font-size: 30px !important;
            padding: 8px 0 16px 0 !important;
        }
        .app-title .lightning {
            font-size: 34px !important;
        }
    }

    /* ========== تب‌ها ========== */
    .stTabs div[role="tablist"] {
        gap: 8px !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        justify-content: center !important;
        display: flex !important;
        padding: 10px 0 5px 0 !important;  /* فضای بیشتر بالای تب‌ها */
        border-bottom: 3px solid #e0e0e0 !important;
        margin-top: 5px !important;
    }
    
    .stTabs [role="tab"] {
        font-size: 20px !important;
        padding: 12px 24px !important;
        border-radius: 12px 12px 0px 0px !important;
        background-color: #f5f5f5 !important;
        color: #888888 !important;
        white-space: nowrap !important;
        min-width: 90px !important;
        text-align: center !important;
        font-weight: 500 !important;
        border: 2px solid #e0e0e0 !important;
        border-bottom: none !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        opacity: 0.7 !important;
        margin-bottom: -2px !important;
    }
    
    .stTabs [role="tab"]:hover {
        background-color: #e8f5e9 !important;
        color: #2e7d32 !important;
        opacity: 1 !important;
        transform: translateY(-3px) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: 700 !important;
        border-color: #4CAF50 !important;
        border-bottom: 3px solid #4CAF50 !important;
        opacity: 1 !important;
        transform: translateY(-4px) !important;
        box-shadow: 0 4px 16px rgba(76, 175, 80, 0.35) !important;
    }
    
    .stTabs [aria-selected="true"]:hover {
        background-color: #43a047 !important;
        transform: translateY(-4px) !important;
    }
    
    /* ========== موبایل ========== */
    @media screen and (max-width: 640px) {
        .stTabs div[role="tablist"] {
            gap: 4px !important;
            padding: 8px 0 4px 0 !important;
            justify-content: flex-start !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
        }
        
        .stTabs [role="tab"] {
            font-size: 14px !important;
            padding: 8px 14px !important;
            min-width: 60px !important;
            border-radius: 8px 8px 0px 0px !important;
            flex: 0 0 auto !important;
            display: inline-block !important;
        }
        
        .stTabs [aria-selected="true"] {
            transform: translateY(-3px) !important;
            box-shadow: 0 2px 10px rgba(76, 175, 80, 0.3) !important;
        }
    }

    @media screen and (max-width: 400px) {
        .stTabs [role="tab"] {
            font-size: 12px !important;
            padding: 6px 10px !important;
            min-width: 50px !important;
        }
    }
    
    /* ========== مخفی کردن المان‌های اضافی ========== */
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
    
    /* ========== جعبه نتایج ========== */
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

    /* ========== استایل برای نتایج تست ========== */
    .test-pass {
        background-color: #e8f5e9 !important;
        border: 3px solid #4CAF50 !important;
    }
    
    .test-fail {
        background-color: #ffebee !important;
        border: 3px solid #f44336 !important;
    }
    
    .test-warning {
        background-color: #fff3e0 !important;
        border: 3px solid #ff9800 !important;
    }

    /* ========== باکس اطلاعات آبی ========== */
    .info-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
        border-left: 5px solid #2196F3;
        direction: rtl;
        text-align: right;
    }
    
    .info-box b {
        color: #0d47a1;
    }

    .highlight-box {
        background-color: #fff8e1;
        padding: 12px;
        border-radius: 8px;
        border-right: 4px solid #ff9800;
        margin: 8px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# --- نمایش اسم نرم‌افزار (با کلاس جدید) ---
# ==============================================================================

st.markdown("""
    <div class="app-title">
        ElectroCalc <span class="lightning">⚡</span> M&F
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# --- توابع کمکی ---
# ==============================================================================

def get_cable_size(current_a, voltage=380, cos_phi=0.8, max_drop=2, length=50, conductor="Copper"):
    """محاسبه سایز کابل مناسب با یک پله بالاتر"""
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
# --- توابع اصلی ---
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

tabs = st.tabs(["📏 Cable", "🔋 UPS", "⚙️ Motor", "🛡️ Protect", "❄️ HVAC Test"])

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
        
        st.markdown("""
        <div class='info-box'>
            <b>📋 نتیجه محاسبه کابل:</b><br><br>
            • <b>جریان نامی:</b> با توجه به توان و ولتاژ ورودی محاسبه شده است<br>
            • <b>سایز استاندارد:</b> نزدیک‌ترین سایز بالاتر به مقدار محاسبه شده<br>
            • <b>سایز ایمن:</b> با در نظر گرفتن ضریب اطمینان برای طول‌های بالای ۸۰ متر<br><br>
            <b>📐 فرمول:</b> S = (P × L × 100) / (σ × V² × ΔV%)
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
        
        st.markdown("""
        <div class='info-box'>
            <b>📋 نتیجه محاسبه UPS:</b><br><br>
            • <b>ظرفیت باتری:</b> بر اساس توان UPS، زمان پشتیبانی و تعداد باتری‌ها محاسبه شده است<br>
            • <b>سایز کابل:</b> با توجه به جریان ورودی UPS و ضریب اطمینان پیشنهاد شده است<br>
            • <b>کلید محافظ:</b> با در نظر گرفتن نوع بار (سلفی) انتخاب شده است<br><br>
            <b>📐 فرمول:</b> Ah = (Ah_Base × kVA/10 × 32) / (N_Battery × V_Battery/12)
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# --- تب ۳: موتور ---
# ==============================================================================

with tabs[2]:
    st.header("⚙️ Motor / Generator Sizing with Dual Mode")
    
    st.markdown("""
    <div style='background-color: #e8f5e9; padding: 12px; border-radius: 8px; margin-bottom: 15px; direction: rtl; text-align: right;'>
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
        
        st.markdown(f"""
        <div class='info-box'>
            <b>📋 نتیجه محاسبه ژنراتور:</b><br><br>
            • <b>حالت محاسبه:</b> {mode_label}<br>
            • <b>جریان طراحی:</b> {design_current:.2f} آمپر<br>
            • <b>سایز کابل پیشنهادی:</b> {cable_size} میلی‌متر مربع ({conductor_type})<br>
            • <b>افت ولتاژ:</b> {voltage_drop}% {'(مناسب)' if voltage_drop <= 3 else '(بیش از حد مجاز)'}<br>
            • <b>کلید محافظ:</b> {breaker_size} آمپر (نامی) | {starting_breaker} آمپر (راه‌اندازی)<br><br>
            <b>📐 فرمول‌ها:</b><br>
            • I_gen = kVA × 1.44 (فرمول تجربی برای ولتاژ ۳۸۰-۴۱۵ ولت)<br>
            • I_design = I_actual × (1 + Future Expansion%)
        </div>
        """, unsafe_allow_html=True)

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
        
        st.markdown("""
        <div class='info-box'>
            <b>📋 نتیجه محاسبه حفاظت:</b><br><br>
            • <b>کلید محافظ:</b> با توجه به جریان بار و نوع آن انتخاب شده است<br>
            • <b>سایز کابل:</b> بر اساس جریان بار و افت ولتاژ مجاز پیشنهاد شده است<br>
            • <b>ضریب ایمنی:</b> برای بارهای مختلف متفاوت است (مقاومتی: ۱.۲۵، سلفی: ۱.۴، موتوری: ۱.۶)<br><br>
            <b>📐 فرمول:</b> I_breaker = I_load × K_safety
        </div>
        """, unsafe_allow_html=True)

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
    
    st.markdown("""
    <div class='info-box'>
        <b>📋 روش تست:</b> تست توان سرمایشی با استفاده از بادسنج (انیمومتر) - اندازه‌گیری غیرمستقیم<br><br>
        <b>📐 فرمول:</b> P = ṁ × Cₚ × ΔT<br><br>
        <b>🔧 پارامترهای پیش‌فرض:</b> چگالی هوا = ۱.۲ kg/m³ | Cₚ = ۱.۰۰۵ kJ/kg·K<br><br>
        <b>🎯 توان هدف:</b> قابل تنظیم - هر توان سرمایشی را تست کنید<br><br>
        <b>📊 تفسیر نتایج:</b><br>
        • ✅ PASS (≥ ۹۵% توان هدف): سیستم به توان اسمی رسیده است<br>
        • ⚠️ WARNING (۸۰% - ۹۵% توان هدف): سیستم به توان اسمی نرسیده، نیاز به بررسی دارد<br>
        • ❌ FAIL (< ۸۰% توان هدف): سیستم دچار مشکل جدی است
    </div>
    """, unsafe_allow_html=True)
    
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
