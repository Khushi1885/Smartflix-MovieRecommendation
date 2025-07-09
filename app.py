# import streamlit as st
# import pandas as pd
# import pickle
# import sqlite3
# import hashlib
# from datetime import datetime
# import base64
# import time
# import requests
# import urllib.parse
# from dotenv import load_dotenv
# import os
# import streamlit.components.v1 as components
# import random
# import gdown


# # ----------------------------
# # Load API Key
# # ----------------------------
# load_dotenv()
# OMDB_API_KEY = os.getenv("OMDB_API_KEY")
# placeholder_url = "https://via.placeholder.com/200x300?text=No+Poster"

# # ----------------------------
# # Set Background + Fonts + Theme
# # ----------------------------
# def set_custom_style():
#     st.markdown("""
#     <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
#     <style>
#         html, body, [class*="css"]  {
#             font-family: 'Poppins', sans-serif;
#         }
#         .stApp {
#             background-color: #121212;
#             color: #E0E0E0;
#         }
#         [data-testid="stSidebar"] {
#             background-color: #1f1f1f;
#         }
#         button {
#             background-color: #E50914 !important;
#             color: white !important;
#             border-radius: 8px !important;
#             font-weight: 600 !important;
#         }
#         button:hover {
#             box-shadow: 0 0 10px #E50914;
#         }
#         ::-webkit-scrollbar {
#             height: 8px;
#         }
#         ::-webkit-scrollbar-thumb {
#             background: #E50914;
#             border-radius: 10px;
#         }
#         ::-webkit-scrollbar-track {
#             background: #121212;
#         }
#     </style>
#     """, unsafe_allow_html=True)

# # ----------------------------
# # Splash Video
# # ----------------------------
# def show_splash_video(video_path):
#     if not os.path.exists(video_path):
#         # Video file not found, skip splash video silently
#         return
#     with open(video_path, "rb") as file:
#         video_base64 = base64.b64encode(file.read()).decode()
#     splash_html = f"""
#     <style>
#         .splash-video {{
#             position: fixed;
#             top: 0;
#             left: 0;
#             width: 100vw;
#             height: 100vh;
#             object-fit: cover;
#             z-index: 999999;
#             background: black;
#         }}
#         .main, .sidebar {{
#             visibility: hidden;
#         }}
#     </style>
#     <video autoplay muted playsinline class="splash-video">
#         <source src="data:video/mp4;base64,{video_base64}" type="video/mp4" />
#     </video>
#     """
#     splash = st.empty()
#     splash.markdown(splash_html, unsafe_allow_html=True)
#     time.sleep(6)
#     splash.empty()

# # ----------------------------
# # Load Data
# # ----------------------------
# # movies = pd.read_pickle("artificats/movie_list.pkl")
# # similarity = pickle.load(open("artificats/similary_list.pkl", "rb"))
# movies = pd.read_pickle("artificats/movie_list.pkl")

# # Download similarity file from Google Drive if not present locally
# file_id = "1a-bZTigBMJ8bZidn_yBi8IG2zq_H98r8"  # google drive file id
# output = "artificats/similary_list.pkl"

# #show_splash_video("artificats/splash_video.mp4")



# if not os.path.exists(output):
#     url = f"https://drive.google.com/uc?id={file_id}"
#     gdown.download(url, output, quiet=False)


# @st.cache_data
# def load_similarity(path):
#     return pickle.load(open(path, "rb"))

# similarity = load_similarity(output)



# # ----------------------------
# # OMDB Data
# # ----------------------------
# @st.cache_data(show_spinner=False)
# def fetch_movie_details(title):
#     if not OMDB_API_KEY:
#         return {}
#     try:
#         url = f"http://www.omdbapi.com/?t={urllib.parse.quote(title)}&apikey={OMDB_API_KEY}"
#         response = requests.get(url)
#         return response.json()
#     except:
#         return {}


# @st.cache_data(show_spinner=False)
# def fetch_poster(title):
#     if not OMDB_API_KEY:
#         return placeholder_url
#     try:
#         url = f"http://www.omdbapi.com/?t={urllib.parse.quote(title)}&apikey={OMDB_API_KEY}"
#         response = requests.get(url)
#         data = response.json()
#         return data.get("Poster", placeholder_url) if data.get("Response") == "True" else placeholder_url
#     except:
#         return placeholder_url


# # ----------------------------
# # Recommend Movies
# # ----------------------------
# def recommend(movie):
#     if movie not in movies['title'].values:
#         return [], []
#     idx = movies[movies['title'] == movie].index[0]
#     distances = sorted(list(enumerate(similarity[idx])), key=lambda x: x[1], reverse=True)[1:6]
#     titles, posters = [], []
#     for i in distances:
#         title = movies.iloc[i[0]].title
#         poster = fetch_poster(title)
#         titles.append(title)
#         posters.append(poster)
#     return titles, posters
# #--------------------
# #movie of the day
# #--------------------
# from datetime import date
# import hashlib

# def get_movie_of_the_day():
#     today = str(date.today())  # e.g., '2025-07-04'
#     # Create a hash of the date to use as a seed
#     seed = int(hashlib.sha256(today.encode()).hexdigest(), 16) % (10 ** 8)
#     random.seed(seed)
#     return random.choice(movies['title'].values)



# # ----------------------------
# # SQLite User Auth
# # ----------------------------
# def get_connection():
#     return sqlite3.connect("users.db")

# def init_db():
#     with get_connection() as conn:
#         conn.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 email TEXT PRIMARY KEY,
#                 name TEXT NOT NULL,
#                 password TEXT NOT NULL,
#                 created_at TEXT NOT NULL
#             )
#         """)

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def user_exists(email):
#     with get_connection() as conn:
#         return conn.execute("SELECT 1 FROM users WHERE email = ?", (email,)).fetchone() is not None

# def add_user(name, email, password):
#     with get_connection() as conn:
#         conn.execute(
#             "INSERT INTO users (email, name, password, created_at) VALUES (?, ?, ?, ?)",
#             (email, name, hash_password(password), datetime.now().isoformat())
#         )

# def validate_login(email, password):
#     with get_connection() as conn:
#         result = conn.execute("SELECT name, password FROM users WHERE email = ?", (email,)).fetchone()
#         if result and result[1] == hash_password(password):
#             return result[0]
#         return None

# # ----------------------------
# # App State & Init
# # ----------------------------
# init_db()
# if 'show_splash' not in st.session_state:
#     st.session_state.show_splash = True
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
# if 'current_user' not in st.session_state:
#     st.session_state.current_user = None
# if st.session_state.show_splash:
#     show_splash_video("artificats/splash_video.mp4")  
#     st.session_state.show_splash = False


# # Splash Video
# # if st.session_state.show_splash:
# #     show_splash_video("artificats/splash_video.mp4")  

# #     st.session_state.show_splash = False

# # set_custom_style()

# # ----------------------------
# # UI Layout
# # ----------------------------
# st.sidebar.title("🎬 Movie App Navigation")
# menu = st.sidebar.radio("Go to", ["Login", "Sign Up", "Dashboard"])


# # Movie of the Day - show only on Dashboard when logged in
# if menu == "Dashboard" and st.session_state.logged_in:
#     st.sidebar.markdown("---")
#     st.sidebar.markdown("🎁 Movie of the Day")
#     movie_of_day = get_movie_of_the_day()
#     poster = fetch_poster(movie_of_day)
#     st.sidebar.image(poster, caption=movie_of_day, use_container_width=True)
# #Trailer button

    
#     trailer_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(movie_of_day + ' trailer')}"
#     st.sidebar.markdown(f"""
#     <a href="{trailer_url}" target="_blank" style="
#         display: inline-block;
#         margin-top: 10px;
#         padding: 8px 12px;
#         background-color: #E50914;
#         color: white;
#         border-radius: 6px;
#         font-weight: 600;
#         text-align: center;
#         text-decoration: none;
#     ">▶ Watch Trailer</a>
#     """, unsafe_allow_html=True)

# #login page

