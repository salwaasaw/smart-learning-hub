import streamlit as st
import random
import mysql.connector
import time

st.set_page_config(
    page_title="Smart Learning Hub",
    page_icon="⚡",
    layout="centered"
)

# ==================== KONEKSI DATABASE MYSQL ====================
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",          # Kosongkan jika pakai XAMPP default
            database="db_smart_learning"
        )
        return connection
    except Exception as e:
        return None

def setup_database_tables():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS highscores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50),
                mode VARCHAR(50),
                score INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_stats (
                username VARCHAR(50) PRIMARY KEY,
                total_xp INT DEFAULT 0,
                games_played INT DEFAULT 0
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

setup_database_tables()

# ==================== STYLING CSS ELEGAN ====================
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
        padding: 22px 25px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }

    .cartoon-row {
        text-align: center;
        font-size: 1.8rem;
        letter-spacing: 8px;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    @keyframes bounceMonster {
        0%, 100% { transform: translateY(0) scale(1); }
        50% { transform: translateY(-8px) scale(1.08); }
    }

    .monster-emoji {
        text-align: center;
        font-size: 4.5rem;
        animation: bounceMonster 1.8s infinite ease-in-out;
        margin-bottom: 10px;
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

    .stat-box {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        padding: 15px;
        text-align: center;
    }

    .stat-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #38bdf8;
    }

    .stat-lbl {
        font-size: 0.75rem;
        color: #cbd5e1;
        text-transform: uppercase;
        letter-spacing: 1px;
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

# ==================== SESSION STATE INIT ====================
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
if "matched_count" not in st.session_state: st.session_state.matched_count = 0
if "word_target" not in st.session_state: st.session_state.word_target = ""
if "word_hint" not in st.session_state: st.session_state.word_hint = ""

TIME_LIMIT = 25

# ==================== BANK SOAL DIPERBANYAK ====================
MATH_BANK = [
    {"id": m, "q": q, "ans": a, "monster": name, "emoji": em} for m, (q, a, name, em) in enumerate([
        ("Berapakah hasil dari 12 x 5 - 15 ?", 45, "Goblin Frost", "👾"),
        ("Berapakah hasil dari 8 x 8 + 20 - 4 ?", 80, "Dragon Flame", "🐉"),
        ("Berapakah hasil dari (50 / 2) + (5 x 4) ?", 45, "Wizard Shadow", "🧙‍♂️"),
        ("Berapakah hasil dari 100 - 25 x 2 ?", 50, "Cyborg Mech", "🤖"),
        ("Berapakah hasil dari 15 + 15 x 3 ?", 60, "Forest Spirit", "🦊"),
        ("Berapakah hasil dari 9 x 9 - 31 ?", 50, "Cosmic Phantom", "👻"),
        ("Berapakah hasil dari 25 ditambah 5 dikali 4 ?", 45, "Math Guardian", "📐"),
        ("Berapakah hasil dari 144 dibagi 12 ditambah 8 ?", 20, "Number Knight", "🛡️"),
        ("Berapakah hasil dari 15 dikali 4 dikurangi 30 ?", 30, "Algebra Beast", "🔮"),
        ("Berapakah hasil dari 50 dikurang 5 dikali 6 ?", 20, "Calculus Titan", "⚡")
    ])
]

ENGLISH_BANK = [
    {"id": e, "q": q, "options": opt, "ans": a, "monster": name, "emoji": em} for e, (q, opt, a, name, em) in enumerate([
        ('Lengkapi kalimat: "She _______ to the library yesterday."', ["--- Pilih ---", "go", "went", "gone", "going"], "went", "Ghost Writer", "👻"),
        ('Apa sinonim dari kata "Brave"?', ["--- Pilih ---", "Coward", "Courageous", "Lazy", "Sad"], "Courageous", "Knight Honor", "🛡️"),
        ('Apa bentuk V2 (Past Tense) dari "Eat"?', ["--- Pilih ---", "Eaten", "Ate", "Eating", "Eats"], "Ate", "Tense Dragon", "🐲"),
        ('Apa arti dari kata "Smart"?', ["--- Pilih ---", "Bodoh", "Cerdas", "Malas", "Lambat"], "Cerdas", "Wise Owl", "🦉"),
        ('Lengkapi kalimat: "They _______ football last Sunday."', ["--- Pilih ---", "play", "playing", "played", "plays"], "played", "Sports Panther", "🐅"),
        ('Lengkapi kalimat: "He has _______ finished his homework."', ["--- Pilih ---", "already", "yet", "still", "ever"], "already", "Time Warden", "⏳"),
        ('Apa bentuk V3 (Past Participle) dari "Go"?', ["--- Pilih ---", "Went", "Gone", "Going", "Goes"], "Gone", "Grammar Knight", "⚔️"),
        ('Lengkapi kalimat: "We _______ a movie last night."', ["--- Pilih ---", "watch", "watched", "watching", "watches"], "watched", "Cinema Phantom", "🎬"),
        ('Apa sinonim dari kata "Fast"?', ["--- Pilih ---", "Slow", "Quick", "Lazy", "Tired"], "Quick", "Velocity Beast", "⚡"),
        ('Lengkapi kalimat: "I _______ a book right now."', ["--- Pilih ---", "am reading", "read", "reads", "readed"], "am reading", "Reader Mage", "📖")
    ])
]

CUSTOM_MATCH_DATA = [
    {"term": "Python", "def": "Bahasa Pemrograman AI & Web"},
    {"term": "MySQL", "def": "Sistem Database Relasional"},
    {"term": "Streamlit", "def": "Framework Web App Python"},
    {"term": "Algorithm", "def": "Langkah-langkah Logis Penyelesaian Masalah"},
    {"term": "RAM", "def": "Memori Penyimpanan Sementara"}
]

WORD_GUESS_DATA = [
    {"word": "PYTHON", "hint": "Bahasa pemograman yang sering digunakan untuk AI & Data Science"},
    {"word": "DATABASE", "hint": "Tempat penyimpanan data terstruktur di sistem komputer"},
    {"word": "ALGORITMA", "hint": "Urutan langkah logis untuk menyelesaikan masalah"},
    {"word": "HARDWARE", "hint": "Komponen fisik pada sistem komputer"}
]

# ==================== DATABASE HELPER FUNCTIONS ====================
def get_user_stats(username):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT total_xp, games_played FROM user_stats WHERE username = %s", (username,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return row["total_xp"], row["games_played"]
    return 0, 0

def add_xp_and_game(username, xp_gained):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_stats (username, total_xp, games_played) 
            VALUES (%s, %s, 1)
            ON DUPLICATE KEY UPDATE total_xp = total_xp + %s, games_played = games_played + 1
        """, (username, xp_gained, xp_gained))
        conn.commit()
        cursor.close()
        conn.close()

def save_score_to_mysql(score):
    if not st.session_state.saved_to_db:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            # Disesuaikan dengan kolom tabel highscores yang ada (username, mode, score)
            query = "INSERT INTO highscores (username, mode, score) VALUES (%s, %s, %s)"
            values = (st.session_state.username, st.session_state.mode, score)
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            
            earned_xp = max(score, 10) if score > 0 else 10
            add_xp_and_game(st.session_state.username, earned_xp)
            st.session_state.saved_to_db = True

def get_badge(xp):
    if xp >= 300:
        return "🥇 Master Belajar"
    elif xp >= 100:
        return "🥈 Jago Kuis"
    else:
        return "🥉 Pemula"

def get_new_question(mode):
    bank = MATH_BANK if mode == "math" else ENGLISH_BANK
    available = [q for q in bank if q["id"] not in st.session_state.used_questions]
    if not available:
        st.session_state.used_questions = []
        available = bank
    chosen = random.choice(available)
    st.session_state.used_questions.append(chosen["id"])
    st.session_state.start_time = time.time()
    return chosen

# ==================== HALAMAN 1: LOGIN AKUN ====================
if st.session_state.page == "login":
    st.markdown("<h1 class='game-title'>Smart Learning Hub</h1>", unsafe_allow_html=True)
    st.markdown("<div class='game-subtitle'>Belajar jadi lebih seru!</div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='card-unified'>
            <div class='cartoon-row'>🚀 🦊 🦖 🦉 🧙‍♂️ 🌟 🎮</div>
            <h3 style='margin-bottom: 5px; color: #ffffff;'>👋 Login Akun Pemain</h3>
            <p style='color: #cbd5e1; margin-bottom: 20px;'>Masukkan nama akunmu untuk melacak XP, level, dan skor di database.</p>
        </div>
    """, unsafe_allow_html=True)
    
    input_user = st.text_input("Username Akun:", value=st.session_state.username, placeholder="Ketik nama kamu...")
    
    if st.button("Masuk ke Dashboard 🚀"):
        if input_user.strip():
            st.session_state.username = input_user.strip()
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("INSERT IGNORE INTO user_stats (username, total_xp, games_played) VALUES (%s, 0, 0)", (st.session_state.username,))
                conn.commit()
                cursor.close()
                conn.close()
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.warning("Mohon isi username akun terlebih dahulu!")

# ==================== HALAMAN 2: DASHBOARD PROGRES ====================
elif st.session_state.page == "dashboard":
    st.markdown("<h1 class='game-title'>Smart Learning Hub</h1>", unsafe_allow_html=True)
    st.markdown("<div class='game-subtitle'>Platform Edukasi Gamifikasi</div>", unsafe_allow_html=True)

    xp, games_cnt = get_user_stats(st.session_state.username)
    level = (xp // 50) + 1
    badge = get_badge(xp)

    st.markdown(f"<h3 style='color: #38bdf8;'>PROGRES BELAJAR: {st.session_state.username}</h3>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div class='stat-box'>
                <div class='stat-val'>🏆 {xp}</div>
                <div class='stat-lbl'>Total XP</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class='stat-box'>
                <div class='stat-val'>🎮 {games_cnt}</div>
                <div class='stat-lbl'>Game Selesai</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class='stat-box'>
                <div class='stat-val'>⭐ Lvl {level}</div>
                <div class='stat-lbl'>Tingkat Level</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f"<p style='margin-top: 15px;'>Badge Saat Ini: <b>{badge}</b></p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 🎯 Pilih Permainan")

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("""
            <div class='card-unified' style='margin-bottom: 10px;'>
                <h4>⚔️ Quiz Battle</h4>
                <p style='font-size: 0.85rem; color: #cbd5e1;'>Jawab pertanyaan pilihan ganda & matematika sebelum waktu habis.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Main Quiz Battle"):
            st.session_state.page = "mode_select_quiz"
            st.rerun()

    with col_g2:
        st.markdown("""
            <div class='card-unified' style='margin-bottom: 10px;'>
                <h4>🧩 Match the Answer</h4>
                <p style='font-size: 0.85rem; color: #cbd5e1;'>Pasangkan istilah komputer dengan definisinya yang tepat.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Main Cocokkan Jawaban"):
            st.session_state.score = 0
            st.session_state.game_over = False
            st.session_state.saved_to_db = False
            st.session_state.matched_count = 0
            st.session_state.page = "game_match"
            st.rerun()

    col_g3, col_g4 = st.columns(2)
    with col_g3:
        st.markdown("""
            <div class='card-unified' style='margin-bottom: 10px;'>
                <h4>🔤 Tebak Kata</h4>
                <p style='font-size: 0.85rem; color: #cbd5e1;'>Tebak istilah berdasarkan clue petunjuk yang diberikan.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Main Tebak Kata"):
            chosen_w = random.choice(WORD_GUESS_DATA)
            st.session_state.word_target = chosen_w["word"]
            st.session_state.word_hint = chosen_w["hint"]
            st.session_state.score = 0
            st.session_state.game_over = False
            st.session_state.saved_to_db = False
            st.session_state.page = "game_word"
            st.rerun()

    with col_g4:
        st.markdown("""
            <div class='card-unified' style='margin-bottom: 10px;'>
                <h4>🏆 Leaderboard</h4>
                <p style='font-size: 0.85rem; color: #cbd5e1;'>Lihat papan peringkat pemain dengan XP & skor tertinggi.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Lihat Papan Peringkat"):
            st.session_state.page = "leaderboard"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Keluar / Ganti Akun"):
        st.session_state.page = "login"
        st.rerun()

# ==================== SUB-PAGE: PILIH MODE QUIZ BATTLE ====================
elif st.session_state.page == "mode_select_quiz":
    st.markdown("<h2 style='text-align: center;'>⚔️ Pilih Mode Quiz Battle</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🧮 Matematika"):
            st.session_state.mode = "math"
            st.session_state.score = 0
            st.session_state.game_over = False
            st.session_state.saved_to_db = False
            st.session_state.used_questions = []
            st.session_state.current_q = get_new_question("math")
            st.session_state.page = "game_quiz"
            st.rerun()
    with c2:
        if st.button("📚 B. Inggris"):
            st.session_state.mode = "english"
            st.session_state.score = 0
            st.session_state.game_over = False
            st.session_state.saved_to_db = False
            st.session_state.used_questions = []
            st.session_state.current_q = get_new_question("english")
            st.session_state.page = "game_quiz"
            st.rerun()
    with c3:
        if st.button("🏠 Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

# ==================== GAME 1: QUIZ BATTLE ====================
elif st.session_state.page == "game_quiz":
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, int(TIME_LIMIT - elapsed_time))

    if remaining_time == 0 and not st.session_state.game_over:
        st.session_state.game_over = True
        st.session_state.wrong_msg = "⏰ Waktu Habis! Kamu terlalu lama berpikir dan monster berhasil menangkapmu!"
        st.rerun()

    if st.session_state.game_over:
        save_score_to_mysql(st.session_state.score)

        st.markdown("<h2 style='text-align: center; color: #f87171;'>Permainan Berakhir</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #e2e8f0; font-size: 1.1rem;'>{st.session_state.wrong_msg}</p>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class='card-unified' style='text-align: center;'>
                <div class='cartoon-row'>🏆 💀 ✨ 📉 🎮</div>
                <p style='font-size: 1.1rem; margin-bottom: 5px; color: #ffffff;'>Total Skor / XP Diperoleh:</p>
                <h1 style='color: #38bdf8; font-size: 3rem; margin-top: 0;'>+{max(st.session_state.score, 10)} XP</h1>
                <p style='color: #34d399; font-size: 0.85rem; margin-top: 10px;'>✓ XP & game selesai berhasil dicatat ke database!</p>
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
            if st.button("Kembali ke Dashboard"):
                st.session_state.page = "dashboard"
                st.rerun()
        st.stop()

    q = st.session_state.current_q

    st.markdown(f"""
        <div class='status-panel'>
            <span>User: <b>{st.session_state.username}</b></span>
            <span>⏱️ Waktu: <b style='color: {"#f87171" if remaining_time <= 8 else "#38bdf8"};'>{remaining_time} Detik</b></span>
            <span>Skor: <b style='color: #38bdf8;'>{st.session_state.score}</b></span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class='card-unified'>
            <div class='cartoon-row'>🎯 ⚔️ 🧩 🔮 🚀</div>
            <div class='monster-emoji'>{q['emoji']}</div>
            <h4 style='text-align: center; color: #ffffff; margin-bottom: 15px;'>Tantangan {q['monster']}</h4>
            <p style='text-align: center; font-size: 1.15rem; margin-bottom: 25px; color: #ffffff;'><b>Soal:</b> {q['q']}</p>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.mode == "math":
        ans = st.number_input("Masukkan jawaban angka:", step=1, format="%d", key=f"m_ans_{q['id']}")
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
        ans = st.radio("Pilih jawaban:", q["options"], key=f"e_ans_{q['id']}")
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
    if st.button("Keluar ke Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

    time.sleep(1)
    st.rerun()

# ==================== GAME 2: MATCH THE ANSWER ====================
elif st.session_state.page == "game_match":
    st.markdown("<h2 style='text-align: center;'>🧩 Match the Answer</h2>", unsafe_allow_html=True)
    st.write("Pasangkan istilah di sebelah kiri dengan definisi yang benar di sebelah kanan.")

    all_matched = True
    for item in CUSTOM_MATCH_DATA:
        if st.session_state.get(f"match_{item['term']}") != item["def"]:
            all_matched = False
            break

    for item in CUSTOM_MATCH_DATA:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.info(f"📌 **{item['term']}**")
        with col2:
            options = ["--- Pilih Definisi ---"] + [d["def"] for d in CUSTOM_MATCH_DATA]
            st.selectbox(f"Definisi {item['term']}:", options, key=f"match_{item['term']}")

    if st.button("Cek Jawaban"):
        if all_matched:
            st.session_state.score = 50
            save_score_to_mysql(st.session_state.score)
            st.success("🎉 Selamat! Semua pasangan benar! (+50 XP ditambahkan ke database).")
        else:
            st.error("Masih ada pasangan yang keliru. Silakan periksa kembali!")

    if st.session_state.saved_to_db:
        if st.button("Kembali ke Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Keluar ke Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

# ==================== GAME 3: TEBAK KATA ====================
elif st.session_state.page == "game_word":
    st.markdown("<h2 style='text-align: center;'>🔤 Tebak Kata</h2>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class='card-unified'>
            <h4>💡 Petunjuk (Clue):</h4>
            <p style='font-size: 1.1rem; color: #38bdf8;'>"{st.session_state.word_hint}"</p>
            <p>Panjang kata: <b>{len(st.session_state.word_target)} Huruf</b></p>
        </div>
    """, unsafe_allow_html=True)

    guess = st.text_input("Masukkan kata tebakanmu:", placeholder="Ketik jawaban di sini...", key="word_guess_input").strip().upper()

    if st.button("Kirim Tebakan"):
        if guess == st.session_state.word_target:
            st.session_state.score = 30
            save_score_to_mysql(st.session_state.score)
            st.success(f"🎉 TEPAT SEKALI! Jawabannya adalah **{st.session_state.word_target}** (+30 XP ditambahkan)!")
            st.session_state.game_over = True
        else:
            st.error("Tebakanmu masih belum tepat, coba lagi!")

    if st.session_state.game_over:
        if st.button("Kembali ke Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Keluar ke Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

# ==================== HALAMAN 4: LEADERBOARD ====================
elif st.session_state.page == "leaderboard":
    st.markdown("<h2 style='text-align: center;'>🏆 Papan Peringkat (Leaderboard)</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1; margin-bottom: 25px;'>Pemain dengan XP dan Level Tertinggi di Platform</p>", unsafe_allow_html=True)

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username, total_xp, games_played FROM user_stats ORDER BY total_xp DESC LIMIT 10")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if rows:
            leaderboard_data = []
            for i, r in enumerate(rows, start=1):
                badge = get_badge(r["total_xp"])
                leaderboard_data.append({
                    "Peringkat": f"#{i}",
                    "Pemain": r["username"],
                    "Total XP": r["total_xp"],
                    "Game Selesai": r["games_played"],
                    "Badge": badge
                })
            st.table(leaderboard_data)
        else:
            st.info("Belum ada data pemain di database. Jadilah yang pertama bermain!")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
