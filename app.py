import streamlit as st
import json
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Virtual Textile Warehouse", page_icon="🏭", layout="wide")

# --- CUSTOM CSS (GLASSMORPHISM & BRANDING REMOVAL) ---
custom_css = """
<style>
/* Hide Streamlit Branding completely */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.viewerBadge_container__1QSob {display: none !important;}
[data-testid="stToolbar"] {display: none !important;}

/* Global Background */
.stApp {
    background-color: #0E1117;
    color: #FAFAFA;
}

/* Glassmorphism Card Style */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 20px;
    margin-bottom: 15px;
    transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 10px 20px rgba(0, 212, 255, 0.2);
    background: rgba(255, 255, 255, 0.1);
}

/* Accent texts */
.accent-blue { color: #00D4FF; }
.accent-green { color: #00FF88; }
.accent-red { color: #FF3366; }

/* Pulsing Red Light for Low Stock */
.pulse-red {
    display: inline-block;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #FF3366;
    box-shadow: 0 0 0 0 rgba(255, 51, 102, 1);
    animation: pulse 1.5s infinite;
    margin-right: 8px;
}

@keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 51, 102, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(255, 51, 102, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 51, 102, 0); }
}

/* Metric styling */
.metric-box {
    text-align: center;
    padding: 20px;
}
.metric-title {
    font-size: 1.2rem;
    color: #AAAAAA;
}
.metric-value {
    font-size: 2.5rem;
    font-weight: bold;
    color: #00D4FF;
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- DATA MANAGEMENT ---
DATA_FILE = "warehouse.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Initialize Session State
if "inventory" not in st.session_state:
    st.session_state.inventory = load_data()
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"
if "edit_batch" not in st.session_state:
    st.session_state.edit_batch = None

def navigate(page):
    st.session_state.current_page = page
    st.session_state.edit_batch = None

# --- SIDEBAR (Sleek Navigation) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00D4FF;'>🏭 Textile ERP</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    if st.button("🏠 Dashboard", use_container_width=True, type="primary" if st.session_state.current_page == "Dashboard" else "secondary"):
        navigate("Dashboard")
        st.rerun()
    if st.button("📦 Inventory Grid", use_container_width=True, type="primary" if st.session_state.current_page == "Inventory Grid" else "secondary"):
        navigate("Inventory Grid")
        st.rerun()
    if st.button("➕ Add New Batch", use_container_width=True, type="primary" if st.session_state.current_page == "Add New Batch" else "secondary"):
        navigate("Add New Batch")
        st.rerun()
    if st.button("⚙️ Settings", use_container_width=True, type="primary" if st.session_state.current_page == "Settings" else "secondary"):
        navigate("Settings")
        st.rerun()

    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #555; font-size: 0.8rem;'>System v2.0 Enterprise</p>", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def get_low_stock_count():
    return sum(1 for details in st.session_state.inventory.values() if details.get("Quantity (Meters)", 0) < 500)

def get_total_meters():
    return sum(details.get("Quantity (Meters)", 0) for details in st.session_state.inventory.values())

# --- PAGE RENDERING ---

if st.session_state.current_page == "Dashboard":
    st.markdown("<h1 style='color: #FAFAFA;'>Dashboard Overview</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    total_items = len(st.session_state.inventory)
    low_stock = get_low_stock_count()
    total_meters = get_total_meters()
    
    with col1:
        st.markdown(f"""
        <div class="glass-card metric-box">
            <div class="metric-title">Total Batches</div>
            <div class="metric-value">{total_items}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="glass-card metric-box">
            <div class="metric-title">Low Stock Alerts</div>
            <div class="metric-value" style="color: #FF3366;">{low_stock}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="glass-card metric-box">
            <div class="metric-title">Total Meterage</div>
            <div class="metric-value" style="color: #00FF88;">{total_meters:,.1f} m</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.subheader("System Health")
    st.info("All systems operational. Data is currently persisted in secure JSON format.")

