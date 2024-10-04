import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Load dataset
df_raw = pd.read_csv("main_data.csv")
df_time = df_raw.copy()
df_time['dteday'] = pd.to_datetime(df_time['dteday'])
df_time['hr'] = pd.to_timedelta(df_time['hr'], unit='h')
df_time['hr'] = df_time['hr'].dt.total_seconds().apply(lambda x: f"{int(x // 3600):02}:{int((x % 3600) // 60):02}:{int(x % 60):02}")

df = df_time.copy()
# Melakukan mapping untuk setiap variabel kategorikal
df['holiday'] = df['holiday'].map({0: 'Tidak', 1: 'Ya'})
df['weekday'] = df['weekday'].map({0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'})
df['workingday'] = df['workingday'].map({0: 'Tidak', 1: 'Ya'})


# Sidebar untuk pertanyaan

st.sidebar.title('Pertanyaan')
st.sidebar.markdown('Pilih pertanyaannya:')

data_choices = st.sidebar.selectbox(
    'Pertanyaan', 
    [
        'Bagaimana jumlah peminjaman sepeda berubah dari waktu ke waktu?',
        'Apakah cuaca mempengaruhi seberapa banyak orang meminjam sepeda?',
        'Apakah ada pola musiman dalam penggunaan sepeda?',
        'Bagaimana jumlah pengguna sepeda casual dan registered berubah seiring waktu?'
    ]
)
st.sidebar.caption('Reni Uswatun Hasanah')

###
st.header('🚲Bike Sharing Analysis Dashboard🚲')

# Analysis based on selected question
if data_choices == 'Bagaimana jumlah peminjaman sepeda berubah dari waktu ke waktu?':
    # Membuat pivot tabel dengan hour 
    pivot_hour_weekday = df.groupby('hr').agg({'cnt': 'mean'}).reset_index()
    # Membuat pivot tabel untuk hari
    pivot_weekday = df.groupby(by=["weekday"]).agg({"cnt": "mean"}).reindex(['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']).reset_index()
    # Membuat pivot table combine
    pivot_combined = df.groupby(['weekday', 'hr']).agg({'cnt': 'mean'}).reset_index()
    # Pivot tabel untuk hari libur dan kerja
    pivot_holiday = df.groupby('holiday').agg({'cnt': 'mean'}).reset_index()
    pivot_workingday = df.groupby('workingday').agg({"cnt": "mean"}).reset_index()

    # Judul untuk section
    st.subheader('Jumlah Peminjaman Sepeda dari Waktu ke Waktu')
    st.write("""#### Rata-rata Peminjaman Sepeda per Jam""")
    # Rata-rata Peminjaman Sepeda per Jam
    plt.figure(figsize=(25, 10))
    sns.lineplot(x='hr', y='cnt', data=pivot_hour_weekday, palette='pastel')
    plt.title('Rata-rata Peminjaman Sepeda per Jam')
    plt.xlabel('Jam')
    plt.ylabel('Jumlah Peminjaman')
    st.pyplot(plt)  # Menampilkan plot di Streamlit
    
    # Penjelasan untuk plot Rata-rata Peminjaman Sepeda per Jam
    st.write("""
    **Penjelasan:**
    Grafik di atas menunjukkan rata-rata jumlah peminjaman sepeda per jam. 
    Dari grafik ini, kita dapat melihat pola penggunaan sepeda selama sehari. 
    Biasanya, penggunaan tertinggi terjadi pada jam pagi (sekitar jam 8-9) dan sore (sekitar jam 5-6), 
    mencerminkan kebiasaan orang-orang yang menggunakan sepeda untuk perjalanan ke dan dari tempat kerja.
    """)

    st.write("""#### Rata-rata Peminjaman Sepeda per Hari""")
    # Bar plot untuk pivot_weekday
    plt.figure(figsize=(25, 10))
    sns.barplot(x='weekday', y='cnt', data=pivot_weekday, palette='pastel')
    plt.title('Rata-rata Peminjaman Sepeda per Hari')
    plt.xlabel('Hari')
    plt.ylabel('Jumlah Peminjaman')
    st.pyplot(plt)  # Menampilkan plot di Streamlit
    # Penjelasan untuk plot Rata-rata Peminjaman Sepeda per Hari
    st.write("""
    **Penjelasan:**
    Grafik ini menunjukkan rata-rata peminjaman sepeda berdasarkan hari dalam seminggu. 
    Dari grafik, terlihat bahwa jumlah peminjaman cenderung lebih tinggi pada hari kerja dibandingkan dengan akhir pekan, 
    menunjukkan bahwa sepeda lebih banyak digunakan untuk transportasi sehari-hari.
    """)
    
    st.write("""#### Rata-rata Peminjaman Sepeda per Jam dan per Hari""")
    # Plot Rata-rata Peminjaman Sepeda per Jam dan Hari
    plt.figure(figsize=(25, 10))
    pivot_combined_pivot = pivot_combined.pivot(index='weekday', columns='hr', values='cnt')
    sns.heatmap(pivot_combined_pivot, annot=True, fmt='.2f', cmap='YlGnBu')
    plt.title('Rata-rata Peminjaman Sepeda per Jam dan Hari')
    plt.xlabel('Jam')
    plt.ylabel('Hari')
    st.pyplot(plt)  # Menampilkan plot di Streamlit
    
    # Penjelasan untuk plot Rata-rata Peminjaman Sepeda per Jam dan Hari
    st.write("""
    **Penjelasan:**
    Heatmap di atas menunjukkan rata-rata peminjaman sepeda per jam untuk setiap hari dalam seminggu. 
    Setiap sel dalam heatmap menunjukkan jumlah peminjaman, dengan warna yang lebih gelap menandakan jumlah yang lebih tinggi. 
    Ini membantu kita memahami pola peminjaman secara lebih mendetail berdasarkan waktu dan hari. Dapat dilihat warna cenderung menggelap pada hari kerja diantara jamberangkat kerja dan jam pulang kerja. Serta, ketika liburan warna cenderung gelap ketika siang menuju sore.
    """)

    st.write("""#### Rata-rata Peminjaman Sepeda berdasarkan hari kerja""")
    # Plot Rata-rata Peminjaman Sepeda terhadap Hari Kerja
    plt.figure(figsize=(25, 10))
    sns.barplot(x='workingday', y='cnt', data=pivot_workingday, palette='coolwarm')
    plt.title('Rata-rata Peminjaman Sepeda berdasarkan Hari Kerja')
    plt.xlabel('Hari Kerja')
    plt.ylabel('Rata-rata Peminjaman')
    st.pyplot(plt)  # Menampilkan plot di Streamlit
    # Penjelasan untuk plot Rata-rata Peminjaman Sepeda berdasarkan Hari Kerja
    st.write("""
    **Penjelasan:**
    Grafik ini menunjukkan rata-rata peminjaman sepeda berdasarkan status hari kerja (kerja atau tidak). 
    Dari grafik, terlihat bahwa peminjaman lebih tinggi pada hari kerja, menunjukkan bahwa sepeda digunakan lebih banyak untuk perjalanan ke tempat kerja serta pulang ketika hari kerja.
    """)

elif data_choices == 'Apakah cuaca mempengaruhi seberapa banyak orang meminjam sepeda?':
    st.subheader('Pengaruh Cuaca terhadap Peminjaman Sepeda')
    # Pengaruh Suhu Rata-Rata Harian terhadap Peminjaman
    pivot_daily_temp = df.groupby('dteday').agg({
        "temp": "mean",
        "atemp": "mean",
        "cnt": "mean"
    }).reset_index()
    # Pengaruh Suhu per Jam
    pivot_hourly_temp = df.groupby('hr').agg({
        "temp": "mean",
        "atemp": "mean",
        "cnt": "mean"
    }).reset_index()
    # Pengaruh Suhu dan Hari dalam Seminggu:
    pivot_weekday_temp = df.groupby(['weekday', 'hr']).agg({
        "temp": "mean",
        "atemp": "mean",
        "cnt": "mean"
    }).reset_index()
    # Gabungan Semua Variabel
    pivot_combined_temp = df.groupby(['dteday', 'hr', 'temp', 'atemp']).agg({'cnt': 'mean'}).reset_index()
    
    # Visualisasi hubungan antara suhu dan jumlah peminjaman
    st.write("""#### Hubungan antara Suhu dan Jumlah Peminjaman""")
    plt.figure(figsize=(25, 10))
    sns.scatterplot(x='temp', y='cnt', data=pivot_daily_temp)
    plt.title('Hubungan antara Suhu dan Jumlah Peminjaman')
    plt.xlabel('Suhu (temp)')
    plt.ylabel('Jumlah Peminjaman')
    st.pyplot(plt)
    st.write("""
    **Penjelasan:**
    Grafik ini menunjukkan hubungan antara suhu dan jumlah peminjaman sepeda. 
    Dari grafik ini, kita dapat melihat bahwa seiring dengan meningkatnya suhu, 
    jumlah peminjaman sepeda juga cenderung meningkat. Ini menunjukkan bahwa 
    suhu yang lebih hangat mendorong lebih banyak orang untuk menggunakan sepeda.
    """)

    # Plot Pengaruh Suhu Hari terhadap Peminjaman
    st.write("""#### Rata-rata Peminjaman Sepeda Hari (Senin-Minggu) berdasarkan Suhu""")
    plt.figure(figsize=(25, 10))
    pivot_dteday_temp_cnt = pivot_weekday_temp.pivot(index='weekday', columns='temp', values='cnt')
    sns.heatmap(pivot_dteday_temp_cnt, annot=True, fmt='.2f', cmap='YlGnBu')
    plt.title('Rata-rata Peminjaman Sepeda Hari (senin-minggu) berdasarkan suhu')
    plt.xlabel('Suhu')
    plt.ylabel('Hari')
    st.pyplot(plt)
    st.write("""
    **Penjelasan:**
    Heatmap ini menunjukkan rata-rata peminjaman sepeda untuk setiap hari dalam seminggu 
    berdasarkan suhu. Setiap sel menunjukkan jumlah peminjaman dengan suhu yang berbeda, 
    membantu kita memahami bagaimana peminjaman bervariasi menurut hari dan suhu.
    """)

    # Plot Pengaruh Suhu per Jam terhadap Peminjaman
    st.write("""#### Rata-rata Peminjaman Sepeda per Jam berdasarkan Suhu""")
    plt.figure(figsize=(25, 10))
    pivot_hr_temp_cnt = pivot_hourly_temp.pivot(index='hr', columns='temp', values='cnt')
    sns.heatmap(pivot_hr_temp_cnt, annot=True, fmt='.2f', cmap='YlGnBu')
    plt.title('Rata-rata Peminjaman Sepeda per Jam berdasarkan suhu')
    plt.xlabel('Suhu')
    plt.ylabel('Jam')
    st.pyplot(plt)
    st.write("""
    **Penjelasan:**
    Heatmap ini menunjukkan rata-rata peminjaman sepeda per jam berdasarkan suhu. 
    Ini memberikan gambaran yang jelas tentang bagaimana peminjaman bervariasi selama 
    jam-jam tertentu pada suhu yang berbeda. dapat dilihat pada jam malam dan terjadi peningkatan suhu juga terjadi lonjakan peminjaman sepeda.
    """)

elif data_choices == 'Apakah ada pola musiman dalam penggunaan sepeda?':
    # Melakukan mapping untuk setiap variabel kategorikal dengan cara yang lebih ringkas
    mapping_weathersit = {1: 'Cerah', 2: 'Berkabut', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}
    mapping_season = {1: 'Semi', 2: 'Panas', 3: 'Gugur', 4: 'Dingin'}

    df['weathersit'] = df['weathersit'].map(mapping_weathersit)
    df['season'] = df['season'].map(mapping_season)

    # Mengatur urutan kelas
    weathersit_order = ['Cerah', 'Berkabut', 'Hujan Ringan', 'Hujan Lebat']
    season_order = ['Semi', 'Panas', 'Gugur', 'Dingin']
    
    st.subheader('Pola Musiman dalam Peminjaman Sepeda')
    season_counts = df.groupby('season')['cnt'].mean().reset_index()
    
    # Membuat pivot tabel untuk rata-rata jumlah peminjaman sepeda terhadap variabel cuaca dan musim
    pivot_weathersit = df.groupby('weathersit')['cnt'].mean().reindex(weathersit_order, fill_value=0).reset_index()
    pivot_season = df.groupby('season')['cnt'].mean().reindex(season_order, fill_value=0).reset_index()
  
    # 1. Plot rata-rata peminjaman terhadap cuaca
    st.write("""#### Rata-rata Jumlah Peminjaman Sepeda terhadap Keadaan Cuaca""")
    plt.figure(figsize=(10, 5))
    sns.barplot(x='weathersit', y='cnt', data=pivot_weathersit, palette='viridis')
    plt.title('Rata-rata Jumlah Peminjaman Sepeda terhadap Keadaan Cuaca')
    plt.xlabel('Keadaan Cuaca')
    plt.ylabel('Rata-rata Jumlah Peminjaman')
    st.pyplot(plt)

    # Penjelasan untuk plot keadaan cuaca
    st.write("""
    Grafik ini menunjukkan rata-rata jumlah peminjaman sepeda berdasarkan keadaan cuaca. 
    Anda dapat melihat bagaimana cuaca mempengaruhi keputusan pengguna dalam meminjam sepeda. Dapat dilihat jika cerah maka banyak peminat dalam melakukan peminjaman sepeda.
    """)

    # 2. Plot rata-rata peminjaman terhadap musim
    st.write("""#### Rata-rata Jumlah Peminjaman Sepeda terhadap Keadaan Musim""")
    plt.figure(figsize=(10, 5))
    sns.barplot(x='season', y='cnt', data=pivot_season, palette='viridis')
    plt.title('Rata-rata Jumlah Peminjaman Sepeda terhadap Musim')
    plt.xlabel('Musim')
    plt.ylabel('Rata-rata Jumlah Peminjaman')
    st.pyplot(plt)

    # Penjelasan untuk plot musim
    st.write("""
    Grafik ini menunjukkan rata-rata jumlah peminjaman sepeda berdasarkan musim. 
    Dengan informasi ini, Anda dapat mengidentifikasi pola musiman dalam penggunaan 
    sepeda, dapat dilihat musim gugur memiliki banyak penggemar dalam memnggunakan sepeda.
    """)

elif data_choices == 'Bagaimana jumlah pengguna sepeda casual dan registered berubah seiring waktu?':
    st.subheader('Perbandingan Pengguna Casual dan Registered')
    # Menghitung rata-rata untuk pengguna biasa dan terdaftar dengan method groupby
    avg_counts = df[['casual', 'registered']].mean().reset_index()
    avg_counts.columns = ['Variabel', 'Rata-rata']  # Mengubah nama kolom

    # Menghitung rata-rata untuk pengguna biasa dan terdaftar per jam
    avg_hourly = df.groupby('hr')[['casual', 'registered']].mean().reset_index()
    avg_hourly = avg_hourly.melt(id_vars='hr', var_name='Tipe Pengguna', value_name='Rata-rata')

    # Menghitung rata-rata untuk pengguna biasa dan terdaftar per hari
    avg_daily = df.groupby('dteday')[['casual', 'registered']].mean().reset_index()
    avg_daily = avg_daily.melt(id_vars='dteday', var_name='Tipe Pengguna', value_name='Rata-rata')
    
    # 1. Plot Rata-rata Peminjaman Secara Keseluruhan
    st.write("""#### Rata-rata Peminjaman Sepeda: Pengguna Biasa vs Terdaftar""")
    plt.figure(figsize=(12, 6))
    avg_counts.columns = ['Tipe Pengguna', 'Rata-rata']
    sns.barplot(x='Tipe Pengguna', y='Rata-rata', data=avg_counts, palette='Set2')
    plt.title('Rata-rata Peminjaman Sepeda: Pengguna Biasa vs Terdaftar')
    plt.ylabel('Rata-rata Jumlah Peminjaman')
    plt.ylim(0, avg_counts['Rata-rata'].max() + 10)
    st.pyplot(plt)

    # Penjelasan untuk plot rata-rata peminjaman
    st.write("""
    Grafik ini menunjukkan perbandingan rata-rata peminjaman sepeda antara pengguna biasa dan terdaftar. 
    Dari grafik ini, Anda dapat melihat perbedaan dalam pola peminjaman antara kedua tipe pengguna. 
    Hal ini bisa membantu dalam memahami preferensi dan perilaku pengguna. Yang mana lebih banyak pengguna yang terdaftar
    """)

    # 2. Plot Rata-rata Peminjaman per Jam
    st.write("""#### Rata-rata Peminjaman Sepeda per Jam""")
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='hr', y='Rata-rata', hue='Tipe Pengguna', data=avg_hourly, palette='Set1', marker='o')
    plt.title('Rata-rata Peminjaman Sepeda per Jam')
    plt.xlabel('Jam')
    plt.ylabel('Rata-rata Jumlah Peminjaman')
    plt.legend(title='Tipe Pengguna')
    plt.ylim(0, avg_hourly['Rata-rata'].max() + 10)
    st.pyplot(plt)

    # Penjelasan untuk plot rata-rata peminjaman per jam
    st.write("""
    Grafik ini menunjukkan rata-rata peminjaman sepeda per jam untuk pengguna biasa dan terdaftar. 
    Anda dapat melihat waktu-waktu tertentu di mana peminjaman lebih tinggi, yang dapat memberikan 
    insight tentang kapan sepeda lebih banyak digunakan.
    """)

    # 3. Plot Rata-rata Peminjaman per Hari
    st.write("""#### Rata-rata Peminjaman Sepeda per Hari""")
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='dteday', y='Rata-rata', hue='Tipe Pengguna', data=avg_daily, palette='Set1', marker='o')
    plt.title('Rata-rata Peminjaman Sepeda per Hari')
    plt.xlabel('Tanggal')
    plt.ylabel('Rata-rata Jumlah Peminjaman')
    plt.legend(title='Tipe Pengguna')
    plt.xticks(rotation=45)
    plt.ylim(0, avg_daily['Rata-rata'].max() + 10)
    st.pyplot(plt)

    # Penjelasan untuk plot rata-rata peminjaman per hari
    st.write("""
    Grafik ini menunjukkan rata-rata peminjaman sepeda per hari, dibedakan antara pengguna biasa dan terdaftar. 
    Melalui grafik ini, Anda dapat mengamati tren peminjaman dari waktu ke waktu dan mengidentifikasi 
    hari-hari tertentu dengan jumlah peminjaman yang tinggi atau rendah.
    """)
