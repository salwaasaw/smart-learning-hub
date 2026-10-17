import streamlit as st
import random

st.set_page_config(
    page_title="Smart Learning Hub: 3D Animated RPG",
    page_icon="⚡",
    layout="centered"
)

# STYLING CSS: Background Bergerak, Efek 3D, Animasi Monster & Efek Getar Serangan
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@400;600;800&display=swap');

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #4f46e5, #06b6d4, #3b82f6, #8b5cf6);
        background-size: 400% 400%;
        animation: gradientShift 12s ease infinite;
        font-family: 'Poppins', sans-serif;
        color: #ffffff;
    }

    .game-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 2.2rem;
        text-align: center;
        color: #ffffff;
        text-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 0px;
    }

    .game-subtitle {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        color: #e0e7ff;
        font-size: 0.85rem;
        letter-spacing: 2px;
        margin-bottom: 25px;
    }

    .rpg-card-3d {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.4);
        margin-bottom: 20px;
    }

    /* Animasi Monster Memantul */
    @keyframes bounceMonster {
        0%, 100% { transform: translateY(0) scale(1); }
        50% { transform: translateY(-15px) scale(1.08); }
    }

    /* Animasi Layar Bergetar Saat Diserang Monster */
    @keyframes shakeScreen {
        0% { transform: translate(0, 0); }
        20% { transform: translate(-10px, 5px); }
        40% { transform: translate(10px, -5px); }
        60% { transform: translate(-5px, -5px); }
        80% { transform: translate(5px, 5px); }
        100% { transform: translate(0, 0); }
    }

    .monster-3d {
        text-align: center;
        font-size: 6rem;
        animation: bounceMonster 1.5s infinite ease-in-out;
        text-shadow: 0 10px 20px rgba(0,0,0,0.3);
        margin-bottom: 10px;
    }

    .monster-attack-effect {
        animation: shakeScreen 0.4s ease-in-out;
    }

    .status-bar {
        display: flex;
        justify-content: space-around;
        background: rgba(15, 23, 42, 0.6);
        padding: 14px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        font-family: 'Orbitron', sans-serif;
        font-size: 0.9rem;
        margin-bottom: 20px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        padding: 14px;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
        transition: all 0.2s ease-in-out;
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.6);
        background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
    }

    .stTextInput input, .stNumberInput input {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #0f172a !important;
        font-weight: 600;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Session State
if "page" not in st.session_state: st.session_state.page = "menu"
if "username" not in st.session_state: st.session_state.username = ""
if "score" not in st.session_state: st.session_state.score = 0
if "hp" not in st.session_state: st.session_state.hp = 100
if "mode" not in st.session_state: st.session_state.mode = ""
if "current_q" not in st.session_state: st.session_state.current_q = None
if "attack_effect" not in st.session_state: st.session_state.attack_effect = False

# Bank Soal Bersih Tanpa Kode Aneh
MATH_BANK = [
    {"q": "Berapakah hasil dari 12 x 5 - 15 ?", "ans": 45, "monster": "Goblin Gesit", "emoji": "👺"},
    {"q": "Berapakah hasil dari 8 x 8 + 20 - 4 ?", "ans": 80, "monster": "Naga Api Purba", "emoji": "🐉"},
    {"q": "Berapakah hasil dari (50 / 2) + (5 x 4) ?", "ans": 45, "monster": "Penyihir Angka", "emoji": "🧙‍♂️"},
]
ENGLISH_BANK = [
    {"q": 'Lengkapi kalimat: "She _______ to the library yesterday."', "options": ["--- Pilih ---", "go", "went", "gone", "going"], "ans": "went", "monster": "Hantu Grammar", "emoji": "👻"},
    {"q": 'Apa sinonim dari kata "Brave"?', "options": ["--- Pilih ---", "Coward", "Courageous", "Lazy", "Sad"], "ans": "Courageous", "monster": "Penyihir Kosakata", "emoji": "🧙‍♀️"},
]

def get_question(mode):
    return random.choice(MATH_BANK if mode == "math" else ENGLISH_BANK)

# Menu Utama
if st.session_state.page == "menu":
    st.markdown("<h1 class='game-title'>SMART LEARNING HUB</h1>", unsafe_allow_html=True)
    st.markdown("<div class='game-subtitle'>// 3D ANIMATED ARCADE RPG</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='rpg-card-3d'>", unsafe_allow_html=True)
    st.subheader("🛡️ Masukkan Nama Petualang")
    st.session_state.username = st.text_input("Username:", value=st.session_state.username, placeholder="Ketik nama kamu di sini...")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.session_state.username:
        st.success(f"✨ Halo, **{st.session_state.username}**! Pilih jalur pertempuranmu:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🟦 MODE MATEMATIKA"):
                st.session_state.mode = "math"
                st.session_state.hp = 100
                st.session_state.score = 0
                st.session_state.current_q = get_question("math")
                st.session_state.page = "game"
                st.rerun()
        with col2:
            if st.button("🟩 MODE BAHASA INGGRIS"):
                st.session_state.mode = "english"
                st.session_state.hp = 100
                st.session_state.score = 0
                st.session_state.current_q = get_question("english")
                st.session_state.page = "game"
                st.rerun()
    else:
        st.warning("⚠️ Masukkan username terlebih dahulu untuk membuka game.")

# Gameplay Arena
elif st.session_state.page == "game":
    if st.session_state.hp <= 0:
        st.markdown("<h1 class='game-title' style='color: #ff4d4d;'>💀 KAMU KALAH (GAME OVER) 💀</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-size: 1.1rem;'>Monster berhasil mengalahkanmu, <b>{st.session_state.username}</b>!</p>", unsafe_allow_html=True)
        if st.button("🔄 COBA MAIN LAGI"):
            st.session_state.hp = 100
            st.session_state.score = 0
            st.session_state.page = "menu"
            st.rerun()
        st.stop()

    q = st.session_state.current_q

    st.markdown(f"""
        <div class='status-bar'>
            <span>👤 <b>{st.session_state.username}</b></span>
            <span>❤️ NYAWA: <b style='color: #ff4d4d;'>{st.session_state.hp}%</b></span>
            <span>⭐ SKOR: <b style='color: #fde047;'>{st.session_state.score}</b></span>
        </div>
    """, unsafe_allow_html=True)
    
    # Efek Kelas Getar jika Salah Jawab
    card_class = "rpg-card-3d monster-attack-effect" if st.session_state.attack_effect else "rpg-card-3d"
    st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='monster-3d'>{q['emoji']}</div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #fde047; font-family: Orbitron;'>⚔️ {q['monster']} Menyerang! ⚔️</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 1.15rem; margin-bottom: 20px;'><b>Tantangan:</b> {q['q']}</p>", unsafe_allow_html=True)

    st.write("---")

    if st.session_state.mode == "math":
        ans = st.number_input("Masukkan jawaban angka:", step=1, format="%d", key="m_ans")
        if st.button("⚡ LUNCURKAN SERANGAN BALIK!"):
            if ans == q["ans"]:
                st.session_state.attack_effect = False
                st.balloons()
                st.success("🎉 TELAK! Monster terpental mundur! (+25 Skor)")
                st.session_state.score += 25
                st.session_state.current_q = get_question("math")
                st.rerun()
            else:
                st.session_state.hp -= 34
                st.session_state.attack_effect = True
                st.error("💥 GAGAL! Naga menerjang dan melukaimu dengan api! (-34 HP)")
                st.rerun()

    elif st.session_state.mode == "english":
        ans = st.radio("Pilih jawaban yang tepat:", q["options"], key="e_ans")
        if st.button("⚡ UJI MANTRA / JAWAB!"):
            if ans == q["ans"]:
                st.session_state.attack_effect = False
                st.balloons()
                st.success("✨ BERHASIL! Sihirmu melumpuhkan monster! (+25 Skor)")
                st.session_state.score += 25
                st.session_state.current_q = get_question("english")
                st.rerun()
            elif ans == "--- Pilih ---":
                st.warning("⚠️ Pilih salah satu opsi jawaban dulu!")
            else:
                st.session_state.hp -= 34
                st.session_state.attack_effect = True
                st.error("❌ SALAH! Monster membalas dengan cakar mautnya! (-34 HP)")
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("🚪 KELUAR KE MENU"):
        st.session_state.page = "menu"
        st.rerun()
