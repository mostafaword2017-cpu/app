# power_app.py
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from decimal import Decimal, getcontext
import matplotlib.pyplot as plt

# تنظیم دقت Decimal
getcontext().prec = 50

# ==================== تنظیمات صفحه ====================
st.set_page_config(
    page_title="نرمافزار تخصصی برق قدرت",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== استایل سفارشی ====================
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
            color: #f0f0f0;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
            background-color: #1e2229;
            padding: 10px;
            border-radius: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #2d3138;
            color: #aaa;
            border-radius: 8px;
            padding: 10px 25px;
            font-weight: bold;
            font-size: 16px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #007acc !important;
            color: white !important;
        }
        .result-box {
            background-color: #0a0a0a;
            border: 1px solid #00ff00;
            border-radius: 10px;
            padding: 20px;
            font-family: 'Courier New', monospace;
            direction: ltr;
        }
        .metric-card {
            background-color: #1e2229;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #007acc;
        }
    </style>
""", unsafe_allow_html=True)

# ==================== هدر ====================
col_logo, col_title = st.columns([1, 10])
with col_logo:
    st.write("⚡")
with col_title:
    st.title("نرمافزار تخصصی محاسبات برق قدرت")
    st.caption("طراحی شده برای مهندسان شبکه، حفاظت و بهرهبرداری | نسخه ۳.۰ (Web-Based)")

st.markdown("---")

# ==================== تبها ====================
tab1, tab2, tab3, tab4 = st.tabs([
    "📉 افت ولتاژ و تلفات",
    "⚡ اتصال کوتاه (IEC)", 
    "🧮 پخش بار NR",
    "🛡️ هماهنگی حفاظتی"
])

# =====================================================
# تب ۱: افت ولتاژ
# =====================================================
with tab1:
    st.header("📉 محاسبه افت ولتاژ و تلفات خطوط")
    st.info("این ابزار افت ولتاژ و تلفات توان را در خطوط انتقال و توزیع محاسبه میکند.", icon="ℹ️")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("پارامترهای خط")
        V_nom = st.number_input("ولتاژ نامی (kV)", value=20.0, step=1.0, format="%.1f", key="v_nom")
        I_load = st.number_input("جریان بار (A)", value=400.0, step=10.0, format="%.1f", key="i_load")
        pf = st.slider("ضریب توان (cos φ)", min_value=0.5, max_value=1.0, value=0.85, step=0.01, key="pf")
        
    with col2:
        st.subheader("مشخصات خط")
        R = st.number_input("مقاومت خط (Ω/km)", value=0.15, step=0.01, format="%.3f", key="r_line")
        X = st.number_input("راکتانس خط (Ω/km)", value=0.35, step=0.01, format="%.3f", key="x_line")
        length = st.number_input("طول خط (km)", value=5.0, step=0.5, format="%.1f", key="length")
    
    if st.button("🔍 محاسبه افت ولتاژ", type="primary", use_container_width=True):
        try:
            V = Decimal(str(V_nom))
            I = Decimal(str(I_load))
            cos = Decimal(str(pf))
            R_dec = Decimal(str(R))
            X_dec = Decimal(str(X))
            L = Decimal(str(length))
            
            sin = (1 - cos**2).sqrt()
            R_total = R_dec * L
            X_total = X_dec * L
            
            dV = I * (R_total * cos + X_total * sin)
            dV_percent = (dV / V) * 100
            P_loss = 3 * (I**2) * R_total
            Q_loss = 3 * (I**2) * X_total
st.markdown("---")
            st.subheader("📊 نتایج محاسبه")
            
            col_res1, col_res2, col_res3 = st.columns(3)
            with col_res1:
                st.metric("افت ولتاژ خطی", f"{float(dV):.3f} kV", delta=f"{float(dV_percent):.2f}%")
            with col_res2:
                st.metric("تلفات اکتیو سهفاز", f"{float(P_loss/1000):.2f} kW")
            with col_res3:
                st.metric("تلفات راکتیو سهفاز", f"{float(Q_loss/1000):.2f} kVAR")
            
            # نمایش فرمول
            with st.expander("📐 مشاهده فرمول محاسبه", expanded=False):
                st.latex(r"\Delta V = I \times (R \cos\phi + X \sin\phi)")
                st.latex(r"\Delta V\% = \frac{\Delta V}{V_{nom}} \times 100")
                st.latex(r"P_{loss} = 3 I^2 R")
                st.latex(r"Q_{loss} = 3 I^2 X")
                
        except Exception as e:
            st.error(f"❌ خطا در محاسبه: {str(e)}")
            st.warning("لطفاً مقادیر ورودی را بررسی کنید.")

# =====================================================
# تب ۲: اتصال کوتاه
# =====================================================
with tab2:
    st.header("⚡ محاسبه اتصال کوتاه مطابق IEC 60909")
    st.info("محاسبه جریان اتصال کوتاه سهفاز متقارن و جریان پیک بر اساس استاندارد IEC.", icon="ℹ️")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("پارامترهای شبکه")
        V_sc = st.number_input("ولتاژ نامی (kV)", value=20.0, step=1.0, key="sc_v")
        S_sc = st.number_input("توان اتصال کوتاه شبکه (MVA)", value=500.0, step=50.0, format="%.1f", key="sc_s")
        
    with col2:
        st.subheader("امپدانس تجهیز")
        R1 = st.number_input("مقاومت توالی مثبت (Ω)", value=0.8, step=0.1, format="%.2f", key="r1")
        X1 = st.number_input("راکتانس توالی مثبت (Ω)", value=4.5, step=0.1, format="%.2f", key="x1")
    
    if st.button("⚡ محاسبه جریان اتصال کوتاه", type="primary", use_container_width=True):
        try:
            V = float(V_sc)
            S_k = float(S_sc)
            R = float(R1)
            X = float(X1)
            
            Z_net = (V**2) / S_k
            I_k3 = (V * 1000) / (np.sqrt(3) * np.sqrt(R**2 + X**2))
            
            # ضریب پیک IEC
            ratio = X / R if R != 0 else float('inf')
            kappa = 1.02 + 0.98 * np.exp(-3 * ratio) if ratio < 10 else 1.8
            I_peak = kappa * np.sqrt(2) * I_k3
            
            st.markdown("---")
            st.subheader("📊 نتایج اتصال کوتاه")
            
            col_res1, col_res2, col_res3 = st.columns(3)
            with col_res1:
                st.metric("امپدانس شبکه", f"{Z_net:.4f} Ω")
                st.metric("نسبت X/R", f"{ratio:.2f}")
            with col_res2:
                st.metric("جریان اتصال کوتاه", f"{I_k3:,.2f} A", delta="RMS")
            with col_res3:
                st.metric("جریان پیک (I_p)", f"{I_peak:,.2f} A", delta=f"κ = {kappa:.3f}")
            
            # نمایش استاندارد
            with st.expander("📖 مرجع استاندارد IEC 60909", expanded=False):
                st.markdown("""
                روابط محاسباتی:
                - امپدانس شبکه: Z_net = V² / S_k
                - جریان اتصال کوتاه: I_k3 = V / (√3 × √(R² + X²))
                - ضریب پیک: κ = 1.02 + 0.98 × e^(-3×X/R)
                """)
                
        except Exception as e:
            st.error(f"❌ خطا: {str(e)}")

# =====================================================
# تب ۳: پخش بار نیوتن-رافسون
# =====================================================
with tab3:
    st.header("🧮 پخش بار با روش نیوتن-رافسون (سیستم ۳ باسه)")
    st.info("تحلیل پخش بار برای سیستم ۳ باسه با باس ۱ به عنوان اسلک (Slack).", icon="ℹ️")
    
    st.markdown("""
    توپولوژی شبکه:
    - باس ۱: اسلک (ولتاژ مرجع)
