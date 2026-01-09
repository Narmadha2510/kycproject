import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. CONFIGURATION ---
API_KEY = "AIzaSyBsoaTDy0_zkPSrBMMMdmsEfDZ3idEgiyI" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="KYC Verification Portal", page_icon="🏦", layout="wide")

# --- 2. LANGUAGE DICTIONARY ---
lang_data = {
    "English": {
        "nav_kyc": "📄 KYC Verification",
        "nav_dash": "📊 Dashboard",
        "nav_settings": "⚙️ Settings",
        "nav_help": "❓ Help Center",
        "header": "KYC Verification Portal",
        "welcome": "Welcome back,",
        "acc_no_label": "Account Number",
        "balance": "Total Balance",
        "kyc_status": "KYC Status",
        "active_loans": "Active Loans",
        "recent_trans": "Recent Transactions",
        "upload_title": "Identity Verification Documents",
        "upload_aadhaar": "Upload Aadhaar Card",
        "upload_pan": "Upload PAN Card",
        "upload_selfie": "Upload Live Selfie",
        "submit_btn": "Submit Documents",
        "logout": "Logout",
        "support_text": "Need assistance? Contact our 24/7 Priority Desk.",
        "lang_select": "Select Language",
        "phone_label": "Mobile Number",
        "otp_label": "Enter 6-Digit OTP",
        "send_otp": "Send OTP",
        "login_btn": "Verify & Login",
        "pending_msg": "Under Review: We are verifying your documents.",
        "approved_msg": "Verification Complete: Your account is fully secured."
    },
    "Tamil": {
        "nav_kyc": "📄 KYC சரிபார்ப்பு",
        "nav_dash": "📊 டாஷ்போர்டு",
        "nav_settings": "⚙️ அமைப்புகள்",
        "nav_help": "❓ உதவி மையம்",
        "header": "KYC சரிபார்ப்பு போர்டல்",
        "welcome": "மீண்டும் வருக,",
        "acc_no_label": "கணக்கு எண்",
        "balance": "மொத்த இருப்பு",
        "kyc_status": "KYC நிலை",
        "active_loans": "செயலில் உள்ள கடன்கள்",
        "recent_trans": "சமீபத்திய பரிவர்த்தனைகள்",
        "upload_title": "அடையாள சரிபார்ப்பு ஆவணங்கள்",
        "upload_aadhaar": "ஆதார் கார்டைப் பதிவேற்றவும்",
        "upload_pan": "பான் கார்டைப் பதிவேற்றவும்",
        "upload_selfie": "நேரடி செல்பியைப் பதிவேற்றவும்",
        "submit_btn": "ஆவணங்களைச் சமர்ப்பிக்கவும்",
        "logout": "வெளியேறு",
        "support_text": "உதவி தேவையா? எங்களின் 24/7 முன்னுரிமை மையத்தைத் தொடர்பு கொள்ளவும்.",
        "lang_select": "மொழியைத் தேர்ந்தெடுக்கவும்",
        "phone_label": "கைபேசி எண்",
        "otp_label": "6-இலக்க OTP-ஐ உள்ளிடவும்",
        "send_otp": "OTP அனுப்பவும்",
        "login_btn": "சரிபார்த்து உள்நுழையவும்",
        "pending_msg": "பரிசீலனையில் உள்ளது: உங்கள் ஆவணங்களைச் சரிபார்க்கிறோம்.",
        "approved_msg": "சரிபார்ப்பு முடிந்தது: உங்கள் கணக்கு பாதுகாக்கப்பட்டது."
    }
}