elif st.session_state.current_page == "Inventory Grid":
    st.markdown("<h1 style='color: #FAFAFA;'>Inventory Grid</h1>", unsafe_allow_html=True)
    
    if not st.session_state.inventory:
        st.info("No stock available. Please add some fabrics.")
    else:
        # Quick Edit Form Logic (if a batch is selected for editing)
        if st.session_state.edit_batch:
            batch = st.session_state.edit_batch
            details = st.session_state.inventory[batch]
            st.markdown(f"### ✏️ Quick Edit: {details['Fabric Name']} ({batch})")
            
            with st.form("quick_edit_form"):
                new_qty = st.number_input("Update Quantity (Meters)", min_value=0.0, value=float(details["Quantity (Meters)"]), step=50.0)
                col_save, col_cancel = st.columns([1, 1])
                with col_save:
                    save_btn = st.form_submit_button("Save Changes", type="primary")
                with col_cancel:
                    cancel_btn = st.form_submit_button("Cancel")
                
                if save_btn:
                    st.session_state.inventory[batch]["Quantity (Meters)"] = new_qty
                    save_data(st.session_state.inventory)
                    st.session_state.edit_batch = None
                    st.success("Successfully updated!")
                    st.rerun()
                if cancel_btn:
                    st.session_state.edit_batch = None
                    st.rerun()
            
            st.markdown("---")
            
        # Display Grid
        cols = st.columns(3)
        col_idx = 0
        
        for batch_id, details in st.session_state.inventory.items():
            fabric_name = details.get("Fabric Name", "N/A")
            color_name = details.get("Color", "N/A")
            hex_color = details.get("Hex", "#FFFFFF")
            qty = details.get("Quantity (Meters)", 0)
            
            status_html = ""
            if qty < 500:
                status_html = '<div class="pulse-red"></div> <span class="accent-red">Low Stock</span>'
            else:
                status_html = '<span class="accent-green">In Stock</span>'
            
            card_html = f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-size: 0.8rem; color: #888;">{batch_id}</span>
                    <div style="width: 20px; height: 20px; border-radius: 50%; background-color: {hex_color}; border: 1px solid #FFF;"></div>
                </div>
                <h3 style="margin: 0; color: #00D4FF;">{fabric_name}</h3>
                <p style="margin: 5px 0; color: #CCC;">Color: {color_name}</p>
                <h4 style="margin: 10px 0;">{qty} Meters</h4>
                <div style="font-size: 0.9rem; margin-top: 10px;">{status_html}</div>
            </div>
            """
            
            with cols[col_idx % 3]:
                st.markdown(card_html, unsafe_allow_html=True)
                if st.button("⚡ Quick Edit", key=f"edit_btn_{batch_id}", use_container_width=True):
                    st.session_state.edit_batch = batch_id
                    st.rerun()
            
            col_idx += 1

elif st.session_state.current_page == "Add New Batch":
    st.markdown("<h1 style='color: #FAFAFA;'>Add New Batch</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        with st.form("add_fabric_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                batch_id = st.text_input("Batch ID", placeholder="e.g., BATCH-101")
                fabric_type = st.selectbox("Fabric Type", ["Cotton", "Silk", "Linen", "Denim", "Polyester", "Wool", "Blend"])
            with col2:
                color_name = st.text_input("Color Name", placeholder="e.g., Midnight Blue")
                hex_color = st.color_picker("Pick Exact Color", "#00D4FF")
                
            quantity = st.number_input("Quantity (Meters)", min_value=0.0, value=1000.0, step=100.0)
            
            submitted = st.form_submit_button("➕ Add to Warehouse", use_container_width=True, type="primary")
            
            if submitted:
                if batch_id and color_name:
                    if batch_id in st.session_state.inventory:
                        st.error("Batch ID already exists. Use a unique ID.")
                    else:
                        st.session_state.inventory[batch_id] = {
                            "Fabric Name": fabric_type,
                            "Color": color_name,
                            "Hex": hex_color,
                            "Quantity (Meters)": quantity
                        }
                        save_data(st.session_state.inventory)
                        st.success(f"Successfully added {fabric_type} to the warehouse!")
                else:
                    st.error("Please fill in Batch ID and Color Name.")
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_page == "Settings":
    st.markdown("<h1 style='color: #FAFAFA;'>Settings & Data</h1>", unsafe_allow_html=True)
    
    st.markdown("### 💾 Backup Data")
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            json_data = f.read()
        st.download_button("Download JSON Backup", data=json_data, file_name="warehouse_backup.json", mime="application/json")
    else:
        st.info("No data available to backup yet.")
        
    st.markdown("---")
    
    st.markdown("### ⚠️ Danger Zone")
    st.markdown("Clear all inventory data. This action cannot be undone.")
    if st.button("🗑️ Clear All Data", type="primary"):
        st.session_state.inventory = {}
        save_data(st.session_state.inventory)
        st.success("All data has been cleared!")
        st.rerun()
