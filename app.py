import streamlit as st
import random

st.set_page_config(
    page_title="Smart Learning Hub: Unlimited Quest",
    page_icon="✨",
    layout="centered"
)

# STYLING CSS: Warna Hangat Estetik (Tanpa Biru), Background Bergerak Jelas, 3D Glassmorphism
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@500;700;900&family=Quicksand:wght@500;700&display=swap');

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #ff7e5f, #feb47b, #ff416c, #845ec2);
        background-size: 400% 400%;
        animation: gradientBG 10s ease infinite;
        font-family: 'Quicksand', sans-serif;
        color: #ffffff;
    }

    .game-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 900;
        font-size: 2.3rem;
        text-align: center;
        color: #ffffff;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        margin-bottom: 0px;
    }

    .game-subtitle {
        font-family: 'Outfit', sans-serif;
        text-align: center;
        color: #fff1f2;
        font-size: 0.9rem;
        letter-spacing: 2px;
        margin-bottom: 25px;
    }

    .rpg-card-3d {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.5);
        margin-bottom: 20px;
    }

    @keyframes bounceChar {
        0%, 100% { transform: translateY(0) scale(1); }
        50% { transform: translateY(-12px) scale(1.05); }
    }

    @keyframes shakeScreen {
        0% { transform: translate(0, 0); }
        20% { transform: translate(-8px, 4px); }
        40% { transform: translate(8px, -4px); }
        60% { transform: translate(-4px, -4px); }
        80% { transform: translate(4px, 4px); }
        100% { transform: translate(0, 0); }
    }

    .char-avatar {
        text-align: center;
        font-size: 5.5rem;
        animation: bounceChar 1.8s infinite ease-in-out;
        margin-bottom: 10px;
    }

    .screen-shake {
        animation: shakeScreen 0.35s ease-in-out;
    }

    .status-bar {
        display: flex;
        justify-content: space-around;
        background: rgba(45, 27, 105, 0.4);
        padding: 14px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        font-family: 'Outfit', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        margin-bottom: 20px;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #f72585 0%, #b5179e 100%);
        color: white;
        border: none;
        border-radius: 14px;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        padding: 14px;
        box-shadow: 0 6px 20px rgba(247, 37, 133, 0.4);
        transition: all 0.2s ease-in-out;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(247, 37, 133, 0.6);
        background: linear-gradient(135deg, #ff54b0 0%, #f72585 100%);
    }

    .stTextInput input, .stNumberInput input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #2d1b69 !important;
        font-weight: 700;
        border-radius: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Session State
if "page" not in st.session_state: st.session_state.page = "menu"
if "username" not in st.session_state: st.session_state.username = ""
if "score" not in st.session_state: st.session_state.score = 0
if "hp" not in st.session_state: st.session_state.hp = 100
if "mode" not in st.session_state: st.session_state.mode = ""
if "used_questions" not in st.session_state: st.session_state.used_questions = []
if "current_q" not in st.session_state: st.session_state.current_q = None
if "shake" not in st.session_state: st.session_state.shake = False

# Bank Soal Lengkap (Unlimited Pool)
MATH_BANK = [
    {"id": m, "q": q, "ans": a, "monster": name, "emoji": em} for m, (q, a, name, em) in enumerate([
        ("Berapakah hasil dari 12 x 5 - 15 ?", 45, "Goblin Ceria", "🦊"),
        ("Berapakah hasil dari 8 x 8 + 20 - 4 ?", 80, "Naga Pelangi", "🐲"),
        ("Berapakah hasil dari (50 / 2) + (5 x 4) ?", 45, "Penyihir Kacamata", "🧙‍♂️"),
        ("Berapakah hasil dari 100 - 25 x 2 ?", 50, "Kelinci Logika", "🐰"),
        ("Berapakah hasil dari 15 + 15 x 3 ?", 60, "Beruang Hitung", "🐻")
    ])
]

ENGLISH_BANK = [
    {"id": e, "q": q, "options": opt, "ans": a, "monster": name, "emoji": em} for e, (q, opt, a, name, em) in enumerate([
        ('Lengkapi kalimat: "She _______ to the library yesterday."', ["--- Pilih ---", "go", "went", "gone", "going"], "went", "Hantu Kata", "👻"),
        ('Apa sinonim dari kata "Brave"?', ["--- Pilih ---", "Coward", "Courageous", "Lazy", "Sad"], "Courageous", "Penyihir Kosakata", "🧚‍♀️"),
        ('Apa bentuk V2 (Past Tense) dari "Eat"?', ["--- Pilih ---", "Eaten", "Ate", "Eating", "Eats"], "Ate", "Dinosaurus Tense", "🦖"),
        ('Lengkapi kalimat: "They _______ football last Sunday."', ["--- Pilih ---", "play", "playing", "played", "plays"], "played", "Kucing Olahraga", "🐱"),
        ('Apa arti dari kata "Smart"?', ["--- Pilih ---", "Bodoh", "Cerdas", "Malas", "Lambat"], "Cerdas", "Burung Hantu Bijak", "🦉")
    ])
]

def get_new_question(mode):
    bank = MATH_BANK if mode == "math" else ENGLISH_BANK
    available = [q for q in bank if q["id"] not in st.session_state.used_questions]
    
    # Jika semua soal sudah habis terjawab, reset ulang supaya jadi UNLIMITED
    if not available:
        st.session_state.used_questions = []
        available = bank
        
    chosen = random.choice(available)
    st.session_state.used_questions.append(chosen["id"])
    return chosen

# Menu Utama
if st.session_state.page == "menu":
    st.markdown("<h1 class='game-title'>SMART LEARNING HUB</h1>", unsafe_allow_html=True)
    st.markdown("<div class='game-subtitle'>// UNLIMITED QUEST ADVENTURE</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='rpg-card-3d'>", unsafe_allow_html=True)
    st.subheader("🌸 Masukkan Nama Petualang")
    st.session_state.username = st.text_input("Username:", value=st.session_state.username, placeholder="Ketik nama kamu di sini...")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.session_state.username:
        st.success(f"✨ Halo, **{st.session_state.username}**! Pilih mode petualanganmu:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌸 MODE MATEMATIKA"):
                st.session_state.mode = "math"
                st.session_state.hp = 100
                st.session_state.score = 0
                st.session_state.used_questions = []
                st.session_state.current_q = get_new_question("math")
                st.session_state.page = "game"
                st.rerun()
        with col2:
            if st.button("🍀 MODE BAHASA INGGRIS"):
                st.session_state.mode = "english"
                st.session_state.hp = 100
                st.session_state.score = 0
                st.session_state.used_questions = []
                st.session_state.current_q = get_new_question("english")
                st.session_state.page = "game"
                st.rerun()
    else:
        st.warning("⚠️ Masukkan nama kamu dulu untuk memulai petualangan.")

# Gameplay Arena
elif st.session_state.page == "game":
    if st.session_state.hp <= 0:
        st.markdown("<h1 class='game-title' style='color: #ffe5ec;'>💀 PERMAINAN BERAKHIR 💀</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-size: 1.2rem;'>Kamu kehabisan nyawa, <b>{st.session_state.username}</b>! Jangan menyerah, coba lagi yuk!</p>", unsafe_allow_html=True)
        if st.button("🔄 MAIN LAGI"):
            st.session_state.hp = 100
            st.session_state.score = 0
            st.session_state.used_questions = []
            st.session_state.page = "menu"
            st.rerun()
        st.stop()

    q = st.session_state.current_q

    st.markdown(f"""
        <div class='status-bar'>
            <span>👤 <b>{st.session_state.username}</b></span>
            <span>❤️ NYAWA: <b style='color: #ffe5ec;'>{st.session_state.hp}%</b></span>
            <span>⭐ SKOR: <b style='color: #fef08a;'>{st.session_state.score}</b></span>
        </div>
    """, unsafe_allow_html=True)
    
    card_cls = "rpg-card-3d screen-shake" if st.session_state.shake else "rpg-card-3d"
    st.markdown(f"<div class='{card_cls}'>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='char-avatar'>{q['emoji']}</div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #fef08a; font-family: Outfit;'>✨ {q['monster']} Menghadang! ✨</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 1.2rem; margin-bottom: 20px; font-weight: 700;'><b>Soal:</b> {q['q']}</p>", unsafe_allow_html=True)

    st.write("---")

    if st.session_state.mode == "math":
        ans = st.number_input("Masukkan jawaban angka:", step=1, format="%d", key="m_ans")
        if st.button("🚀 JAWAB SEKARANG!"):
            if ans == q["ans"]:
                st.session_state.shake = False
                st.success("🎉 BENAR SEKALI! Petualangan berlanjut! (+20 Skor)")
                st.session_state.score += 20
                st.session_state.current_q = get_new_question("math")
                st.rerun()
            else:
                st.session_state.hp -= 34
                st.session_state.shake = True
                st.error("💥 SALAH! Monster menyerang balik! (-34 HP)")
                st.rerun()

    elif st.session_state.mode == "english":
        ans = st.radio("Pilih opsi jawaban:", q["options"], key="e_ans")
        if st.button("🚀 JAWAB SEKARANG!"):
            if ans == q["ans"]:
                st.session_state.shake = False
                st.success("✨ TEPAT BANGET! Pintu terbuka! (+20 Skor)")
                st.session_state.score += 20
                st.session_state.current_q = get_new_question("english")
                st.rerun()
            elif ans == "--- Pilih ---":
                st.warning("⚠️ Pilih salah satu opsi jawaban dulu ya!")
            else:
                st.session_state.hp -= 34
                st.session_state.shake = True
                st.error("❌ SALAH! Pertahananmu jebol! (-34 HP)")
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("🚪 KELUAR KE MENU UTAMA"):
        st.session_state.page = "menu"
        st.rerun()
