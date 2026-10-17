import streamlit as st
import random
import mysql.connector
import time

st.set_page_config(
    page_title="Smart Learning Hub",
    page_icon="⚡",
    layout="centered"
)

# KONEKSI KE DATABASE MYSQL (XAMPP Lokal)
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_smart_learning"
        )
        return connection
    except Exception as e:
        return None

# STYLING CSS: Tampilan Elegan & Animasi
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&display=swap');

    @keyframes movingGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #311042, #0f172a);
        background-size: 300% 300%;
        animation: movingGradient 12s ease infinite;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #ffffff !important;
    }

    .stMarkdown, p, label, .stRadio label, .stTextInput label, .stNumberInput label, span {
        color: #ffffff !important;
    }

    .game-title {
        font-weight: 800;
        font-size: 2.2rem;
        text-align: center;
        color: #ffffff !important;
        letter-spacing: -0.5px;
        margin-bottom: 0px;
        text-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }

    .game-subtitle {
        text-align: center;
        color: #38bdf8 !important;
        font-size: 0.85rem;
        letter-spacing: 1.5px;
        margin-bottom: 20px;
        text-transform: uppercase;
        font-weight: 700;
    }

    .card-unified {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 18px;
        padding: 25px 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }

    .cartoon-row {
        text-align: center;
        font-size: 2rem;
        letter-spacing: 10px;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .monster-gif {
        display: block;
        margin: 0 auto 15px auto;
        width: 140px;
        height: 140px;
        object-fit: contain;
        border-radius: 50%;
        border: 3px solid #38bdf8;
        background: rgba(56, 189, 248, 0.1);
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.4);
    }

    .status-panel {
        display: flex;
        justify-content: space-between;
        background: rgba(15, 23, 42, 0.85);
        padding: 12px 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        font-size: 0.9rem;
        font-weight: 700;
        margin-bottom: 20px;
        color: #ffffff !important;
    }

    .stButton>button {
        width: 100%;
        background: #2563eb;
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        font-size: 0.95rem;
        padding: 12px;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
        transition: all 0.2s ease-in-out;
    }

    .stButton>button:hover {
        background: #1d4ed8;
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.6);
    }

    .stTextInput input, .stNumberInput input {
        background-color: rgba(15, 23, 42, 0.95) !important;
        color: #ffffff !important;
        font-weight: 600;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if "page" not in st.session_state: st.session_state.page = "login"
if "username" not in st.session_state: st.session_state.username = ""
if "score" not in st.session_state: st.session_state.score = 0
if "mode" not in st.session_state: st.session_state.mode = ""
if "used_questions" not in st.session_state: st.session_state.used_questions = []
if "current_q" not in st.session_state: st.session_state.current_q = None
if "game_over" not in st.session_state: st.session_state.game_over = False
if "wrong_msg" not in st.session_state: st.session_state.wrong_msg = ""
if "saved_to_db" not in st.session_state: st.session_state.saved_to_db = False
if "start_time" not in st.session_state: st.session_state.start_time = time.time()

TIME_LIMIT = 25  # Waktu dalam detik per soal

# Bank Soal dengan GIF Monster Animasi Bergerak
MATH_BANK = [
    {"id": m, "q": q, "ans": a, "monster": name, "gif": gif} for m, (q, a, name, gif) in enumerate([
        ("Berapakah hasil dari 12 x 5 - 15 ?", 45, "Goblin Frost", "https://media.giphy.com/media/3o7bu3XilJ5BOiSGic/giphy.gif"),
        ("Berapakah hasil dari 8 x 8 + 20 - 4 ?", 80, "Dragon Flame", "https://media.giphy.com/media/l0HlRnAWXxn0MhOBK/giphy.gif"),
        ("Berapakah hasil dari (50 / 2) + (5 x 4) ?", 45, "Wizard Shadow", "https://media.giphy.com/media/26FPnj46S7IWgVPeE/giphy.gif"),
        ("Berapakah hasil dari 100 - 25 x 2 ?", 50, "Cyborg Mech", "https://media.giphy.com/media/3ohhwytHcusSC7OUg0/giphy.gif"),
        ("Berapakah hasil dari 15 + 15 x 3 ?", 60, "Forest Spirit", "https://media.giphy.com/media/xT5LMFZDsj0AKUDYTS/giphy.gif"),
        ("Berapakah hasil dari 9 x 9 - 31 ?", 50, "Cosmic Phantom", "https://media.giphy.com/media/3oKIPnAiaMCws8nOsE/giphy.gif"),
        ("Berapakah hasil dari 145 - 25 x 4 ?", 45, "Ancient Golem", "https://media.giphy.com/media/3o7TKSjRrfIPjeiDiM/giphy.gif"),
        ("Berapakah hasil dari 24 / 3 + 12 ?", 20, "Temple Guardian", "https://media.giphy.com/media/l2Je66voqIs4nAcU0/giphy.gif")
    ])
]

ENGLISH_BANK = [
    {"id": e, "q": q, "options": opt, "ans": a, "monster": name, "gif": gif} for e, (q, opt, a, name, gif) in enumerate([
        ('Lengkapi kalimat: "She _______ to the library yesterday."', ["--- Pilih ---", "go", "went", "gone", "going"], "went", "Ghost Writer", "https://media.giphy.com/media/26FPnj46S7IWgVPeE/giphy.gif"),
        ('Apa sinonim dari kata "Brave"?', ["--- Pilih ---", "Coward", "Courageous", "Lazy", "Sad"], "Courageous", "Knight Honor", "https://media.giphy.com/media/l0HlRnAWXxn0MhOBK/giphy.gif"),
        ('Apa bentuk V2 (Past Tense) dari "Eat"?', ["--- Pilih ---", "Eaten", "Ate", "Eating", "Eats"], "Ate", "Tense Dragon", "https://media.giphy.com/media/3o7bu3XilJ5BOiSGic/giphy.gif"),
        ('Lengkapi kalimat: "They _______ football last Sunday."', ["--- Pilih ---", "play", "playing", "played", "plays"], "played", "Sports Panther", "https://media.giphy.com/media/3ohhwytHcusSC7OUg0/giphy.gif"),
        ('Apa arti dari kata "Smart"?', ["--- Pilih ---", "Bodoh", "Cerdas", "Malas", "Lambat"], "Cerdas", "Wise Owl", "https://media.giphy.com/media/xT5LMFZDsj0AKUDYTS/giphy.gif"),
        ('Lengkapi kalimat: "He has _______ finished his homework."', ["--- Pilih ---", "already", "yet", "still", "ever"], "already", "Time Warden", "https://media.giphy.com/media/3oKIPnAiaMCws8nOsE/giphy.gif"),
        ('Apa bentuk V3 (Past Participle) dari "Go"?', ["--- Pilih ---", "Went", "Gone", "Going", "Goes"], "Gone", "Grammar Knight", "https://media.giphy.com/media/3o7TKSjRrfIPjeiDiM/giphy.gif"),
        ('Lengkapi kalimat: "We _______ a movie last night."', ["--- Pilih ---", "watch", "watched", "watching", "watches"], "watched", "Cinema Phantom", "https://media.giphy.com/media/l2Je66voqIs4nAcU0/giphy.gif")
    ])
]

def get_new_question(mode):
    bank = MATH_BANK if mode == "math" else ENGLISH_BANK
    available = [q for q in bank if q["id"] not in st.session_state.used_questions]
    if not available:
        st.session_state.used_questions = []
        available = bank
    chosen = random.choice(available)
    st.session_state.used_questions.append(chosen["id"])
    st.session_state.start_time = time.time()  # Reset timer untuk soal baru
    return chosen

def save_score_to_mysql():
    if not st.session_state.saved_to_db:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            query = "INSERT INTO highscores (username, mode, score) VALUES (%s, %s, %s)"
            values = (st.session_state.username, st.session_state.mode, st.session_state.score)
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            st.session_state.saved_to_db = True

# ==================== HALAMAN 1: LOGIN ====================
if st.session_state.page == "login":
    st.markdown("<h1 class='game-title'>Smart Learning Hub</h1>", unsafe_allow_html=True)
    st.markdown("<div class='game-subtitle'>Interactive Learning Platform</div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='card-unified'>
            <div class='cartoon-row'>🚀 🦊 🦖 🦉 🧙‍♂️ 🌟 🎮</div>
            <h3 style='margin-bottom: 5px; color: #ffffff;'>👋 Selamat Datang!</h3>
            <p style='color: #cbd5e1; margin-bottom: 20px;'>Silakan masukkan nama kamu sebelum memulai petualangan belajar.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.session_state.username = st.text_input("Masukkan Nama:", value=st.session_state.username, placeholder="Contoh: Salwa")
    
    if st.button("Masuk ke Arena 🚀"):
        if st.session_state.username.strip():
            st.session_state.page = "welcome"
            st.rerun()
        else:
            st.warning("Mohon isi nama kamu terlebih dahulu!")

# ==================== HALAMAN 2: DASHBOARD SAMBUTAN ====================
elif st.session_state.page == "welcome":
    st.markdown("<h1 class='game-title'>Smart Learning Hub</h1>", unsafe_allow_html=True)
    st.markdown("<div class='game-subtitle'>Interactive Learning Platform</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class='card-unified' style='text-align: center;'>
            <div class='cartoon-row'>🌟 🦉 🎮 ✨ 🧭</div>
            <h2 style='color: #38bdf8; margin-bottom: 5px;'>Halo, {st.session_state.username}! 👋</h2>
            <p style='font-size: 1rem; color: #cbd5e1;'>Siap menguji kemampuanmu dengan batas waktu menjawab? Pilih tantangan di bawah:</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Mulai Matematika 🧮"):
            st.session_state.mode = "math"
            st.session_state.score = 0
            st.session_state.game_over = False
            st.session_state.saved_to_db = False
            st.session_state.used_questions = []
            st.session_state.current_q = get_new_question("math")
            st.session_state.page = "game"
            st.rerun()

    with col2:
        if st.button("Mulai B. Inggris 📚"):
            st.session_state.mode = "english"
            st.session_state.score = 0
            st.session_state.game_over = False
            st.session_state.saved_to_db = False
            st.session_state.used_questions = []
            st.session_state.current_q = get_new_question("english")
            st.session_state.page = "game"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Ganti Nama User"):
        st.session_state.page = "login"
        st.rerun()

# ==================== HALAMAN 3: GAMEPLAY ARENA DENGAN TIMER AKTIF ====================
elif st.session_state.page == "game":
    # Hitung sisa waktu
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, int(TIME_LIMIT - elapsed_time))

    # Jika Waktu Habis
    if remaining_time == 0 and not st.session_state.game_over:
        st.session_state.game_over = True
        st.session_state.wrong_msg = "⏰ Waktu Habis! Kamu terlalu lama berpikir dan monster berhasil menangkapmu!"
        st.rerun()

    if st.session_state.game_over:
        save_score_to_mysql()

        st.markdown("<h2 style='text-align: center; color: #f87171;'>Permainan Berakhir</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #e2e8f0; font-size: 1.1rem;'>{st.session_state.wrong_msg}</p>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class='card-unified' style='text-align: center;'>
                <div class='cartoon-row'>🏆 💀 ✨ 📉 🎮</div>
                <p style='font-size: 1.1rem; margin-bottom: 5px; color: #ffffff;'>Total Skor Akhir Kamu:</p>
                <h1 style='color: #38bdf8; font-size: 3rem; margin-top: 0;'>{st.session_state.score}</h1>
                <p style='color: #34d399; font-size: 0.85rem; margin-top: 10px;'>✓ Riwayat skor berhasil dicatat!</p>
            </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Main Lagi"):
                st.session_state.score = 0
                st.session_state.game_over = False
                st.session_state.saved_to_db = False
                st.session_state.used_questions = []
                st.session_state.current_q = get_new_question(st.session_state.mode)
                st.rerun()
        with col_b:
            if st.button("Kembali ke Menu"):
                st.session_state.page = "welcome"
                st.rerun()
        st.stop()

    q = st.session_state.current_q

    st.markdown(f"""
        <div class='status-panel'>
            <span>User: <b>{st.session_state.username}</b></span>
            <span>⏱️ Waktu: <b style='color: {"#f87171" if remaining_time <= 10 else "#38bdf8"};'>{remaining_time} Detik</b></span>
            <span>Skor: <b style='color: #38bdf8;'>{st.session_state.score}</b></span>
        </div>
    """, unsafe_allow_html=True)
    
    # Menampilkan Monster GIF Animasi Bergerak
    st.markdown(f"""
        <div class='card-unified'>
            <div class='cartoon-row'>🎯 ⚔️ 🧩 🔮 🚀</div>
            <img src="{q['gif']}" class="monster-gif" alt="Animated Monster">
            <h4 style='text-align: center; color: #ffffff; margin-bottom: 15px;'>Tantangan {q['monster']}</h4>
            <p style='text-align: center; font-size: 1.15rem; margin-bottom: 25px; color: #ffffff;'><b>Soal:</b> {q['q']}</p>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.mode == "math":
        ans = st.number_input("Masukkan jawaban angka:", step=1, format="%d", key="m_ans")
        if st.button("Kirim Jawaban"):
            if ans == q["ans"]:
                st.session_state.score += 10
                st.session_state.current_q = get_new_question("math")
                st.rerun()
            else:
                st.session_state.game_over = True
                st.session_state.wrong_msg = f"Jawaban kamu kurang tepat. Jawaban yang benar adalah **{q['ans']}**."
                st.rerun()

    elif st.session_state.mode == "english":
        ans = st.radio("Pilih jawaban:", q["options"], key="e_ans")
        if st.button("Kirim Jawaban"):
            if ans == q["ans"]:
                st.session_state.score += 10
                st.session_state.current_q = get_new_question("english")
                st.rerun()
            elif ans == "--- Pilih ---":
                st.warning("Silakan pilih salah satu opsi terlebih dahulu.")
            else:
                st.session_state.game_over = True
                st.session_state.wrong_msg = f"Jawaban kamu kurang tepat. Jawaban yang benar adalah **{q['ans']}**."
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Keluar ke Menu Dashboard"):
        st.session_state.page = "welcome"
        st.rerun()

    # Auto-refresh halaman setiap 1 detik agar timer hitung mundur jalan otomatis di layar
    time.sleep(1)
    st.rerun()
