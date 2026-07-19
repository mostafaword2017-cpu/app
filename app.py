# ==============================================================================
# --- Tab 3: Motor ---
# ==============================================================================

with tabs[2]:
    st.header("⚙️ Motor / Generator Sizing with Dual Mode")
    
    st.markdown(f"""
    <div class="dual-mode-box">
        <b>📌 دو حالت محاسبه:</b><br>
        • <b>حالت توان نامی ژنراتور:</b> محاسبه بر اساس حداکثر توان ژنراتور (مناسب برای طراحی اولیه)<br>
        • <b>حالت بار مصرفی واقعی:</b> محاسبه بر اساس بار واقعی (مناسب برای انتخاب کابل و کلید اقتصادی)
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