with st.expander("📖 توضیحات منحنی", expanded=False):
                    st.markdown("""
                    مشخصه بسیار معکوس (Very Inverse) طبق IEC:
                    - فرمول: t = TMS × (13.5 / (I/Ip) - 1)
                    - مناسب برای هماهنگی با فیوزها و بریکرهای پاییندست
                    - هرچه جریان خطا بیشتر باشد، زمان عملکرد کوتاهتر میشود
                    """)
            
        except Exception as e:
            st.error(f"❌ خطا: {str(e)}")

# ==================== فوتر ====================
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("⚡ توسعه‌یافته برای مهندسی برق قدرت")
with col2:
    st.caption("📚 منبع: استانداردهای IEC 60909 و IEC 60255")
with col3:
    st.caption("🔄 نسخه ۳.۰ - Web-Based")

# اطلاعات جلسه
with st.sidebar:
    st.header("📋 اطلاعات")
    st.info("""
    نرم‌افزار محاسبات برق قدرت
    
    ✅ ۴ ماژول تخصصی
    ✅ محاسبات با دقت بالا
    ✅ نمودارهای تعاملی
    ✅ قابل اجرا در مرورگر
    """)
    
    st.markdown("---")
    st.caption("ساخته شده با ❤️ توسط تیم مهندسی")