# --- 3. CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #F0F2F6; color: #1A365D; }
    
    /* SIDEBAR: Navy Blue Background */
    [data-testid="stSidebar"] { 
        background-color: #002147 !important; 
        border-right: 3px solid #C5A059; 
    }

    /* SIDEBAR MENU ITEMS: FORCE WHITE */
    [data-testid="stSidebar"] div[role="radiogroup"] label p {
        color: white !important;
        font-size: 1.1rem;
        font-weight: 500;
    }

    /* ALL OTHER SIDEBAR TEXT: WHITE */
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: white !important;
    }

    /* THE LANGUAGE BOX: WHITE BACKGROUND WITH BLACK TEXT */
    [data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: white !important;
        border: 2px solid #C5A059 !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: black !important;
        -webkit-text-fill-color: black !important;
    }

    /* Top Banner Header */
    .bank-header {
        background: linear-gradient(135deg, #002147 0%, #004a99 100%);
        padding: 20px;
        border-radius: 15px;
        color: white !important;
        text-align: center;
        margin-bottom: 25px;
        border-bottom: 5px solid #C5A059;
    }
    .bank-header h1 { color: white !important; margin: 0; }

    /* Input Box Visibility (Main Page & Login) */
    div[data-baseweb="input"] {
        background-color: white !important;
        border: 1px solid #1A365D !important;
    }
    input { color: black !important; }

    /* Action Buttons */
    .stButton>button {
        background-color: #002147;
        color: #C5A059 !important;
        border: 2px solid #C5A059;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SESSION STATE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "kyc_status" not in st.session_state: st.session_state.kyc_status = "Not Submitted"
if "language" not in st.session_state: st.session_state.language = "English"
if "otp_sent" not in st.session_state: st.session_state.otp_sent = False
if "user_acc" not in st.session_state: st.session_state.user_acc = ""

T = lang_data[st.session_state.language]

# --- 5. LOGIN PAGE (ACC NO, PHONE & OTP) ---
if not st.session_state.logged_in:
    _, col2, _ = st.columns([1,2,1])
    with col2:
        st.markdown(f'<div class="bank-header"><h1>🏦 KYC Verification</h1></div>', unsafe_allow_html=True)
        st.subheader("Customer Authentication")
        
        # New Account Number Field
        acc_input = st.text_input(T["acc_no_label"], placeholder="Enter Your Bank Account Number")
        phone_input = st.text_input(T["phone_label"], placeholder="+91 XXXXX XXXXX")
        
        if st.button(T["send_otp"]):
            if len(acc_input) > 5 and len(phone_input) >= 10:
                st.session_state.user_acc = acc_input # Save account number
                st.session_state.otp_sent = True
                st.success("OTP sent! (Use 123456 to login)")
            else:
                st.error("Please enter a valid Account Number and Mobile Number.")
        
        if st.session_state.otp_sent:
            otp = st.text_input(T["otp_label"], type="password")
            if st.button(T["login_btn"]):
                if otp == "123456":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid OTP. Please check the code.")

# --- 6. MAIN APP (AFTER LOGIN) ---
else:
    # --- SIDEBAR NAVIGATION ---
    with st.sidebar:
        st.markdown(f"### 🌐 {T['lang_select']}")
        st.session_state.language = st.selectbox("Lang", ["English", "Tamil"], label_visibility="collapsed")
        
        st.divider()
        
        # Swapped Order: KYC Verification first
        menu = st.radio("Navigation", [
            T["nav_kyc"], 
            T["nav_dash"], 
            T["nav_settings"], 
            T["nav_help"]
        ])
        
        st.divider()
        if st.button(T["logout"]):
            st.session_state.logged_in = False
            st.session_state.otp_sent = False
            st.rerun()

    # --- TOP HEADER ---
    st.markdown(f'<div class="bank-header"><h1>{T["header"]}</h1></div>', unsafe_allow_html=True)

    # --- FEATURE 1: KYC VERIFICATION (Default Page) ---
    if menu == T["nav_kyc"]:
        st.subheader(T["upload_title"])
        st.info(f"📍 **{T['acc_no_label']}:** {st.session_state.user_acc}")
        
        if st.session_state.kyc_status == "Approved":
            st.success(T["approved_msg"])
        elif st.session_state.kyc_status == "Pending":
            st.info(T["pending_msg"])
        else:
            st.warning("Action Required: Please upload official documents to verify your identity.")
            st.file_uploader(T["upload_aadhaar"], type=['png','jpg','pdf'])
            st.file_uploader(T["upload_pan"], type=['png','jpg','pdf'])
            st.file_uploader(T["upload_selfie"], type=['png','jpg'])
            
            if st.button(T["submit_btn"]):
                with st.spinner("Processing Documents..."):
                    time.sleep(2)
                    st.session_state.kyc_status = "Pending"
                    st.rerun()

    # --- FEATURE 2: DASHBOARD (Rupees ₹) ---
    elif menu == T["nav_dash"]:
        st.subheader(f"{T['welcome']} Keerthikumar")
        st.write(f"💳 **{T['acc_no_label']}:** `{st.session_state.user_acc}`")
        
        c1, c2, c3 = st.columns(3)
        c1.metric(T["balance"], "₹1,42,200.50")
        c2.metric(T["kyc_status"], st.session_state.kyc_status)
        c3.metric(T["active_loans"], "0")
        
        st.markdown(f"### {T['recent_trans']}")
        st.table([
            {"Date": "2026-01-09", "Ref": "UPI/Transfer/9902", "Amount": "-₹5,000.00"},
            {"Date": "2026-01-05", "Ref": "Interest Credit", "Amount": "+₹420.00"}
        ])

    # --- FEATURE 3: SETTINGS ---
    elif menu == T["nav_settings"]:
        st.subheader(T["nav_settings"])
        st.write(f"Settings for Account: **{st.session_state.user_acc}**")
        st.checkbox("Enable SMS Alerts")
        st.checkbox("WhatsApp Updates")
        
        st.divider()
        st.markdown("### Compliance Admin Mode")
        if st.button("Simulate KYC Approval"):
            st.session_state.kyc_status = "Approved"
            st.rerun()
        if st.button("Reset KYC Status"):
            st.session_state.kyc_status = "Not Submitted"
            st.rerun()

    # --- FEATURE 4: HELP CENTER ---
    elif menu == T["nav_help"]:
        st.subheader(T["nav_help"])
        st.info(T["support_text"])
        st.write(f"Support Request for Account ID: {st.session_state.user_acc}")
        st.write("📞 Support: 1800-123-4567")
        st.write("📧 Email: support@kyc-portal.in")

st.markdown("---")
st.caption("© 2026 Official KYC Verification Portal | Ministry of Finance Compliant")