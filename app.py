import streamlit as st
import json
import os
from datetime import datetime, date
import base64
from PIL import Image
import random
import io

# Configure page
st.set_page_config(
    page_title="Our Memory Locker 💕",
    page_icon="💝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for romantic theme
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;700&family=Poppins:wght@300;400;600&display=swap');
    
    /* Main background and theme */
    .stApp {
        background: #ffc0d4 !important;
        background-attachment: fixed;
    }
    
    /* Floating hearts animation */
    .hearts {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .heart {
        position: absolute;
        color: #d63384;
        font-size: 20px;
        animation: float 8s infinite ease-in-out;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10%, 90% { opacity: 1; }
        50% { transform: translateY(-10vh) rotate(180deg); }
    }
    
    /* Title styling */
    .main-title {
        font-family: 'Dancing Script', cursive;
        font-size: 3.5em;
        color: #000000 !important;
        text-align: center;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        font-weight: 700;
    }
    
    .section-title {
        font-family: 'Dancing Script', cursive;
        font-size: 2.5em;
        color: #000000 !important;
        text-align: center;
        margin: 30px 0 20px 0;
        font-weight: 700;
    }
    
    /* Card styling */
    .memory-card {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 2px solid rgba(214, 51, 132, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .photo-card {
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 15px;
        padding: 15px;
        margin: 15px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(214, 51, 132, 0.2);
        transition: transform 0.3s ease;
    }
    
    .photo-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(214, 51, 132, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b9d, #ffa8cc);
        color: white !important;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 157, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 157, 0.4);
    }
    
    /* Input styling - Fixed for better visibility */
    .stTextInput > div > div > input {
        border-radius: 15px !important;
        border: 2px solid #ffb3d1 !important;
        background: rgba(255, 255, 255, 0.95) !important;
        color: #000000 !important;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 15px !important;
        border: 2px solid #ffb3d1 !important;
        background: rgba(255, 255, 255, 0.95) !important;
        color: #000000 !important;
    }
    
    /* Selectbox styling - Fixed for better visibility */
    .stSelectbox > div > div > div {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #ffb3d1 !important;
        border-radius: 15px !important;
        color: #000000 !important;
    }
    
    .stSelectbox > div > div > div > div {
        color: #000000 !important;
    }
    
    /* Selectbox dropdown options */
    .stSelectbox [role="listbox"] {
        background: white !important;
        border: 2px solid #ffb3d1 !important;
        border-radius: 15px !important;
    }
    
    .stSelectbox [role="option"] {
        color: #000000 !important;
        background: white !important;
    }
    
    .stSelectbox [role="option"]:hover {
        background: #ffe6f0 !important;
        color: #000000 !important;
    }
    
    .stSelectbox [aria-selected="true"] {
        background: #ffccdd !important;
        color: #000000 !important;
    }
    
    /* Date input styling */
    .stDateInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #ffb3d1 !important;
        border-radius: 15px !important;
        color: #000000 !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #ffb3d1 !important;
        border-radius: 15px !important;
        color: #000000 !important;
    }
    
    .stFileUploader label {
        color: #000000 !important;
    }
    
    /* Date styling */
    .memory-date {
        color: #d63384 !important;
        font-style: italic;
        font-size: 0.9em;
        margin-bottom: 10px;
        font-weight: 600;
    }
    
    /* Success messages */
    .success-message {
        background: linear-gradient(45deg, #4ecdc4, #44a08d);
        color: white !important;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        font-weight: 600;
    }
    
    /* General text styling - Make sure all text is black */
    .stApp, .stApp * {
        color: #000000 !important;
    }
    
    /* Specific text elements */
    p, h1, h2, h3, h4, h5, h6, span, div, label {
        color: #000000 !important;
    }
    
    /* Input labels */
    .stTextInput > label, 
    .stTextArea > label, 
    .stSelectbox > label, 
    .stDateInput > label,
    .stFileUploader > label {
        color: #000000 !important;
        font-weight: 600;
    }
    
    /* Tab text styling */
    .stTabs [data-baseweb="tab"] {
        color: #000000 !important;
        font-weight: 600;
        background: rgba(255, 255, 255, 0.7) !important;
        border-radius: 10px 10px 0 0 !important;
        margin-right: 2px !important;
    }
    
    /* Selected tab */
    .stTabs [aria-selected="true"] {
        color: #d63384 !important;
        background: rgba(255, 255, 255, 0.95) !important;
        font-weight: 700;
    }
    
    /* Tab content background */
    .stTabs [data-baseweb="tab-panel"] {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 0 15px 15px 15px !important;
        padding: 20px !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffeef7, #f8e8ff);
    }
    
    /* Ensure dropdown menus are visible */
    [data-baseweb="popover"] {
        background: white !important;
    }
    
    /* Fix for any remaining invisible text */
    * {
        color: inherit !important;
    }
    
    .stMarkdown {
        color: #000000 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def add_floating_hearts():
    hearts_html = """
    <div class="hearts">
        <div class="heart" style="left: 10%; animation-delay: 0s;">💖</div>
        <div class="heart" style="left: 20%; animation-delay: 1s;">💕</div>
        <div class="heart" style="left: 30%; animation-delay: 2s;">💗</div>
        <div class="heart" style="left: 40%; animation-delay: 3s;">💝</div>
        <div class="heart" style="left: 50%; animation-delay: 4s;">💖</div>
        <div class="heart" style="left: 60%; animation-delay: 5s;">💕</div>
        <div class="heart" style="left: 70%; animation-delay: 6s;">💗</div>
        <div class="heart" style="left: 80%; animation-delay: 7s;">💝</div>
        <div class="heart" style="left: 90%; animation-delay: 0.5s;">💖</div>
    </div>
    """
    st.markdown(hearts_html, unsafe_allow_html=True)

# Initialize data directories
def init_directories():
    os.makedirs("photos", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("static/music", exist_ok=True)

# Load or create JSON files
def load_json(filename):
    filepath = f"data/{filename}"
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_json(filename, data):
    filepath = f"data/{filename}"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)

# Initialize session state
def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    if 'show_surprise' not in st.session_state:
        st.session_state.show_surprise = False

# Create sample data
def create_sample_data():
    # Sample photos metadata
    sample_photos = [
        {
            "filename": "sample1.jpg",
            "date": "2023-01-14",
            "caption": "Our first coffee date together ☕💕",
            "upload_date": "2024-01-15"
        },
        {
            "filename": "sample2.jpg", 
            "date": "2023-02-14",
            "caption": "Valentine's Day surprise! 🌹❤️",
            "upload_date": "2024-02-15"
        }
    ]
    
    # Sample letters
    sample_letters = [
        {
            "date": "2023-01-01",
            "title": "New Year, New Us",
            "content": "As we step into this new year together, I can't help but feel overwhelmed with gratitude for having you in my life. Every moment with you feels like a beautiful dream that I never want to wake up from. Your smile lights up my entire world, and your laughter is the sweetest melody I've ever heard. Here's to creating countless more memories together! 💕",
            "created_date": "2024-01-02"
        },
        {
            "date": "2023-06-15",
            "title": "Six Months of Magic",
            "content": "It's been six incredible months since you walked into my life and changed everything. You've shown me what true love feels like, and every day with you is an adventure I treasure. From our silly inside jokes to our deep midnight conversations, every moment has been perfect because it's been with you. I love you more than words can express! 🌟💖",
            "created_date": "2024-06-16"
        }
    ]
    
    # Save sample data if files don't exist
    if not os.path.exists("data/photos.json"):
        save_json("photos.json", sample_photos)
    if not os.path.exists("data/letters.json"):
        save_json("letters.json", sample_letters)

# Login functions
def login_page():
    st.markdown('<h1 class="main-title">Our Memory Locker 💝</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="memory-card">
        <h3 style="text-align: center; color: #d63384; font-family: 'Dancing Script', cursive; font-size: 1.8em;">
            Welcome to Our Special Place 💕
        </h3>
        <p style="text-align: center; color: #666; font-style: italic;">
            A treasure trove of our beautiful memories together
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Choose Your Access Mode")
        
        mode = st.selectbox(
            "Select Mode:",
            ["Select...", "Admin Mode (Add Memories)", "Viewer Mode (View Memories)"],
            key="login_mode"
        )
        
        if mode != "Select...":
            password = st.text_input("Enter Password:", type="password", key="password_input")
            
            if st.button("Login", key="login_btn"):
                if mode == "Admin Mode (Add Memories)" and password == "admin123":  # Change this password!
                    st.session_state.logged_in = True
                    st.session_state.user_type = "admin"
                    st.rerun()
                elif mode == "Viewer Mode (View Memories)" and password == "love123":  # Change this password!
                    st.session_state.logged_in = True
                    st.session_state.user_type = "viewer"
                    st.rerun()
                else:
                    st.error("❌ Invalid password! Please try again.")

def logout():
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.show_surprise = False
    st.rerun()

# Admin Mode Functions
def admin_mode():
    st.markdown('<h1 class="main-title">Admin Panel 👨‍💻💕</h1>', unsafe_allow_html=True)
    
    if st.button("Logout", key="admin_logout"):
        logout()
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📷 Add Photos", "💌 Write Letters", "🗑️ Manage Photos", "🗑️ Manage Letters"])
    
    with tab1:
        add_photo_section()
    
    with tab2:
        add_letter_section()
    
    with tab3:
        manage_photos_section()
    
    with tab4:
        manage_letters_section()

def add_photo_section():
    st.markdown('<h2 class="section-title">Add New Photo</h2>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a photo", type=['png', 'jpg', 'jpeg'])
    photo_date = st.date_input("Photo Date", value=date.today())
    caption = st.text_area("Caption for this photo", placeholder="Describe this beautiful memory...")
    
    if st.button("Save Photo", key="save_photo"):
        if uploaded_file and caption:
            # Save the uploaded file
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_file.name}"
            filepath = os.path.join("photos", filename)
            
            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Save metadata
            photos = load_json("photos.json")
            photos.append({
                "filename": filename,
                "date": photo_date.strftime("%Y-%m-%d"),
                "caption": caption,
                "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_json("photos.json", photos)
            
            st.markdown('<div class="success-message">📸 Photo saved successfully! 💕</div>', unsafe_allow_html=True)
        else:
            st.error("Please select a photo and add a caption!")

def add_letter_section():
    st.markdown('<h2 class="section-title">Write a Love Letter</h2>', unsafe_allow_html=True)
    
    letter_date = st.date_input("Letter Date", value=date.today(), key="letter_date")
    title = st.text_input("Letter Title", placeholder="Give your letter a beautiful title...")
    content = st.text_area("Letter Content", height=200, placeholder="Pour your heart out here...")
    
    if st.button("Save Letter", key="save_letter"):
        if title and content:
            letters = load_json("letters.json")
            letters.append({
                "date": letter_date.strftime("%Y-%m-%d"),
                "title": title,
                "content": content,
                "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_json("letters.json", letters)
            
            st.markdown('<div class="success-message">💌 Letter saved successfully! 💕</div>', unsafe_allow_html=True)
        else:
            st.error("Please add both title and content!")

def manage_photos_section():
    st.markdown('<h2 class="section-title">Manage Photos 🗑️</h2>', unsafe_allow_html=True)
    
    photos = load_json("photos.json")
    photos.sort(key=lambda x: x['date'], reverse=True)
    
    if not photos:
        st.markdown("""
        <div class="memory-card">
            <h3 style="text-align: center; color: #666;">No photos to manage! 📸</h3>
            <p style="text-align: center; color: #888;">Add some photos first...</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown("### Current Photos")
    
    for idx, photo in enumerate(photos):
        with st.container():
            col1, col2, col3 = st.columns([2, 3, 1])
            
            with col1:
                photo_path = os.path.join("photos", photo['filename'])
                if os.path.exists(photo_path):
                    try:
                        image = Image.open(photo_path)
                        st.image(image, width=150)
                    except Exception as e:
                        st.markdown("📷 Photo preview unavailable")
                else:
                    st.markdown("📷 Sample Photo")
            
            with col2:
                st.markdown(f"**Date:** {photo['date']}")
                st.markdown(f"**Caption:** {photo['caption']}")
                st.markdown(f"**Uploaded:** {photo.get('upload_date', 'Unknown')}")
            
            with col3:
                if st.button("🗑️ Delete", key=f"delete_photo_{idx}"):
                    # Delete the photo file if it exists
                    photo_path = os.path.join("photos", photo['filename'])
                    if os.path.exists(photo_path):
                        try:
                            os.remove(photo_path)
                        except Exception as e:
                            st.error(f"Could not delete photo file: {e}")
                    
                    # Remove from JSON
                    photos.pop(idx)
                    save_json("photos.json", photos)
                    
                    st.markdown('<div class="success-message">📸 Photo deleted successfully! 💕</div>', unsafe_allow_html=True)
                    st.rerun()
            
            st.markdown("---")

def manage_letters_section():
    st.markdown('<h2 class="section-title">Manage Letters 🗑️</h2>', unsafe_allow_html=True)
    
    letters = load_json("letters.json")
    letters.sort(key=lambda x: x['date'], reverse=True)
    
    if not letters:
        st.markdown("""
        <div class="memory-card">
            <h3 style="text-align: center; color: #666;">No letters to manage! 💌</h3>
            <p style="text-align: center; color: #888;">Write some letters first...</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown("### Current Letters")
    
    for idx, letter in enumerate(letters):
        with st.container():
            st.markdown(f"""
            <div class="memory-card">
                <div class="memory-date">{letter['date']}</div>
                <h3 style="color: #d63384; font-family: 'Dancing Script', cursive; font-size: 1.8em; margin-bottom: 15px;">{letter['title']}</h3>
                <p style="line-height: 1.6; color: #555; font-size: 1.0em;">{letter['content'][:200]}{'...' if len(letter['content']) > 200 else ''}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("🗑️ Delete Letter", key=f"delete_letter_{idx}"):
                    letters.pop(idx)
                    save_json("letters.json", letters)
                    
                    st.markdown('<div class="success-message">💌 Letter deleted successfully! 💕</div>', unsafe_allow_html=True)
                    st.rerun()
            
            st.markdown("---")

# Viewer Mode Functions
def viewer_mode():
    st.markdown('<h1 class="main-title">Our Memory Locker 💝</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("*A collection of our most precious moments* ✨")
    with col2:
        if st.button("Logout", key="viewer_logout"):
            logout()
    
    st.markdown("---")
    
    # Navigation
    tab1, tab2, tab3 = st.tabs(["📷 Our Photos", "💌 Love Letters", "🎁 Surprise Me!"])
    
    with tab1:
        display_photos()
    
    with tab2:
        display_letters()
    
    with tab3:
        surprise_section()

def display_photos():
    st.markdown('<h2 class="section-title">Our Photo Memories 📷</h2>', unsafe_allow_html=True)
    
    photos = load_json("photos.json")
    photos.sort(key=lambda x: x['date'], reverse=True)
    
    if not photos:
        st.markdown("""
        <div class="memory-card">
            <h3 style="text-align: center; color: #666;">No photos yet! 📸</h3>
            <p style="text-align: center; color: #888;">Your beautiful memories will appear here soon...</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display photos in a grid
    cols = st.columns(2)
    for idx, photo in enumerate(photos):
        with cols[idx % 2]:
            photo_path = os.path.join("photos", photo['filename'])
            if os.path.exists(photo_path):
                try:
                    image = Image.open(photo_path)
                    st.image(image, caption=f"{photo['caption']} ({photo['date']})", use_column_width=True)
                except Exception as e:
                    st.error(f"Could not load image: {photo['filename']}")
            else:
                st.markdown(f"""
                <div class="photo-card">
                    <div style="background: #f0f0f0; height: 200px; display: flex; align-items: center; justify-content: center; border-radius: 10px;">
                        <p style="color: #666;">📷 Sample Photo</p>
                    </div>
                    <div class="memory-date">{photo['date']}</div>
                    <p><strong>{photo['caption']}</strong></p>
                </div>
                """, unsafe_allow_html=True)

def display_letters():
    st.markdown('<h2 class="section-title">Love Letters 💌</h2>', unsafe_allow_html=True)
    
    letters = load_json("letters.json")
    letters.sort(key=lambda x: x['date'], reverse=True)
    
    if not letters:
        st.markdown("""
        <div class="memory-card">
            <h3 style="text-align: center; color: #666;">No letters yet! 💌</h3>
            <p style="text-align: center; color: #888;">Heartfelt words will appear here soon...</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    for letter in letters:
        st.markdown(f"""
        <div class="memory-card">
            <div class="memory-date">{letter['date']}</div>
            <h3 style="color: #d63384; font-family: 'Dancing Script', cursive; font-size: 1.8em; margin-bottom: 15px;">{letter['title']}</h3>
            <p style="line-height: 1.6; color: #555; font-size: 1.1em;">{letter['content']}</p>
        </div>
        """, unsafe_allow_html=True)

def surprise_section():
    st.markdown('<h2 class="section-title">Surprise Me! 🎁</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="memory-card">
        <p style="text-align: center; font-size: 1.2em; color: #666; margin-bottom: 25px;">
            Click the button below for a random memory! 🌟
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🎲 Surprise Me!", key="surprise_btn"):
            show_random_memory()

def show_random_memory():
    photos = load_json("photos.json")
    letters = load_json("letters.json")
    
    all_memories = []
    
    # Add photos to memories pool
    for photo in photos:
        all_memories.append({
            'type': 'photo',
            'content': photo
        })
    
    # Add letters to memories pool  
    for letter in letters:
        all_memories.append({
            'type': 'letter',
            'content': letter
        })
    
    if not all_memories:
        st.warning("No memories to surprise you with yet! Add some photos or letters first. 💕")
        return
    
    # Pick random memory
    random_memory = random.choice(all_memories)
    
    if random_memory['type'] == 'photo':
        photo = random_memory['content']
        photo_path = os.path.join("photos", photo['filename'])
        
        st.markdown("### 📷 Random Photo Memory!")
        
        if os.path.exists(photo_path):
            image = Image.open(photo_path)
            st.image(image, caption=f"{photo['caption']} ({photo['date']})")
        else:
            st.markdown(f"""
            <div class="memory-card">
                <div style="background: #f0f0f0; height: 200px; display: flex; align-items: center; justify-content: center; border-radius: 10px; margin-bottom: 15px;">
                    <p style="color: #666;">📷 Sample Photo</p>
                </div>
                <div class="memory-date">{photo['date']}</div>
                <p><strong>{photo['caption']}</strong></p>
            </div>
            """, unsafe_allow_html=True)
    
    else:  # letter
        letter = random_memory['content']
        st.markdown("### 💌 Random Love Letter!")
        
        st.markdown(f"""
        <div class="memory-card">
            <div class="memory-date">{letter['date']}</div>
            <h3 style="color: #d63384; font-family: 'Dancing Script', cursive; font-size: 1.8em; margin-bottom: 15px;">{letter['title']}</h3>
            <p style="line-height: 1.6; color: #555; font-size: 1.1em;">{letter['content']}</p>
        </div>
        """, unsafe_allow_html=True)

# Main app function
def main():
    # Initialize everything
    init_directories()
    init_session_state()
    create_sample_data()
    load_css()
    add_floating_hearts()
    
    # Route based on login state
    if not st.session_state.logged_in:
        login_page()
    elif st.session_state.user_type == "admin":
        admin_mode()
    elif st.session_state.user_type == "viewer":
