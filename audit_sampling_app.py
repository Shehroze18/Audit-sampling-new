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

# Professional CSS styling
st.markdown("""
<style>

    /* Hide GitHub icon and toolbar */
    [data-testid="stToolbar"] {
        display: none !important;
    }

    .stActionButton {
        display: none !important;
    }

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
""", unsafe_allow_html=True)

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

def show_file_upload():
    st.header("🗂️ Smart Data Import")
    
    # Professional upload interface
    st.markdown("""
    <div class="section-header">
        <h2>📤 Upload Your Audit Population Data</h2>
        <p>Start your audit sampling process by uploading your population data file</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File format information cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin: 1rem 0;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem; color: #3498db;">📊</div>
            <h4 style="color: #333; margin-bottom: 0.5rem;">Excel Files</h4>
            <p style="color: #666; font-size: 0.9rem;">.xlsx, .xls formats</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin: 1rem 0;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem; color: #3498db;">📄</div>
            <h4 style="color: #333; margin-bottom: 0.5rem;">CSV Files</h4>
            <p style="color: #666; font-size: 0.9rem;">Comma-separated values</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin: 1rem 0;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem; color: #3498db;">⚡</div>
            <h4 style="color: #333; margin-bottom: 0.5rem;">Fast Processing</h4>
            <p style="color: #666; font-size: 0.9rem;">Up to 200MB file size</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Best practices section
    st.info("""
    **💡 Best Practices for Data Upload:**
    
    • Ensure your data has clear column headers
    • Remove any merged cells or formatting  
    • Include unique identifiers for each record
    • Verify data completeness before upload
    """)
    
    # Enhanced file uploader
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 15px; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.1); border: 2px dashed #3498db; 
                text-align: center; margin: 2rem 0;">
        <div style="font-size: 3rem; color: #3498db; margin-bottom: 1rem;">📤</div>
        <h3 style="color: #3498db; margin-bottom: 0.5rem;">Drop your file here or click to browse</h3>
        <p style="color: #888; margin-bottom: 0;">Supported: Excel (.xlsx, .xls), CSV (.csv) • Max 200MB</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['xlsx', 'xls', 'csv'],
        help="Upload your population data for audit sampling"
    )
    
    if uploaded_file is not None:
        try:
            # Show upload progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text('📖 Reading file...')
            progress_bar.progress(25)
            
            # Read file based on type
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            progress_bar.progress(50)
            status_text.text('🔍 Validating data...')
            
            # Basic validation
            if len(df) == 0:
                st.error("❌ File is empty. Please upload a file with data.")
                return
            
            if len(df.columns) == 0:
                st.error("❌ No columns found in file.")
                return
            
            progress_bar.progress(75)
            status_text.text('✅ Processing complete!')
            progress_bar.progress(100)
            
            # Store in session state
            st.session_state.uploaded_data = df
            
            st.success(f"✅ Successfully uploaded {len(df):,} records with {len(df.columns)} columns!")
            
            # Show basic file info
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Records", f"{len(df):,}")
            with col2:
                st.metric("📋 Columns", len(df.columns))
            with col3:
                st.metric("💾 File Size", f"{uploaded_file.size / 1024:.1f} KB")
            with col4:
                file_type = "Excel" if uploaded_file.name.endswith(('.xlsx', '.xls')) else "CSV"
                st.metric("📄 Format", file_type)
            
            # Quick preview
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Column information
            st.subheader("📊 Column Information")
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes.astype(str),
                'Non-Null Count': df.count(),
                'Null Count': df.isnull().sum(),
                'Unique Values': df.nunique()
            })
            st.dataframe(col_info, use_container_width=True)
            
            # Auto-advance to next step
            if st.button("⚡ Continue to Data Review", type="primary", use_container_width=True):
                st.session_state.workflow_step = 2
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.info("💡 Please ensure your file is a valid Excel or CSV file with proper formatting.")

def show_data_preview():
    st.header("🔍 Data Review & Validation")
    
    if st.session_state.uploaded_data is None:
        st.warning("⚠️ No data uploaded. Please upload a file first.")
        if st.button("🗂️ Go to Data Import", type="primary"):
            st.session_state.workflow_step = 1
            st.rerun()
        return
    
    df = st.session_state.uploaded_data
    
    # Data quality indicators
    st.subheader("📊 Data Quality Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📈 Total Records", f"{len(df):,}")
    with col2:
        missing_values = df.isnull().sum().sum()
        st.metric("❓ Missing Values", f"{missing_values:,}")
    with col3:
        duplicates = df.duplicated().sum()
        st.metric("🔄 Duplicates", f"{duplicates:,}")
    with col4:
        numeric_cols = len(df.select_dtypes(include=[np.number]).columns)
        st.metric("🔢 Numeric Columns", numeric_cols)
    
    # Data quality visualization
    if missing_values > 0:
        st.subheader("🔍 Data Quality Analysis")
        
        # Missing values by column
        missing_by_col = df.isnull().sum()
        missing_by_col = missing_by_col[missing_by_col > 0].sort_values(ascending=False)
        
        if not missing_by_col.empty:
            fig = px.bar(x=missing_by_col.index, y=missing_by_col.values,
                        title="Missing Values by Column",
                        labels={'x': 'Column', 'y': 'Missing Count'})
            st.plotly_chart(fig, use_container_width=True)
    
    # Interactive data explorer
    st.subheader("🔍 Interactive Data Explorer")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        # Column filter
        columns_to_show = st.multiselect(
            "Select columns to display:",
            options=df.columns.tolist(),
            default=df.columns.tolist()[:5] if len(df.columns) > 5 else df.columns.tolist()
        )
    
    with col2:
        # Row count
        show_rows = st.slider("Number of rows to display:", 10, min(100, len(df)), 20)
    
    # Display filtered data
    if columns_to_show:
        display_df = df[columns_to_show].head(show_rows)
        st.dataframe(display_df, use_container_width=True)
    else:
        st.warning("Please select at least one column to display.")
    
    # Statistical summary for numeric columns
    numeric_df = df.select_dtypes(include=[np.number])
    if not numeric_df.empty:
        st.subheader("📈 Statistical Summary")
        st.dataframe(numeric_df.describe(), use_container_width=True)
        
        # Distribution analysis
        if len(numeric_df.columns) > 0:
            st.subheader("📊 Distribution Analysis")
            selected_col = st.selectbox("Select column for distribution analysis:", numeric_df.columns)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_hist = px.histogram(df, x=selected_col, title=f"Distribution of {selected_col}")
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                fig_box = px.box(df, y=selected_col, title=f"Box Plot of {selected_col}")
                st.plotly_chart(fig_box, use_container_width=True)
    
    # Continue button
    st.markdown("---")
    if st.button("⚡ Continue to Configuration", type="primary", use_container_width=True):
        st.session_state.workflow_step = 3
        st.rerun()

def show_sampling_config():
    st.header("🎛️ Interactive Sampling Configuration")
    
    if st.session_state.uploaded_data is None:
        st.warning("⚠️ No data uploaded. Please upload a file first.")
        if st.button("🗂️ Go to Data Import", type="primary"):
            st.session_state.workflow_step = 1
            st.rerun()
        return
    
    df = st.session_state.uploaded_data
    population_size = len(df)
    
    # Risk Assessment Section
    st.subheader("🎯 Risk Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Control Risk Assessment**")
        control_risk = st.slider("Control Risk", 0.1, 1.0, 0.5, 0.1,
                                help="Assessment of internal control effectiveness (0.1 = Strong, 1.0 = Weak)")
        
        st.write("**Detection Risk Assessment**") 
        detection_risk = st.slider("Detection Risk", 0.1, 1.0, 0.3, 0.1,
                                  help="Risk that audit procedures fail to detect material misstatement")
    
    with col2:
        st.write("**Materiality Settings**")
        materiality = st.number_input("Materiality Amount ($)", min_value=1000, value=50000, step=1000,
                                     help="The maximum amount of misstatement that would not influence users")
        
        confidence_level = st.selectbox("Confidence Level (%)", [90, 95, 99], index=1,
                                       help="Statistical confidence level for sampling")
        
        # Calculate overall risk
        overall_risk = control_risk * detection_risk
        risk_level = "Low" if overall_risk < 0.3 else "Medium" if overall_risk < 0.6 else "High"
        
        st.markdown(f"""
        **Overall Risk Assessment:**
        <div class="risk-indicator risk-{risk_level.lower()}">
            {risk_level} Risk ({overall_risk:.2f})
        </div>
        """, unsafe_allow_html=True)
    
    # Sampling Method Selection
    st.subheader("🎲 Sampling Method Selection")
    
    methods = {
        "Random Sampling": "Simple random selection from population - Best for homogeneous populations",
        "Systematic Sampling": "Every nth item selected systematically - Good for large populations", 
        "Stratified Sampling": "Population divided into strata, samples from each - Best for heterogeneous populations",
        "Monetary Unit Sampling": "Probability proportional to monetary value - Best for value-based audits"
    }
    
    selected_method = st.radio("Choose Sampling Method:", list(methods.keys()))
    st.info(f"ℹ️ {methods[selected_method]}")
    
    # Sample Size Calculation
    st.subheader("📊 Sample Size Calculator")
    
    # Calculate sample size based on confidence level and risk
    z_scores = {90: 1.645, 95: 1.96, 99: 2.576}
    z = z_scores[confidence_level]
    
    # Improved sample size calculation
    if population_size <= 50:
        base_sample_size = max(10, int(population_size * 0.3))
    elif population_size <= 100:
        base_sample_size = max(15, int(population_size * 0.25))
    elif population_size <= 500:
        base_sample_size = max(25, int(population_size * 0.15))
    else:
        # For larger populations, use statistical formula
        margin_error = 0.05
        p = 0.5  # Conservative estimate
        base_sample_size = int((z**2 * p * (1-p)) / (margin_error**2))
        
        # Adjust for finite population
        base_sample_size = int(base_sample_size / (1 + (base_sample_size - 1) / population_size))
    
    # Risk adjustment
    risk_multiplier = 1.5 if risk_level == "High" else 1.2 if risk_level == "Medium" else 1.0
    calculated_sample_size = int(base_sample_size * risk_multiplier)
    
    # Ensure sample size doesn't exceed population
    calculated_sample_size = min(calculated_sample_size, population_size)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Population Size", f"{population_size:,}")
    with col2:
        st.metric("🧮 Calculated Sample Size", f"{calculated_sample_size:,}")
    with col3:
        coverage = (calculated_sample_size / population_size) * 100
        st.metric("📈 Coverage", f"{coverage:.1f}%")
    
    # Allow manual override with proper constraints
    st.write("**Sample Size Override (Optional)**")
    manual_sample_size = st.number_input(
        "Custom Sample Size:", 
        min_value=1, 
        max_value=population_size,
        value=calculated_sample_size,
        help=f"Enter a value between 1 and {population_size:,}"
    )
    
    # Store configuration
    st.session_state.sampling_config = {
        'control_risk': control_risk,
        'detection_risk': detection_risk,
        'overall_risk': risk_level,
        'materiality': materiality,
        'confidence_level': confidence_level,
        'method': selected_method,
        'sample_size': manual_sample_size,
        'population_size': population_size
    }
    
    # Stratification setup (if selected)
    if selected_method == "Stratified Sampling":
        st.subheader("📋 Stratification Setup")
        
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if categorical_cols or numeric_cols:
            strata_column = st.selectbox("Select column for stratification:", 
                                       categorical_cols + numeric_cols)
            
            if strata_column:
                if strata_column in categorical_cols:
                    strata_counts = df[strata_column].value_counts()
                else:
                    # For numeric columns, create bins
                    df_temp = df.copy()
                    df_temp['strata_bins'] = pd.cut(df_temp[strata_column], bins=5, labels=['Low', 'Low-Med', 'Medium', 'Med-High', 'High'])
                    strata_counts = df_temp['strata_bins'].value_counts()
                
                st.write("**Strata Distribution:**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.pie(values=strata_counts.values, 
                                names=strata_counts.index,
                                title="Population Strata Distribution")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    strata_df = pd.DataFrame({
                        'Stratum': strata_counts.index,
                        'Count': strata_counts.values,
                        'Percentage': (strata_counts.values / len(df) * 100).round(1)
                    })
                    st.dataframe(strata_df, use_container_width=True)
                
                st.session_state.sampling_config['strata_column'] = strata_column
        else:
            st.warning("No suitable columns found for stratification. Consider using a different sampling method.")
    
    # Configuration summary
    st.subheader("📋 Configuration Summary")
    
    summary_data = {
        'Parameter': ['Population Size', 'Sample Size', 'Sampling Method', 'Confidence Level', 'Risk Level', 'Materiality'],
        'Value': [
            f"{population_size:,}",
            f"{manual_sample_size:,}",
            selected_method,
            f"{confidence_level}%",
            f"{risk_level} ({overall_risk:.2f})",
            f"${materiality:,}"
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    # Continue button
    st.markdown("---")
    if st.button("⚡ Generate Sample", type="primary", use_container_width=True):
        st.session_state.workflow_step = 4
        st.rerun()

def show_sample_selection():
    st.header("📈 Sample Generation & Selection")
    
    if st.session_state.uploaded_data is None or not st.session_state.sampling_config:
        st.warning("⚠️ Please complete data upload and configuration first.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗂️ Upload Data", type="primary"):
                st.session_state.workflow_step = 1
                st.rerun()
        with col2:
            if st.button("🎛️ Configure Sampling"):
                st.session_state.workflow_step = 3
                st.rerun()
        return
    
    df = st.session_state.uploaded_data
    config = st.session_state.sampling_config
    
    # Generate sample based on selected method
    method = config['method']
    sample_size = config['sample_size']
    
    st.subheader(f"🎲 Generating Sample using {method}")
    
    # Progress indicator
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("🔄 Generating sample...")
        progress_bar.progress(25)
        
        if method == "Random Sampling":
            sample_df = df.sample(n=sample_size, random_state=42)
            
        elif method == "Systematic Sampling":
            if sample_size >= len(df):
                sample_df = df.copy()
            else:
                interval = len(df) // sample_size
                start = np.random.randint(0, max(1, interval))
                indices = [start + i * interval for i in range(sample_size) if start + i * interval < len(df)]
                # If we don't have enough indices, fill with random selection
                if len(indices) < sample_size:
                    remaining = sample_size - len(indices)
                    available_indices = [i for i in range(len(df)) if i not in indices]
                    additional_indices = np.random.choice(available_indices, size=min(remaining, len(available_indices)), replace=False)
                    indices.extend(additional_indices)
                sample_df = df.iloc[indices[:sample_size]]
                
        elif method == "Stratified Sampling":
            if 'strata_column' in config:
                strata_col = config['strata_column']
                sample_dfs = []
                
                # Handle numeric columns by creating bins
                if df[strata_col].dtype in ['int64', 'float64']:
                    df_temp = df.copy()
                    df_temp['strata_bins'] = pd.cut(df_temp[strata_col], bins=5, labels=['Low', 'Low-Med', 'Medium', 'Med-High', 'High'])
                    strata_col = 'strata_bins'
                    df = df_temp
                
                for stratum in df[strata_col].unique():
                    if pd.isna(stratum):
                        continue
                    stratum_df = df[df[strata_col] == stratum]
                    stratum_size = max(1, int(sample_size * len(stratum_df) / len(df)))
                    stratum_sample = stratum_df.sample(n=min(stratum_size, len(stratum_df)), random_state=42)
                    sample_dfs.append(stratum_sample)
                
                if sample_dfs:
                    sample_df = pd.concat(sample_dfs, ignore_index=True)
                    # If we have too many samples, randomly reduce
                    if len(sample_df) > sample_size:
                        sample_df = sample_df.sample(n=sample_size, random_state=42)
                else:
                    sample_df = df.sample(n=sample_size, random_state=42)
            else:
                sample_df = df.sample(n=sample_size, random_state=42)
        
        else:  # Monetary Unit Sampling
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                value_col = st.selectbox("Select monetary value column:", numeric_cols)
                
                # Remove zero and negative values for MUS
                positive_df = df[df[value_col] > 0]
                if len(positive_df) == 0:
                    st.error("No positive values found in selected column. Using random sampling instead.")
                    sample_df = df.sample(n=sample_size, random_state=42)
                else:
                    # Probability proportional to size sampling
                    weights = positive_df[value_col] / positive_df[value_col].sum()
                    sample_indices = np.random.choice(
                        positive_df.index, 
                        size=min(sample_size, len(positive_df)), 
                        replace=False, 
                        p=weights
                    )
                    sample_df = df.loc[sample_indices]
            else:
                st.warning("No numeric columns found for Monetary Unit Sampling. Using random sampling instead.")
                sample_df = df.sample(n=sample_size, random_state=42)
        
        progress_bar.progress(75)
        status_text.text("✅ Sample generated successfully!")
        progress_bar.progress(100)
        
        # Store selected sample
        st.session_state.selected_sample = sample_df.reset_index(drop=True)
        
        # Display sample statistics
        st.subheader("📊 Sample Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📋 Sample Size", len(sample_df))
        with col2:
            coverage = (len(sample_df) / len(df)) * 100
            st.metric("📈 Population Coverage", f"{coverage:.1f}%")
        with col3:
            st.metric("🎲 Method Used", method.split()[0])
        with col4:
            if len(df.select_dtypes(include=[np.number]).columns) > 0:
                numeric_col = df.select_dtypes(include=[np.number]).columns[0]
                if numeric_col in sample_df.columns and numeric_col in df.columns:
                    value_coverage = (sample_df[numeric_col].sum() / df[numeric_col].sum()) * 100
                    st.metric("💰 Value Coverage", f"{value_coverage:.1f}%")
                else:
                    st.metric("💰 Value Coverage", "N/A")
            else:
                st.metric("💰 Value Coverage", "N/A")
        
        # Sample visualization
        st.subheader("📊 Sample Distribution Analysis")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            selected_col = st.selectbox("Select column for analysis:", numeric_cols)
            
            if selected_col in sample_df.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig1 = go.Figure()
                    fig1.add_trace(go.Histogram(x=df[selected_col], name="Population", opacity=0.7, nbinsx=20))
                    fig1.add_trace(go.Histogram(x=sample_df[selected_col], name="Sample", opacity=0.7, nbinsx=20))
                    fig1.update_layout(title="Population vs Sample Distribution", barmode='overlay')
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    fig2 = go.Figure()
                    fig2.add_trace(go.Box(y=df[selected_col], name="Population"))
                    fig2.add_trace(go.Box(y=sample_df[selected_col], name="Sample"))
                    fig2.update_layout(title="Box Plot Comparison")
                    st.plotly_chart(fig2, use_container_width=True)
        
        # Interactive sample review
        st.subheader("🔍 Sample Review & Validation")
        
        # Sample preview with selection capability
        st.write("**Sample Items Preview:**")
        
        # Add row numbers for easy identification
        display_sample = sample_df.copy()
        display_sample.insert(0, 'Sample_ID', range(1, len(display_sample) + 1))
        
        # Show sample with editing capability
        edited_sample = st.data_editor(
            display_sample.head(20),  # Show first 20 rows for performance
            use_container_width=True,
            num_rows="fixed",
            disabled=['Sample_ID'],  # Don't allow editing the ID column
            key="sample_editor"
        )
        
        if len(display_sample) > 20:
            st.info(f"Showing first 20 of {len(display_sample)} sample items. Full sample will be used for analysis.")
        
        # Sample quality indicators
        st.subheader("✅ Sample Quality Validation")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Representativeness check
            if len(numeric_cols) > 0:
                pop_mean = df[numeric_cols[0]].mean()
                sample_mean = sample_df[numeric_cols[0]].mean()
                diff_pct = abs(sample_mean - pop_mean) / pop_mean * 100
                
                if diff_pct < 10:
                    st.success(f"✅ Representative Sample\n(Mean difference: {diff_pct:.1f}%)")
                else:
                    st.warning(f"⚠️ Check Representativeness\n(Mean difference: {diff_pct:.1f}%)")
            else:
                st.info("ℹ️ No numeric data for representativeness check")
        
        with col2:
            # Coverage adequacy
            if coverage >= 5:
                st.success(f"✅ Adequate Coverage\n({coverage:.1f}% of population)")
            else:
                st.warning(f"⚠️ Low Coverage\n({coverage:.1f}% of population)")
        
        with col3:
            # Sample size adequacy
            min_recommended = max(30, int(len(df) * 0.05))
            if len(sample_df) >= min_recommended:
                st.success(f"✅ Adequate Sample Size\n({len(sample_df)} items)")
            else:
                st.warning(f"⚠️ Consider Larger Sample\n(Recommended: {min_recommended}+)")
        
        st.success(f"✅ Sample successfully generated with {len(sample_df)} items using {method}")
        
        # Continue button
        st.markdown("---")
        if st.button("⚡ Continue to Analysis", type="primary", use_container_width=True):
            st.session_state.workflow_step = 5
            st.rerun()
            
    except Exception as e:
        progress_bar.progress(0)
        status_text.text("")
        st.error(f"❌ Error generating sample: {str(e)}")
        st.info("💡 Try adjusting your sample size or selecting a different sampling method.")

def show_analysis_evaluation():
    st.header("📋 Analysis & Evaluation")
    
    if st.session_state.selected_sample is None:
        st.warning("⚠️ No sample selected. Please complete sample selection first.")
        if st.button("📈 Go to Sample Generation", type="primary"):
            st.session_state.workflow_step = 4
            st.rerun()
        return
    
    sample_df = st.session_state.selected_sample
    config = st.session_state.sampling_config
    
    st.subheader("🔍 Audit Testing Interface")
    
    # Initialize findings if not exists
    if 'audit_findings' not in st.session_state:
        st.session_state.audit_findings = {
            'errors_found': 0,
            'total_error_amount': 0.0,
            'error_details': []
        }
    
    # Simple analysis interface
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Audit Test Results**")
        errors_found = st.number_input(
            "Number of Errors Found:", 
            min_value=0, 
            max_value=len(sample_df), 
            value=st.session_state.audit_findings['errors_found'],
            help="Total number of errors identified in the sample"
        )
        
        total_error_amount = st.number_input(
            "Total Error Amount ($):", 
            min_value=0.0, 
            value=st.session_state.audit_findings['total_error_amount'], 
            step=100.0,
            help="Sum of all monetary errors found"
        )
        
        # Store findings
        st.session_state.audit_findings['errors_found'] = errors_found
        st.session_state.audit_findings['total_error_amount'] = total_error_amount
    
    with col2:
        st.write("**Sample Statistics**")
        error_rate = errors_found / len(sample_df) if len(sample_df) > 0 else 0
        st.metric("📊 Error Rate", f"{error_rate:.1%}")
        
        avg_error = total_error_amount / errors_found if errors_found > 0 else 0
        st.metric("💰 Average Error", f"${avg_error:,.2f}")
        
        sample_size = len(sample_df)
        st.metric("🎯 Sample Size", f"{sample_size:,}")
    
    # Statistical Projection
    st.subheader("📈 Statistical Projection to Population")
    
    if st.session_state.uploaded_data is not None:
        population_size = len(st.session_state.uploaded_data)
        sample_size = len(sample_df)
        
        # Point estimate
        projected_error = (total_error_amount / sample_size) * population_size if sample_size > 0 else 0
        projected_error_rate = error_rate * 100
        
        # Confidence interval calculation
        confidence_level = config.get('confidence_level', 95)
        z_scores = {90: 1.645, 95: 1.96, 99: 2.576}
        z = z_scores[confidence_level]
        
        # Standard error calculation (simplified)
        if sample_size > 1 and errors_found > 0:
            # For error amounts
            sample_errors = [total_error_amount / errors_found] * errors_found + [0] * (sample_size - errors_found)
            sample_std = np.std(sample_errors)
            standard_error = sample_std * np.sqrt((population_size - sample_size) / (population_size - 1)) / np.sqrt(sample_size)
            margin_error = z * standard_error * population_size / sample_size
            
            lower_bound = max(0, projected_error - margin_error)
            upper_bound = projected_error + margin_error
        else:
            lower_bound = upper_bound = projected_error
        
        # Display projection results
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🎯 Point Estimate", f"${projected_error:,.2f}")
        with col2:
            st.metric("📉 Lower Bound", f"${lower_bound:,.2f}")
        with col3:
            st.metric("📈 Upper Bound", f"${upper_bound:,.2f}")
        with col4:
            st.metric("📊 Projected Error Rate", f"{projected_error_rate:.2f}%")
        
        # Confidence interval visualization
        if errors_found > 0:
            st.subheader("📊 Confidence Interval Visualization")
            
            fig = go.Figure()
            
            # Add confidence interval
            fig.add_trace(go.Scatter(
                x=['Lower Bound', 'Point Estimate', 'Upper Bound'],
                y=[lower_bound, projected_error, upper_bound],
                mode='markers+lines',
                name=f'{confidence_level}% Confidence Interval',
                line=dict(color='blue', width=3),
                marker=dict(size=10)
            ))
            
            # Add materiality line
            materiality = config.get('materiality', 50000)
            fig.add_hline(y=materiality, line_dash="dash", line_color="red", 
                         annotation_text=f"Materiality Threshold: ${materiality:,}")
            
            fig.update_layout(
                title="Population Error Projection with Confidence Interval",
                yaxis_title="Error Amount ($)",
                xaxis_title="Estimate Type",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Materiality assessment
        st.subheader("⚖️ Materiality Assessment")
        
        materiality = config.get('materiality', 50000)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("💼 Materiality Threshold", f"${materiality:,}")
            st.metric("🔍 Upper Bound vs Materiality", f"{(upper_bound/materiality)*100:.1f}%")
        
        with col2:
            if upper_bound > materiality:
                st.error("🚨 **MATERIAL MISSTATEMENT DETECTED**")
                st.write(f"Upper bound (${upper_bound:,.2f}) exceeds materiality threshold (${materiality:,.2f})")
                st.write("**Recommended Actions:**")
                st.write("• Extend audit procedures")
                st.write("• Increase sample size")
                st.write("• Request management adjustments")
                
            elif projected_error > materiality * 0.75:
                st.warning("⚠️ **POTENTIAL MATERIAL MISSTATEMENT**")
                st.write(f"Projected error (${projected_error:,.2f}) is close to materiality threshold")
                st.write("**Consider:**")
                st.write("• Additional testing")
                st.write("• Review risk assessment")
                
            else:
                st.success("✅ **NO MATERIAL MISSTATEMENT**")
                st.write("Projected error is below materiality threshold")
                st.write("**Conclusion:**")
                st.write("• Sample results are acceptable")
                st.write("• No additional procedures required based on current results")
        
        # Risk assessment update
        st.subheader("🎯 Updated Risk Assessment")
        
        # Calculate actual vs expected error rate
        expected_error_rate = 0.02  # 2% baseline expectation
        
        if error_rate > expected_error_rate * 2:
            updated_risk = "High"
            risk_color = "🔴"
        elif error_rate > expected_error_rate:
            updated_risk = "Medium"
            risk_color = "🟡"
        else:
            updated_risk = "Low"
            risk_color = "🟢"
        
        st.info(f"""
        **Risk Level Update:** {risk_color} {updated_risk}
        
        • **Sample Error Rate:** {error_rate:.1%}
        • **Expected Rate:** {expected_error_rate:.1%}
        • **Population Projection:** ${projected_error:,.2f}
        • **Confidence Level:** {confidence_level}%
        """)
    
    # Detailed findings (optional)
    with st.expander("📝 Detailed Error Analysis (Optional)"):
        st.write("Record specific errors found during testing:")
        
        if 'error_details' not in st.session_state.audit_findings:
            st.session_state.audit_findings['error_details'] = []
        
        # Simple error entry
        col1, col2, col3 = st.columns(3)
        
        with col1:
            error_type = st.selectbox("Error Type:", 
                                    ["Overstatement", "Understatement", "Misclassification", "Other"])
        with col2:
            error_amount = st.number_input("Error Amount ($):", min_value=0.0, step=10.0)
        with col3:
            if st.button("⚡ Add Error"):
                st.session_state.audit_findings['error_details'].append({
                    'type': error_type,
                    'amount': error_amount,
                    'timestamp': datetime.now()
                })
                st.success("Error added!")
        
        # Display recorded errors
        if st.session_state.audit_findings['error_details']:
            error_df = pd.DataFrame(st.session_state.audit_findings['error_details'])
            st.dataframe(error_df, use_container_width=True)
    
    # Continue button
    st.markdown("---")
    if st.button("⚡ Generate Reports", type="primary", use_container_width=True):
        st.session_state.workflow_step = 6
        st.rerun()

def show_reports_export():
    st.header("📄 Professional Reports & Export")
    
    if st.session_state.selected_sample is None:
        st.warning("⚠️ No sample data available for reporting.")
        if st.button("📈 Go to Sample Generation", type="primary"):
            st.session_state.workflow_step = 4
            st.rerun()
        return
    
    # Report configuration
    st.subheader("📋 Report Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_title = st.text_input("Report Title", "Audit Sampling Report")
        auditor_name = st.text_input("Auditor Name", st.session_state.user_info.get('name', 'Senior Auditor'))
        client_name = st.text_input("Client Name", "ABC Company Ltd.")
    
    with col2:
        report_date = st.date_input("Report Date", datetime.now())
        period_end = st.date_input("Period End Date", datetime.now())
        engagement_partner = st.text_input("Engagement Partner", "Partner Name")
    
    # Report sections selection
    st.subheader("📑 Report Sections")
    
    col1, col2 = st.columns(2)
    
    with col1:
        include_summary = st.checkbox("Executive Summary", True)
        include_methodology = st.checkbox("Sampling Methodology", True)
        include_results = st.checkbox("Detailed Results", True)
    
    with col2:
        include_conclusions = st.checkbox("Conclusions & Recommendations", True)
        include_appendices = st.checkbox("Technical Appendices", True)
        include_compliance = st.checkbox("ISA 530 Compliance Checklist", True)
    
    # Generate comprehensive report
    if st.button("📖 Generate Full Report Preview", type="primary"):
        
        # Get data for report
        sample_df = st.session_state.selected_sample
        config = st.session_state.sampling_config
        findings = st.session_state.audit_findings if 'audit_findings' in st.session_state else {'errors_found': 0, 'total_error_amount': 0}
        
        population_size = len(st.session_state.uploaded_data)
        sample_size = len(sample_df)
        error_rate = findings['errors_found'] / sample_size if sample_size > 0 else 0
        projected_error = (findings['total_error_amount'] / sample_size) * population_size if sample_size > 0 else 0
        materiality = config.get('materiality', 50000)
        
        report_content = f"""
# {report_title}

---

**Prepared by:** {auditor_name} ({st.session_state.user_info.get('role', 'Auditor')})  
**Engagement Partner:** {engagement_partner}  
**Client:** {client_name}  
**Report Date:** {report_date.strftime('%B %d, %Y')}  
**Period End:** {period_end.strftime('%B %d, %Y')}  

---

## Executive Summary

This report presents the results of audit sampling procedures performed in accordance with International Standard on Auditing (ISA) 530 "Audit Sampling". The sampling was conducted to obtain sufficient appropriate audit evidence regarding the population under examination.

### Key Findings Summary

| Metric | Value |
|--------|-------|
| **Population Size** | {population_size:,} items |
| **Sample Size** | {sample_size:,} items |
| **Sample Coverage** | {(sample_size/population_size)*100:.1f}% |
| **Errors Identified** | {findings['errors_found']} |
| **Error Rate** | {error_rate:.2%} |
| **Projected Error** | ${projected_error:,.2f} |
| **Materiality Threshold** | ${materiality:,} |

### Overall Conclusion

{"🚨 **MATERIAL MISSTATEMENT IDENTIFIED** - Projected error exceeds materiality threshold." if projected_error > materiality else "✅ **NO MATERIAL MISSTATEMENT** - Sample results are within acceptable limits."}

---

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Software:** Modern Audit Sampling Software v1.0  
**Compliance:** ISA 530 Certified  
**Generated by:** {st.session_state.user_info.get('name', 'User')} ({st.session_state.user_info.get('role', 'Auditor')})

---

*This report contains confidential information and is intended solely for the use of [Client Name] and their authorized representatives.*
        """
        
        st.markdown(report_content)
    
    # Export options
    st.subheader("💾 Export & Download Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**📊 Data Exports**")
        
        if st.button("📋 Export Sample Data", use_container_width=True):
            # Create Excel download
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                # Sample data
                sample_export = st.session_state.selected_sample.copy()
                sample_export.insert(0, 'Sample_ID', range(1, len(sample_export) + 1))
                sample_export.to_excel(writer, sheet_name='Sample_Data', index=False)
                
                # Configuration
                config_data = []
                for key, value in st.session_state.sampling_config.items():
                    config_data.append({'Parameter': key, 'Value': str(value)})
                config_df = pd.DataFrame(config_data)
                config_df.to_excel(writer, sheet_name='Configuration', index=False)
                
                # Summary statistics
                summary_data = {
                    'Metric': ['Population Size', 'Sample Size', 'Coverage %', 'Method', 'Confidence Level', 'Generated By'],
                    'Value': [
                        len(st.session_state.uploaded_data),
                        len(st.session_state.selected_sample),
                        f"{(len(st.session_state.selected_sample)/len(st.session_state.uploaded_data))*100:.1f}%",
                        st.session_state.sampling_config.get('method', 'N/A'),
                        f"{st.session_state.sampling_config.get('confidence_level', 95)}%",
                        f"{st.session_state.user_info.get('name', 'User')} ({st.session_state.user_info.get('role', 'Auditor')})"
                    ]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            st.download_button(
                label="📥 Download Excel Workbook",
                data=output.getvalue(),
                file_name=f"audit_sampling_data_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col2:
        st.write("**📄 Report Formats**")
        
        if st.button("📝 Export Report (Text)", use_container_width=True):
            # Generate simplified report for download
            simple_report = f"""
AUDIT SAMPLING REPORT
{report_title}

Client: {client_name}
Auditor: {auditor_name} ({st.session_state.user_info.get('role', 'Auditor')})
Date: {report_date}

SUMMARY:
Population: {len(st.session_state.uploaded_data):,} items
Sample: {len(st.session_state.selected_sample):,} items
Method: {st.session_state.sampling_config.get('method', 'N/A')}
Confidence: {st.session_state.sampling_config.get('confidence_level', 95)}%

Generated by Modern Audit Sampling Software
User: {st.session_state.user_info.get('name', 'User')}
            """
            
            st.download_button(
                label="📥 Download Text Report",
                data=simple_report,
                file_name=f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )
    
    with col3:
        st.write("**🔧 Working Papers**")
        
        if st.button("📊 Export Working Papers", use_container_width=True):
            # Create comprehensive working paper
            csv_data = st.session_state.selected_sample.to_csv(index=False)
            
            st.download_button(
                label="📥 Download CSV Data",
                data=csv_data,
                file_name=f"sample_working_paper_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
    
    # ISA 530 Compliance checklist
    st.subheader("✅ ISA 530 Compliance Checklist")
    
    compliance_items = [
        ("Risk assessment performed and documented", True),
        ("Appropriate sampling method selected based on audit objectives", True),
        ("Sample size adequately determined considering risk and materiality", True),
        ("Sample selection performed using appropriate technique", True),
        ("Audit procedures applied consistently to sample items", True),
        ("Sample results evaluated and projected to population", True),
        ("Conclusions documented and supported by evidence", True),
        ("Results considered in forming overall audit opinion", True)
    ]
    
    col1, col2 = st.columns(2)
    
    for i, (item, status) in enumerate(compliance_items):
        with col1 if i % 2 == 0 else col2:
            if status:
                st.success(f"✅ {item}")
            else:
                st.warning(f"⚠️ {item}")
    
    # Final summary
    st.markdown("---")
    st.success("🎉 **Audit Sampling Process Complete!**")
    st.info(f"""
    **Next Steps:**
    1. Review and validate all results
    2. Include findings in audit documentation
    3. Consider results in overall audit opinion
    4. Archive working papers and reports
    
    **Session Info:**
    - Completed by: {st.session_state.user_info.get('name', 'User')} ({st.session_state.user_info.get('role', 'Auditor')})
    - Session started: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    """)
    
    # Reset workflow option
    if st.button("🔄 Start New Sampling Project", type="secondary"):
        # Clear workflow data but keep user logged in
        st.session_state.workflow_step = 0
        st.session_state.uploaded_data = None
        st.session_state.sampling_config = {}
        st.session_state.selected_sample = None
        if 'audit_findings' in st.session_state:
            del st.session_state.audit_findings
        st.rerun()

if __name__ == "__main__":
    main()
