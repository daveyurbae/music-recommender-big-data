import streamlit as st
import pandas as pd
import time
# Mengimpor fungsi dummy dari utils.py
from utils import get_recommendations_dummy, get_music_info_dummy

# --- Konfigurasi Halaman Streamlit ---
# Mengatur judul halaman, ikon, layout lebar, dan sidebar terbuka secara default
st.set_page_config(
    page_title="Music Recommender Lakehouse",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Kustom untuk Styling Aplikasi ---
# Disematkan menggunakan st.markdown dengan unsafe_allow_html=True
st.markdown("""
<style>
    /* Mengatur padding dan lebar area konten utama Streamlit */
    .main .block-container {
        padding-top: 2rem; /* Padding atas */
        padding-right: 3rem; /* Padding kanan untuk desktop */
        padding-left: 3rem;  /* Padding kiri untuk desktop */
        padding-bottom: 2rem; /* Padding bawah */
    }

    /* Gaya dasar untuk kartu musik */
    .music-card {
        background-color: #262730; /* Warna latar belakang kartu, sesuai secondaryBackgroundColor dari config.toml */
        border-radius: 12px; /* Sudut membulat yang lebih elegan */
        padding: 15px;
        margin-bottom: 20px; /* Jarak antar kartu */
        box-shadow: 0 6px 12px 0 rgba(0,0,0,0.3); /* Bayangan untuk efek kedalaman */
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out; /* Transisi halus untuk efek hover */
        text-align: center; /* Teks di tengah */
        display: flex; /* Menggunakan flexbox untuk layout konten di dalam kartu */
        flex-direction: column; /* Konten disusun secara vertikal */
        justify-content: space-between; /* Mendistribusikan ruang secara merata */
        height: 100%; /* Memastikan semua kartu memiliki tinggi yang sama dalam satu baris */
        overflow: hidden; /* Mencegah konten meluap dari batas kartu */
        cursor: pointer; /* Menunjukkan bahwa kartu dapat diklik (untuk fitur interaktif masa depan) */
    }

    /* Efek hover untuk kartu musik */
    .music-card:hover {
        transform: translateY(-8px); /* Kartu sedikit naik saat di-hover */
        box-shadow: 0 12px 24px 0 rgba(0,0,0,0.5); /* Bayangan menjadi lebih gelap dan menyebar */
    }

    /* Gaya untuk gambar di dalam kartu */
    .music-card img {
        border-radius: 8px; /* Sudut gambar membulat */
        width: 100%; /* Gambar mengisi lebar kartu */
        height: 180px; /* Tinggi gambar tetap untuk konsistensi */
        object-fit: cover; /* Memastikan gambar terisi penuh tanpa distorsi */
        margin-bottom: 12px;
        transition: transform 0.2s ease-in-out; /* Transisi untuk gambar saat hover */
    }

    /* Efek hover pada gambar saat kartu di-hover */
    .music-card:hover img {
        transform: scale(1.05); /* Gambar sedikit membesar */
    }

    /* Gaya untuk judul lagu di kartu */
    .music-card h5 {
        color: #F63366; /* Warna judul lagu, sesuai primaryColor */
        margin-bottom: 4px;
        font-size: 1.2em; /* Ukuran font judul */
        white-space: nowrap; /* Mencegah judul pindah baris */
        overflow: hidden; /* Menyembunyikan jika terlalu panjang */
        text-overflow: ellipsis; /* Menambahkan elipsis (...) jika teks terlalu panjang */
    }

    /* Gaya untuk teks artis/genre di kartu */
    .music-card p {
        color: #F0F2F6; /* Warna teks biasa, mendekati putih */
        font-size: 0.9em;
        margin-bottom: 2px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* Gaya untuk bagian genre dan tahun di kartu */
    .music-card .genre-year {
        font-size: 0.8em;
        color: #bbb; /* Warna abu-abu terang */
        margin-top: auto; /* Mendorong ini ke bagian bawah kartu */
        padding-top: 5px; /* Sedikit padding di atas */
    }

    /* Gaya kustom untuk tombol Streamlit */
    div.stButton > button {
        background-color: #F63366; /* Warna latar belakang sesuai primaryColor */
        color: white; /* Warna teks putih */
        border-radius: 8px; /* Sudut tombol membulat */
        border: none; /* Tanpa border */
        padding: 0.6em 1.2em; /* Padding internal tombol */
        font-size: 1em; /* Ukuran font */
        font-weight: bold; /* Teks tebal */
        transition: background-color 0.2s, transform 0.2s; /* Transisi halus untuk efek hover */
    }
    div.stButton > button:hover {
        background-color: #e02f5a; /* Warna sedikit lebih gelap saat hover */
        transform: translateY(-2px); /* Tombol sedikit naik saat hover */
    }

    /* Gaya kustom untuk expander Streamlit */
    .stExpander div[data-testid="stExpanderForm"] {
        border: 1px solid #3d3e42; /* Border abu-abu gelap untuk expander */
        border-radius: 8px; /* Sudut membulat */
        padding: 15px; /* Padding internal */
        background-color: #1a1b1e; /* Warna latar belakang sedikit lebih terang dari background utama */
    }
</style>
""", unsafe_allow_html=True) # Memungkinkan Streamlit untuk merender HTML/CSS


# --- BAGIAN HEADER APLIKASI DENGAN GAMBAR BANNER ---
try:
    # Mencoba memuat gambar banner lokal dari folder assets
    # Pastikan nama file 'Music-banner.jpg' dan lokasinya benar
    st.image("assets/Music-banner-vector.jpg", use_container_width=True)
except FileNotFoundError:
    # Jika gambar lokal tidak ditemukan, fallback ke gambar placeholder dari internet
    st.warning("Gambar banner tidak ditemukan secara lokal. Menggunakan placeholder.")
    st.image("https://via.placeholder.co/1200x200/4a4e69/ffffff?text=Music+Recommender+Banner", use_container_width=True)

# Judul utama aplikasi
st.title("🎵 Music Recommender Lakehouse")
# Deskripsi singkat aplikasi
st.markdown("""
    Selamat datang di **Music Recommender Lakehouse**!
    Temukan **lagu favorit** Anda berikutnya dari koleksi musik kami yang luas.
    Aplikasi ini memanfaatkan arsitektur data modern untuk rekomendasi yang cerdas dan personal.
""")

st.write("---") # Garis pemisah visual

# --- SIDEBAR UNTUK NAVIGASI ---
st.sidebar.header("Pilih Menu 🎼") # Judul sidebar
st.sidebar.markdown("Navigasikan melalui fitur utama aplikasi kami.") # Deskripsi sidebar

# Radio button untuk memilih halaman
page_selection = st.sidebar.radio(
    "Pilih halaman:",
    ("Dapatkan Rekomendasi 🎶", "Jelajahi Katalog 🎧", "Tentang Proyek Ini 💡")
)

st.sidebar.write("---")
st.sidebar.info("Aplikasi ini dibuat dengan Streamlit untuk proyek Data Lakehouse.")


# --- KONTEN UTAMA BERDASARKAN PILIHAN SIDEBAR ---

if page_selection == "Dapatkan Rekomendasi 🎶":
    st.header("✨ Dapatkan Rekomendasi Musik Personal")

    st.markdown("""
        Masukkan judul lagu yang Anda suka, dan kami akan merekomendasikan lagu-lagu serupa.
        *(Catatan: Rekomendasi saat ini bersifat simulasi. Integrasi data nyata akan datang!)*
    """)

    # Container untuk bagian input rekomendasi
    with st.container(border=True):
        st.subheader("Cari Rekomendasi Berdasarkan Lagu Favorit Anda")
        # Menggunakan kolom untuk tata letak input dan slider
        col1, col2 = st.columns([3, 1]) # Kolom 1 lebih lebar (3 unit), Kolom 2 lebih sempit (1 unit)

        with col1:
            # Input teks untuk judul lagu favorit
            user_song_input = st.text_input(
                "Judul Lagu Favorit Anda:",
                placeholder="Misalnya: Bohemian Rhapsody, Shape of You",
                help="Ketik judul lagu lengkap atau sebagian yang Anda nikmati."
            )
        with col2:
            # Slider untuk memilih jumlah rekomendasi
            num_recommendations = st.slider(
                "Jumlah Rekomendasi:",
                min_value=5,
                max_value=20,
                value=10,
                step=1,
                help="Pilih berapa banyak lagu yang ingin Anda rekomendasikan."
            )

        # Tombol untuk mendapatkan rekomendasi
        if st.button("🚀 Dapatkan Rekomendasi", use_container_width=True, type="primary"):
            if user_song_input:
                # Menampilkan spinner saat proses loading
                with st.spinner(f"Mencari rekomendasi untuk '{user_song_input}'..."):
                    time.sleep(2) # Simulasi waktu loading backend

                    # Memanggil fungsi dummy untuk mendapatkan rekomendasi
                    recommendations_df = get_recommendations_dummy(user_song_input, num_recommendations)

                    if not recommendations_df.empty:
                        st.success(f"Ditemukan {len(recommendations_df)} rekomendasi untuk '{user_song_input}'!")
                        st.markdown("<br>", unsafe_allow_html=True) # Spasi visual

                        # --- Menampilkan Rekomendasi dalam Format Kartu ---
                        num_cols = 4 # Jumlah kolom untuk tampilan desktop
                        # st.columns akan secara otomatis menyesuaikan jumlah kolom berdasarkan lebar layar
                        cols = st.columns(num_cols)
                        
                        for i, row in recommendations_df.iterrows():
                            # Mendapatkan URL gambar dari data dummy, dengan fallback jika tidak ada
                            image_url = row.get('Image_URL', 'https://via.placeholder.co/200x200/808080/ffffff?text=No+Image')
                            with cols[i % num_cols]: # Mendistribusikan kartu ke kolom secara bergantian
                                st.markdown(f"""
                                <div class="music-card">
                                    <img src="{image_url}" alt="Album Art for {row['Title']}">
                                    <h5>{row['Title']}</h5>
                                    <p>Oleh: {row['Artist']}</p>
                                    <div class="genre-year">
                                        <p>{row['Genre']} | {row['Year']}</p>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True) # Spasi setelah kartu
                    else:
                        st.warning(f"Ups! Tidak dapat menemukan rekomendasi untuk '{user_song_input}'. Coba judul lagu lain atau periksa ejaannya.")
            else:
                st.info("💡 Silakan masukkan judul lagu untuk memulai pencarian rekomendasi.")

    st.write("---") # Garis pemisah

# --- Halaman 'Jelajahi Katalog' (Tampilan Kartu) ---
elif page_selection == "Jelajahi Katalog 🎧":
    st.header("🎵 Jelajahi Katalog Musik Kami")
    st.markdown("""
        Lihat koleksi lengkap lagu kami dalam format kartu yang interaktif dan responsif.
        Anda dapat mencari lagu berdasarkan judul atau artis.
    """)

    with st.container(border=True):
        # Input teks untuk pencarian musik di katalog
        search_term = st.text_input("🔍 Cari Musik (Judul atau Artis):",
                                    placeholder="Misalnya: Queen, Blinding Lights",
                                    help="Ketik untuk menyaring katalog musik.")

        # Mengambil semua data musik dummy yang tersedia
        # Perhatikan: get_music_info_dummy(limit=len(get_music_info_dummy(limit=1000))) memastikan kita mendapatkan
        # semua data dummy yang ada, bukan hanya 100 teratas dari default
        all_music_df = get_music_info_dummy(limit=len(get_music_info_dummy(limit=1000)))

        if not all_music_df.empty:
            filtered_df = all_music_df
            # Menyaring DataFrame jika ada term pencarian
            if search_term:
                filtered_df = all_music_df[
                    all_music_df['Title'].str.contains(search_term, case=False, na=False) |
                    all_music_df['Artist'].str.contains(search_term, case=False, na=False)
                ]

            if not filtered_df.empty:
                st.success(f"Ditemukan {len(filtered_df)} lagu yang cocok.")
                st.markdown("<br>", unsafe_allow_html=True) # Spasi

                # --- Menampilkan Kartu Musik dalam Kolom Responsif ---
                num_cols_desktop = 4 # Jumlah kolom yang diinginkan untuk tampilan desktop
                # Streamlit's st.columns akan secara otomatis mengatur penumpukan kolom pada layar yang lebih kecil (mis. mobile)
                cols = st.columns(num_cols_desktop)
                
                # Iterasi melalui baris DataFrame yang difilter untuk membuat kartu
                for i, row in filtered_df.iterrows():
                    # Mendapatkan URL gambar dari data dummy, dengan fallback jika tidak ada
                    image_url = row.get('Image_URL', 'https://via.placeholder.co/200x200/808080/ffffff?text=No+Image')
                    with cols[i % num_cols_desktop]: # Mendistribusikan kartu secara bergantian ke kolom
                        st.markdown(f"""
                        <div class="music-card">
                            <img src="{image_url}" alt="Album Art for {row['Title']}">
                            <h5>{row['Title']}</h5>
                            <p>Oleh: {row['Artist']}</p>
                            <div class="genre-year">
                                <p>{row['Genre']} | {row['Year']}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True) # Spasi setelah kartu

            else:
                st.info("Tidak ada musik yang cocok dengan pencarian Anda.")
        else:
            st.error("Tidak ada data musik yang tersedia untuk ditampilkan. Mohon periksa sumber data.")

    st.write("---")


# --- Halaman 'Tentang Proyek Ini' ---
elif page_selection == "Tentang Proyek Ini 💡":
    st.header("Tentang Proyek Music Recommender Lakehouse 📊")
    st.markdown("""
        Proyek ini adalah demonstrasi sistem rekomendasi musik yang komprehensif, dibangun di atas arsitektur **Lakehouse** modern.
        Tujuannya adalah untuk menunjukkan bagaimana teknologi data canggih dapat diintegrasikan
        untuk menciptakan solusi penemuan musik yang skalabel, efisien, dan personal.
    """)

    st.subheader("Arsitektur Sistem 🏛️")
    # Menggunakan gambar placeholder dari internet untuk diagram arsitektur
    # Menggunakan use_container_width=True untuk responsivitas
    st.image("https://raw.githubusercontent.com/streamlit/docs/main/docs/images/arch-example.png",
             caption="[Image of Conceptual Architecture Diagram (Ganti dengan diagram Anda yang sebenarnya!)]",
             use_container_width=True)
    st.markdown("""
        **Komponen inti** yang membangun ekosistem ini meliputi:
        -   **Kafka**: Mengelola aliran data preferensi pengguna secara *real-time*.
        -   **Spark**: Memproses data *batch* untuk pelatihan model rekomendasi (misalnya, *content-based filtering*) dan *stream processing* untuk interaksi *real-time*.
        -   **Hive**: Menyediakan lapisan metadata dan skema tabel di atas data yang disimpan di MinIO, memungkinkan kueri SQL.
        -   **MinIO**: Berfungsi sebagai *object storage* yang kompatibel dengan S3, menjadi tulang punggung *data lake* kami untuk menyimpan dataset mentah dan hasil olahan.
        -   **Trino**: Mesin kueri SQL terdistribusi yang cepat, memungkinkan akses dan analisis data di seluruh *data lake* (termasuk hasil rekomendasi) secara efisien.
        -   **Streamlit**: Aplikasi web interaktif ini, yang menjadi antarmuka pengguna untuk menampilkan dan berinteraksi dengan sistem rekomendasi.
    """)

    st.subheader("Bagaimana Cara Kerjanya ⚙️")
    st.markdown("""
        1.  **Pengambilan Data (*Data Ingestion*)**: Dataset musik mentah diunggah ke MinIO. Interaksi dan preferensi pengguna (misalnya, lagu yang didengarkan) dapat di-*stream* melalui Kafka.
        2.  **Pemrosesan Data (*Data Processing*)**: Spark memproses data yang ada. Model rekomendasi berbasis konten dilatih dari dataset `Music Info.csv` untuk menemukan kemiripan antar lagu. Interaksi pengguna *real-time* dapat digunakan untuk memperbarui atau menyempurnakan preferensi.
        3.  **Penyimpanan Data (*Data Storage*)**: Data yang sudah diproses, termasuk hasil rekomendasi dan fitur lagu, disimpan kembali di MinIO. Hive mengelola katalog data dan skemanya.
        4.  **Kueri Data (*Data Querying*)**: Trino memungkinkan kueri SQL yang efisien terhadap data yang tersimpan di MinIO melalui metadata Hive, termasuk mengambil hasil rekomendasi yang sudah dihitung.
        5.  **Antarmuka Pengguna (*User Interface*)**: Aplikasi Streamlit ini berinteraksi dengan Trino (melalui fungsi-fungsi di `utils.py`) untuk mengambil dan menampilkan rekomendasi serta informasi katalog musik kepada pengguna.
    """)

    st.subheader("Struktur Proyek 📂")
    st.code("""
music-recommender-lakehouse/
│
├── docker/                  # Pengaturan Docker untuk semua layanan
├── data/                    # Dataset mentah
├── ingestion/               # Kafka producer, MinIO uploader
├── processing/              # Skrip Spark (pelatihan, streaming)
├── metadata/                # Inisialisasi tabel Hive
├── query/                   # Kueri Trino
├── web/                     # Aplikasi web Streamlit (ini!)
├── models/                  # Model yang dilatih (opsional)
├── notebooks/               # Notebook EDA
├── .env                     # Variabel lingkungan
├── requirements.txt         # Dependensi Python
└── README.md                # Dokumentasi proyek
    """, language="bash")

    st.write("---")
    st.info("✨ Proyek ini adalah bagian dari eksplorasi dan implementasi arsitektur Data Lakehouse.")
