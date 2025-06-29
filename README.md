| Nama  | NRP        |
| ----- | ---------- |
| Mendo | 5027221073 |
| Dani  | 5027221057 |
| Dave  | 5027231043 |


**Arsitektur Spotify Recommendation**
![WhatsApp Image 2025-06-27 at 10 56 26_d2276c3e](https://github.com/user-attachments/assets/42910bf1-0a8c-4ae3-9110-865fa123ca22)

# Music Recommender System - Big Data Final Project
## Gambaran Umum

Proyek ini adalah **Music Recommender System** yang dibangun sebagai bagian dari **proyek akhir mata kuliah Big Data**. Sistem ini menggunakan berbagai alat dan teknologi untuk pengambilan data, pemrosesan, dan analisis, yang pada akhirnya memberikan rekomendasi musik kepada pengguna. Fokus dari proyek ini adalah untuk memanfaatkan teknik big data dalam menangani dataset besar dan memberikan rekomendasi secara real-time.

### Komponen Utama:
1. **UI (Streamlit)**: Menyediakan antarmuka pengguna yang ramah untuk berinteraksi dengan sistem rekomendasi.
2. **Pengambilan dan Pemrosesan Data**: Melibatkan ekstraksi, pembersihan, dan pemrosesan dataset besar.
3. **Pelatihan Model**: Menggabungkan model pembelajaran mesin untuk rekomendasi musik.
4. **Kafka & Minio**: Untuk streaming data secara real-time dan manajemen penyimpanan.

## Struktur Proyek

```
music-recommender-big-data-main/
├── assets/                     # Aset untuk UI (gambar, ikon, dll.)
├── Docker/                     # Konfigurasi Docker untuk containerization
├── ingestion/                  # Skrip untuk pengambilan data
├── minio/                      # Minio untuk penyimpanan objek
├── processing/                 # Skrip pemrosesan data
├── web/                        # Aplikasi UI Streamlit
│   ├── app.py                  # Aplikasi Streamlit utama untuk UI
│   ├── requirements.txt        # Daftar paket Python yang diperlukan
│   └── utils.py                # Fungsi utilitas untuk UI
├── .env                        # Variabel lingkungan untuk informasi sensitif
├── .gitignore                  # Pengaturan git ignore
├── README.md                   # Dokumentasi proyek (file ini)
└── requirements.txt            # Ketergantungan paket Python untuk proyek
```

- **Streamlit**: Digunakan untuk membangun antarmuka pengguna interaktif.
- **Kafka**: Untuk streaming data secara real-time.
- **Minio**: Manajemen penyimpanan objek untuk menangani dataset besar.
- **Docker**: Mengonversi aplikasi menjadi container untuk kemudahan deployment.
- **Python**: Bahasa pemrograman untuk pemrosesan data dan pembelajaran mesin.
- **Pandas**: Manipulasi dan analisis data.
- **Scikit-learn**: Perpustakaan pembelajaran mesin untuk pelatihan model.

## Instalasi dan Pengaturan
Langkah 1: Instal Dependesnsi
pip install -r requirements.txt
![Screenshot 2025-06-27 134743](https://github.com/user-attachments/assets/1e877a06-2139-4c9b-939a-44c21a3a9991)
![Screenshot 2025-06-27 134748](https://github.com/user-attachments/assets/d900e21f-da34-41e5-8112-8b588a72a192)


Langkah 2: Jalankan UI Streamlit
streamlit run web/app.py
![Screenshot 2025-06-27 134959](https://github.com/user-attachments/assets/b8c3da06-3f53-47f9-929c-1578664463c8)
![Screenshot 2025-06-27 135009](https://github.com/user-attachments/assets/83429430-19fa-46e7-b3eb-2bf136eab64e)

