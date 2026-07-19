""")

# --- جعبه اطلاعات ---
show_info_box(
"📋 تفسیر نتایج اتصال کوتاه",
[
    f'<span class="highlight">Uk% = {Uk_percent}%</span> - هرچه کمتر باشد، جریان اتصال کوتاه بیشتر است',
    'جریان اتصال کوتاه در ترمینال ترانس: حداکثر مقدار ممکن',
    'با افزودن کابلها، جریان کاهش مییابد (امپدانس افزایش مییابد)',
    'کلید محافظ باید قدرت قطعی ≥ جریان اتصال کوتاه محل نصب داشته باشد',
    '<span class="highlight">ضریب پیک κ:</span> برای محاسبه جریان دینامیکی (الکترودینامیکی)',
    '<span class="highlight">جریان نامتقارن:</span> برای انتخاب کلیدهای قدرت (بریکرها)',
    'در شبکههای LV، جریان اتصال کوتاه معمولاً ۵-۲۰ kA در تابلوها است'
]
)

# ==============================================================================
# --- تب ۷: تنظیمات (Settings) ---
# ==============================================================================

with tabs[6]:
st.header("⚙️ Settings")

st.markdown(f"""
<div class="settings-box">
<b>📋 مدیریت تنظیمات نرم‌افزار</b><br>
در این بخش می‌توانید تنظیمات ظاهری نرم‌افزار را تغییر دهید.
</div>
""", unsafe_allow_html=True)

# ========== تنظیمات تم ==========
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

# ========== اطلاعات نرم‌افزار ==========
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

# ========== وضعیت ==========
st.subheader("🔒 Status")
st.markdown(f"""
✅ **Application Status:** Online  
✅ **Theme:** {current_theme}  
✅ **Version:** 2.0
""")