# if menu == "Login":
#     st.title("🔐 Login")
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         name = validate_login(email, password)
#         if name:
#             st.session_state.logged_in = True
#             st.session_state.current_user = name
#             st.success(f"Welcome back, {name}!")
#         else:
#             st.error("Invalid credentials.")


# #signup
# elif menu == "Sign Up":
#     st.title("📝 Sign Up")
#     name = st.text_input("Name")
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     confirm_password = st.text_input("Confirm Password", type="password")
#     if st.button("Register"):
#         if user_exists(email):
#             st.warning("Email already registered.")
#         elif password != confirm_password:
#             st.error("Passwords do not match.")
#         else:
#             add_user(name, email, password)
#             st.success("Registration successful! Please login.")


# #dashboard

# elif menu == "Dashboard":
#     if not st.session_state.logged_in:
#         st.warning("Login first!")
#     else:
#         # Header
#         st.markdown(f"""
#         <div style="background-color:#141414; padding:12px 20px; border-radius:8px; display:flex; align-items:center; gap:12px; margin-bottom:20px;">
#             <div style="width:50px; height:50px; background:#E50914; border-radius:50%; display:flex; justify-content:center; align-items:center; font-weight:bold; font-size:22px; color:white;">
#                 {st.session_state.current_user[0].upper()}
#             </div>
#             <h2 style="margin:0; color:#E50914; font-family:'Poppins', sans-serif;">
#                 Welcome back, {st.session_state.current_user}!
#             </h2>
#         </div>
#         """, unsafe_allow_html=True)
# # Movie select box
#         selected_movie = st.selectbox("🎥 Select a movie", movies['title'].values, key="selected_movie")

#         # Show recommendations button
#         if st.button("Show Recommendations"):
#             with st.spinner("Fetching your movies... 🍿"):
#                 titles, posters = recommend(selected_movie)

#             if titles:
#                 modal_html = """
#                 <style>
#                 .modal-overlay {
#                     position: fixed;
#                     top: 0; left: 0;
#                     width: 100vw; height: 100vh;
#                     background: rgba(0, 0, 0, 0.7);
#                     backdrop-filter: blur(8px);
#                     display: none;
#                     z-index: 10000;
#                     justify-content: center;
#                     align-items: center;
#                 }
#                 .modal-overlay.active {
#                     display: flex;
#                 }
#                 .modal-content {
#                     background-color: #1f1f1f;
#                     color: white;
#                     border-radius: 10px;
#                     width: 90%;
#                     max-width: 320px;
#                     padding: 15px 20px;
#                     box-shadow: 0 0 20px #e50914;
#                     position: relative;
#                     font-family: 'Poppins', sans-serif;
#                     text-align: center;
#                     animation: fadeIn 0.3s ease-in-out;
#                 }
#                 @keyframes fadeIn {
#                     from { opacity: 0; transform: scale(0.9); }
#                     to { opacity: 1; transform: scale(1); }
#                 }
#                 .modal-close {
#                     position: absolute;
#                     top: 8px; right: 12px;
#                     font-size: 22px;
#                     cursor: pointer;
#                     color: #fff;
#                 }
#                 .movie-poster {
#                     width: 150px;
#                     border-radius: 8px;
#                     margin-bottom: 10px;
#                     object-fit: cover;
#                 }
#                 .movie-container {
#                     display: flex;
#                     overflow-x: auto;
#                     gap: 20px;
#                     padding: 10px 0;
#                 }
#                 .movie-card {
#                     width: 140px;
#                     cursor: pointer;
#                     transition: transform 0.3s ease;
#                     background: rgba(255,255,255,0.05);
#                     border-radius: 12px;
#                     box-shadow: 0 0 10px rgba(0,0,0,0.5);
#                     text-align: center;
#                     padding-bottom: 10px;
#                 }
#                 .movie-card:hover {
#                     transform: scale(1.05);
#                     box-shadow: 0 0 20px #E50914;
#                 }
#                 .movie-title {
#                     color:#00C9A7;
#                     margin-top: 4px;
#                     font-size: 13px;
#                     font-weight: bold;
#                     text-shadow: 0 0 5px #00C9A7;
#                 }
#                 .trailer-button {
#                     display: inline-block;
#                     margin-top: 6px;
#                     padding: 5px 8px;
#                     background-color: #E50914;
#                     color: white;
#                     border-radius: 6px;
#                     font-size: 11px;
#                     text-decoration: none;
#                 }
#                 .trailer-button:hover {
#                     background-color: #FF0A16;
#                 }
#                 </style>

#                 <script>
#                 function showModal(poster, title, plot, rating) {
#                     document.getElementById("modal-poster").src = poster;
#                     document.getElementById("modal-title").innerText = title;
#                     document.getElementById("modal-plot").innerText = plot;
#                     document.getElementById("modal-rating").innerText = "⭐ " + rating + " / 10";
#                     document.getElementById("modal").classList.add("active");
#                 }

#                 function hideModal(event) {
#                     if (event.target.id === "modal" || event.target.classList.contains("modal-close")) {
#                         document.getElementById("modal").classList.remove("active");
#                     }
#                 }
#                 </script>

#                 <div id="modal" class="modal-overlay" onclick="hideModal(event)">
#                     <div class="modal-content" id="modal-content">
#                         <span class="modal-close" onclick="hideModal(event)">&times;</span>
#                         <img id="modal-poster" class="movie-poster" src="" />
#                         <h3 id="modal-title" style="font-size: 18px; margin-bottom: 6px;"></h3>
#                         <p id="modal-plot" style="font-size: 13px; color: #ccc; margin-bottom: 8px;"></p>
#                         <p id="modal-rating" style="color: gold; font-size: 14px; font-weight: bold;"></p>
#                     </div>
#                 </div>

#                 <div class="movie-container">
#                 """

#                 for title, poster in zip(titles, posters):
#                     details = fetch_movie_details(title)
#                     plot = details.get("Plot", "No summary available.")
#                     rating = details.get("imdbRating", "N/A")

#                     safe_title = title.replace("'", "\\'")
#                     safe_plot = plot.replace("'", "\\'")

#                     youtube_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(title + ' trailer')}"

#                     modal_html += f"""
#                     <div class="movie-card" onclick="showModal('{poster}', '{safe_title}', '{safe_plot}', '{rating}')">
#                         <img src="{poster}" alt="{safe_title}" class="movie-poster"/>
#                         <div class="movie-title">{safe_title}</div>
#                         <a class="trailer-button" href="{youtube_url}" target="_blank" onclick="event.stopPropagation()">▶ Watch Trailer</a>
#                     </div>
#                     """

#                 modal_html += "</div>"

#                 components.html(modal_html, height=600, scrolling=True)

#             else:
#                 st.warning("No recommendations found.")
# #footer 
# st.markdown("""
#         <style>
#         .footer {
#             position: fixed;
#             left: 0;
#             bottom: 0;
#             width: 100%;
#             background-color: #1f1f1f;
#             color: #E50914;
#             text-align: center;
#             padding: 10px 0;
#             font-family: 'Poppins', sans-serif;
#             font-size: 14px;
#             box-shadow: 0 -1px 5px rgba(0,0,0,0.5);
#             z-index: 9999;
#         }
#         </style>
#         <div class="footer">
#             2025- Smartflix Movie Recommender  | Powered by Streamlit
#         </div>
#         """, unsafe_allow_html=True)
#-------------------------------------------------------------------
#-----------------------------------------------------------------------





# import streamlit as st
# import pandas as pd
# import pickle
# import sqlite3
# import hashlib
# from datetime import datetime, date
# import base64
# import time
# import requests
# import urllib.parse
# from dotenv import load_dotenv
# import os
# import streamlit.components.v1 as components
# import random
# import gdown
# import gspread
# from google.oauth2.service_account import Credentials

# # ----------------------------
# # Load API Key
# # ----------------------------
# load_dotenv()
# OMDB_API_KEY = os.getenv("OMDB_API_KEY")
# placeholder_url = "https://via.placeholder.com/200x300?text=No+Poster"

