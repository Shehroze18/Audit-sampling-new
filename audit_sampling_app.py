import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy import stats
import io
import base64
from datetime import datetime
import json
import hashlib

# Configure page
st.set_page_config(
    page_title="Modern Audit Sampling Software",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# User credentials (in production, these would be in a secure database)
USERS = {
    "admin": {
        "password": "admin123",
        "name": "System Administrator",
        "role": "Administrator"
    },
    "auditor": {
        "password": "audit2024",
        "name": "Senior Auditor",
        "role": "Senior Auditor"
    },
    "senior": {
        "password": "senior123",
        "name": "Senior Audit Manager",
        "role": "Audit Manager"
    },
    "demo": {
        "password": "demo123",
        "name": "Demo User",
        "role": "Auditor"
    }
}

# Add ONLY this minimal CSS to hide GitHub icon - keep everything else unchanged
st.markdown("""
<style>
    /* Hide only the GitHub icon and toolbar - minimal impact */
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* Alternative selector for GitHub icon */
    .stActionButton {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Professional CSS styling (your existing styles)
professional_css = """
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        letter-spacing: 0.5px;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    
    .login-container {
        max-width: 420px;
        margin: 0 auto;
        padding: 2.5rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid #e8e8e8;
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-title {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: 0.5px;
    }
    
    .login-subtitle {
        color: #666;
        font-size: 1rem;
        margin-bottom: 1rem;
        font-weight: 400;
    }
    
    .user-info {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.75rem 1.25rem;
        border-radius: 25px;
        font-size: 0.9rem;
        display: inline-block;
        margin-bottom: 1rem;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    
    .metric-card {
        background: white;
        padding: 1.75rem;
        border-radius: 8px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border-left: 4px solid #3498db;
        text-align: center;
        min-height: 130px;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 0.5rem 0;
        letter-spacing: -0.5px;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    .metric-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .risk-indicator {
        padding: 0.6rem 1.2rem;
        border-radius: 20px;
        color: white;
        font-weight: 600;
        text-align: center;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        letter-spacing: 0.3px;
    }
    
    .risk-low { 
        background: linear-gradient(90deg, #27ae60, #2ecc71);
        box-shadow: 0 2px 8px rgba(39, 174, 96, 0.3);
    }
    .risk-medium { 
        background: linear-gradient(90deg, #f39c12, #e67e22);
        color: white;
        box-shadow: 0 2px 8px rgba(243, 156, 18, 0.3);
    }
    .risk-high { 
        background: linear-gradient(90deg, #e74c3c, #c0392b);
        box-shadow: 0 2px 8px rgba(231, 76, 60, 0.3);
    }
    .risk-not-set { 
        background: linear-gradient(90deg, #95a5a6, #7f8c8d);
        box-shadow: 0 2px 8px rgba(149, 165, 166, 0.3);
    }
    
    .upload-zone {
        border: 2px dashed #3498db;
        border-radius: 12px;
        padding: 2.5rem;
        text-align: center;
        background: linear-gradient(90deg, #f8f9ff 0%, #e8f4fd 100%);
        transition: all 0.3s ease;
    }
    
    .upload-zone:hover {
        border-color: #2980b9;
        background: linear-gradient(90deg, #f0f8ff 0%, #e0f2fe 100%);
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.4rem 0.9rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .status-ready { 
        background-color: #d4edda; 
        color: #155724; 
        border: 1px solid #c3e6cb;
    }
    .status-pending { 
        background-color: #fff3cd; 
        color: #856404; 
        border: 1px solid #ffeaa7;
    }
    .status-error { 
        background-color: #f8d7da; 
        color: #721c24; 
        border: 1px solid #f5c6cb;
    }
    
    .credentials-info {
        background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        font-size: 0.95rem;
    }
    
    .workflow-step {
        padding: 0.5rem 0;
        border-radius: 6px;
        margin: 0.2rem 0;
        transition: background-color 0.2s ease;
    }
    
    .workflow-step:hover {
        background-color: rgba(52, 152, 219, 0.1);
    }
    
    .section-header {
        background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        border-left: 4px solid #3498db;
    }
    
    .section-header h2 {
        color: #2c3e50;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .section-header p {
        color: #666;
        margin: 0;
        font-size: 1.1rem;
    }
    
    .professional-button {
        background: linear-gradient(90deg, #3498db 0%, #2980b9 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(52, 152, 219, 0.3);
    }
    
    .professional-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.4);
    }
</style>
"""

# Apply both CSS styles
st.markdown(professional_css, unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'workflow_step' not in st.session_state:
    st.session_state.workflow_step = 0
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'sampling_config' not in st.session_state:
    st.session_state.sampling_config = {}
if 'selected_sample' not in st.session_state:
    st.session_state.selected_sample = None

def authenticate_user(username, password):
    """Authenticate user credentials"""
    if username in USERS and USERS[username]["password"] == password:
        return True, USERS[username]
    return False, None

def show_login():
    """Display professional login screen"""
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Professional title
        st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <h1 style="background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;
               background-clip: text; font-size: 2.8rem; font-weight: 700; margin-bottom: 0.5rem;
               letter-spacing: 0.5px;">
         Modern Audit Sampling
    </h1>
    <p style="color: #666; font-size: 1.3rem; margin-bottom: 0.5rem; font-weight: 500;">Professional Audit Sampling Software</p>
    <p style="color: #888; font-size: 1rem;">Please sign in to continue</p>
</div>
""", unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            st.markdown("### 🔐 Sign In")
            
            username = st.text_input(
                "👤 Username",
                placeholder="Enter your username",
                help="Enter your assigned username"
            )
            
            password = st.text_input(
                "🔒 Password",
                type="password",
                placeholder="Enter your password",
                help="Enter your assigned password"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                remember_me = st.checkbox("Remember me")
            with col2:
                login_button = st.form_submit_button("⚡ Sign In", use_container_width=True, type="primary")
            
            if login_button:
                if username and password:
                    is_valid, user_info = authenticate_user(username, password)
                    
                    if is_valid:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.user_info = user_info
                        st.success(f"✅ Welcome back, {user_info['name']}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password. Please try again.")
                else:
                    st.warning("⚠️ Please enter both username and password.")
        
        # Contact administrator info
        st.markdown("""
<div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
            border: 1px solid #dee2e6; border-radius: 12px; 
            padding: 1.5rem; margin: 1.5rem 0;">
    <h4 style="color: #495057; margin-bottom: 1rem; text-align: center;">
        🔐 Access Required
    </h4>
    <div style="text-align: center; color: #666; font-size: 0.95rem; line-height: 1.6;">
        <p style="margin-bottom: 1rem;">Contact your system administrator for login credentials</p>
        <div style="background: white; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <p style="margin: 0.5rem 0;"><strong>📧 Email:</strong> shehroze.pkf@gmail.com</p>
            <p style="margin: 0.5rem 0;"><strong>📞 Phone:</strong> +92 311-4518765</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

def show_user_info():
    """Display user info in sidebar"""
    if st.session_state.authenticated:
        user_info = st.session_state.user_info
        st.markdown(f"""
        <div class="user-info">
            👤 {user_info['name']} ({user_info['role']})
        </div>
        """, unsafe_allow_html=True)

def main():
    # Check authentication
    if not st.session_state.authenticated:
        show_login()
        return
    
    # Main title at the very top as header (removed welcome message)
    st.markdown(f"""
    <div class="main-header">
        <h1>⚖️ Modern Audit Sampling Software</h1>
        <p>Professional audit sampling - ISA 530 Compliant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        # User info at top
        show_user_info()
        st.markdown("---")
        
        st.title("📋 Workflow Navigation")
        
        workflow_steps = [
            "📊 Dashboard",
            "🗂️ Data Import", 
            "🔍 Data Review",
            "🎛️ Configuration",
            "📈 Sample Generation",
            "📋 Analysis & Evaluation",
            "📄 Reports & Export"
        ]
        
        selected_step = st.radio("Select Step:", workflow_steps, index=st.session_state.workflow_step)
        st.session_state.workflow_step = workflow_steps.index(selected_step)
        
        # Progress indicator
        progress = (st.session_state.workflow_step + 1) / len(workflow_steps)
        st.progress(progress)
        st.write(f"Progress: {int(progress * 100)}%")
        
        # Status indicators
        st.markdown("---")
        st.subheader("📊 Status Overview")
        
        # Data status
        if st.session_state.uploaded_data is not None:
            st.markdown('<span class="status-badge status-ready">✅ Data Loaded</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-badge status-pending">⚠️ No Data</span>', unsafe_allow_html=True)
        
        # Config status
        if st.session_state.sampling_config:
            st.markdown('<span class="status-badge status-ready">✅ Config Set</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-badge status-pending">⚠️ Config Pending</span>', unsafe_allow_html=True)
        
        # Sample status
        if st.session_state.selected_sample is not None:
            st.markdown('<span class="status-badge status-ready">✅ Sample Ready</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-badge status-pending">⚠️ No Sample</span>', unsafe_allow_html=True)
        
        # Logout button moved to the bottom
        st.markdown("---")
        if st.button("🔐 Logout", key="sidebar_logout_btn", use_container_width=True, type="secondary"):
            # Clear session state
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.user_info = {}
            st.session_state.workflow_step = 0
            st.rerun()
    
    # Main content based on selected step
    if st.session_state.workflow_step == 0:
        show_dashboard()
    elif st.session_state.workflow_step == 1:
        show_file_upload()
    elif st.session_state.workflow_step == 2:
        show_data_preview()
    elif st.session_state.workflow_step == 3:
        show_sampling_config()
    elif st.session_state.workflow_step == 4:
        show_sample_selection()
    elif st.session_state.workflow_step == 5:
        show_analysis_evaluation()
    elif st.session_state.workflow_step == 6:
        show_reports_export()

# [Rest of your functions remain exactly the same - show_dashboard(), show_file_upload(), etc.]
# I'm not including them here to keep the response concise, but they should remain unchanged

def show_dashboard():
    st.header("📊 Audit Sampling Dashboard")
    
    # Get current data for metrics
    population_count = len(st.session_state.uploaded_data) if st.session_state.uploaded_data is not None else 0
    sample_count = len(st.session_state.selected_sample) if st.session_state.selected_sample is not None else 0
    risk_level = st.session_state.sampling_config.get('overall_risk', 'Not Set')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📊 Data Status</div>
            <div class="metric-number">{population_count:,}</div>
            <div class="metric-label">Population Records</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📈 Sample Size</div>
            <div class="metric-number">{sample_count:,}</div>
            <div class="metric-label">Items Selected</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        risk_class = 'risk-low' if risk_level == 'Low' else 'risk-medium' if risk_level == 'Medium' else 'risk-high' if risk_level == 'High' else 'risk-not-set'
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🎯 Risk Level</div>
            <div class="risk-indicator {risk_class}">
                {risk_level}
            </div>
            <div class="metric-label">Overall Assessment</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        compliance_status = "✅ Compliant" if st.session_state.sampling_config else "⚠️ Pending"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📋 Compliance</div>
            <div class="metric-number" style="font-size: 1.5rem;">ISA 530</div>
            <div class="metric-label">{compliance_status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📤 Upload New Data", use_container_width=True, type="primary"):
            st.session_state.workflow_step = 1
            st.rerun()
    
    with col2:
        if st.button("🎛️ Configure Sampling", use_container_width=True):
            st.session_state.workflow_step = 3
            st.rerun()
    
    with col3:
        if st.button("📋 Generate Report", use_container_width=True):
            st.session_state.workflow_step = 6
            st.rerun()
    
    # Show data overview if available
    if st.session_state.uploaded_data is not None:
        st.subheader("📈 Population Overview")
        
        df = st.session_state.uploaded_data
        
        # Basic statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Records", f"{len(df):,}")
        with col2:
            st.metric("Columns", len(df.columns))
        with col3:
            numeric_cols = len(df.select_dtypes(include=[np.number]).columns)
            st.metric("Numeric Fields", numeric_cols)
        with col4:
            missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            st.metric("Data Quality", f"{100-missing_pct:.1f}%")
        
        # Create sample visualization if numeric data exists
        numeric_df = df.select_dtypes(include=[np.number])
        if not numeric_df.empty and len(numeric_df.columns) > 0:
            col_to_plot = numeric_df.columns[0]
            fig = px.histogram(df, x=col_to_plot, title=f"Distribution of {col_to_plot}")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    else:
        # Show getting started guide
        st.subheader("⚡ Getting Started")
        st.info("""
        **Welcome to Modern Audit Sampling Software!**
        
        To get started:
        1. 📤 **Upload your data** - Click 'Upload New Data' or go to Data Import
        2. 🎛️ **Configure sampling** - Set risk parameters and select method
        3. 📈 **Generate sample** - Create your audit sample
        4. 📋 **Analyze results** - Input findings and view projections
        5. 📄 **Export reports** - Generate professional audit documentation
        """)

# Add all your other functions here (show_file_upload, show_data_preview, etc.)
# They remain exactly the same as in your original code

if __name__ == "__main__":
    main()
