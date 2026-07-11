import streamlit as st
import math
import numpy as np
import networkx as nx
import plotly.graph_objects as go
import pandas as pd
from typing import Tuple, Optional, Dict, List

# ==============================================================================
# --- تنظیمات صفحه ---
# ==============================================================================
st.set_page_config(
    page_title="ElectroCalc ⚡ M&F", 
    page_icon="⚡️", 
    layout="wide"
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
    plot_bg = "rgba(255,255,255,0)"
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
    plot_bg = "rgba(30,30,30,0)"

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
    
    .plot-container {{
        background-color: {plot_bg} !important;
        border-radius: 10px !important;
        padding: 10px !important;
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
# --- کلاس اتصال کوتاه (Short Circuit) ---
# ==============================================================================

class ShortCircuitCalculator:
    
    @staticmethod
    def calculate_short_circuit_current(
        voltage_ll: float, source_r: float, source_x: float,
        cable_r: float, cable_x: float, cable_length: float = 100.0,
        motor_contribution: float = 0.0, xr_ratio: float = 10.0
    ) -> dict:
        
        z_source = complex(source_r, source_x)
        z_cable = complex(cable_r * cable_length / 1000, cable_x * cable_length / 1000)
        z_total = z_source + z_cable
        z_magnitude = abs(z_total)
        
        if z_magnitude == 0:
            return {'error': 'امپدانس کل صفر است!'}
        
        ik_rms = voltage_ll / (math.sqrt(3) * z_magnitude)
        ik_rms_ka = ik_rms / 1000
        ik_total_ka = ik_rms_ka + motor_contribution
        
        pi = math.pi
        if xr_ratio > 0:
            peak_factor = 1 + math.exp(-3 * pi / xr_ratio)
        else:
            peak_factor = 2
        ip_ka = math.sqrt(2) * ik_total_ka * peak_factor
        sk_mva = (math.sqrt(3) * voltage_ll * ik_total_ka * 1000) / 1_000_000
        m_factor = 1.0 + math.exp(-4 * pi / xr_ratio)
        n_factor = 1.0
        ith_ka = ik_total_ka * math.sqrt(m_factor + n_factor)
        
        return {
            'ik_rms': round(ik_rms, 2), 'ik_rms_ka': round(ik_rms_ka, 3),
            'ik_total_ka': round(ik_total_ka, 3), 'ip_ka': round(ip_ka, 3),
            'sk_mva': round(sk_mva, 2), 'ith_ka': round(ith_ka, 3),
            'z_magnitude': round(z_magnitude, 4), 'xr_ratio': xr_ratio,
            'motor_contribution': motor_contribution
        }
    
    @staticmethod
    def calculate_cable_thermal_sizing(ith_ka: float, t_clear: float, k_factor: float = 143.0) -> dict:
        required_area = (ith_ka * 1000 * math.sqrt(t_clear)) / k_factor
        standard_sizes = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300]
        selected_size = 1.5
        for size in standard_sizes:
            if size >= required_area:
                selected_size = size
                break
        return {
            'required_area': round(required_area, 2), 'selected_size': selected_size,
            'is_ok': required_area <= selected_size, 'time_clearance': t_clear,
            'k_factor': k_factor
        }


# ==============================================================================
# --- کلاس یکخطی (Single-Line Diagram) ---
# ==============================================================================

class SingleLineDiagram:
    
    def __init__(self):
        self.graph = nx.Graph()
        self.bus_data = {}
        self.line_data = {}
        self.color_scheme = {'Slack': '#FF6B6B', 'PV': '#4ECDC4', 'PQ': '#45B7D1'}
    
    def add_bus(self, bus_id: str, voltage: float, label: str = None, 
                bus_type: str = "PQ", position: tuple = None):
        if position is None:
            n = max(len(self.bus_data) + 2, 6)
            angle = (2 * math.pi * len(self.bus_data)) / n
            pos = (0.5 + 0.4 * math.cos(angle), 0.5 + 0.4 * math.sin(angle))
        else:
            pos = position
        self.graph.add_node(bus_id, voltage=voltage, label=label or bus_id,
                           bus_type=bus_type, pos=pos)
        self.bus_data[bus_id] = {
            'voltage': voltage, 'label': label or bus_id,
            'bus_type': bus_type, 'position': pos
        }
    
    def add_line(self, from_bus: str, to_bus: str, impedance: complex,
                current: float = 0, length: float = 0, rating: float = 0):
        self.graph.add_edge(from_bus, to_bus, impedance=impedance,
                           current=current, length=length, rating=rating)
        self.line_data[f"{from_bus}-{to_bus}"] = {
            'from': from_bus, 'to': to_bus,
            'impedance': impedance, 'current': current,
            'length': length, 'rating': rating
        }
    
    def get_positions(self):
        return nx.get_node_attributes(self.graph, 'pos')
    
    def plot_diagram(self, show_values: bool = True, show_impedance: bool = False,
                    width: int = 800, height: int = 600):
        pos = self.get_positions()
        nodes = list(self.graph.nodes())
        edges = list(self.graph.edges())
        
        edge_x, edge_y, edge_texts = [], [], []
        for edge in edges:
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            line_info = self.line_data.get(f"{edge[0]}-{edge[1]}", {})
            if show_impedance:
                z = line_info.get('impedance', 0j)
                text = f"Z={z.real:.2f}+j{z.imag:.2f}Ω"
            else:
                current = line_info.get('current', 0)
                text = f"I={current:.1f}A" if show_values else ""
            edge_texts.append(text)
        
        node_x, node_y, node_texts, node_colors, node_sizes = [], [], [], [], []
        for node in nodes:
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            bus = self.bus_data.get(node, {})
            voltage = bus.get('voltage', 0)
            bus_type = bus.get('bus_type', 'PQ')
            color = self.color_scheme.get(bus_type, '#45B7D1')
            size = 30 if bus_type == 'Slack' else 25 if bus_type == 'PV' else 20
            node_colors.append(color)
            node_sizes.append(size)
            text = f"<b>{bus.get('label', node)}</b><br>V={voltage:.2f} kV<br>Type: {bus_type}"
            node_texts.append(text)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines',
                   line=dict(width=2, color='#888'), hoverinfo='text',
                   text=edge_texts, name='Lines'))
        fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text',
                   marker=dict(size=node_sizes, color=node_colors,
                              line=dict(width=2, color='DarkSlateGray')),
                   text=[f"<b>{node}</b>" for node in nodes],
                   textposition="top center", hovertext=node_texts,
                   hoverinfo='text', name='Buses'))
        
        fig.update_layout(
            title={'text': "📊 Single-Line Diagram", 'x': 0.5, 'xanchor': 'center'},
            showlegend=False, hovermode='closest',
            width=width, height=height,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.1, 1.1]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.1, 1.1]),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig


def create_sample_network():
    sld = SingleLineDiagram()
    buses = {
        'Bus1': {'voltage': 132, 'type': 'Slack'},
        'Bus2': {'voltage': 132, 'type': 'PV'},
        'Bus3': {'voltage': 132, 'type': 'PV'},
        'Bus4': {'voltage': 33, 'type': 'PQ'},
        'Bus5': {'voltage': 33, 'type': 'PQ'},
        'Bus6': {'voltage': 11, 'type': 'PQ'},
        'Bus7': {'voltage': 11, 'type': 'PQ'},
    }
    for bus_id, data in buses.items():
        sld.add_bus(bus_id, data['voltage'], bus_id, data['type'])
    lines = [
        ('Bus1', 'Bus2', 0.1, 150, 50), ('Bus2', 'Bus3', 0.15, 120, 40),
        ('Bus2', 'Bus4', 0.2, 80, 30), ('Bus3', 'Bus5', 0.25, 70, 25),
        ('Bus4', 'Bus5', 0.12, 90, 35), ('Bus5', 'Bus6', 0.18, 60, 20),
        ('Bus4', 'Bus6', 0.22, 50, 15), ('Bus6', 'Bus7', 0.15, 45, 12),
    ]
    for f, t, z, curr, rating in lines:
        sld.add_line(f, t, complex(z, z*0.2), curr, rating*2, rating)
    return sld


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

tabs = st.tabs(["📏 Cable", "🔋 UPS", "⚙️ Motor", "🛡️ Protect", "⚡ Short Circuit"])

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
# --- تب ۴: حفاظت (Protection) ---
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
        with col1:
            st.metric("🛡️ Breaker", f"{result['suggested_breaker']} A")
        with col2:
            st.metric("Required", f"{result['required_current']} A")
        with col3:
            st.metric("Safety Factor", f"{result['multiplier']}")
        
        with st.expander("📊 Details"):
            st.write(f"**Load Type:** {result['load_type']}")
            st.write(f"**Required Current:** {result['required_current']} A")
            st.write(f"**Safety Factor:** {result['multiplier']}")
            st.latex(r"I_{breaker} = I_{load} \times K_{safety}")

# ==============================================================================
# --- تب ۵: اتصال کوتاه و یکخطی (Short Circuit & Single-Line) ---
# ==============================================================================

