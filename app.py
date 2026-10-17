import streamlit as st
import random

st.set_page_config(
    page_title="Smart Learning Hub",
    page_icon="⚡",
    layout="centered"
)

# STYLING CSS: Background Bergerak Jelas & Kontras Nyaman
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&display=swap');

    /* Animasi Gradasi Dibuat Lebih Kontras & Terlihat Bergerak */
    @keyframes movingGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #311042, #0f2744);
        background-size: 300% 300%;
        animation: movingGradient 8s ease infinite;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f8fafc;
    }

    .game-title {
        font-weight: 800;
        font-size: 2.2rem;
        text-align: center;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin-bottom: 0px;
    }

    .game-subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 0.85rem;
        letter-spacing: 1.5px;
        margin-bottom: 25px;
        text-transform: uppercase;
    }

    /* Kotak Kaca Modern Transparan agar Background Tetap Kelihatan Bergerak di Belakangnya */
    .card-clean {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 18px;
        padding: 28px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
    }

    @keyframes floatChar {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }

    .char-icon {
        text-align: center;
        font-size: 4.5rem;
        animation: floatChar 2.5s infinite ease-in-out;
        margin-bottom: 10px;
    }

    .status-panel {
        display: flex;
        justify-content: space-between;
        background: rgba(15, 23, 42, 0.75);
        padding: 12px 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        font-size: 0.9rem;
        font-weight: 700;
        margin-bottom: 20px;
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
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
        transition: all 0.2s ease-in-out;
    }

    .stButton>button:hover {
        background: #1d4ed8;
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.5);
    }

    .stTextInput input, .stNumberInput input {
        background-color: rgba(15, 23, 42, 0.85) !important;
        color: #ffffff !important;
        font-weight: 600;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Session State
if "page" not in st.session_state: st.session_state.page = "menu"
if "username" not in st.session_state: st.session_state.username = ""
if "score" not in st.session_state: st.session_state.score = 0
if "mode" not in st.session_state: st.session_state.mode = ""
if "used_questions" not in st.session_state: st.session_state.used_questions = []
if "current_q" not in st.session_state: st.session_state.current_q = None
if "game_over" not in st.session_state: st.session_state.game_over = False
if "wrong_msg" not in st.session_state: st.session_state.wrong_msg = ""

# Bank Soal Unlimited
MATH_BANK = [
    {"id": m, "q": q, "ans": a, "monster": name, "emoji": em} for m, (q, a, name, em) in enumerate([
        ("Berapakah hasil dari 12 x 5 - 15 ?", 45, "Penjaga Angka", "🔢"),
        ("Berapakah hasil dari 8 x 8 + 20 - 4 ?", 80, "Penjaga Gerbang", "🛡️"),
        ("Berapakah hasil dari (50 / 2) + (5 x 4) ?", 45, "Kalkulator Kuno", "⚙️"),
        ("Berapakah hasil dari 100 - 25 x 2 ?", 50, "Penjaga Waktu", "⏳"),
        ("Berapakah hasil dari 15 + 15 x 3 ?", 60, "Penjaga Logika", "🧭")
    ])
]

ENGLISH_BANK = [
    {"id": e, "q": q, "options": opt, "ans": a, "monster": name, "emoji": em} for e, (q, opt, a, name, em) in enumerate([
        ('Lengkapi kalimat: "She _______ to the library yesterday."', ["--- Pilih ---", "go", "went", "gone", "going"], "went", "Penjaga Kata", "📖"),
        ('Apa sinonim dari kata "Brave"?', ["--- Pilih ---", "Coward", "Courageous", "Lazy", "Sad"], "Courageous", "Pemberantas Huruf", "✍️"),
        ('Apa bentuk V2 (Past Tense) dari "Eat"?', ["--- Pilih ---", "Eaten", "Ate", "Eating", "Eats"], "Ate", "Arsiparis Bahasa", "📜"),
        ('Lengkapi kalimat: "They _______ football last Sunday."', ["--- Pilih ---", "play", "playing", "played", "plays"], "played", "Pengawal Kalimat", "🛡️"),
        ('Apa arti dari kata "Smart"?', ["--- Pilih ---", "Bodoh", "Cerdas", "Malas", "Lambat"], "Cerdas", "Master Kosakata", "💡")
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
    return chosen

# Menu Utama
if st.session_state.page == "menu":
    st.markdown("<h1 class='game-title'>Smart Learning Hub</h1>", unsafe_allow_html=True)
    st.markdown("<div class='game-subtitle'>Interactive Learning Platform</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card-clean'>", unsafe_allow_html=True)
    st.subheader("Identitas Pengguna")
    st.session_state.username = st.text_input("Masukkan Nama:", value=st.session_state.username, placeholder="Ketik nama kamu...")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.session_state.username:
        st.success(f"Selamat datang, **{st.session_state.username}**. Pilih mode latihan:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Mode Matematika"):
                st.session_state.mode = "math"
                st.session_state.score = 0
                st.session_state.game_over = False
                st.session_state.used_questions = []
                st.session_state.current_q = get_new_question("math")
                st.session_state.page = "game"
                st.rerun()
        with col2:
            if st.button("Mode Bahasa Inggris"):
                st.session_state.mode = "english"
                st.session_state.score = 0
                st.session_state.game_over = False
                st.session_state.used_questions = []
                st.session_state.current_q = get_new_question("english")
                st.session_state.page = "game"
                st.rerun()
    else:
        st.warning("Silakan masukkan nama terlebih dahulu.")

# Gameplay Arena
elif st.session_state.page == "game":
    if st.session_state.game_over:
        st.markdown("<h2 style='text-align: center; color: #ef4444;'>Permainan Berakhir</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #cbd5e1;'>{st.session_state.wrong_msg}</p>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class='card-clean' style='text-align: center;'>
                <p style='font-size: 1.1rem; margin-bottom: 5px;'>Total Skor Akhir Kamu:</p>
                <h1 style='color: #38bdf8; font-size: 3rem; margin-top: 0;'>{st.session_state.score}</h1>
            </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Main Lagi"):
                st.session_state.score = 0
                st.session_state.game_over = False
                st.session_state.used_questions = []
                st.session_state.current_q = get_new_question(st.session_state.mode)
                st.rerun()
        with col_b:
            if st.button("Kembali ke Menu"):
                st.session_state.page = "menu"
                st.rerun()
        st.stop()

    q = st.session_state.current_q

    st.markdown(f"""
        <div class='status-panel'>
            <span>User: <b>{st.session_state.username}</b></span>
            <span>Skor: <b style='color: #38bdf8;'>{st.session_state.score}</b></span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='card-clean'>", unsafe_allow_html=True)
    st.markdown(f"<div class='char-icon'>{q['emoji']}</div>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; color: #e2e8f0; margin-bottom: 15px;'>Tantangan {q['monster']}</h4>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 1.15rem; margin-bottom: 25px;'><b>Soal:</b> {q['q']}</p>", unsafe_allow_html=True)

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

    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Keluar ke Menu"):
        st.session_state.page = "menu"
        st.rerun()
