import streamlit as st
import random

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Smart Learning Hub: Animated Arcade",
    page_icon="🎮",
    layout="centered"
)

# Styling CSS Kustom (Estetik, Animasi Halus, Tidak Nabrak)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');

    .stApp {
        background: radial-gradient(circle at center, #111827 0%, #030712 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f3f4f6;
    }

    .arcade-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 2rem;
        text-align: center;
        background: linear-gradient(135deg, #38bdf8 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }

    .arcade-subtitle {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        color: #9ca3af;
        font-size: 0.8rem;
        letter-spacing: 2px;
        margin-bottom: 20px;
    }

    .game-arena {
        background: rgba(17, 24, 39, 0.75);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
        margin-bottom: 20px;
    }

    .status-panel {
        display: flex;
        justify-content: space-around;
        background: rgba(31, 41, 55, 0.9);
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #4b5563;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.85rem;
        margin-bottom: 15px;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        padding: 12px;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        transition: all 0.2s ease-in-out;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6);
        background: linear-gradient(135deg, #60a5fa 0%, #a855f7 100%);
    }

    .stTextInput input {
        background-color: rgba(3, 7, 18, 0.9) !important;
        color: #ffffff !important;
        border: 1px solid #4b5563 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inisialisasi Session State
if "page" not in st.session_state: st.session_state.page = "menu"
if "username" not in st.session_state: st.session_state.username = ""
if "score" not in st.session_state: st.session_state.score = 0
if "hp" not in st.session_state: st.session_state.hp = 100
if "mode" not in st.session_state: st.session_state.mode = ""
if "current_question" not in st.session_state: st.session_state.current_question = None

# ==========================================
# BANK SOAL DENGAN ANIMASI GIF MONSTER BERGERAK
# ==========================================
MATH_BANK = [
    {"q": "Berapakah hasil dari $12 \\times 5 - 15$ ?", "ans": 45, "monster": "Goblin Angka", "img": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3ZveHV3Z3c2d3R5NWx0OWZ1Z3R6ZGNucWZxd2k5bW02cG12Z2g4dSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Lq0h93752f6J9tijrh/giphy.gif"},
    {"q": "Berapakah hasil dari $8 \\times 8 + 20 - 4$ ?", "ans": 80, "monster": "Naga Aljabar", "img": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExYnJmdm52dmJqNDh0czFzdmoxMXFmbmN3ZHRwNDN2cWkzaWlyMjczdyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5nsKxUnzSYlV7W5X7n/giphy.gif"},
    {"q": "Berapakah hasil dari $(50 \\div 2) + (5 \\times 4)$ ?", "ans": 45, "monster": "Penyihir Pecahan", "img": "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnZjcW03dXN5bTF3MXZzOHI1YXBmYjltNHk2cGl1ZmQxMjR3YTNjcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw5/1247/giphy.gif"},
    {"q": "Berapakah hasil dari $145 - 25 \\times 4$ ?", "ans": 45, "monster": "Golem Logika", "img": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExaWVubmN2NWFqZWpkNDlkZDBpbHlyZWhnMHl5NWs2aXJ5MW5nOWYwMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPnAiaMCws8nOsE/giphy.gif"},
    {"q": "Berapakah hasil dari $9 \\times 9 - 31$ ?", "ans": 50, "monster": "Ksatria Angka", "img": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3ZveHV3Z3c2d3R5NWx0OWZ1Z3R6ZGNucWZxd2k5bW02cG12Z2g4dSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Lq0h93752f6J9tijrh/giphy.gif"}
]

ENGLISH_BANK = [
    {"q": 'Lengkapi kalimat: "She _______ to the library yesterday to borrow a book."', "options": ["--- Pilih ---", "go", "went", "gone", "going"], "ans": "went", "monster": "Hantu Grammar", "img": "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3g4MW00cjFzMnJ1MXl4bnk3ZXVhM3Z1Zm1qMGh2dTR0bTRpMHp5dyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKoWnHwjd6UkN8Q/giphy.gif"},
    {"q": 'Apa sinonim (persamaan kata) dari kata "Brave"?', "options": ["--- Pilih ---", "Coward", "Courageous", "Lazy", "Sad"], "ans": "Courageous", "monster": "Penyihir Kosakata", "img": "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHMyZWc4bjY4ZXo0Z2Q3MXB2M2x2MXl6azZpb29pazgxb2xpaWZ1eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26FPnj46AKHIMgY6c/giphy.gif"},
    {"q": 'Lengkapi kalimat Present Perfect: "They have _______ finished their homework."', "options": ["--- Pilih ---", "already", "yet", "still", "ever"], "ans": "already", "monster": "Goblin Tense", "img": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3ZveHV3Z3c2d3R5NWx0OWZ1Z3R6ZGNucWZxd2k5bW02cG12Z2g4dSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Lq0h93752f6J9tijrh/giphy.gif"},
    {"q": 'Apa bentuk V2 (Past Tense) dari kata "Eat"?', "options": ["--- Pilih ---", "Eaten", "Ate", "Eating", "Eats"], "ans": "Ate", "monster": "Monster Irregular", "img": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExaWVubmN2NWFqZWpkNDlkZDBpbHlyZWhnMHl5NWs2aXJ5MW5nOWYwMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPnAiaMCws8nOsE/giphy.gif"},
    {"q": 'Lengkapi kalimat: "I _______ a movie with my friends last night."', "options": ["--- Pilih ---", "watch", "watching", "watched", "watches"], "ans": "watched", "monster": "Bayangan Verb", "img": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExYnJmdm52dmJqNDh0czFzdmoxMXFmbmN3ZHRwNDN2cWkzaWlyMjczdyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5nsKxUnzSYlV7W5X7n/giphy.gif"}
]

def get_random_question(mode):
    if mode == "math":
        return random.choice(MATH_BANK)
    else:
        return random.choice(ENGLISH_BANK)

# ==========================================
# HALAMAN 1: MENU UTAMA
# ==========================================
if st.session_state.page == "menu":
    st.markdown("<h1 class='arcade-title'>SMART LEARNING HUB</h1>", unsafe_allow_html=True)
    st.markdown("<div class='arcade-subtitle'>// ANIMATED ARCADE & MONSTER ADVENTURE</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='game-arena'>", unsafe_allow_html=True)
    st.subheader("👤 Masukkan Identitas Pemain")
    st.session_state.username = st.text_input("Username:", value=st.session_state.username, placeholder="Ketik nama kamu di sini...")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.session_state.username:
        st.success(f"🎮 Siap bertempur, **{st.session_state.username}**! Pilih mode quiz arcade di bawah:")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🟦 MODE MATEMATIKA"):
                st.session_state.mode = "math"
                st.session_state.hp = 100
                st.session_state.score = 0
                st.session_state.current_question = get_random_question("math")
                st.session_state.page = "game"
                st.rerun()
        with col2:
            if st.button("🟩 MODE BAHASA INGGRIS"):
                st.session_state.mode = "english"
                st.session_state.hp = 100
                st.session_state.score = 0
                st.session_state.current_question = get_random_question("english")
                st.session_state.page = "game"
                st.rerun()
    else:
        st.warning("⚠️ Masukkan nama kamu dulu untuk menyalakan mesin game.")

# ==========================================
# HALAMAN 2: GAMEPLAY ARENA
# ==========================================
elif st.session_state.page == "game":
    if st.session_state.hp <= 0:
        st.markdown("<h1 class='arcade-title' style='color: #ef4444;'>💀 GAME OVER 💀</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Kamu kehabisan nyawa, <b>{st.session_state.username}</b>. Semangat coba lagi!</p>", unsafe_allow_html=True)
        if st.button("🔄 MAIN LAGI"):
            st.session_state.hp = 100
            st.session_state.score = 0
            st.session_state.page = "menu"
            st.rerun()
        st.stop()

    q_data = st.session_state.current_question

    st.markdown(f"""
        <div class='status-panel'>
            <span>👤 PLAYER: <b>{st.session_state.username}</b></span>
            <span>❤️ NYAWA: <b style='color: #ef4444;'>{st.session_state.hp}%</b></span>
            <span>⭐ SKOR: <b style='color: #fbbf24;'>{st.session_state.score}</b></span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='game-arena'>", unsafe_allow_html=True)
    
    col_img, col_txt = st.columns([1, 1.5])
    with col_img:
        st.image(q_data["img"], use_container_width=True)
    with col_txt:
        st.markdown(f"### 👾 {q_data['monster']} Menghadang!")
        st.markdown(f"**Soal:** {q_data['q']}")

    st.write("---")

    if st.session_state.mode == "math":
        user_ans = st.number_input("Ketik jawaban angka:", step=1, format="%d", key="ans_math")
        if st.button("⚔️ SERANG MONSTER!"):
            if user_ans == q_data["ans"]:
                st.success("🎉 BENAR! Monster berhasil dikalahkan! (+20 Skor)")
                st.session_state.score += 20
                st.session_state.current_question = get_random_question("math")
                st.rerun()
            else:
                st.session_state.hp -= 34
                st.error("💥 SALAH! Monster menyerang balik! (-34 HP)")

    elif st.session_state.mode == "english":
        user_ans = st.radio("Pilih jawaban yang benar:", q_data["options"], key="ans_eng")
        if st.button("🔑 JAWAB & BUKA PINTU!"):
            if user_ans == q_data["ans"]:
                st.success("✨ BENAR! Pintu terbuka dan monster kabur! (+20 Skor)")
                st.session_state.score += 20
                st.session_state.current_question = get_random_question("english")
                st.rerun()
            elif user_ans == "--- Pilih ---":
                st.warning("⚠️ Pilih salah satu opsi jawaban terlebih dahulu.")
            else:
                st.session_state.hp -= 34
                st.error("❌ SALAH! Pertahananmu jebol! (-34 HP)")

    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("🚪 KELUAR KE MENU UTAMA"):
        st.session_state.page = "menu"
        st.rerun()
