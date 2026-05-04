import streamlit as st
import json
import uuid
import os  # You're missing this import too!
from datetime import datetime

# CONFIGURATION & PERSISTENCE
st.set_page_config(
    page_title="Nexus Textile ERP",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ADD THIS: A manual sidebar toggle button in the main area
# This creates a button that users can click if the sidebar disappears
col1, col2, col3 = st.columns([1, 10, 1])
with col1:
    if st.button("☰ Show/Hide Sidebar", key="toggle_sidebar_btn"):
        # This toggles the sidebar using session state
        if "sidebar_hidden" not in st.session_state:
            st.session_state.sidebar_hidden = False
        st.session_state.sidebar_hidden = not st.session_state.sidebar_hidden
        st.rerun()

# Display current sidebar status
with st.sidebar:
    st.write("### ✅ Sidebar is Visible")
    st.write("Click the '☰' in top-left or press Ctrl+Shift+S to hide/show")

# ==========================================
# CONFIGURATION & PERSISTENCE
# ==========================================
st.set_page_config(
    page_title="Nexus Textile ERP", 
    page_icon="🧵", 
    layout="wide",
    initial_sidebar_state="expanded"  # This forces the sidebar to show up
)
DATA_FILE = "erp_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        "raw_materials": [],
        "spinning_weaving": [],
        "wet_processing": [],
        "finished_goods": []
    }

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

if 'data' not in st.session_state:
    st.session_state.data = load_data()

def update_data():
    save_data(st.session_state.data)