with tabs[4]:
    st.header("⚡ Short Circuit & Single-Line")
    
    # زیرتب‌ها
    sub_tabs = st.tabs(["📊 Short Circuit", "📈 Single-Line", "📋 Results"])
    
    # ---- زیرتب ۱: محاسبه اتصال کوتاه ----
    with sub_tabs[0]:
        st.subheader("🔌 Short Circuit Calculation (IEC 60909)")
        
        with st.expander("⚙️ Main Parameters", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                sc_voltage = st.number_input("Line Voltage (V)", value=380.0, step=10.0, key="sc_voltage")
                source_r = st.number_input("Source R (Ω)", value=0.05, step=0.001, format="%.3f", key="sc_sr")
                source_x = st.number_input("Source X (Ω)", value=0.5, step=0.01, key="sc_sx")
            with col2:
                cable_r = st.number_input("Cable R (Ω/km)", value=0.1, step=0.001, format="%.3f", key="sc_cr")
                cable_x = st.number_input("Cable X (Ω/km)", value=0.08, step=0.001, format="%.3f", key="sc_cx")
                cable_length = st.number_input("Cable Length (m)", value=100.0, step=10.0, key="sc_cl")
        
        with st.expander("🔧 Advanced Parameters", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                motor_contribution = st.number_input("Motor Contribution (kA)", value=0.0, step=0.1, key="sc_motor")
                xr_ratio = st.number_input("X/R Ratio", value=10.0, step=1.0, key="sc_xr")
            with col2:
                fault_duration = st.number_input("Fault Duration (s)", value=0.2, step=0.05, key="sc_duration")
                k_factor = st.selectbox("Cable Material", ["Copper (k=143)", "Aluminum (k=94)"], key="sc_k")
        
        if st.button("⚡ Calculate Short Circuit", use_container_width=True, key="sc_btn"):
            # محاسبه جریان اتصال کوتاه
            sc_calc = ShortCircuitCalculator()
            result = sc_calc.calculate_short_circuit_current(
                voltage_ll=sc_voltage,
                source_r=source_r,
                source_x=source_x,
                cable_r=cable_r,
                cable_x=cable_x,
                cable_length=cable_length,
                motor_contribution=motor_contribution,
                xr_ratio=xr_ratio
            )
            
            # محاسبه سایز کابل بر اساس جریان اتصال کوتاه
            k_val = 143.0 if "Copper" in k_factor else 94.0
            thermal_result = sc_calc.calculate_cable_thermal_sizing(
                ith_ka=result['ith_ka'],
                t_clear=fault_duration,
                k_factor=k_val
            )
            
            # ذخیره در session_state
            st.session_state['sc_result'] = result
            st.session_state['thermal_result'] = thermal_result
            st.session_state['sc_parameters'] = {
                'voltage': sc_voltage,
                'source_r': source_r,
                'source_x': source_x,
                'cable_r': cable_r,
                'cable_x': cable_x,
                'cable_length': cable_length,
                'motor_contribution': motor_contribution,
                'xr_ratio': xr_ratio,
                'fault_duration': fault_duration,
                'k_factor': k_val
            }
            
            # نمایش نتایج فوری
            st.markdown("---")
            st.subheader("📊 Results")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("I_k RMS", f"{result['ik_rms_ka']} kA")
                st.metric("I_peak", f"{result['ip_ka']} kA")
            with col2:
                st.metric("S_k", f"{result['sk_mva']} MVA")
                st.metric("I_th", f"{result['ith_ka']} kA")
            with col3:
                st.metric("Cable Required", f"{thermal_result['required_area']} mm²")
                st.metric("Selected Size", f"{thermal_result['selected_size']} mm²", 
                         delta="✅ OK" if thermal_result['is_ok'] else "⚠️ Increase",
                         delta_color="normal" if thermal_result['is_ok'] else "inverse")
            
            if not thermal_result['is_ok']:
                st.warning(f"⚠️ Required area ({thermal_result['required_area']} mm²) is greater than selected size ({thermal_result['selected_size']} mm²). Please increase cable size!")
            else:
                st.success(f"✅ Cable size {thermal_result['selected_size']} mm² is sufficient for fault current")
    
    # ---- زیرتب ۲: نمایش یکخطی ----
    with sub_tabs[1]:
        st.subheader("📈 Single-Line Diagram")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🏗️ Create Sample Network (7-Bus)", use_container_width=True):
                sld = create_sample_network()
                st.session_state['sld'] = sld
                st.success("✅ Sample network created successfully!")
        
        # نمایش دیاگرام
        if 'sld' in st.session_state:
            sld = st.session_state['sld']
            
            # تنظیمات نمایش
            col1, col2 = st.columns(2)
            with col1:
                show_values = st.checkbox("Show Line Currents", value=True, key="sld_show_values")
            with col2:
                show_impedance = st.checkbox("Show Impedance", value=False, key="sld_show_impedance")
            
            # رسم دیاگرام
            fig = sld.plot_diagram(
                show_values=show_values,
                show_impedance=show_impedance,
                width=700,
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # نمایش اطلاعات باسها
            with st.expander("📋 Bus Information"):
                bus_data = []
                for bus_id in sld.bus_data:
                    data = sld.bus_data[bus_id]
                    bus_data.append({
                        'Bus': bus_id,
                        'Voltage (kV)': data['voltage'],
                        'Type': data['bus_type'],
                        'Position': f"({data['position'][0]:.2f}, {data['position'][1]:.2f})"
                    })
                st.dataframe(pd.DataFrame(bus_data), use_container_width=True, hide_index=True)
            
            # نمایش اطلاعات خطوط
            with st.expander("📋 Line Information"):
                line_data = []
                for line_id, data in sld.line_data.items():
                    line_data.append({
                        'Line': line_id,
                        'From': data['from'],
                        'To': data['to'],
                        'Z (Ω)': f"{data['impedance'].real:.3f}+j{data['impedance'].imag:.3f}",
                        'Current (A)': data['current'],
                        'Length (m)': data['length'],
                        'Rating (A)': data['rating']
                    })
                st.dataframe(pd.DataFrame(line_data), use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ Click 'Create Sample Network' to generate a sample single-line diagram")
    
    # ---- زیرتب ۳: نتایج کامل ----
    with sub_tabs[2]:
        st.subheader("📋 Complete Results")
        
        if 'sc_result' in st.session_state:
            result = st.session_state['sc_result']
            thermal = st.session_state['thermal_result']
            params = st.session_state['sc_parameters']
            
            # پارامترهای ورودی
            st.markdown("### 📥 Input Parameters")
            input_df = pd.DataFrame({
                'Parameter': ['Voltage (V)', 'Source R (Ω)', 'Source X (Ω)', 
                             'Cable R (Ω/km)', 'Cable X (Ω/km)', 'Cable Length (m)',
                             'Motor Contribution (kA)', 'X/R Ratio', 'Fault Duration (s)'],
                'Value': [params['voltage'], params['source_r'], params['source_x'],
                         params['cable_r'], params['cable_x'], params['cable_length'],
                         params['motor_contribution'], params['xr_ratio'], params['fault_duration']]
            })
            st.dataframe(input_df, use_container_width=True, hide_index=True)
            
            # نتایج اتصال کوتاه
            st.markdown("### ⚡ Short Circuit Results")
            sc_df = pd.DataFrame({
                'Parameter': ['I_k RMS (A)', 'I_k RMS (kA)', 'I_k Total (kA)', 
                             'I_peak (kA)', 'S_k (MVA)', 'I_th (kA)', 
                             'Z_magnitude (Ω)', 'X/R Ratio'],
                'Value': [result['ik_rms'], result['ik_rms_ka'], result['ik_total_ka'],
                         result['ip_ka'], result['sk_mva'], result['ith_ka'],
                         result['z_magnitude'], result['xr_ratio']]
            })
            st.dataframe(sc_df, use_container_width=True, hide_index=True)
            
            # نتایج کابل
            st.markdown("### 🔌 Cable Thermal Sizing")
            cable_df = pd.DataFrame({
                'Parameter': ['Required Area (mm²)', 'Selected Size (mm²)', 
                             'Status', 'Fault Duration (s)', 'k Factor'],
                'Value': [thermal['required_area'], thermal['selected_size'],
                         '✅ Pass' if thermal['is_ok'] else '❌ Increase',
                         thermal['time_clearance'], thermal['k_factor']]
            })
            st.dataframe(cable_df, use_container_width=True, hide_index=True)
            
            # جمع‌بندی
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if thermal['is_ok']:
                    st.success(f"✅ Cable selection is correct - {thermal['selected_size']} mm²")
                else:
                    st.error(f"❌ Cable is undersized! Required: {thermal['required_area']} mm²")
            
            with col2:
                st.info(f"📊 Fault current level: {result['ik_total_ka']} kA")
                
        else:
            st.info("ℹ️ Please calculate a short circuit first in the 'Short Circuit' tab")

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
    **IEC 60909** - Short Circuit  
    
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