# #-----------------google sheet setup---------------------- 
# SERVICE_ACCOUNT_FILE = 'path/to/service-account.json'  # <-- Change this to your JSON file path
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# credentials = Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE,
#     scopes=SCOPES
# )

# gc = gspread.authorize(credentials)
# sh = gc.open("users data")  # Your Google Sheet name
# worksheet = sh.sheet1
# # ----------------------------
# # Set Background + Fonts + Theme
# # ----------------------------
# def set_custom_style():
#     st.markdown("""
#     <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
#     <style>
#         html, body, [class*="css"]  {
#             font-family: 'Poppins', sans-serif;
#         }
#         .stApp {
#             background-color: #121212;
#             color: #E0E0E0;
#         }
#         [data-testid="stSidebar"] {
#             background-color: #1f1f1f;
#         }
#         button {
#             background-color: #E50914 !important;
#             color: white !important;
#             border-radius: 8px !important;
#             font-weight: 600 !important;
#         }
#         button:hover {
#             box-shadow: 0 0 10px #E50914;
#         }
#         ::-webkit-scrollbar {
#             height: 8px;
#         }
#         ::-webkit-scrollbar-thumb {
#             background: #E50914;
#             border-radius: 10px;
#         }
#         ::-webkit-scrollbar-track {
#             background: #121212;
#         }
#     </style>
#     """, unsafe_allow_html=True)

# # ----------------------------
# # Load Data
# # ----------------------------
# movies = pd.read_pickle("artificats/movie_list.pkl")

# # Download similarity file from Google Drive if not present locally
# file_id = "1a-bZTigBMJ8bZidn_yBi8IG2zq_H98r8"  # google drive file id
# output = "artificats/similary_list.pkl"

# if not os.path.exists(output):
#     url = f"https://drive.google.com/uc?id={file_id}"
#     gdown.download(url, output, quiet=False)

# @st.cache_data
# def load_similarity(path):
#     return pickle.load(open(path, "rb"))

# similarity = load_similarity(output)

# # ----------------------------
# # OMDB Data
# # ----------------------------
# @st.cache_data(show_spinner=False)
# def fetch_movie_details(title):
#     if not OMDB_API_KEY:
#         return {}
#     try:
#         url = f"http://www.omdbapi.com/?t={urllib.parse.quote(title)}&apikey={OMDB_API_KEY}"
#         response = requests.get(url)
#         return response.json()
#     except:
#         return {}

# @st.cache_data(show_spinner=False)
# def fetch_poster(title):
#     if not OMDB_API_KEY:
#         return placeholder_url
#     try:
#         url = f"http://www.omdbapi.com/?t={urllib.parse.quote(title)}&apikey={OMDB_API_KEY}"
#         response = requests.get(url)
#         data = response.json()
#         return data.get("Poster", placeholder_url) if data.get("Response") == "True" else placeholder_url
#     except:
#         return placeholder_url

# # ----------------------------
# # Recommend Movies
# # ----------------------------
# def recommend(movie):
#     if movie not in movies['title'].values:
#         return [], []
#     idx = movies[movies['title'] == movie].index[0]
#     distances = sorted(list(enumerate(similarity[idx])), key=lambda x: x[1], reverse=True)[1:6]
#     titles, posters = [], []
#     for i in distances:
#         title = movies.iloc[i[0]].title
#         poster = fetch_poster(title)
#         titles.append(title)
#         posters.append(poster)
#     return titles, posters

# # ----------------------------
# # Movie of the Day
# # ----------------------------
# def get_movie_of_the_day():
#     today = str(date.today())  # e.g., '2025-07-04'
#     seed = int(hashlib.sha256(today.encode()).hexdigest(), 16) % (10 ** 8)
#     random.seed(seed)
#     return random.choice(movies['title'].values)

# # ----------------------------
# # SQLite User Auth
# # ----------------------------
# def get_connection():
#     return sqlite3.connect("users.db")

# def init_db():
#     with get_connection() as conn:
#         conn.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 email TEXT PRIMARY KEY,
#                 name TEXT NOT NULL,
#                 password TEXT NOT NULL,
#                 created_at TEXT NOT NULL
#             )
#         """)

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def user_exists(email):
#     with get_connection() as conn:
#         return conn.execute("SELECT 1 FROM users WHERE email = ?", (email,)).fetchone() is not None

# def add_user(name, email, password):
#     with get_connection() as conn:
#         conn.execute(
#             "INSERT INTO users (email, name, password, created_at) VALUES (?, ?, ?, ?)",
#             (email, name, hash_password(password), datetime.now().isoformat())
#         )

# def validate_login(email, password):
#     with get_connection() as conn:
#         result = conn.execute("SELECT name, password FROM users WHERE email = ?", (email,)).fetchone()
#         if result and result[1] == hash_password(password):
#             return result[0]
#         return None

# # ----------------------------
# # App State & Init
# # ----------------------------
# init_db()
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
# if 'current_user' not in st.session_state:
#     st.session_state.current_user = None

# set_custom_style()  # Uncomment if you want custom styles

# # ----------------------------
# # UI Layout
# # ----------------------------
# st.sidebar.title("🎬 Movie App Navigation")
# menu = st.sidebar.radio("Go to", ["Login", "Sign Up", "Dashboard"])

# # Movie of the Day - show only on Dashboard when logged in
# if menu == "Dashboard" and st.session_state.logged_in:
#     st.sidebar.markdown("---")
#     st.sidebar.markdown("🎁 Movie of the Day")
#     movie_of_day = get_movie_of_the_day()
#     poster = fetch_poster(movie_of_day)
#     st.sidebar.image(poster, caption=movie_of_day, use_container_width=True)

#     trailer_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(movie_of_day + ' trailer')}"
#     st.sidebar.markdown(f"""
#     <a href="{trailer_url}" target="_blank" style="
#         display: inline-block;
#         margin-top: 10px;
#         padding: 8px 12px;
#         background-color: #E50914;
#         color: white;
#         border-radius: 6px;
#         font-weight: 600;
#         text-align: center;
#         text-decoration: none;
#     ">▶ Watch Trailer</a>
#     """, unsafe_allow_html=True)

# # Login page
# if menu == "Login":
#     st.title("🔐 Login")
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         name = validate_login(email, password)
#         if name:
#             st.session_state.logged_in = True
#             st.session_state.current_user = name
#             st.success(f"Welcome back, {name}!")
#         else:
#             st.error("Invalid credentials.")

# # Sign up page
# elif menu == "Sign Up":
#     st.title("📝 Sign Up")
#     name = st.text_input("Name")
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     confirm_password = st.text_input("Confirm Password", type="password")
#     if st.button("Register"):
#         if user_exists(email):
#             st.warning("Email already registered.")
#         elif password != confirm_password:
#             st.error("Passwords do not match.")
#         else:
#             add_user(name, email, password)
#             st.success("Registration successful! Please login.")

# # Dashboard
# elif menu == "Dashboard":
#     if not st.session_state.logged_in:
#         st.warning("Login first!")
#     else:
#         st.markdown(f"""
#         <div style="background-color:#141414; padding:12px 20px; border-radius:8px; display:flex; align-items:center; gap:12px; margin-bottom:20px;">
#             <div style="width:50px; height:50px; background:#E50914; border-radius:50%; display:flex; justify-content:center; align-items:center; font-weight:bold; font-size:22px; color:white;">
#                 {st.session_state.current_user[0].upper()}
#             </div>
#             <h2 style="margin:0; color:#E50914; font-family:'Poppins', sans-serif;">
#                 Welcome back, {st.session_state.current_user}!
#             </h2>
#         </div>
#         """, unsafe_allow_html=True)

#         selected_movie = st.selectbox("🎥 Select a movie", movies['title'].values, key="selected_movie")

#         if st.button("Show Recommendations"):
#             with st.spinner("Fetching your movies... 🍿"):
#                 titles, posters = recommend(selected_movie)