# ==========================================
# CUSTOM CSS / BRANDING
# ==========================================
custom_css = """
<style>
/* Hide Streamlit default elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}

/* Global Theme */
body, .stApp {
    background-color: #0E1117;
    color: #FFFFFF;
    font-family: 'Inter', sans-serif;
}

/* Glassmorphism Cards */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    transition: transform 0.3s ease, border-color 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-5px);
    border-color: #00D4FF;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF;
    font-weight: 800;
}

.neon-cyan {
    color: #00D4FF;
    text-shadow: 0 0 15px rgba(0, 212, 255, 0.6);
}

.neon-emerald {
    color: #00FF88;
    text-shadow: 0 0 15px rgba(0, 255, 136, 0.6);
}

/* Grid Layout */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
}
.metric-value {
    font-size: 3rem;
    font-weight: bold;
    margin: 15px 0;
}
.metric-label {
    font-size: 1.1rem;
    color: #A0AEC0;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
}

/* Streamlit Button Overrides */
div.stButton > button {
    background-color: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.2);
    color: white;
    border-radius: 8px;
    transition: all 0.3s;
}
div.stButton > button:hover {
    border-color: #00D4FF;
    color: #00D4FF;
    background-color: rgba(0, 212, 255, 0.1);
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown("<h1 class='neon-cyan' style='text-align: center;'>🏭 NEXUS ERP</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #A0AEC0; font-weight: bold;'>ENTERPRISE TEXTILE SUITE</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "SYSTEM MODULES",
    [
        "🌐 Global Command Dashboard",
        "🌾 Raw Materials Stage",
        "🧵 Spinning & Weaving",
        "🧪 Wet Processing",
        "📦 Finished Goods"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center; padding: 15px; border-radius: 10px; background: rgba(0, 255, 136, 0.1); border: 1px solid #00FF88;'>
    <h3 style='margin:0; color: #00FF88; font-size: 1rem;'>🟢 SYSTEM ONLINE</h3>
    <p style='margin:0; font-size: 0.8rem; color: #A0AEC0;'>All modules active</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# MODULE IMPLEMENTATIONS
# ==========================================

if menu == "🌐 Global Command Dashboard":
    st.markdown("<h1>🌐 Global <span class='neon-cyan'>Command Dashboard</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #A0AEC0; font-size: 1.2rem;'>High-level metrics across all enterprise manufacturing nodes.</p><br>", unsafe_allow_html=True)
    
    total_raw = len(st.session_state.data.get("raw_materials", []))
    total_spinning = len(st.session_state.data.get("spinning_weaving", []))
    total_chemicals = len(st.session_state.data.get("wet_processing", []))
    total_finished = len(st.session_state.data.get("finished_goods", []))
    
    low_stock_chemicals = sum(1 for c in st.session_state.data.get("wet_processing", []) if float(c['volume_liters']) <= float(c['alert_level']))
    
    dashboard_html = f"""
    <div class="metric-grid">
        <div class="glass-card">
            <div class="metric-label">🌾 Raw Material Batches</div>
            <div class="metric-value neon-cyan">{total_raw}</div>
            <div style="color: #A0AEC0; font-size: 0.9rem;">Active bales in facility</div>
        </div>
        <div class="glass-card">
            <div class="metric-label">🧵 Active Production</div>
            <div class="metric-value neon-cyan">{total_spinning}</div>
            <div style="color: #A0AEC0; font-size: 0.9rem;">Yarn & Fabric on looms</div>
        </div>
        <div class="glass-card">
            <div class="metric-label">📦 Finished Goods</div>
            <div class="metric-value neon-emerald">{total_finished}</div>
            <div style="color: #A0AEC0; font-size: 0.9rem;">Ready for dispatch</div>
        </div>
        <div class="glass-card" style="border-color: {'#FF4444' if low_stock_chemicals > 0 else 'rgba(255,255,255,0.1)'}; box-shadow: {'0 0 20px rgba(255,68,68,0.4)' if low_stock_chemicals > 0 else '0 4px 30px rgba(0,0,0,0.5)'};">
            <div class="metric-label">⚠️ Chemical Alerts</div>
            <div class="metric-value" style="color: {'#FF4444' if low_stock_chemicals > 0 else '#00FF88'}; text-shadow: {'0 0 10px rgba(255,68,68,0.5)' if low_stock_chemicals > 0 else '0 0 10px rgba(0,255,136,0.5)'};">{low_stock_chemicals}</div>
            <div style="color: #A0AEC0; font-size: 0.9rem;">Dyes/Chemicals running low</div>
        </div>
    </div>
    """
    st.markdown(dashboard_html, unsafe_allow_html=True)

elif menu == "🌾 Raw Materials Stage":
    st.markdown("<h1>🌾 Raw Material <span class='neon-emerald'>& Preparatory</span></h1>", unsafe_allow_html=True)
    
    with st.expander("➕ INGEST NEW COTTON BALE", expanded=False):
        with st.form("add_raw_material"):
            col1, col2, col3 = st.columns(3)
            with col1:
                origin = st.text_input("Bale Origin (e.g., Texas, India, Egypt)")
            with col2:
                weight = st.number_input("Weight (kg)", min_value=0.0, step=10.0, value=250.0)
            with col3:
                stage = st.selectbox("Current Stage", ["Raw Storage", "Ginning", "Blowroom", "Draw Frame"])
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("REGISTER BALE TO SYSTEM", use_container_width=True)
            if submitted and origin:
                new_bale = {
                    "id": f"BL-{uuid.uuid4().hex[:6].upper()}",
                    "origin": origin,
                    "weight": weight,
                    "stage": stage,
                    "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.data["raw_materials"].append(new_bale)
                update_data()
                st.success("✅ Bale ingested successfully!")
                st.rerun()

    st.markdown("<h3>📦 CURRENT INVENTORY TRACKING</h3>", unsafe_allow_html=True)
    items = st.session_state.data.get("raw_materials", [])
    if not items:
        st.info("No raw materials registered in the system.")
    else:
        cols = st.columns(3)
        for i, item in enumerate(items):
            with cols[i % 3]:
                card_html = f"""
                <div class="glass-card" style="margin-bottom: 10px; padding: 20px;">
                    <h3 class="neon-cyan" style="margin-top: 0; font-size: 1.5rem;">{item['id']}</h3>
                    <p style="margin: 5px 0; font-size: 1.1rem;"><b>Origin:</b> {item['origin']}</p>
                    <p style="margin: 5px 0; font-size: 1.1rem;"><b>Weight:</b> {item['weight']} kg</p>
                    <div style="margin-top: 15px; padding: 5px; background: rgba(0, 255, 136, 0.1); border-radius: 5px; border-left: 3px solid #00FF88;">
                        <b style="color: #00FF88;">STAGE:</b> {item['stage']}
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                if st.button(f"🗑️ Remove Bale", key=f"del_raw_{item['id']}", use_container_width=True):
                    st.session_state.data["raw_materials"].remove(item)
                    update_data()
                    st.rerun()

