import streamlit as st
import json
from datetime import datetime, date
import random
import io
import cloudinary
import cloudinary.uploader
import cloudinary.api
import requests
from PIL import Image

# Configure Cloudinary (using secrets)
cloudinary.config(
    cloud_name=st.secrets["CLOUDINARY_CLOUD_NAME"],
    api_key=st.secrets["CLOUDINARY_API_KEY"],
    api_secret=st.secrets["CLOUDINARY_API_SECRET"],
    secure=True
)

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
    
    /* Photo grid styling */
    .photo-container {
        width: 100%;
        height: 300px;
        object-fit: cover;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .photo-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        padding: 20px 0;
    }
    
    .photo-item {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(214, 51, 132, 0.2);
        transition: transform 0.3s ease;
    }
    
    .photo-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(214, 51, 132, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b9d, #ffa8cc);
        color: white;
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
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 15px !important;
        border: 2px solid #ffb3d1 !important;
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 15px !important;
        border: 2px solid #ffb3d1 !important;
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Date input styling */
    .stDateInput > div > div > input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #ffb3d1 !important;
        border-radius: 15px !important;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div > select {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #ffb3d1 !important;
        border-radius: 15px !important;
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
    
    /* General text styling */
    .stApp, .stApp * {
        color: #000000 !important;
    }
    
    /* Make sure all text is black */
    p, h1, h2, h3, h4, h5, h6, span, div, label {
        color: #000000 !important;
    }
    
    /* Tab text styling */
    .stTabs [data-baseweb="tab"] {
        color: #000000 !important;
        font-weight: 600;
    }
    
    /* Selected tab */
    .stTabs [aria-selected="true"] {
        color: #d63384 !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffeef7, #f8e8ff);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Upload progress styling */
    .upload-progress {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #ffb3d1;
    }
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

# Cloudinary JSON functions
def load_json(filename):
    cloud_name = st.secrets["CLOUDINARY_CLOUD_NAME"]
    base_url = f"https://res.cloudinary.com/{cloud_name}/raw/upload/memory_locker_data/{filename}"
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            data = json.loads(response.text)
            return data if isinstance(data, list) else []
        else:
            return []
    except Exception as e:
        st.warning(f"Could not load {filename}: {str(e)}. Initializing empty list.")
        return []

def save_json(filename, data):
    json_str = json.dumps(data, indent=2, ensure_ascii=False, default=str)
    try:
        response = cloudinary.uploader.upload(
            io.BytesIO(json_str.encode('utf-8')),
            public_id=filename,
            folder="memory_locker_data",
            resource_type="raw",
            overwrite=True,
            invalidate=True
        )
        return response['secure_url']
    except Exception as e:
        st.error(f"Error saving {filename}: {str(e)}")
        return None

# Cloudinary image upload function
def upload_image_to_cloudinary(image_file):
    try:
        # Read the image
        image = Image.open(image_file)
        
        # Handle EXIF orientation
        try:
            exif = image._getexif()
            if exif is not None:
                orientation = exif.get(0x0112)
                if orientation == 3:
                    image = image.rotate(180, expand=True)
                elif orientation == 6:
                    image = image.rotate(270, expand=True)
                elif orientation == 8:
                    image = image.rotate(90, expand=True)
        except:
            pass
        
        # Convert to RGB if necessary
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')
        
        # Resize image for storage efficiency (max 800px on longest side)
        max_size = 800
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = tuple([int(x * ratio) for x in image.size])
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Save to bytes
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='JPEG', quality=85, optimize=True)
        img_buffer.seek(0)
        
        # Upload to Cloudinary
        response = cloudinary.uploader.upload(
            img_buffer,
            resource_type="image",
            folder="memory_locker_photos"
        )
        return response['secure_url'], response['public_id']
    except Exception as e:
        st.error(f"Error uploading image to Cloudinary: {str(e)}")
        return None, None

# Cloudinary video upload function
def upload_video_to_cloudinary(video_file):
    try:
        # Upload to Cloudinary as video
        response = cloudinary.uploader.upload(
            video_file,
            resource_type="video",
            folder="memory_locker_videos"
        )
        return response['secure_url'], response['public_id']
    except Exception as e:
        st.error(f"Error uploading video to Cloudinary: {str(e)}")
        return None, None

# Delete resource from Cloudinary
def delete_from_cloudinary(public_id, resource_type="image"):
    try:
        cloudinary.uploader.destroy(public_id, resource_type=resource_type)
        return True
    except Exception as e:
        st.error(f"Error deleting from Cloudinary: {str(e)}")
        return False

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
    letters = load_json("letters.json")
    photos = load_json("photos.json")
    videos = load_json("videos.json")
    
    if not letters:
        sample_letters = [
            {
                "id": 1,
                "date": "2023-01-01",
                "title": "New Year, New Us",
                "content": "As we step into this new year together, I can't help but feel overwhelmed with gratitude for having you in my life. Every moment with you feels like a beautiful dream that I never want to wake up from. Your smile lights up my entire world, and your laughter is the sweetest melody I've ever heard. Here's to creating countless more memories together! 💕",
                "created_date": "2024-01-02"
            },
            {
                "id": 2,
                "date": "2023-06-15",
                "title": "Six Months of Magic",
                "content": "It's been six incredible months since you walked into my life and changed everything. You've shown me what true love feels like, and every day with you is an adventure I treasure. From our silly inside jokes to our deep midnight conversations, every moment has been perfect because it's been with you. I love you more than words can express! 🌟💖",
                "created_date": "2024-06-16"
            }
        ]
        save_json("letters.json", sample_letters)
    
    if not photos:
        save_json("photos.json", [])
    if not videos:
        save_json("videos.json", [])

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
        <p style="text-align: center; color: #888; font-size: 0.9em;">
            ✨ Now with permanent cloud storage! ✨
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
    
    tab1, tab2, tab3, tab4 = st.tabs(["📷 Add Photos", "🎥 Add Videos", "💌 Write Letters", "🗑️ Manage Content"])
    
    with tab1:
        st.markdown('<h2 class="section-title">Add New Photo</h2>', unsafe_allow_html=True)
        
        st.info("📸 Photos are stored permanently on Cloudinary! 🎉")
        
        uploaded_file = st.file_uploader("Choose a photo", type=['png', 'jpg', 'jpeg'])
        photo_date = st.date_input("Photo Date", value=date.today())
        caption = st.text_area("Caption for this photo", placeholder="Describe this beautiful memory...")
        
        if st.button("Save Photo", key="save_photo"):
            if uploaded_file and caption:
                try:
                    progress_placeholder = st.empty()
                    progress_placeholder.markdown("""
                    <div class="upload-progress">
                        <p>📤 Processing photo... Please wait! ✨</p>
                        <p style="font-size: 0.9em; color: #666;">Uploading to permanent cloud storage...</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    url, public_id = upload_image_to_cloudinary(uploaded_file)
                    
                    if url and public_id:
                        photos = load_json("photos.json")
                        photos.append({
                            "id": len(photos) + 1,
                            "original_name": uploaded_file.name,
                            "date": photo_date.strftime("%Y-%m-%d"),
                            "caption": caption,
                            "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "file_size": uploaded_file.size,
                            "url": url,
                            "public_id": public_id,
                            "storage_type": "cloudinary"
                        })
                        save_json("photos.json", photos)
                        
                        progress_placeholder.empty()
                        st.success(f"📸 Photo '{uploaded_file.name}' saved permanently! 💕")
                        
                        st.markdown("### Preview:")
                        st.image(url, caption=caption, width=300)
                        
                        st.rerun()
                    else:
                        progress_placeholder.empty()
                        st.error("❌ Failed to upload photo!")
                        
                except Exception as e:
                    progress_placeholder.empty()
                    st.error(f"❌ Error saving photo: {str(e)}")
            else:
                st.error("Please select a photo and add a caption!")
    
    with tab2:
        st.markdown('<h2 class="section-title">Add New Video</h2>', unsafe_allow_html=True)
        
        st.info("🎥 Videos are stored on Cloudinary for reliable streaming! 🚀")
        
        uploaded_file = st.file_uploader("Choose a video", type=['mp4', 'mov', 'avi'])
        video_date = st.date_input("Video Date", value=date.today(), key="video_date")
        caption = st.text_area("Caption for this video", placeholder="Describe this beautiful memory...", key="video_caption")
        
        if st.button("Save Video", key="save_video"):
            if uploaded_file and caption:
                try:
                    progress_placeholder = st.empty()
                    progress_placeholder.markdown("""
                    <div class="upload-progress">
                        <p>📤 Uploading video to Cloudinary... Please wait! ✨</p>
                        <p style="font-size: 0.9em; color: #666;">This may take a moment for larger files...</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    url, public_id = upload_video_to_cloudinary(uploaded_file)
                    
                    if url and public_id:
                        videos = load_json("videos.json")
                        videos.append({
                            "id": len(videos) + 1,
                            "original_name": uploaded_file.name,
                            "date": video_date.strftime("%Y-%m-%d"),
                            "caption": caption,
                            "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "file_size": uploaded_file.size,
                            "url": url,
                            "public_id": public_id,
                            "storage_type": "cloudinary"
                        })
                        save_json("videos.json", videos)
                        
                        progress_placeholder.empty()
                        st.success(f"🎥 Video '{uploaded_file.name}' saved to Cloudinary! 💕")
                        
                        st.markdown("### Preview:")
                        st.video(url)
                        st.write(caption)
                        
                        st.rerun()
                    else:
                        progress_placeholder.empty()
                        st.error("❌ Failed to upload video!")
                        
                except Exception as e:
                    progress_placeholder.empty()
                    st.error(f"❌ Error saving video: {str(e)}")
            else:
                st.error("Please select a video and add a caption!")
    
    with tab3:
        st.markdown('<h2 class="section-title">Write a Love Letter</h2>', unsafe_allow_html=True)
        
        letter_date = st.date_input("Letter Date", value=date.today(), key="letter_date")
        title = st.text_input("Letter Title", placeholder="Give your letter a beautiful title...")
        content = st.text_area("Letter Content", height=200, placeholder="Pour your heart out here...")
        
        if st.button("Save Letter", key="save_letter"):
            if title and content:
                try:
                    letters = load_json("letters.json")
                    letters.append({
                        "id": len(letters) + 1,
                        "date": letter_date.strftime("%Y-%m-%d"),
                        "title": title,
                        "content": content,
                        "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    save_json("letters.json", letters)
                    
                    st.success("💌 Letter saved successfully! 💕")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error saving letter: {str(e)}")
            else:
                st.error("Please add both title and content!")
    
    with tab4:
        st.markdown('<h2 class="section-title">Manage Content</h2>', unsafe_allow_html=True)
        
        # Manage Photos
        st.subheader("📷 Manage Photos")
        photos = load_json("photos.json")
        
        if photos:
            st.info(f"📊 Total photos: {len(photos)} | Storage: Cloudinary")
            
            for i, photo in enumerate(photos):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{photo['original_name']}** - {photo['date']}")
                    st.write(f"*{photo['caption'][:50]}...*" if len(photo['caption']) > 50 else f"*{photo['caption']}*")
                    st.write(f"URL: {photo['url'][:30]}...")
                with col2:
                    st.success("✅ Stored on Cloudinary")
                with col3:
                    if st.button("🗑️ Delete", key=f"del_photo_{i}"):
                        try:
                            # Delete from Cloudinary
                            if 'public_id' in photo:
                                delete_from_cloudinary(photo['public_id'], resource_type="image")
                            # Remove from JSON
                            photos.pop(i)
                            save_json("photos.json", photos)
                            st.success("Photo deleted!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting photo: {str(e)}")
                st.divider()
        else:
            st.info("No photos to manage yet!")
        
        # Manage Videos
        st.subheader("🎥 Manage Videos")
        videos = load_json("videos.json")
        
        if videos:
            st.info(f"📊 Total videos: {len(videos)} | Storage: Cloudinary")
            
            for i, video in enumerate(videos):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{video['original_name']}** - {video['date']}")
                    st.write(f"*{video['caption'][:50]}...*" if len(video['caption']) > 50 else f"*{video['caption']}*")
                    st.write(f"URL: {video['url'][:30]}...")
                with col2:
                    st.success("✅ Stored on Cloudinary")
                with col3:
                    if st.button("🗑️ Delete", key=f"del_video_{i}"):
                        try:
                            # Delete from Cloudinary
                            if 'public_id' in video:
                                delete_from_cloudinary(video['public_id'], resource_type="video")
                            # Remove from JSON
                            videos.pop(i)
                            save_json("videos.json", videos)
                            st.success("Video deleted!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting video: {str(e)}")
                st.divider()
        else:
            st.info("No videos to manage yet!")
        
        st.markdown("---")
        
        # Manage Letters
        st.subheader("💌 Manage Letters")
        letters = load_json("letters.json")
        
        if letters:
            for i, letter in enumerate(letters):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**{letter['title']}** - {letter['date']}")
                    st.write(f"*{letter['content'][:100]}...*" if len(letter['content']) > 100 else f"*{letter['content']}*")
                with col2:
                    if st.button("🗑️ Delete", key=f"del_letter_{i}"):
                        try:
                            letters.pop(i)
                            save_json("letters.json", letters)
                            st.success("Letter deleted!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting letter: {str(e)}")
                st.divider()
        else:
            st.info("No letters to manage yet!")

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
    
    tab1, tab2, tab3, tab4 = st.tabs(["📷 Our Photos", "🎥 Our Videos", "💌 Love Letters", "🎁 Surprise Me!"])
    
    with tab1:
        display_photos()
    
    with tab2:
        display_videos()
    
    with tab3:
        display_letters()
    
    with tab4:
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
            <p style="text-align: center; color: #d63384; font-size: 0.9em;">✨ Photos are now stored permanently! ✨</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.info(f"📊 **{len(photos)} beautiful memories** stored permanently! 💕")
    
    cols_per_row = 3
    for i in range(0, len(photos), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(photos):
                photo = photos[i + j]
                with cols[j]:
                    try:
                        st.image(photo['url'], use_container_width=True)
                        st.markdown(f"""
                        <div style="text-align: center; margin-top: 10px;">
                            <p style="color: #d63384; font-weight: 600; margin: 5px 0;">{photo['date']}</p>
                            <p style="color: #333; font-size: 0.9em; margin: 0;">{photo['caption']}</p>
                            <p style="color: #4CAF50; font-size: 0.8em; margin: 5px 0;">☁️ Cloud Storage</p>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error displaying photo: {str(e)}")
                    st.markdown("---")

def display_videos():
    st.markdown('<h2 class="section-title">Our Video Memories 🎥</h2>', unsafe_allow_html=True)
    
    videos = load_json("videos.json")
    videos.sort(key=lambda x: x['date'], reverse=True)
    
    if not videos:
        st.markdown("""
        <div class="memory-card">
            <h3 style="text-align: center; color: #666;">No videos yet! 🎥</h3>
            <p style="text-align: center; color: #888;">Your beautiful video memories will appear here soon...</p>
            <p style="text-align: center; color: #d63384; font-size: 0.9em;">✨ Videos are stored on Cloudinary! ✨</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.info(f"📊 **{len(videos)} beautiful video memories** stored on Cloudinary! 💕")
    
    cols_per_row = 2
    for i in range(0, len(videos), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(videos):
                video = videos[i + j]
                with cols[j]:
                    try:
                        st.video(video['url'])
                        st.markdown(f"""
                        <div style="text-align: center; margin-top: 10px;">
                            <p style="color: #d63384; font-weight: 600; margin: 5px 0;">{video['date']}</p>
                            <p style="color: #333; font-size: 0.9em; margin: 0;">{video['caption']}</p>
                            <p style="color: #4CAF50; font-size: 0.8em; margin: 5px 0;">☁️ Cloudinary Storage</p>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error displaying video: {str(e)}")
                    st.markdown("---")

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
    videos = load_json("videos.json")
    letters = load_json("letters.json")
    
    all_memories = []
    
    for photo in photos:
        if 'url' in photo:
            all_memories.append({
                'type': 'photo',
                'content': photo
            })
    
    for video in videos:
        if 'url' in video:
            all_memories.append({
                'type': 'video',
                'content': video
            })
    
    for letter in letters:
        all_memories.append({
            'type': 'letter',
            'content': letter
        })
    
    if not all_memories:
        st.warning("No memories to surprise you with yet! Add some photos, videos, or letters first. 💕")
        return
    
    random_memory = random.choice(all_memories)
    
    if random_memory['type'] == 'photo':
        photo = random_memory['content']
        st.markdown("### 📷 Random Photo Memory!")
        try:
            st.image(photo['url'], caption=f"{photo['caption']} ({photo['date']})")
        except Exception as e:
            st.error(f"Error displaying random photo: {str(e)}")
    
    elif random_memory['type'] == 'video':
        video = random_memory['content']
        st.markdown("### 🎥 Random Video Memory!")
        try:
            st.video(video['url'])
            st.markdown(f"""
            <div class="memory-card">
                <div class="memory-date">{video['date']}</div>
                <p style="line-height: 1.6; color: #555; font-size: 1.1em;">{video['caption']}</p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error displaying random video: {str(e)}")
    
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
    init_session_state()
    create_sample_data()
    load_css()
    add_floating_hearts()
    
    if not st.session_state.logged_in:
        login_page()
    elif st.session_state.user_type == "admin":
        admin_mode()
    elif st.session_state.user_type == "viewer":
        viewer_mode()

if __name__ == "__main__":
    main()