#             if titles:
#                 modal_html = """
#                 <style>
#                 .modal-overlay {
#                     position: fixed;
#                     top: 0; left: 0;
#                     width: 100vw; height: 100vh;
#                     background: rgba(0, 0, 0, 0.7);
#                     backdrop-filter: blur(8px);
#                     display: none;
#                     z-index: 10000;
#                     justify-content: center;
#                     align-items: center;
#                 }
#                 .modal-overlay.active {
#                     display: flex;
#                 }
#                 .modal-content {
#                     background-color: #1f1f1f;
#                     color: white;
#                     border-radius: 10px;
#                     width: 90%;
#                     max-width: 320px;
#                     padding: 15px 20px;
#                     box-shadow: 0 0 20px #e50914;
#                     position: relative;
#                     font-family: 'Poppins', sans-serif;
#                     text-align: center;
#                     animation: fadeIn 0.3s ease-in-out;
#                 }
#                 @keyframes fadeIn {
#                     from { opacity: 0; transform: scale(0.9); }
#                     to { opacity: 1; transform: scale(1); }
#                 }
#                 .modal-close {
#                     position: absolute;
#                     top: 8px; right: 12px;
#                     font-size: 22px;
#                     cursor: pointer;
#                     color: #fff;
#                 }
#                 .movie-poster {
#                     width: 150px;
#                     border-radius: 8px;
#                     margin-bottom: 10px;
#                     object-fit: cover;
#                 }
#                 .movie-container {
#                     display: flex;
#                     overflow-x: auto;
#                     gap: 20px;
#                     padding: 10px 0;
#                 }
#                 .movie-card {
#                     width: 140px;
#                     cursor: pointer;
#                     transition: transform 0.3s ease;
#                     background: rgba(255,255,255,0.05);
#                     border-radius: 12px;
#                     box-shadow: 0 0 10px rgba(0,0,0,0.5);
#                     text-align: center;
#                     padding-bottom: 10px;
#                 }
#                 .movie-card:hover {
#                     transform: scale(1.05);
#                     box-shadow: 0 0 20px #E50914;
#                 }
#                 .movie-title {
#                     color:#00C9A7;
#                     margin-top: 4px;
#                     font-size: 13px;
#                     font-weight: bold;
#                     text-shadow: 0 0 5px #00C9A7;
#                 }
#                 .trailer-button {
#                     display: inline-block;
#                     margin-top: 6px;
#                     padding: 5px 8px;
#                     background-color: #E50914;
#                     color: white;
#                     border-radius: 6px;
#                     font-size: 11px;
#                     text-decoration: none;
#                 }
#                 .trailer-button:hover {
#                     background-color: #FF0A16;
#                 }
#                 </style>

#                 <script>
#                 function showModal(poster, title, plot, rating) {
#                     document.getElementById("modal-poster").src = poster;
#                     document.getElementById("modal-title").innerText = title;
#                     document.getElementById("modal-plot").innerText = plot;
#                     document.getElementById("modal-rating").innerText = "⭐ " + rating + " / 10";
#                     document.getElementById("modal").classList.add("active");
#                 }

#                 function hideModal(event) {
#                     if (event.target.id === "modal" || event.target.classList.contains("modal-close")) {
#                         document.getElementById("modal").classList.remove("active");
#                     }
#                 }
#                 </script>

#                 <div id="modal" class="modal-overlay" onclick="hideModal(event)">
#                     <div class="modal-content" id="modal-content">
#                         <span class="modal-close" onclick="hideModal(event)">&times;</span>
#                         <img id="modal-poster" class="movie-poster" src="" />
#                         <h3 id="modal-title" style="font-size: 18px; margin-bottom: 6px;"></h3>
#                         <p id="modal-plot" style="font-size: 13px; color: #ccc; margin-bottom: 8px;"></p>
#                         <p id="modal-rating" style="color: gold; font-size: 14px; font-weight: bold;"></p>
#                     </div>
#                 </div>

#                 <div class="movie-container">
#                 """

#                 for title, poster in zip(titles, posters):
#                     details = fetch_movie_details(title)
#                     plot = details.get("Plot", "No summary available.")
#                     rating = details.get("imdbRating", "N/A")

#                     safe_title = title.replace("'", "\\'")
#                     safe_plot = plot.replace("'", "\\'")

#                     youtube_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(title + ' trailer')}"

#                     modal_html += f"""
#                     <div class="movie-card" onclick="showModal('{poster}', '{safe_title}', '{safe_plot}', '{rating}')">
#                         <img src="{poster}" alt="{safe_title}" class="movie-poster"/>
#                         <div class="movie-title">{safe_title}</div>
#                         <a class="trailer-button" href="{youtube_url}" target="_blank" onclick="event.stopPropagation()">▶ Watch Trailer</a>
#                     </div>
#                     """

#                 modal_html += "</div>"

#                 components.html(modal_html, height=600, scrolling=True)

#             else:
#                 st.warning("No recommendations found.")

# # Footer
# st.markdown("""
#     <style>
#     .footer {
#         position: fixed;
#         left: 0;
#         bottom: 0;
#         width: 100%;
#         background-color: #1f1f1f;
#         color: #E50914;
#         text-align: center;
#         padding: 10px 0;
#         font-family: 'Poppins', sans-serif;
#         font-size: 14px;
#         box-shadow: 0 -1px 5px rgba(0,0,0,0.5);
#         z-index: 9999;
#     }
#     </style>
#     <div class="footer">
#         2025- Smartflix Movie Recommender  | Powered by Streamlit
#     </div>
# """, unsafe_allow_html=True)

#--------------------------------------------------------------------------------------------



# import streamlit as st
# import pandas as pd
# import pickle
# import hashlib
# from datetime import datetime, date
# import base64
# import time
# import requests
# import urllib.parse
# from dotenv import load_dotenv
# import os
# import streamlit.components.v1 as components
# import random
# import gdown
# import gspread
# from google.oauth2.service_account import Credentials
# from pytz import timezone
# import json

# # ----------------------------
# # Load API Key
# # ----------------------------
# load_dotenv()
# OMDB_API_KEY = os.getenv("OMDB_API_KEY")
# placeholder_url = "https://via.placeholder.com/200x300?text=No+Poster"

# # ----------------------------
# # Google Sheets Setup for Users
# # ----------------------------
# # SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# # Streamlit Secrets se service account JSON load karo
# service_account_info = json.loads(st.secrets["gcp_service_account"]["json"])

# credentials = service_account.Credentials.from_service_account_info(
#     service_account_info,
#     scopes=SCOPES
# )

# gc = gspread.authorize(credentials)
# sh = gc.open("users data")  # Your Google Sheet name
# worksheet = sh.sheet1
# # ----------------------------
# # Set Background + Fonts + Theme
# # ----------------------------
# def set_custom_style():
#     st.markdown("""
#     <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
#     <style>
#         html, body, [class*="css"]  {
#             font-family: 'Poppins', sans-serif;
#         }
#         .stApp {
#             background-color: #121212;
#             color: #E0E0E0;
#         }
#         [data-testid="stSidebar"] {
#             background-color: #1f1f1f;
#         }
#         button {
#             background-color: #E50914 !important;
#             color: white !important;
#             border-radius: 8px !important;
#             font-weight: 600 !important;
#         }
#         button:hover {
#             box-shadow: 0 0 10px #E50914;
#         }
#         ::-webkit-scrollbar {
#             height: 8px;
#         }
#         ::-webkit-scrollbar-thumb {
#             background: #E50914;
#             border-radius: 10px;
#         }
#         ::-webkit-scrollbar-track {
#             background: #121212;
#         }
#     </style>
#     """, unsafe_allow_html=True)

# # ----------------------------
# # Load Data
# # ----------------------------
# movies = pd.read_pickle("artificats/movie_list.pkl")

# file_id = "1a-bZTigBMJ8bZidn_yBi8IG2zq_H98r8"
# output = "artificats/similary_list.pkl"

# if not os.path.exists(output):
#     url = f"https://drive.google.com/uc?id={file_id}"
#     gdown.download(url, output, quiet=False)

# @st.cache_data
# def load_similarity(path):
#     return pickle.load(open(path, "rb"))

# similarity = load_similarity(output)