elif menu == "🧵 Spinning & Weaving":
    st.markdown("<h1>🧵 The Spinning <span class='neon-cyan'>& Weaving Pipeline</span></h1>", unsafe_allow_html=True)

    with st.expander("➕ INITIALIZE PRODUCTION BATCH", expanded=False):
        with st.form("add_spinning"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                yarn_count = st.text_input("Yarn Count (e.g., 40s, 60s)")
            with col2:
                gsm_target = st.number_input("GSM Target", min_value=0, value=150)
            with col3:
                loom_id = st.text_input("Loom / Machine ID")
            with col4:
                status = st.selectbox("Production Status", ["In Transit", "On Loom", "Quality Check", "Completed"])
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("COMMENCE PRODUCTION BATCH", use_container_width=True)
            if submitted and yarn_count and loom_id:
                new_batch = {
                    "id": f"PRD-{uuid.uuid4().hex[:6].upper()}",
                    "yarn_count": yarn_count,
                    "gsm_target": gsm_target,
                    "loom_id": loom_id,
                    "status": status,
                    "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.data["spinning_weaving"].append(new_batch)
                update_data()
                st.success("✅ Batch initialized successfully!")
                st.rerun()

    st.markdown("<h3>⚙️ ACTIVE MANUFACTURING BATCHES</h3>", unsafe_allow_html=True)
    items = st.session_state.data.get("spinning_weaving", [])
    if not items:
        st.info("No active production batches.")
    else:
        cols = st.columns(3)
        for i, item in enumerate(items):
            with cols[i % 3]:
                card_html = f"""
                <div class="glass-card" style="margin-bottom: 10px; padding: 20px;">
                    <h3 class="neon-cyan" style="margin-top: 0; font-size: 1.5rem;">{item['id']}</h3>
                    <p style="margin: 5px 0; font-size: 1.1rem;"><b>Yarn Count:</b> {item['yarn_count']}</p>
                    <p style="margin: 5px 0; font-size: 1.1rem;"><b>GSM Target:</b> {item['gsm_target']}</p>
                    <p style="margin: 5px 0; font-size: 1.1rem;"><b>Loom ID:</b> {item['loom_id']}</p>
                    <div style="margin-top: 15px; padding: 5px; background: rgba(0, 212, 255, 0.1); border-radius: 5px; border-left: 3px solid #00D4FF;">
                        <b style="color: #00D4FF;">STATUS:</b> {item['status']}
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                if st.button(f"🗑️ Terminate Batch", key=f"del_spin_{item['id']}", use_container_width=True):
                    st.session_state.data["spinning_weaving"].remove(item)
                    update_data()
                    st.rerun()

elif menu == "🧪 Wet Processing":
    st.markdown("<h1>🧪 Wet Processing <span class='neon-emerald'>& Chemicals</span></h1>", unsafe_allow_html=True)

    with st.expander("➕ REGISTER DYE / CHEMICAL", expanded=False):
        with st.form("add_chemical"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                chem_name = st.text_input("Chemical Name (e.g., Indigo Dye)")
            with col2:
                chem_type = st.selectbox("Type", ["Dye", "Bleach", "Softener", "Enzyme", "Other"])
            with col3:
                volume = st.number_input("Volume (Liters)", min_value=0.0, value=1000.0)
            with col4:
                alert_level = st.number_input("Alert Threshold (L)", min_value=0.0, value=200.0)
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("ADD TO CHEMICAL INVENTORY", use_container_width=True)
            if submitted and chem_name:
                new_chem = {
                    "id": f"CHM-{uuid.uuid4().hex[:6].upper()}",
                    "name": chem_name,
                    "type": chem_type,
                    "volume_liters": volume,
                    "alert_level": alert_level,
                    "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.data["wet_processing"].append(new_chem)
                update_data()
                st.success("✅ Chemical registered successfully!")
                st.rerun()

    st.markdown("<h3>🛢️ CHEMICAL INVENTORY REGISTRY</h3>", unsafe_allow_html=True)
    items = st.session_state.data.get("wet_processing", [])
    if not items:
        st.info("No chemicals in inventory.")
    else:
        cols = st.columns(3)
        for i, item in enumerate(items):
            with cols[i % 3]:
                is_low = float(item['volume_liters']) <= float(item['alert_level'])
                border_col = "#FF4444" if is_low else "rgba(255, 255, 255, 0.1)"
                status_text = "⚠️ CRITICAL LOW" if is_low else "🟢 OPTIMAL"
                status_color = "#FF4444" if is_low else "#00FF88"
                bg_color = "rgba(255, 68, 68, 0.1)" if is_low else "rgba(0, 255, 136, 0.1)"
                
                card_html = f"""
                <div class="glass-card" style="margin-bottom: 10px; padding: 20px; border: 1px solid {border_col}; box-shadow: {'0 0 15px rgba(255,68,68,0.3)' if is_low else '0 4px 30px rgba(0,0,0,0.5)'};">
                    <h3 class="neon-cyan" style="margin-top: 0; font-size: 1.5rem;">{item['id']}</h3>
                    <p style="margin: 5px 0; font-size: 1.1rem;"><b>Name:</b> {item['name']}</p>
                    <p style="margin: 5px 0; font-size: 1.1rem;"><b>Type:</b> {item['type']}</p>
                    <p style="margin: 5px 0; font-size: 1.1rem;"><b>Current Vol:</b> <span style="font-size: 1.3rem; font-weight: bold;">{item['volume_liters']} L</span></p>
                    <p style="margin: 5px 0; color: #A0AEC0;">Threshold: {item['alert_level']} L</p>
                    <div style="margin-top: 15px; padding: 5px; background: {bg_color}; border-radius: 5px; border-left: 3px solid {status_color}; text-align: center;">
                        <b style="color: {status_color};">{status_text}</b>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                if st.button(f"🗑️ Delete Item", key=f"del_chem_{item['id']}", use_container_width=True):
                    st.session_state.data["wet_processing"].remove(item)
                    update_data()
                    st.rerun()

elif menu == "📦 Finished Goods":
    st.markdown("<h1>📦 Finished Goods <span class='neon-cyan'>Warehouse</span></h1>", unsafe_allow_html=True)

    with st.expander("➕ LOG FINISHED FABRIC ROLL", expanded=False):
        with st.form("add_finished"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                fabric = st.text_input("Fabric Type (e.g., Denim, Silk)")
            with col2:
                length = st.number_input("Length (meters)", min_value=0.0, value=1000.0)
            with col3:
                color = st.text_input("Final Color")
            with col4:
                qa_status = st.selectbox("QA Status", ["Pending", "Approved", "Rejected"])
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("STORE IN WAREHOUSE DATABASE", use_container_width=True)
            if submitted and fabric and color:
                new_roll = {
                    "id": f"ROL-{uuid.uuid4().hex[:6].upper()}",
                    "fabric": fabric,
                    "length_m": length,
                    "color": color,
                    "qa_status": qa_status,
                    "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.data["finished_goods"].append(new_roll)
                update_data()
                st.success("✅ Roll added to warehouse!")
                st.rerun()

    st.markdown("<h3>🏭 SECURE STORAGE GRID</h3>", unsafe_allow_html=True)
    items = st.session_state.data.get("finished_goods", [])
    if not items:
        st.info("Warehouse is empty.")
    else:
        cols = st.columns(3)
        for i, item in enumerate(items):
            with cols[i % 3]:
                qa_color = "#00FF88" if item['qa_status'] == "Approved" else ("#FF4444" if item['qa_status'] == "Rejected" else "#FFAA00")
                qa_bg = "rgba(0, 255, 136, 0.1)" if item['qa_status'] == "Approved" else ("rgba(255, 68, 68, 0.1)" if item['qa_status'] == "Rejected" else "rgba(255, 170, 0, 0.1)")
                
                card_html = f"""
                <div class="glass-card" style="margin-bottom: 10px; padding: 20px;">
                    <h3 class="neon-cyan" style="margin-top: 0; font-size: 1.5rem;">{item['id']}</h3>
                    <p style="margin: 5px 0; font-size: 1.1rem;"><b>Fabric:</b> {item['fabric']}</p>
                    <p style="margin: 5px 0; font-size: 1.1rem;"><b>Length:</b> {item['length_m']} m</p>
                    <p style="margin: 5px 0; font-size: 1.1rem;"><b>Color:</b> {item['color']}</p>
                    <div style="margin-top: 15px; padding: 5px; background: {qa_bg}; border-radius: 5px; border-left: 3px solid {qa_color}; text-align: center;">
                        <b style="color: {qa_color};">QA: {item['qa_status'].upper()}</b>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button(f"🚚 Dispatch", key=f"disp_{item['id']}", use_container_width=True):
                        st.session_state.data["finished_goods"].remove(item)
                        update_data()
                        st.rerun()
                with col_b:
                    if st.button(f"🗑️ Delete", key=f"del_fin_{item['id']}", use_container_width=True):
                        st.session_state.data["finished_goods"].remove(item)
                        update_data()
                        st.rerun()
