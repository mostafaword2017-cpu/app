import streamlit as st
import math

# ۱. تنظیمات اولیه صفحه (باید اولین دستور باشد)
st.set_page_config(page_title="ElectroCalc M&F", page_icon="⚡", layout="centered")

# ۲. استایل‌های پیشرفته (حذف هدر/فوتر و بهینه‌سازی فونت‌ها)
hide_st_style = """
    <style>
    / حذف منوی اصلی و فوتر /
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stAppDeployButton"] {display: none;}

    / نگه داشتن دکمه تغییر تم در هدر اما حذف لینک گیت‌هاب /
    .stApp header div[data-testid="stHeader"] {
        visibility: visible;
    }
    header div[data-testid="stHeader"] a {
        display: none !important;
    }

    / اصلاح فونت تیتر برای گوشی (تک خطی و مرتب) /
    .stApp h1 {
        font-size: 26px !important;
        text-align: center;
        white-space: nowrap;
    }
    @media screen and (max-width: 640px) {
        .stApp h1 {
            font-size: 20px !important;
        }
    }

    / استایل تب‌ها /
    .stTabs div[role="tablist"] { gap: 10px; }
    .stTabs [role="tab"] {
        font-size: 14px !important;
        font-weight: bold !important;
        padding: 8px 15px !important;
        border-radius: 10px 10px 0px 0px !important;
    }
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- بخش تیتر برنامه ---
st.title("⚡ ElectroCalc M&F")

# ایجاد تب‌ها
tabs = st.tabs(["🔌 کابل", "🔋 UPS", "⚙️ موتور"])

with tabs[0]:
    st.markdown("### 📏 محاسبه سطح مقطع (افت ولتاژ)")

    # ورودی‌ها (به صورت ستونی برای زیبایی در دسکتاپ و موبایل)
    power = st.number_input("توان مصرفی (kW)", value=85.0, step=1.0)
    length = st.number_input("طول مسیر (متر)", value=90.0, step=1.0)
    sigma = st.number_input("ضریب رسانایی (Sigma)", value=56.0, step=0.1)
    voltage_drop = st.number_input("افت ولتاژ مجاز (%)", value=3.0, step=0.1)

    # --- بخش محاسبات ---
    # نکته: من اینجا فرمول ساده‌ای گذاشتم، تو فرمول‌های دقیق خودت را جایگزین کن
    # مثال: result_area = (some_formula)
    result_area = (power  length) / (voltage_drop  sigma) 

    st.success(f"سطح مقطع محاسبه شده: {result_area:.2f} mm²")

with tabs[1]:
    st.info("بخش UPS در حال توسعه است...")

with tabs[2]:
    st.info("بخش موتور در حال توسعه است...")