# # ----------------------------
# # OMDB Data Functions (unchanged)
# # ----------------------------
# @st.cache_data(show_spinner=False)
# def fetch_movie_details(title):
#     if not OMDB_API_KEY:
#         return {}
#     try:
#         url = f"http://www.omdbapi.com/?t={urllib.parse.quote(title)}&apikey={OMDB_API_KEY}"
#         response = requests.get(url)
#         return response.json()
#     except:
#         return {}

# @st.cache_data(show_spinner=False)
# def fetch_poster(title):
#     if not OMDB_API_KEY:
#         return placeholder_url
#     try:
#         url = f"http://www.omdbapi.com/?t={urllib.parse.quote(title)}&apikey={OMDB_API_KEY}"
#         response = requests.get(url)
#         data = response.json()
#         return data.get("Poster", placeholder_url) if data.get("Response") == "True" else placeholder_url
#     except:
#         return placeholder_url

# # ----------------------------
# # Recommend Movies (unchanged)
# # ----------------------------
# def recommend(movie):
#     if movie not in movies['title'].values:
#         return [], []
#     idx = movies[movies['title'] == movie].index[0]
#     distances = sorted(list(enumerate(similarity[idx])), key=lambda x: x[1], reverse=True)[1:6]
#     titles, posters = [], []
#     for i in distances:
#         title = movies.iloc[i[0]].title
#         poster = fetch_poster(title)
#         titles.append(title)
#         posters.append(poster)
#     return titles, posters

# # ----------------------------
# # Movie of the Day (unchanged)
# # ----------------------------
# def get_movie_of_the_day():
#     today = str(date.today())
#     seed = int(hashlib.sha256(today.encode()).hexdigest(), 16) % (10 ** 8)
#     random.seed(seed)
#     return random.choice(movies['title'].values)

# # ----------------------------
# # Google Sheets User Auth Functions
# # ----------------------------

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def user_exists(email):
#     users = worksheet.get_all_records()
#     return any(user['email'] == email for user in users)

# # def add_user(name, email, password):
# #     hashed_pw = hash_password(password)
# #     created_at = datetime.now().isoformat()
# #     worksheet.append_row([name, email, password, created_at])


# def validate_login(email, password):
#     hashed_pw = hash_password(password)
#     users = worksheet.get_all_records()
#     for user in users:
#         if user['email'] == email and user['password'] == hashed_pw:
#             return user['name']
#     return None

# # ----------------------------
# # App State & Init
# # ----------------------------
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
# if 'current_user' not in st.session_state:
#     st.session_state.current_user = None

# set_custom_style()

# # ----------------------------
# # UI Layout
# # ----------------------------
# st.sidebar.title("🎬 Movie App Navigation")
# menu = st.sidebar.radio("Go to", ["Login", "Sign Up", "Dashboard"])

# if menu == "Dashboard" and st.session_state.logged_in:
#     st.sidebar.markdown("---")
#     st.sidebar.markdown("🎁 Movie of the Day")
#     movie_of_day = get_movie_of_the_day()
#     poster = fetch_poster(movie_of_day)
#     st.sidebar.image(poster, caption=movie_of_day, use_container_width=True)

#     trailer_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(movie_of_day + ' trailer')}"
#     st.sidebar.markdown(f"""
#     <a href="{trailer_url}" target="_blank" style="
#         display: inline-block;
#         margin-top: 10px;
#         padding: 8px 12px;
#         background-color: #E50914;
#         color: white;
#         border-radius: 6px;
#         font-weight: 600;
#         text-align: center;
#         text-decoration: none;
#     ">▶ Watch Trailer</a>
#     """, unsafe_allow_html=True)

# if menu == "Login":
#     st.title("🔐 Login")
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         name = validate_login(email, password)
#         if name:
#             st.session_state.logged_in = True
#             st.session_state.current_user = name
#             st.success(f"Welcome back, {name}!")
#         else:
#             st.error("Invalid credentials.")

# elif menu == "Sign Up":
#     st.title("📝 Sign Up")
#     name = st.text_input("Name")
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     confirm_password = st.text_input("Confirm Password", type="password")
#     if st.button("Register"):
#         if user_exists(email):
#             st.warning("Email already registered.")
#         elif password != confirm_password:
#             st.error("Passwords do not match.")
#         else:
#             add_user(name, email, password)
#             st.success("Registration successful! Please login.")

# elif menu == "Dashboard":
#     if not st.session_state.logged_in:
#         st.warning("Login first!")
#     else:
#         # Welcome header
#         st.markdown(f"""
#         <div style="background-color:#141414; padding:12px 20px; border-radius:8px; display:flex; align-items:center; gap:12px; margin-bottom:20px;">
#             <div style="width:50px; height:50px; background:#E50914; border-radius:50%; display:flex; justify-content:center; align-items:center; font-weight:bold; font-size:22px; color:white;">
#                 {st.session_state.current_user[0].upper()}
#             </div>
#             <h2 style="margin:0; color:#E50914; font-family:'Poppins', sans-serif;">
#                 Welcome back, {st.session_state.current_user}!
#             </h2>
#         </div>
#         """, unsafe_allow_html=True)

#         selected_movie = st.selectbox("🎥 Select a movie", movies['title'].values, key="selected_movie")

#         if st.button("Show Recommendations"):
#             with st.spinner("Fetching your movies... 🍿"):
#                 titles, posters = recommend(selected_movie)

#             if titles:
#                 modal_html = """
#                 <style>
#                 .modal-overlay {
#                     position: fixed;
#                     top: 0; left: 0;
#                     width: 100vw; height: 100vh;
#                     background: rgba(0, 0, 0, 0.7);
#                     backdrop-filter: blur(8px);
#                     display: none;
#                     z-index: 10000;
#                     justify-content: center;
#                     align-items: center;
#                 }
#                 .modal-overlay.active {
#                     display: flex;
#                 }
#                 .modal-content {
#                     background-color: #1f1f1f;
#                     color: white;
#                     border-radius: 10px;
#                     width: 90%;
#                     max-width: 320px;
#                     padding: 15px 20px;
#                     box-shadow: 0 0 20px #e50914;
#                     position: relative;
#                     font-family: 'Poppins', sans-serif;
#                     text-align: center;
#                     animation: fadeIn 0.3s ease-in-out;
#                 }
#                 @keyframes fadeIn {
#                     from { opacity: 0; transform: scale(0.9); }
#                     to { opacity: 1; transform: scale(1); }
#                 }
#                 .modal-close {
#                     position: absolute;
#                     top: 8px; right: 12px;
#                     font-size: 22px;
#                     cursor: pointer;
#                     color: #fff;
#                 }
#                 .movie-poster {
#                     width: 150px;
#                     border-radius: 8px;
#                     margin-bottom: 10px;
#                     object-fit: cover;
#                 }
#                 .movie-container {
#                     display: flex;
#                     overflow-x: auto;
#                     gap: 20px;
#                     padding: 10px 0;
#                 }
#                 .movie-card {
#                     width: 140px;
#                     cursor: pointer;
#                     transition: transform 0.3s ease;
#                     background: rgba(255,255,255,0.05);
#                     border-radius: 12px;
#                     box-shadow: 0 0 10px rgba(0,0,0,0.5);
#                     text-align: center;
#                     padding-bottom: 10px;
#                 }
#                 .movie-card:hover {
#                     transform: scale(1.05);
#                     box-shadow: 0 0 20px #E50914;
#                 }
#                 .movie-title {
#                     color:#00C9A7;
#                     margin-top: 4px;
#                     font-size: 13px;
#                     font-weight: bold;
#                     text-shadow: 0 0 5px #00C9A7;
#                 }
#                 .trailer-button {
#                     display: inline-block;
#                     margin-top: 6px;
#                     padding: 5px 8px;
#                     background-color: #E50914;
#                     color: white;
#                     border-radius: 6px;
#                     font-size: 11px;
#                     text-decoration: none;
#                 }
#                 .trailer-button:hover {
#                     background-color: #FF0A16;
#                 }
#                 </style>

