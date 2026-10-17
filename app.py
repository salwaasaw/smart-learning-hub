import streamlit as st

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Smart Learning Hub: Ultimate RPG",
    page_icon="⚡",
    layout="centered"
)

# Styling CSS Kustom (Desain RPG Profesional, Warna Harmonis, Tidak Nabrak)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Inter:wght@400;600;800&display=swap');

    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #111827 50%, #1e1b4b 100%);
        font-family: 'Inter', sans-serif;
        color: #f3f4f6;
    }

    .rpg-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 2.2rem;
        text-align: center;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    .rpg-subtitle {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        color: #9ca3af;
        font-size: 0.85rem;
        letter-spacing: 2px;
        margin-bottom: 25px;
    }

    .rpg-card {
        background: rgba(17, 24, 39, 0.85);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }

    .status-box {
        display: flex;
        justify-content: space-between;
        background: rgba(31, 41, 55, 0.8);
        padding: 12px 20px;
        border-radius: 10px;
        border: 1px solid #374151;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.9rem;
        margin-bottom: 20px;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        padding: 12px;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
        transition: all 0.2s ease-in-out;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(79, 70, 229, 0.6);
        background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
    }

    .stTextInput input {
        background-color: rgba(3, 7, 18, 0.9) !important;
        color: #ffffff !important;
        border: 1px solid #4b5563 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inisialisasi Data Game (Session State)
if "page" not in st.session_state: st.session_state.page = "menu"
if "username" not in st.session_state: st.session_state.username = ""
if "score" not in st.session_state: st.session_state.score = 0
if "hp" not in st.session_state: st.session_state.hp = 100
if "level" not in st.session_state: st.session_state.level = 1
if "mode" not in st.session_state: st.session_state.mode = ""

# ==========================================
# HALAMAN 1: MENU UTAMA (LOBI PETUALANG)
# ==========================================
if st.session_state.page == "menu":
    st.markdown("<h1 class='rpg-title'>SMART LEARNING HUB</h1>", unsafe_allow_html=True)
    st.markdown("<div class='rpg-subtitle'>// ULTIMATE RPG DUNGEON EDITION</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='rpg-card'>", unsafe_allow_html=True)
    st.subheader("🛡️ Registrasi Petualang")
    st.write("Masukkan nama agen/petualangmu untuk memulai misi:")
    st.session_state.username = st.text_input("Username:", value=st.session_state.username, placeholder="Contoh: Alex_Pro")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.session_state.username:
        st.success(f"⚡ Selamat datang, **{st.session_state.username}**! Pilih jalur dungeon pertempuranmu:")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🟦 DUNGEON MATEMATIKA"):
                st.session_state.mode = "math"
                st.session_state.level = 1
                st.session_state.hp = 100
                st.session_state.score = 0
                st.session_state.page = "game"
                st.rerun()
        with col2:
            if st.button("🟩 DUNGEON BAHASA INGGRIS"):
                st.session_state.mode = "english"
                st.session_state.level = 1
                st.session_state.hp = 100
                st.session_state.score = 0
                st.session_state.page = "game"
                st.rerun()
    else:
        st.warning("⚠️ Masukkan username terlebih dahulu untuk membuka gerbang dungeon.")

# ==========================================
# HALAMAN 2: GAMEPLAY DUNGEON (BERDASARKAN LEVEL & NYAWA)
# ==========================================
elif st.session_state.page == "game":
    # Cek Kondisi Game Over
    if st.session_state.hp <= 0:
        st.markdown("<h1 class='rpg-title' style='color: #ef4444;'>💀 GAME OVER 💀</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Kamu kehabisan nyawa, Agen <b>{st.session_state.username}</b>. Coba lagi dan taklukkan dungeon-nya!</p>", unsafe_allow_html=True)
        if st.button("🔄 COBA LAGI DARI AWAL"):
            st.session_state.hp = 100
            st.session_state.score = 0
            st.session_state.level = 1
            st.session_state.page = "menu"
            st.rerun()
        st.stop()

    mode_nama = "MATEMATIKA" if st.session_state.mode == "math" else "BAHASA INGGRIS"
    
    # Status Bar Atas (HP & Level)
    st.markdown(f"""
        <div class='status-box'>
            <span>🛡️ AGEN: <b>{st.session_state.username}</b></span>
            <span>❤️ HP: <b style='color: #ef4444;'>{st.session_state.hp}%</b></span>
            <span>⭐ SKOR: <b style='color: #fbbf24;'>{st.session_state.score}</b></span>
            <span>🗺️ LEVEL: <b style='color: #38bdf8;'>{st.session_state.level}/3</b></span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='rpg-card'>", unsafe_allow_html=True)
    
    # ==========================================
    # LOGIKA MODE MATEMATIKA (3 LEVEL)
    # ==========================================
    if st.session_state.mode == "math":
        if st.session_state.level == 1:
            st.info("👾 **Level 1: Goblin Kalkulasi** menghadang jalanmu!")
            st.markdown("#### Berapakah hasil dari: $12 \\times 5 - 15$ ?")
            jawaban = st.number_input("Jawaban Angka:", step=1, format="%d", key="m1")
            
            if st.button("⚔️ SERANG GOBLIN"):
                if jawaban == 45:
                    st.success("💥 Telak! Goblin tumbang! (+20 Skor)")
                    st.session_state.score += 20
                    st.session_state.level = 2
                    st.rerun()
                else:
                    st.session_state.hp -= 35
                    st.error("💔 Serangan meleset! Kamu terkena damage monster (-35 HP).")

        elif st.session_state.level == 2:
            st.info("🐉 **Level 2: Naga Aljabar** memuntahkan api kepadamu!")
            st.markdown("#### Selesaikan persamaan: $8 \\times 8 + 25 - 9$ ?")
            jawaban = st.number_input("Jawaban Angka:", step=1, format="%d", key="m2")
            
            if st.button("⚔️ SERANG NAGA"):
                if jawaban == 80:
                    st.success("🔥 Naga Aljabar Berhasil Dikalahkan! (+30 Skor)")
                    st.session_state.score += 30
                    st.session_state.level = 3
                    st.rerun()
                else:
                    st.session_state.hp -= 40
                    st.error("💥 Kamu terkena semburan api naga! (-40 HP).")

        elif st.session_state.level == 3:
            st.info("👑 **Level 3 (BOSS): Raja Matematika Kritis** menantangmu!")
            st.markdown("#### Hitung cepat: $(50 \\div 2) + (15 \\times 3) - 10$ ?")
            jawaban = st.number_input("Jawaban Angka:", step=1, format="%d", key="m3")
            
            if st.button("⚔️ SERANG BOSS AKHIR"):
                if jawaban == 60:
                    st.balloons()
                    st.success("🏆 LUAR BIASA! BOSS TERAKHIR KALAH! Kamu Menang! (+50 Skor)")
                    st.session_state.score += 50
                else:
                    st.session_state.hp -= 50
                    st.error("💀 Serangan Boss sangat fatal! (-50 HP).")

    # ==========================================
    # LOGIKA MODE BAHASA INGGRIS (3 LEVEL)
    # ==========================================
    elif st.session_state.mode == "english":
        if st.session_state.level == 1:
            st.info("📜 **Level 1: Penjaga Gerbang Kata** menghadang!")
            st.markdown("#### Lengkapi kalimat rumpang berikut:")
            st.markdown('> *"She _______ to the library yesterday to borrow a book."*')
            jawaban = st.radio("Opsi:", ["--- Pilih ---", "go", "went", "gone", "going"], key="e1")
            
            if st.button("🔑 UJI KUNCI PINTU"):
                if jawaban == "went":
                    st.success("✨ Pintu Level 1 Terbuka! (+20 Skor)")
                    st.session_state.score += 20
                    st.session_state.level = 2
                    st.rerun()
                elif jawaban == "--- Pilih ---":
                    st.warning("⚠️ Pilih salah satu opsi kata.")
                else:
                    st.session_state.hp -= 35
                    st.error("❌ Salah! Penjaga gerbang menyerangmu (-35 HP).")

        elif st.session_state.level == 2:
            st.info("🦅 **Level 2: Monster Sinonim** terbang menghadang!")
            st.markdown("#### Apa sinonim (persamaan kata) dari kata **'Brave'** ?")
            jawaban = st.radio("Opsi:", ["--- Pilih ---", "Coward", "Courageous", "Lazy", "Sad"], key="e2")
            
            if st.button("🔑 LAWAN MONSTER SINONIM"):
                if jawaban == "Courageous":
                    st.success("✨ Monster Sinonim berhasil dijinakkan! (+30 Skor)")
                    st.session_state.score += 30
                    st.session_state.level = 3
                    st.rerun()
                elif jawaban == "--- Pilih ---":
                    st.warning("⚠️ Pilih salah satu opsi kata.")
                else:
                    st.session_state.hp -= 40
                    st.error("❌ Jawaban keliru! Monster menyerang balik (-40 HP).")

        elif st.session_state.level == 3:
            st.info("👑 **Level 3 (BOSS): Penyihir Grammar Kuno** menantangmu!")
            st.markdown("#### Lengkapi kalimat Perfect Tense ini:")
            st.markdown('> *"They have _______ finished their homework before the teacher arrived."*')
            jawaban = st.radio("Opsi:", ["--- Pilih ---", "already", "yet", "still", "ever"], key="e3")
            
            if st.button("🔑 UJI MANTRA BOSS"):
                if jawaban == "already":
                    st.balloons()
                    st.success("🏆 KELAS ABIS! Kamu Mengalahkan Penyihir Grammar! (+50 Skor)")
                    st.session_state.score += 50
                elif jawaban == "--- Pilih ---":
                    st.warning("⚠️ Pilih salah satu opsi kata.")
                else:
                    st.session_state.hp -= 50
                    st.error("💀 Mantra terlarang menghantammu! (-50 HP).")

    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("⬅️ KELUAR KE LOBI UTAMA"):
        st.session_state.page = "menu"
        st.rerun()
