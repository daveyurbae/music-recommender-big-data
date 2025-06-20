import pandas as pd
import random

# Data dummy untuk simulasi
DUMMY_MUSIC_CATALOG = [
    {"Title": "Bohemian Rhapsody", "Artist": "Queen", "Genre": "Classic Rock", "Year": 1975},
    {"Title": "Stairway to Heaven", "Artist": "Led Zeppelin", "Genre": "Rock", "Year": 1971},
    {"Title": "Hotel California", "Artist": "Eagles", "Genre": "Rock", "Year": 1976},
    {"Title": "Shape of You", "Artist": "Ed Sheeran", "Genre": "Pop", "Year": 2017},
    {"Title": "Blinding Lights", "Artist": "The Weeknd", "Genre": "R&B", "Year": 2019},
    {"Title": "Someone You Loved", "Artist": "Lewis Capaldi", "Genre": "Pop", "Year": 2018},
    {"Title": "Dance Monkey", "Artist": "Tones And I", "Genre": "Dance-Pop", "Year": 2019},
    {"Title": "Levitating", "Artist": "Dua Lipa", "Genre": "Pop", "Year": 2020},
    {"Title": "Heat Waves", "Artist": "Glass Animals", "Genre": "Indie Pop", "Year": 2020},
    {"Title": "Good 4 U", "Artist": "Olivia Rodrigo", "Genre": "Pop Punk", "Year": 2021},
    {"Title": "MONTERO (Call Me By Your Name)", "Artist": "Lil Nas X", "Genre": "Hip Hop", "Year": 2021},
    {"Title": "Stay", "Artist": "The Kid Laroi & Justin Bieber", "Genre": "Pop", "Year": 2021},
    {"Title": "As It Was", "Artist": "Harry Styles", "Genre": "Pop", "Year": 2022},
    {"Title": "Sweet Child O' Mine", "Artist": "Guns N' Roses", "Genre": "Hard Rock", "Year": 1987},
    {"Title": "Wonderwall", "Artist": "Oasis", "Genre": "Britpop", "Year": 1995},
    {"Title": "Smells Like Teen Spirit", "Artist": "Nirvana", "Genre": "Grunge", "Year": 1991},
    {"Title": "Billie Jean", "Artist": "Michael Jackson", "Genre": "Pop", "Year": 1982},
    {"Title": "Like a Rolling Stone", "Artist": "Bob Dylan", "Genre": "Folk Rock", "Year": 1965},
    {"Title": "I Will Always Love You", "Artist": "Whitney Houston", "Genre": "R&B", "Year": 1992},
    {"Title": "Despacito", "Artist": "Luis Fonsi ft. Daddy Yankee", "Genre": "Latin Pop", "Year": 2017},
    # Tambahkan lebih banyak data jika ingin demonstrasi scrolling yang lebih panjang
    {"Title": "Uptown Funk", "Artist": "Mark Ronson ft. Bruno Mars", "Genre": "Funk-Pop", "Year": 2014},
    {"Title": "Shallow", "Artist": "Lady Gaga & Bradley Cooper", "Genre": "Country Pop", "Year": 2018},
    {"Title": "Bad Guy", "Artist": "Billie Eilish", "Genre": "Electropop", "Year": 2019},
    {"Title": "Old Town Road", "Artist": "Lil Nas X ft. Billy Ray Cyrus", "Genre": "Country Rap", "Year": 2019},
    {"Title": "Someone Like You", "Artist": "Adele", "Genre": "Soul", "Year": 2011},
    {"Title": "Happy", "Artist": "Pharrell Williams", "Genre": "Funk-Soul", "Year": 2013},
    {"Title": "Thunder", "Artist": "Imagine Dragons", "Genre": "Pop Rock", "Year": 2017},
    {"Title": "Radioactive", "Artist": "Imagine Dragons", "Genre": "Pop Rock", "Year": 2012},
    {"Title": "Believer", "Artist": "Imagine Dragons", "Genre": "Pop Rock", "Year": 2017},
    {"Title": "Counting Stars", "Artist": "OneRepublic", "Genre": "Pop Rock", "Year": 2013},
    {"Title": "Sugar", "Artist": "Maroon 5", "Genre": "Pop", "Year": 2015},
    {"Title": "Girls Like You", "Artist": "Maroon 5 ft. Cardi B", "Genre": "Pop", "Year": 2018},
    {"Title": "Havana", "Artist": "Camila Cabello ft. Young Thug", "Genre": "Latin Pop", "Year": 2017},
    {"Title": "Senorita", "Artist": "Shawn Mendes & Camila Cabello", "Genre": "Latin Pop", "Year": 2019},
    {"Title": "Watermelon Sugar", "Artist": "Harry Styles", "Genre": "Pop", "Year": 2019},
    {"Title": "Adore You", "Artist": "Harry Styles", "Genre": "Pop", "Year": 2019},
]

def _generate_image_url(title: str, artist: str) -> str:
    """Generates a placeholder image URL based on title and artist."""
    text = f"{title[:10]} - {artist[:10]}" # Ambil beberapa karakter pertama
    text = text.replace(" ", "%20").replace("&", "and").replace(",", "") # Format untuk URL
    # Ukuran gambar 200x200, warna latar belakang abu-abu gelap, teks putih
    return f"https://placehold.co/200x200/343a40/ffffff?text={text}"

def get_recommendations_dummy(user_song_title: str, num_recs: int = 10) -> pd.DataFrame:
    """
    Mengembalikan rekomendasi musik dummy berdasarkan judul lagu input.
    Fungsi ini sekarang juga menambahkan URL gambar.
    """
    lower_input = user_song_title.lower()
    if "queen" in lower_input or "bohemian" in lower_input:
        similar_songs = [s for s in DUMMY_MUSIC_CATALOG if s["Genre"] in ["Classic Rock", "Rock"]]
    elif "pop" in lower_input or "shape of you" in lower_input:
        similar_songs = [s for s in DUMMY_MUSIC_CATALOG if s["Genre"] in ["Pop", "Dance-Pop", "Latin Pop"]]
    elif "hip hop" in lower_input or "montero" in lower_input:
        similar_songs = [s for s in DUMMY_MUSIC_CATALOG if s["Genre"] in ["Hip Hop", "R&B", "Country Rap"]]
    else:
        similar_songs = list(DUMMY_MUSIC_CATALOG)

    random.shuffle(similar_songs)
    recommended_songs = []
    for song in similar_songs:
        if song["Title"].lower() != lower_input:
            song_with_image = song.copy()
            song_with_image["Image_URL"] = _generate_image_url(song["Title"], song["Artist"])
            recommended_songs.append(song_with_image)
        if len(recommended_songs) >= num_recs:
            break

    return pd.DataFrame(recommended_songs)

def get_music_info_dummy(limit: int = 100) -> pd.DataFrame:
    """
    Mengembalikan sampel informasi musik dummy, sekarang juga menambahkan URL gambar.
    """
    # Pastikan limit tidak melebihi jumlah data dummy yang tersedia
    actual_limit = min(limit, len(DUMMY_MUSIC_CATALOG))
    selected_songs = random.sample(DUMMY_MUSIC_CATALOG, actual_limit)

    for song in selected_songs:
        song["Image_URL"] = _generate_image_url(song["Title"], song["Artist"])
    
    return pd.DataFrame(selected_songs)