#                 <script>
#                 function showModal(poster, title, plot, rating) {
#                     document.getElementById("modal-poster").src = poster;
#                     document.getElementById("modal-title").innerText = title;
#                     document.getElementById("modal-plot").innerText = plot;
#                     document.getElementById("modal-rating").innerText = "⭐ " + rating + " / 10";
#                     document.getElementById("modal").classList.add("active");
#                 }

#                 function hideModal(event) {
#                     if (event.target.id === "modal" || event.target.classList.contains("modal-close")) {
#                         document.getElementById("modal").classList.remove("active");
#                     }
#                 }
#                 </script>

#                 <div id="modal" class="modal-overlay" onclick="hideModal(event)">
#                     <div class="modal-content" id="modal-content">
#                         <span class="modal-close" onclick="hideModal(event)">&times;</span>
#                         <img id="modal-poster" class="movie-poster" src="" />
#                         <h3 id="modal-title" style="font-size: 18px; margin-bottom: 6px;"></h3>
#                         <p id="modal-plot" style="font-size: 13px; color: #ccc; margin-bottom: 8px;"></p>
#                         <p id="modal-rating" style="color: gold; font-size: 14px; font-weight: bold;"></p>
#                     </div>
#                 </div>

#                 <div class="movie-container">
#                 """

#                 for title, poster in zip(titles, posters):
#                     details = fetch_movie_details(title)
#                     plot = details.get("Plot", "No summary available.")
#                     rating = details.get("imdbRating", "N/A")

#                     safe_title = title.replace("'", "\\'")
#                     safe_plot = plot.replace("'", "\\'")

#                     youtube_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(title + ' trailer')}"

#                     modal_html += f"""
#                     <div class="movie-card" onclick="showModal('{poster}', '{safe_title}', '{safe_plot}', '{rating}')">
#                         <img src="{poster}" alt="{safe_title}" class="movie-poster"/>
#                         <div class="movie-title">{safe_title}</div>
#                         <a class="trailer-button" href="{youtube_url}" target="_blank" onclick="event.stopPropagation()">▶ Watch Trailer</a>
#                     </div>
#                     """

#                 modal_html += "</div>"

#                 components.html(modal_html, height=600, scrolling=True)

#             else:
#                 st.warning("No recommendations found.")

# # Footer (unchanged)
# st.markdown("""
#     <style>
#     .footer {
#         position: fixed;
#         left: 0;
#         bottom: 0;
#         width: 100%;
#         background-color: #1f1f1f;
#         color: #E50914;
#         text-align: center;
#         padding: 10px 0;
#         font-family: 'Poppins', sans-serif;
#         font-size: 14px;
#         box-shadow: 0 -1px 5px rgba(0,0,0,0.5);
#         z-index: 9999;
#     }
#     </style>
#     <div class="footer">
#         2025- Smartflix Movie Recommender  | Powered by Streamlit
#     </div>
# """, unsafe_allow_html=True)



#-------------------------------------------------------------------------
# app.py

# import streamlit as st
# import pandas as pd
# import pickle
# import sqlite3
# import hashlib
# from datetime import datetime, date
# import os
# import requests
# import urllib.parse
# import random
# import gdown
# from dotenv import load_dotenv
# import streamlit.components.v1 as components

# # ----------------------------
# # Load .env
# # ----------------------------
# load_dotenv()
# OMDB_API_KEY = os.getenv("OMDB_API_KEY")
# placeholder_url = "https://via.placeholder.com/200x300?text=No+Poster"

# # ----------------------------
# # Custom Style
# # ----------------------------
# def set_custom_style():
#     st.markdown("""
#     <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
#     <style>
#         html, body, [class*="css"]  {
#             font-family: 'Poppins', sans-serif;
#         }
#         .stApp {
#             background-color: #121212;
#             color: #E0E0E0;
#         }
#         [data-testid="stSidebar"] {
#             background-color: #1f1f1f;
#         }
#         button {
#             background-color: #E50914 !important;
#             color: white !important;
#             border-radius: 8px !important;
#             font-weight: 600 !important;
#         }
#         button:hover {
#             box-shadow: 0 0 10px #E50914;
#         }
#     </style>
#     """, unsafe_allow_html=True)

# # ----------------------------
# # Data Loaders
# # ----------------------------
# movies = pd.read_pickle("artificats/movie_list.pkl")

# similarity_path = "artificats/similary_list.pkl"
# if not os.path.exists(similarity_path):
#     file_id = "1a-bZTigBMJ8bZidn_yBi8IG2zq_H98r8"
#     gdown.download(f"https://drive.google.com/uc?id={file_id}", similarity_path, quiet=False)

# @st.cache_data
# def load_similarity(path):
#     return pickle.load(open(path, "rb"))

# similarity = load_similarity(similarity_path)

# # ----------------------------
# # Movie Helpers
# # ----------------------------
# @st.cache_data
# def fetch_poster(title):
#     try:
#         url = f"http://www.omdbapi.com/?t={urllib.parse.quote(title)}&apikey={OMDB_API_KEY}"
#         r = requests.get(url).json()
#         return r.get("Poster", placeholder_url)
#     except:
#         return placeholder_url

# @st.cache_data
# def fetch_movie_details(title):
#     try:
#         url = f"http://www.omdbapi.com/?t={urllib.parse.quote(title)}&apikey={OMDB_API_KEY}"
#         return requests.get(url).json()
#     except:
#         return {}

# def recommend(movie):
#     if movie not in movies['title'].values:
#         return [], []
#     idx = movies[movies['title'] == movie].index[0]
#     distances = sorted(list(enumerate(similarity[idx])), key=lambda x: x[1], reverse=True)[1:6]
#     titles, posters = [], []
#     for i in distances:
#         t = movies.iloc[i[0]].title
#         titles.append(t)
#         posters.append(fetch_poster(t))
#     return titles, posters

# def get_movie_of_the_day():
#     seed = int(hashlib.sha256(str(date.today()).encode()).hexdigest(), 16) % (10 ** 8)
#     random.seed(seed)
#     return random.choice(movies['title'].values)

# # ----------------------------
# # SQLite Auth
# # ----------------------------
# def get_conn():
#     return sqlite3.connect("users.db")

# def init_db():
#     with get_conn() as conn:
#         conn.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             email TEXT PRIMARY KEY,
#             name TEXT NOT NULL,
#             password TEXT NOT NULL,
#             created_at TEXT NOT NULL
#         )""")

# def hash_pw(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def add_user(name, email, password):
#     with get_conn() as conn:
#         conn.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
#             (email, name, hash_pw(password), datetime.now().isoformat()))

# def user_exists(email):
#     with get_conn() as conn:
#         return conn.execute("SELECT 1 FROM users WHERE email=?", (email,)).fetchone() is not None

# def validate_login(email, password):
#     with get_conn() as conn:
#         r = conn.execute("SELECT name, password FROM users WHERE email=?", (email,)).fetchone()
#         return r[0] if r and r[1] == hash_pw(password) else None

# # ----------------------------
# # Init State
# # ----------------------------
# init_db()
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
# if 'current_user' not in st.session_state:
#     st.session_state.current_user = None

# set_custom_style()

# # ----------------------------
# # Sidebar Navigation
# # ----------------------------
# st.sidebar.title("🎬 Movie App Navigation")
# menu = st.sidebar.radio("Go to", ["Login", "Sign Up", "Dashboard"])

# if menu == "Dashboard" and st.session_state.logged_in:
#     st.sidebar.markdown("---")
#     st.sidebar.markdown("🎁 Movie of the Day")
#     motd = get_movie_of_the_day()
#     st.sidebar.image(fetch_poster(motd), caption=motd, use_container_width=True)
#     trailer_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(motd + ' trailer')}"
#     st.sidebar.markdown(f'<a href="{trailer_url}" target="_blank">▶ Watch Trailer</a>', unsafe_allow_html=True)

# # ----------------------------
# # Login Page
# # ----------------------------
# if menu == "Login":
#     st.title("🔐 Login")
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         name = validate_login(email, password)
#         if name:
#             st.session_state.logged_in = True
#             st.session_state.current_user = name
#             st.success(f"Welcome, {name}!")
#         else:
#             st.error("Invalid credentials.")