- باس ۲: بار PQ
    - باس ۳: بار PQ
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("بار باس ۲")
        P2 = st.number_input("توان اکتیو (MW)", value=50.0, step=5.0, format="%.1f", key="p2")
        Q2 = st.number_input("توان راکتیو (MVAR)", value=20.0, step=5.0, format="%.1f", key="q2")
        
    with col2:
        st.subheader("بار باس ۳")
        P3 = st.number_input("توان اکتیو (MW)", value=30.0, step=5.0, format="%.1f", key="p3")
        Q3 = st.number_input("توان راکتیو (MVAR)", value=15.0, step=5.0, format="%.1f", key="q3")
    
    iterations = st.slider("تعداد تکرار", min_value=1, max_value=10, value=5, key="iter")
    
    if st.button("🧮 اجرای پخش بار", type="primary", use_container_width=True):
        try:
            # ماتریس ادمیتانس سیستم ۳ باسه
            Y = np.array([[10-30j, -5+15j, -5+15j],
                          [-5+15j, 10-30j, -5+15j],
                          [-5+15j, -5+15j, 10-30j]], dtype=complex)
            
            V = np.array([1.0+0j, 1.0+0j, 1.0+0j], dtype=complex)
            V_history = []
            
            with st.spinner("در حال همگرایی..."):
                for iter_num in range(iterations):
                    I = np.dot(Y, V)
                    S_calc = V * np.conj(I)
                    
                    dP = np.array([0, float(P2) - S_calc[1].real, float(P3) - S_calc[2].real])
                    dQ = np.array([0, float(Q2) - S_calc[1].imag, float(Q3) - S_calc[2].imag])
                    
                    # ژاکوبین سادهشده
                    J = np.array([[50, -20], [-20, 50]])
                    try:
                        dTheta_dV = np.linalg.solve(J, np.array([dP[1], dP[2]]))
                        V[1] += 0.02 * dTheta_dV[0]
                        V[2] += 0.02 * dTheta_dV[1]
                        V_history.append([abs(V[1]), abs(V[2])])
                    except:
                        break
            
            st.markdown("---")
            st.subheader("📊 نتایج پخش بار")
            
            col_res1, col_res2, col_res3 = st.columns(3)
            with col_res1:
                st.metric("ولتاژ باس ۲", f"{abs(V[1]):.4f} pu", delta=f"{np.angle(V[1], deg=True):.2f}°")
            with col_res2:
                st.metric("ولتاژ باس ۳", f"{abs(V[2]):.4f} pu", delta=f"{np.angle(V[2], deg=True):.2f}°")
            with col_res3:
                st.metric("توان تزریقی باس اسلک", f"{S_calc[0]:.3f} MVA")
            
            # رسم نمودار همگرایی
            if len(V_history) > 0:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    y=[v[0] for v in V_history],
                    mode='lines+markers',
                    name='باس ۲',
                    line=dict(color='#00ffff', width=2)
                ))
                fig.add_trace(go.Scatter(
                    y=[v[1] for v in V_history],
                    mode='lines+markers',
                    name='باس ۳',
                    line=dict(color='#ff66ff', width=2)
                ))
                fig.update_layout(
                    title="روند همگرایی ولتاژ",
                    xaxis_title="تکرار",
                    yaxis_title="ولتاژ (پریونیت)",
                    template="plotly_dark",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ خطای همگرایی: {str(e)}")
            st.warning("سیستم ممکن است به نقطه کار قابل قبول نرسد. پارامترها را بررسی کنید.")

# =====================================================
# تب ۴: هماهنگی حفاظتی
# =====================================================
with tab4:
    st.header("🛡️ هماهنگی حفاظتی (رله IDMT)")
    st.info("محاسبه زمان عملکرد رله بر اساس مشخصه بسیار معکوس (Very Inverse) مطابق استاندارد IEC.", icon="ℹ️")
col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("پارامترهای شبکه")
        I_n = st.number_input("جریان نامی تجهیز (A)", value=100.0, step=10.0, format="%.1f", key="in")
        I_fault = st.number_input("جریان خطا (kA)", value=5.0, step=0.5, format="%.2f", key="ifault")
        
    with col2:
        st.subheader("تنظیمات CT و رله")
        ct_primary = st.number_input("CT - جریان اولیه (A)", value=200, step=50, key="ct_p")
        ct_secondary = st.number_input("CT - جریان ثانویه (A)", value=5, step=1, key="ct_s")
        tms = st.slider("تنظیم TMS", min_value=0.05, max_value=1.0, value=0.1, step=0.05, key="tms")
    
    if st.button("🛡️ محاسبه زمان عملکرد", type="primary", use_container_width=True):
        try:
            I_f = float(I_fault) * 1000
            ct_ratio = ct_primary / ct_secondary
            I_secondary = I_f / ct_ratio
            
            # مشخصه بسیار معکوس IEC
            alpha = 13.5
            beta = 1
            if I_secondary > 1:
                t_operate = tms * (alpha / ((I_secondary / 1)**beta - 1))
            else:
                t_operate = float('inf')
            
            st.markdown("---")
            st.subheader("📊 نتایج حفاظتی")
            
            col_res1, col_res2, col_res3 = st.columns(3)
            with col_res1:
                st.metric("جریان اولیه خطا", f"{I_f/1000:.2f} kA")
                st.metric("نسبت CT", f"{ct_primary}/{ct_secondary}")
            with col_res2:
                st.metric("جریان ثانویه CT", f"{I_secondary:.2f} A")
                st.metric("تنظیم TMS", f"{tms:.2f}")
            with col_res3:
                if t_operate != float('inf'):
                    st.metric("زمان عملکرد رله", f"{t_operate:.3f} ثانیه")
                else:
                    st.metric("زمان عملکرد رله", "∞ (بی‌نهایت)")
            
            # رسم منحنی زمان-جریان با Plotly
            if I_secondary > 1:
                currents = np.linspace(1.1, max(I_secondary * 2, 5), 100)
                times = tms * (alpha / (currents**beta - 1))
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=currents,
                    y=times,
                    mode='lines',
                    name='منحنی IDMT (Very Inverse)',
                    line=dict(color='#ff66ff', width=3)
                ))
                
                # نقطه عملکرد
                fig.add_trace(go.Scatter(
                    x=[I_secondary],
                    y=[t_operate if t_operate != float('inf') else 10],
                    mode='markers',
                    name='نقطه عملکرد',
                    marker=dict(size=15, color='red', symbol='x', line=dict(width=3))
                ))
                
                # خطوط راهنما
                fig.add_hline(y=t_operate if t_operate != float('inf') else 10, 
                             line_dash="dash", line_color="gray", 
                             annotation_text=f"t = {t_operate:.3f}s")
                fig.add_vline(x=I_secondary, line_dash="dash", line_color="gray",
                             annotation_text=f"I = {I_secondary:.1f}A")
                
                fig.update_layout(
                    title="منحنی زمان-جریان رله",
                    xaxis_title="جریان ثانویه CT (A)",
                    yaxis_title="زمان عملکرد (ثانیه)",
                    template="plotly_dark",
                    height=450,
                    showlegend=True
                )
                
                # تنظیم مقیاس لگاریتمی برای دید بهتر
                fig.update_xaxis(type="log")
                fig.update_yaxis(type="log")
                
                st.plotly_chart(fig, use_container_width=True)
                
                # توضیحات
