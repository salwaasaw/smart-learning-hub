import streamlit as st

# 1. Konfigurasi Halaman Web
st.set_page_config(
    page_title="Smart Learning Hub: 3D RPG Edition",
    page_icon="⚡",
    layout="centered"
)

# 2. Desain CSS Kustom (Animated Background, Glassmorphism, & 3D Cards)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');

    /* Animasi Background Bergerak Halus ala Game Profesional */
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #090d16, #311042);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f8fafc;
    }

    /* Judul Utama dengan Efek 3D / Neon Tipis */
    .game-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 2.5rem;
        text-align: center;
        background: linear-gradient(135deg, #60a5fa 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(96, 165, 250, 0.3);
        margin-bottom: 0px;
    }

    .game-subtitle {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        color: #94a3b8;
        font-size: 0.9rem;
        letter-spacing: 2px;
        margin-bottom: 30px;
    }

    /* Kotak Bergaya Glassmorphism (Efek Kaca 3D) */
    .rpg-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }

    /* Tombol Kustom ala Game */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        padding: 12px;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
    }

    /* Kotak Input Teks */
    .stTextInput input {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Inisialisasi Data Sesi Game
if "page" not in st.session_state:
    st.session_state.page = "menu"
if "score" not in st.session_state:
    st.session_state.score = 0
if "username" not in st.session_state:
    st.session_state.username = ""

# ==========================================
# HALAMAN 1: MAIN MENU (LOBI UTAMA)
# ==========================================
if st.session_state.page == "menu":
    st.markdown("<h1 class='game-title'>SMART LEARNING HUB</h1>", unsafe_allow_html=True)
    st.markdown("<div class='game-subtitle'>// 3D INTERACTIVE EDUCATIONAL DUNGEON</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='rpg-card'>", unsafe_allow_html=True)
    st.subheader("🛡️ Identifikasi Petualang")
    st.write("Masukkan nama codename/username kamu sebelum memasuki gerbang dungeon:")
    st.session_state.username = st.text_input("Username Petualang:", value=st.session_state.username, placeholder="Contoh: Alex_Gamer")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.session_state.username:
        st.success(f"⚡ Akses Diberikan! Selamat datang, **{st.session_state.username}**. Pilih jalur dungeon kamu:")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🟦 DUNGEON MATEMATIKA"):
                st.session_state.mode = "math"
                st.session_state.page = "game"
                st.rerun()
        with col2:
            if st.button("🟩 DUNGEON BAHASA INGGRIS"):
                st.session_state.mode = "english"
                st.session_state.page = "game"
                st.rerun()
    else:
        st.warning("⚠️ Masukkan username terlebih dahulu untuk mengaktifkan pilihan dungeon.")

# ==========================================
# HALAMAN 2: GAMEPLAY ARENA (DALAM DUNGEON)
# ==========================================
elif st.session_state.page == "game":
    mode_nama = "MATEMATIKA" if st.session_state.mode == "math" else "BAHASA INGGRIS"
    tema_warna = "🔵" if st.session_state.mode == "math" else "🟢"
    
    st.markdown(f"<h2 class='game-title' style='font-size: 1.8rem;'>{tema_warna} ARENA: {mode_nama}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #38bdf8; font-family: Orbitron;'>AGENT: {st.session_state.username} | SCORE: {st.session_state.score}</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='rpg-card'>", unsafe_allow_html=True)
    
    # Logika Soal Matematika
    if st.session_state.mode == "math":
        st.info("👾 **Threat Detected:** Monster Hitungan menghadang jalan keluar!")
        st.markdown("#### Tantangan: Berapakah hasil dari operasi $12 \\times 5 - 15$ ?")
        
        jawaban_math = st.number_input("Masukkan jawaban numerik:", step=1, format="%d")
        
        if st.button("⚔️ LUNCURKAN SERANGAN"):
            if jawaban_math == 45:
                st.success("🎯 Critical Hit! Monster berhasil dilumpuhkan! (+10 Skor)")
                st.session_state.score += 10
            else:
                st.error("❌ Serangan meleset! Sistem pertahanan musuh terlalu kuat. Coba hitung lagi!")

    # Logika Soal Bahasa Inggris
    elif st.session_state.mode == "english":
        st.info("📜 **Quest Active:** Pintu gerbang utama terkunci oleh mantra kuno.")
        st.markdown("#### Tantangan: Lengkapi kalimat rumpang berikut dengan tata bahasa yang tepat:")
        st.markdown('> *"She _______ to the library yesterday to borrow a book."*')
        
        jawaban_eng = st.radio(
            "Pilih opsi kata:", 
            ["--- Pilih Jawaban ---", "go", "went", "gone", "going"]
        )
        
        if st.button("🔑 UJI KUNCI MANTRA"):
            if jawaban_eng == "went":
                st.success("✨ Mantra Berhasil! Pintu dungeon terbuka lebar! (+10 Skor)")
                st.session_state.score += 10
            elif jawaban_eng == "--- Pilih Jawaban ---":
                st.warning("⚠️ Silakan pilih salah satu opsi kata di atas.")
            else:
                st.error("❌ Mantra gagal! Perhatikan bentuk past tense untuk kejadian lampau.")

    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("⬅️ KELUAR KE LOBI UTAMA"):
        st.session_state.page = "menu"
        st.rerun()