# # ----------------------------
# # Sign Up Page
# # ----------------------------
# elif menu == "Sign Up":
#     st.title("📝 Register")
#     name = st.text_input("Name")
#     email = st.text_input("Email")
#     pw1 = st.text_input("Password", type="password")
#     pw2 = st.text_input("Confirm Password", type="password")
#     if st.button("Register"):
#         if user_exists(email):
#             st.warning("Email already registered.")
#         elif pw1 != pw2:
#             st.error("Passwords don't match.")
#         else:
#             add_user(name, email, pw1)
#             st.success("Registration complete!")

# # ----------------------------
# # Dashboard
# # ----------------------------
# elif menu == "Dashboard":
#     if not st.session_state.logged_in:
#         st.warning("Please login to continue.")
#     else:
#         # Movie of the Day poster in sidebar (ensure only once here)
#         st.sidebar.markdown("---")
#         st.sidebar.markdown("🎁 Movie of the Day")
#         movie_of_day = get_movie_of_the_day()
#         poster = fetch_poster(movie_of_day)
#         st.sidebar.image(poster, caption=movie_of_day, use_container_width=True)
        
#         trailer_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(movie_of_day + ' trailer')}"
#         st.sidebar.markdown(f"""
#         <a href="{trailer_url}" target="_blank" style="
#             display: inline-block;
#             margin-top: 10px;
#             padding: 8px 12px;
#             background-color: #E50914;
#             color: white;
#             border-radius: 6px;
#             font-weight: 600;
#             text-align: center;
#             text-decoration: none;
#         ">▶ Watch Trailer</a>
#         """, unsafe_allow_html=True)

#         # Welcome message
#         st.markdown(f"""
#         <div style="background-color:#141414; padding:12px 20px; border-radius:8px; display:flex; align-items:center; gap:12px; margin-bottom:20px;">
#             <div style="width:50px; height:50px; background:#E50914; border-radius:50%; display:flex; justify-content:center; align-items:center; font-weight:bold; font-size:22px; color:white;">
#                 {st.session_state.current_user[0].upper()}
#             </div>
#             <h2 style="margin:0; color:#E50914;">Welcome, {st.session_state.current_user}!</h2>
#         </div>
#         """, unsafe_allow_html=True)

#         selected_movie = st.selectbox("🎥 Select a movie", movies['title'].values)
#         if st.button("Show Recommendations"):
#             titles, posters = recommend(selected_movie)

#             if titles:
#                 # Container to hold movie details on poster click
#                 details_container = st.empty()

#                 # Create clickable posters with buttons for each recommended movie
#                 cols = st.columns(len(titles))
#                 for i, (title, poster_url) in enumerate(zip(titles, posters)):
#                     with cols[i]:
#                         if st.button("", key=f"btn_{title}"):
#                             # Show movie details below on click
#                             details_container.markdown(f"""
#                                 ### {title}
#                                 ![poster]({poster_url})
#                                 *More details about the movie can be shown here...*
#                             """)
                        
#                         # Display poster image under the button (simulate clickable poster)
#                         st.image(poster_url, use_container_width=True)

#             else:
#                 st.error("No recommendations found.")

# # ----------------------------
# # Footer
# # ----------------------------
# st.markdown("""
# <style>
# .footer {
#     position: fixed;
#     left: 0;
#     bottom: 0;
#     width: 100%;
#     background: #1f1f1f;
#     color: #E50914;
#     text-align: center;
#     padding: 10px;
#     font-size: 13px;
# }
# </style>
# <div class="footer">
#     &copy; 2025 - Smartflix Movie Recommender | Built with ❤️ in Streamlit
# </div>
# """, unsafe_allow_html=True)

#-------------------------------------------
import streamlit as st
import pandas as pd
import pickle
import sqlite3
import hashlib
from datetime import datetime, date
import base64
import time
import requests
import urllib.parse
from dotenv import load_dotenv
import os
import streamlit.components.v1 as components
import random
import gdown
import gspread
from google.oauth2.service_account import Credentials

# ----------------------------
# Load API Key
# ----------------------------
load_dotenv()

# OMDB_API_KEY = os.getenv("OMDB_API_KEY")
# 
# #st.write("👉 OMDB_API_KEY =", repr(OMDB_API_KEY))
# st.write("Loaded API Key:", OMDB_API_KEY)
OMDB_API_KEY = os.getenv("OMDB_API_KEY") or st.secrets.get("OMDB_API_KEY")
placeholder_url = "https://via.placeholder.com/200x300?text=No+Poster"
#st.write("Loaded API Key:", OMDB_API_KEY)

# st.write("OMDB API Key:", OMDB_API_KEY if OMDB_API_KEY else "No API key found")

# ----------------------------
# Set Background + Fonts + Theme
# ----------------------------
def set_custom_style():
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
        }
        .stApp {
            background-color: #121212;
            color: #E0E0E0;
        }
        [data-testid="stSidebar"] {
            background-color: #1f1f1f;
        }
        button {
            background-color: #E50914 !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }
        button:hover {
            box-shadow: 0 0 10px #E50914;
        }
        ::-webkit-scrollbar {
            height: 8px;
        }
        ::-webkit-scrollbar-thumb {
            background: #E50914;
            border-radius: 10px;
        }
        ::-webkit-scrollbar-track {
            background: #121212;
        }
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# Load Data
# ----------------------------
movies = pd.read_pickle("artificats/movie_list.pkl")

# Download similarity file from Google Drive if not present locally
file_id = "1a-bZTigBMJ8bZidn_yBi8IG2zq_H98r8"  # google drive file id
output = "artificats/similary_list.pkl"

if not os.path.exists(output):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output, quiet=False)

@st.cache_data
def load_similarity(path):
    return pickle.load(open(path, "rb"))

similarity = load_similarity(output)

# ----------------------------
# OMDB Data
# ----------------------------
@st.cache_data(show_spinner=False)
# def fetch_movie_details(title):
#     if not OMDB_API_KEY:
#         return {}
#     try:
#         url = f"http://www.omdbapi.com/?t={urllib.parse.quote(title)}&apikey={OMDB_API_KEY}"
#         response = requests.get(url)
#         return response.json()
#     except:
#         return {}
# ----------------------------
# OMDB Data
# ----------------------------
def fetch_movie_details(title):
    if not OMDB_API_KEY:
        st.error("OMDB API Key not found!")
        return {}
    try:
        url = f"http://www.omdbapi.com/?t={urllib.parse.quote(title)}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        if response.status_code != 200:
            st.error(f"OMDB API request failed: {response.status_code}")
            return {}
        data = response.json()
        if data.get("Response") == "False":
            st.error(f"OMDB API error: {data.get('Error')}")
            return {}
        return data
    except Exception as e:
        st.error(f"Exception during API call: {str(e)}")
        return {}


@st.cache_data(show_spinner=False)
def fetch_poster(title):
    if not OMDB_API_KEY:
        return placeholder_url
    try:
        url = f"http://www.omdbapi.com/?t={urllib.parse.quote(title)}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        data = response.json()
        return data.get("Poster", placeholder_url) if data.get("Response") == "True" else placeholder_url
    except:
        return placeholder_url

# ----------------------------
# Recommend Movies
# ----------------------------
def recommend(movie):
    if movie not in movies['title'].values:
        return [], []
    idx = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[idx])), key=lambda x: x[1], reverse=True)[1:6]
    titles, posters = [], []
    for i in distances:
        title = movies.iloc[i[0]].title
        poster = fetch_poster(title)
        titles.append(title)
        posters.append(poster)
    return titles, posters

# ----------------------------
# Movie of the Day
# ----------------------------
def get_movie_of_the_day():
    today = str(date.today())  # e.g., '2025-07-04'
    seed = int(hashlib.sha256(today.encode()).hexdigest(), 16) % (10 ** 8)
    random.seed(seed)
    return random.choice(movies['title'].values)

