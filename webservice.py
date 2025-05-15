import streamlit as st
import pandas as pd
import time

# --- Color Palette ---
COLOR_BG1 = "#222222"        # dark background
COLOR_BG2 = "#00BBCC"        # light background
COLOR_PRIMARY = "#1C5D99"   # deep blue
COLOR_ACCENT = "#22C1E3"    # light blue
COLOR_LIGHT = "#F1ECCE"     # cream
COLOR_SUCCESS = "#E7EFC5"   # light green
COLOR_WHITE = "#FFFFFF"     # pure white
COLOR_WARNING = "#FFD166"   # yellow/orange
COLOR_DANGER = "#EF476F"    # red/pink
COLOR_PURPLE = "#7C3AED"    # purple
COLOR_TEAL = "#2EC4B6"      # teal

# --- Dummy Admin Credentials ---
ADMIN_USER = "admin"
ADMIN_PASS = "password123"

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv('track degradation model  -  data/latest_sd_gmt_with_days.csv')
    # Replace with your actual column names if different
    def classify_maintenance(days):
        if days < 90:
            return 'NML'
        elif 90 <= days < 180:
            return 'PML'
        else:
            return 'UML'
    df['Type of maintenance'] = df['days_since_last_rundate'].apply(classify_maintenance)
    return df

# --- Custom CSS for Styling ---
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {COLOR_BG1};
        color: {COLOR_PRIMARY};
    }}
    .css-1d391kg, .css-1v0mbdj {{
        background-color: {COLOR_BG1} !important;
    }}
    ...
    </style>
""", unsafe_allow_html=True)

# --- Login Page ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown(
    f"""
    <style>
    .login-bg {{
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        z-index: -1;
        background: {COLOR_BG2};
    }}
    </style>
    <div class="login-bg"></div>
    """,
    unsafe_allow_html=True
    ) 
    

    st.title("TRACKWISE")
    st.markdown("#### Please log in to access the dashboard.")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            st.session_state.logged_in = True
            st.success("Login successful! Redirecting to dashboard...")
            # --- Loading Animation ---
            with st.spinner("Loading dashboard..."):
                # Custom train animation using st.markdown and HTML/CSS
                train_html = """
                <div style="width:100%;height:100px;position:relative;">
                  <div style="position:absolute;left:0;top:40px;width:100%;height:10px;background:#1C5D99;border-radius:5px;"></div>
                  <div id="train" style="position:absolute;left:0;top:10px;width:80px;height:40px;">
                    <div style="width:80px;height:30px;background:#22C1E3;border-radius:10px 10px 5px 5px;position:relative;">
                      <div style="width:20px;height:20px;background:#E7EFC5;position:absolute;left:10px;top:5px;border-radius:50%;"></div>
                      <div style="width:20px;height:20px;background:#E7EFC5;position:absolute;left:50px;top:5px;border-radius:50%;"></div>
                    </div>
                    <div style="width:80px;height:10px;background:#222222;position:absolute;top:30px;left:0;border-radius:0 0 5px 5px;"></div>
                  </div>
                </div>
                <script>
                let train = document.getElementById('train');
                let pos = 0;
                let interval = setInterval(function() {{
                  if (pos >= window.innerWidth - 100) {{
                    pos = 0;
                  }} else {{
                    pos += 10;
                  }}
                  train.style.left = pos + 'px';
                }}, 50);
                setTimeout(function() {{
                  clearInterval(interval);
                }}, 5000);
                </script>
                """
                st.markdown(train_html, unsafe_allow_html=True)
                time.sleep(5)
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")
    st.stop()

# --- Dashboard ---
st.title("Track Maintenance Dashboard")
st.markdown(
    f"""
    <style>
    .top-bar {{
        width: 100vw;
        height: 60px;
        background: linear-gradient(90deg, {COLOR_ACCENT} 0%, {COLOR_LIGHT} 100%);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 2em;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 100;
        box-shadow: 0 2px 8px 0 {COLOR_ACCENT}33;
    }}
    .trackwise-title {{
        color: {COLOR_PRIMARY};
        font-size: 2em;
        font-weight: 900;
        letter-spacing: 0.15em;
        font-family: 'Segoe UI', 'Arial', sans-serif;
    }}
    .user-btn {{
        background: {COLOR_PRIMARY};
        color: {COLOR_WHITE};
        border: none;
        border-radius: 20px;
        padding: 0.5em 1.2em;
        font-weight: bold;
        font-size: 1em;
        cursor: pointer;
        transition: 0.2s;
    }}
    .user-btn:hover {{
        background: {COLOR_DANGER};
        color: {COLOR_WHITE};
    }}
    </style>
    <div class="top-bar">
        <span class="trackwise-title">TRACKWISE</span>
        <button class="user-btn" onclick="window.location.href='#'">User Profile</button>
    </div>
    <div style="height:70px"></div> <!-- Spacer for fixed bar -->
    """,
    unsafe_allow_html=True
)
st.markdown(
    f"<h4 style='color:{COLOR_ACCENT};'>Welcome, Admin!</h4>",
    unsafe_allow_html=True
)

# 1. Load and process data
df = load_data()
df_display = df.rename(columns={
    'SECCODE': 'SECTION',
    'LINECODE': 'LINE',
    'days_since_last_rundate': 'Days Since Last Rundate'
})[['SECTION', 'LINE', 'Days Since Last Rundate', 'Type of maintenance']]

# 2. Define the highlight function
def highlight_maintenance(row):
    color = COLOR_SUCCESS if row['Type of maintenance'] == 'NML' else (COLOR_ACCENT if row['Type of maintenance'] == 'PML' else COLOR_PRIMARY)
    return [f'background-color: {color}; color: {COLOR_BG1};']*len(row)

# 3. Show styled sample
st.dataframe(
    df_display.head(500).style.apply(highlight_maintenance, axis=1),
    use_container_width=True,
    height=500
)
st.info("Showing only the first 500 rows for performance. Download full data below.")

# 4. Download button for full data
csv = df_display.to_csv(index=False).encode('utf-8')
st.download_button("Download Full Data as CSV", data=csv, file_name="maintenance_table.csv", mime="text/csv")
# --- Dynamic Effects: Add a little animation on table load ---
