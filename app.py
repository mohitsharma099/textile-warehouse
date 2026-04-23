import streamlit as st
import json
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Textile Warehouse Manager", page_icon="🏭")

# --- DATA MANAGEMENT ---
DATA_FILE = "warehouse.json"

def load_data():
    """Load dictionary data from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_data(data):
    """Save dictionary data to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Initialize session state for memory
if "inventory" not in st.session_state:
    st.session_state.inventory = load_data()

def add_item(batch_id, fabric_name, color, quantity):
    st.session_state.inventory[batch_id] = {
        "Fabric Name": fabric_name,
        "Color": color,
        "Quantity (Meters)": quantity
    }
    save_data(st.session_state.inventory)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏭 Menu")
menu = ["View Stock", "Add New Fabric", "Search"]
choice = st.sidebar.radio("Go to:", menu)

st.title("Virtual Textile Warehouse Manager")
st.markdown("---")

# --- 1. VIEW STOCK ---
if choice == "View Stock":
    st.header("📦 Current Inventory")
    
    if not st.session_state.inventory:
        st.info("No stock available. Please add some fabrics.")
    else:
        for batch_id, details in st.session_state.inventory.items():
            fabric_name = details.get("Fabric Name", "N/A")
            color = details.get("Color", "N/A")
            qty = details.get("Quantity (Meters)", 0)
            
            with st.container():
                if qty < 500:
                    st.warning(f"⚠️ **LOW STOCK** | **{fabric_name}** (ID: {batch_id})")
                else:
                    st.success(f"✅ **IN STOCK** | **{fabric_name}** (ID: {batch_id})")
                
                st.write(f"**Color:** {color} | **Quantity:** {qty} meters")
                st.markdown("---")

# --- 2. ADD NEW FABRIC ---
elif choice == "Add New Fabric":
    st.header("➕ Add New Stock Entry")
    
    with st.form("add_fabric_form"):
        batch_id = st.text_input("Batch ID", placeholder="e.g., BATCH-101")
        fabric_name = st.text_input("Fabric Name", placeholder="e.g., Cotton Denim")
        color = st.text_input("Color", placeholder="e.g., Indigo")
        quantity = st.number_input("Quantity (Meters)", min_value=0.0, value=1000.0, step=100.0)
        
        submitted = st.form_submit_button("Add to Warehouse")
        
        if submitted:
            if batch_id and fabric_name and color:
                if batch_id in st.session_state.inventory:
                    st.error("Batch ID already exists. Use a unique ID.")
                else:
                    add_item(batch_id, fabric_name, color, quantity)
                    st.success(f"Successfully added {fabric_name} to the warehouse!")
            else:
                st.error("Please fill in all fields.")

# --- 3. SEARCH ---
elif choice == "Search":
    st.header("🔍 Search Inventory")
    
    if not st.session_state.inventory:
        st.info("No stock available to search.")
    else:
        search_term = st.text_input("Search by Fabric Name or Batch ID").lower()
        
        if search_term:
            found_items = False
            for batch_id, details in st.session_state.inventory.items():
                fabric_name = details.get("Fabric Name", "N/A")
                
                if search_term in fabric_name.lower() or search_term in batch_id.lower():
                    found_items = True
                    color = details.get("Color", "N/A")
                    qty = details.get("Quantity (Meters)", 0)
                    
                    with st.container():
                        if qty < 500:
                            st.warning(f"⚠️ **LOW STOCK** | **{fabric_name}** (ID: {batch_id})")
                        else:
                            st.success(f"✅ **IN STOCK** | **{fabric_name}** (ID: {batch_id})")
                        st.write(f"**Color:** {color} | **Quantity:** {qty} meters")
                        st.markdown("---")
            
            if not found_items:
                st.info(f"No results found for '{search_term}'.")