# ----------------------------
# SQLite User Auth
# ----------------------------
def get_connection():
    return sqlite3.connect("users.db")

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(email):
    with get_connection() as conn:
        return conn.execute("SELECT 1 FROM users WHERE email = ?", (email,)).fetchone() is not None

def add_user(name, email, password):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO users (email, name, password, created_at) VALUES (?, ?, ?, ?)",
            (email, name, hash_password(password), datetime.now().isoformat())
        )

def validate_login(email, password):
    with get_connection() as conn:
        result = conn.execute("SELECT name, password FROM users WHERE email = ?", (email,)).fetchone()
        if result and result[1] == hash_password(password):
            return result[0]
        return None

# ----------------------------
# App State & Init
# ----------------------------
init_db()
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

set_custom_style()  # Uncomment if you want custom styles

# ----------------------------
# UI Layout
# ----------------------------
st.sidebar.title("🎬 Movie App Navigation")
menu = st.sidebar.radio("Go to", ["Login", "Sign Up", "Dashboard"])

# Movie of the Day - show only on Dashboard when logged in
if menu == "Dashboard" and st.session_state.logged_in:
    st.sidebar.markdown("---")
    st.sidebar.markdown("🎁 Movie of the Day")
    movie_of_day = get_movie_of_the_day()
    poster = fetch_poster(movie_of_day)
    st.sidebar.image(poster, caption=movie_of_day, use_container_width=True)

    trailer_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(movie_of_day + ' trailer')}"
    st.sidebar.markdown(f"""
    <a href="{trailer_url}" target="_blank" style="
        display: inline-block;
        margin-top: 10px;
        padding: 8px 12px;
        background-color: #E50914;
        color: white;
        border-radius: 6px;
        font-weight: 600;
        text-align: center;
        text-decoration: none;
    ">▶ Watch Trailer</a>
    """, unsafe_allow_html=True)

# Login page
if menu == "Login":
    st.title("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        name = validate_login(email, password)
        if name:
            st.session_state.logged_in = True
            st.session_state.current_user = name
            st.success(f"Welcome back, {name}!")
        else:
            st.error("Invalid credentials.")

# Sign up page
elif menu == "Sign Up":
    st.title("📝 Sign Up")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Register"):
        if user_exists(email):
            st.warning("Email already registered.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            add_user(name, email, password)
            st.success("Registration successful! Please login.")

# Dashboard
elif menu == "Dashboard":
    if not st.session_state.logged_in:
        st.warning("Login first!")
    else:
        st.markdown(f"""
        <div style="background-color:#141414; padding:12px 20px; border-radius:8px; display:flex; align-items:center; gap:12px; margin-bottom:20px;">
            <div style="width:50px; height:50px; background:#E50914; border-radius:50%; display:flex; justify-content:center; align-items:center; font-weight:bold; font-size:22px; color:white;">
                {st.session_state.current_user[0].upper()}
            </div>
            <h2 style="margin:0; color:#E50914; font-family:'Poppins', sans-serif;">
                Welcome back, {st.session_state.current_user}!
            </h2>
        </div>
        """, unsafe_allow_html=True)

        selected_movie = st.selectbox("🎥 Select a movie", movies['title'].values, key="selected_movie")

        if st.button("Show Recommendations"):
            with st.spinner("Fetching your movies... 🍿"):
                titles, posters = recommend(selected_movie)

            if titles:
                modal_html = """
                <style>
                .modal-overlay {
                    position: fixed;
                    top: 0; left: 0;
                    width: 100vw; height: 100vh;
                    background: rgba(0, 0, 0, 0.7);
                    backdrop-filter: blur(8px);
                    display: none;
                    z-index: 10000;
                    justify-content: center;
                    align-items: center;
                }
                .modal-overlay.active {
                    display: flex;
                }
                .modal-content {
                    background-color: #1f1f1f;
                    color: white;
                    border-radius: 10px;
                    width: 90%;
                    max-width: 320px;
                    padding: 15px 20px;
                    box-shadow: 0 0 20px #e50914;
                    position: relative;
                    font-family: 'Poppins', sans-serif;
                    text-align: center;
                    animation: fadeIn 0.3s ease-in-out;
                }
                @keyframes fadeIn {
                    from { opacity: 0; transform: scale(0.9); }
                    to { opacity: 1; transform: scale(1); }
                }
                .modal-close {
                    position: absolute;
                    top: 8px; right: 12px;
                    font-size: 22px;
                    cursor: pointer;
                    color: #fff;
                }
                .movie-poster {
                    width: 150px;
                    border-radius: 8px;
                    margin-bottom: 10px;
                    object-fit: cover;
                }
                .movie-container {
                    display: flex;
                    overflow-x: auto;
                    gap: 20px;
                    padding: 10px 0;
                }
                .movie-card {
                    width: 140px;
                    cursor: pointer;
                    transition: transform 0.3s ease;
                    background: rgba(255,255,255,0.05);
                    border-radius: 12px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.5);
                    text-align: center;
                    padding-bottom: 10px;
                }
                .movie-card:hover {
                    transform: scale(1.05);
                    box-shadow: 0 0 20px #E50914;
                }
                .movie-title {
                    color:#00C9A7;
                    margin-top: 4px;
                    font-size: 13px;
                    font-weight: bold;
                    text-shadow: 0 0 5px #00C9A7;
                }
                .trailer-button {
                    display: inline-block;
                    margin-top: 6px;
                    padding: 5px 8px;
                    background-color: #E50914;
                    color: white;
                    border-radius: 6px;
                    font-size: 11px;
                    text-decoration: none;
                }
                .trailer-button:hover {
                    background-color: #FF0A16;
                }
                </style>

                <script>
                function showModal(poster, title, plot, rating) {
                    document.getElementById("modal-poster").src = poster;
                    document.getElementById("modal-title").innerText = title;
                    document.getElementById("modal-plot").innerText = plot;
                    document.getElementById("modal-rating").innerText = "⭐ " + rating + " / 10";
                    document.getElementById("modal").classList.add("active");
                }

                function hideModal(event) {
                    if (event.target.id === "modal" || event.target.classList.contains("modal-close")) {
                        document.getElementById("modal").classList.remove("active");
                    }
                }
                </script>

                <div id="modal" class="modal-overlay" onclick="hideModal(event)">
                    <div class="modal-content" id="modal-content">
                        <span class="modal-close" onclick="hideModal(event)">&times;</span>
                        <img id="modal-poster" class="movie-poster" src="" />
                        <h3 id="modal-title" style="font-size: 18px; margin-bottom: 6px;"></h3>
                        <p id="modal-plot" style="font-size: 13px; color: #ccc; margin-bottom: 8px;"></p>
                        <p id="modal-rating" style="color: gold; font-size: 14px; font-weight: bold;"></p>
                    </div>
                </div>

                <div class="movie-container">
                """

                for title, poster in zip(titles, posters):
                    details = fetch_movie_details(title)
                    plot = details.get("Plot", "No summary available.")
                    rating = details.get("imdbRating", "N/A")

                    safe_title = title.replace("'", "\\'")
                    safe_plot = plot.replace("'", "\\'")

                    youtube_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(title + ' trailer')}"

                    modal_html += f"""
                    <div class="movie-card" onclick="showModal('{poster}', '{safe_title}', '{safe_plot}', '{rating}')">
                        <img src="{poster}" alt="{safe_title}" class="movie-poster"/>
                        <div class="movie-title">{safe_title}</div>
                        <a class="trailer-button" href="{youtube_url}" target="_blank" onclick="event.stopPropagation()">▶ Watch Trailer</a>
                    </div>
                    """

                modal_html += "</div>"

                components.html(modal_html, height=600, scrolling=True)

            else:
                st.warning("No recommendations found.")

# Footer
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #1f1f1f;
        color: #E50914;
        text-align: center;
        padding: 10px 0;
        font-family: 'Poppins', sans-serif;
        font-size: 14px;
        box-shadow: 0 -1px 5px rgba(0,0,0,0.5);
        z-index: 9999;
    }
    </style>
    <div class="footer">
        2025- Smartflix Movie Recommender  | Powered by Streamlit
    </div>
""", unsafe_allow_html=True)