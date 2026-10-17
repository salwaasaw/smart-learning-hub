import streamlit as st
import random

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Smart Learning Hub: Arcade Edition",
    page_icon="🎮",
    layout="centered"
)

# Styling CSS Kustom (Animasi Neon, Efek Denyut/Pulse, & UI Arcade)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');

    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f3f4f6;
    }

    .arcade-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 2.2rem;
        text-align: center;
        background: linear-gradient(135deg, #38bdf8 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }

    .arcade-subtitle {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        color: #94a3b8;
        font-size: 0.8rem;
        letter-spacing: 2px;
        margin-bottom: 25px;
    }

    /* Efek Animasi Denyut Monster Bergerak */
    @keyframes pulseMonster {
        0% { transform: scale(1); }
        50% { transform: scale(1.08); }
        100% { transform: scale(1); }
    }

    .monster-container {
        text-align: center;
        font-size: 5rem;
        animation: pulseMonster 1.5s infinite ease-in-out;
        margin: 10px 0;
    }

    .game-arena {
        background: rgba(30, 41, 59, 0.7);
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
        background: rgba(15, 23, 42, 0.9);
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #334155;
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
        border: 1px solid #475569 !important;
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
# BANK SOAL LENGKAP & ACAK OTOMATIS
# ==========================================
MATH_BANK = [
    {"q": "Berapakah hasil dari $12 \\times 5 - 15$ ?", "ans": 45, "monster": "Goblin Angka", "emoji": "👾"},
    {"q": "Berapakah hasil dari $8 \\times 8 + 20 - 4$ ?", "ans": 80, "monster": "Naga Aljabar", "emoji": "🐉"},
    {"q": "Berapakah hasil dari $(50 \\div 2) + (5 \\times 4)$ ?", "ans": 45, "monster": "Penyihir Pecahan", "emoji": "🧙‍♂️"},
    {"q": "Berapakah hasil dari $145 - 25 \\times 4$ ?", "ans": 45, "monster": "Golem Logika", "emoji": "🤖"},
    {"q": "Berapakah hasil dari $9 \\times 9 - 31$ ?", "ans": 50, "monster": "Ksatria Angka", "emoji": "🛡️"}
]

ENGLISH_BANK = [
    {"q": 'Lengkapi kalimat: "She _______ to the library yesterday to borrow a book."', "options": ["--- Pilih ---", "go", "went", "gone", "going"], "ans": "went", "monster": "Hantu Grammar", "emoji": "👻"},
    {"q": 'Apa sinonim (persamaan kata) dari kata "Brave"?', "options": ["--- Pilih ---", "Coward", "Courageous", "Lazy", "Sad"], "ans": "Courageous", "monster": "Penyihir Kosakata", "emoji": "🧙‍♀️"},
    {"q": 'Lengkapi kalimat Present Perfect: "They have _______ finished their homework."', "options": ["--- Pilih ---", "already", "yet", "still", "ever"], "ans": "already", "monster": "Goblin Tense", "emoji": "👺"},
    {"q": 'Apa bentuk V2 (Past Tense) dari kata "Eat"?', "options": ["--- Pilih ---", "Eaten", "Ate", "Eating", "Eats"], "ans": "Ate", "monster": "Monster Irregular", "emoji": "🦖"},
    {"q": 'Lengkapi kalimat: "I _______ a movie with my friends last night."', "options": ["--- Pilih ---", "watch", "watching", "watched", "watches"], "ans": "watched", "monster": "Bayangan Verb", "emoji": "👤"}
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
    st.markdown("<div class='arcade-subtitle'>// ARCADE QUIZ & MONSTER ADVENTURE</div>", unsafe_allow_html=True)
    
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
    
    # Bagian Animasi Monster Bergerak (Pulse Animation dengan Emoji HD)
    st.markdown(f"<div class='monster-container'>{q_data['emoji']}</div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #38bdf8;'>{q_data['monster']} Menghadang!</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 1.1rem; margin-bottom: 20px;'><b>Soal:</b> {q_data['q']}</p>", unsafe_allow_html=True)

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
