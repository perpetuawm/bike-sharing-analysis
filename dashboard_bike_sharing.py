import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="dark")

def create_season_data(df):
    season_data = df.groupby("season")[["registered", "casual"]].sum().reset_index()
   
    return season_data

def create_weathersit_data(df):
    weathersit_data = df.groupby("weathersit")[["registered", "casual"]].sum().reset_index()
   
    return weathersit_data

def create_workingday_data(df):
    workingday_data = df.groupby("workingday")[["registered", "casual"]].sum().reset_index()
   
    return workingday_data

def create_weekday_data(df):
    weekday_data = df.groupby("weekday")[["registered", "casual"]].sum().reset_index()
   
    return weekday_data

def create_daily_data(df):
    daily_data = df.groupby("dteday")[["cnt","casual", "registered"]].sum().reset_index()
   
    return daily_data

def create_mnth_data(df):
    mnth_data = df.groupby(["yr", "mnth"])[["casual", "registered", "cnt"]].sum().reset_index()
    mnth_data["yr"] = mnth_data["yr"].map({0: 2011, 1: 2012})
    
    return mnth_data

def create_corr_mat(df):
    corr_mat = day_df[["temp","atemp","hum","windspeed","casual","registered","cnt"]].corr()
    
    return corr_mat

def create_temp_df(df):
    temp_df = day_df[["temp","cnt"]].copy()

    # tambhakan kolom label
    temp_bins = [0, 0.3, 0.6, 1.00]
    cnt_bins = [0, 3000, 6000, 10000]
    temp_labels = ["Low", "Medium", "High"] 
    cnt_labels = ["Sedikit", "Sedang", "Banyak"]
    temp_df["kondisi_suhu"] = pd.cut(temp_df["temp"], bins=temp_bins, labels=temp_labels, right=False)
    temp_df["jumlah_peminjam"] = pd.cut(temp_df["cnt"], bins=cnt_bins, labels=cnt_labels, right=False)
    
    return temp_df

# Load cleaned data
day_df = pd.read_csv("day_df.csv")
hour_df = pd.read_csv("hour_df.csv")

datetime_columns = ["dteday"]

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

for column in datetime_columns:
    hour_df[column] = pd.to_datetime(hour_df[column])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) & 
                 (day_df["dteday"] <= pd.to_datetime(end_date))]

season_data = create_season_data(main_df)
weathersit_data = create_weathersit_data(main_df)
workingday_data = create_workingday_data(main_df)
weekday_data = create_weekday_data(main_df)
daily_data = create_daily_data(main_df)
mnth_data = create_mnth_data(main_df)
corr_mat = create_corr_mat(main_df)
temp_df = create_temp_df(main_df)

st.header('Bike Sharing Dashboard :bike:')

col1, col2 = st.columns(2)
 
with col1:
    total_casual = daily_data.casual.sum()
    st.metric("Jumlah Casual Users", value=total_casual)
 
with col2:
    total_registered = daily_data.registered.sum()
    st.metric("Jumlah Registered Users", value=total_registered)


# Plot daily users
st.subheader("Pola Peminjaman Terdaftar dan Biasa per Hari")

fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(daily_data["dteday"], daily_data["casual"], label="Casual", color="#FFA126", linewidth=2)
ax.plot(daily_data["dteday"], daily_data["registered"], label="Registered", color="#326DA8", linewidth=2)

# Menambahkan label, legend, dan Judul
ax.set_title("Pola Peminjaman Terdaftar dan Biasa per Hari", fontsize=16)
ax.set_xlabel("Tanggal", fontsize=12)
ax.set_ylabel("Jumlah Pengguna", fontsize=12)
ax.legend(title="Jenis Pengguna", fontsize=10)
ax.grid(alpha=0.5)
plt.tight_layout()

st.pyplot(fig)


# Membuat Plot monthly users
st.subheader("Pola Peminjaman Sepeda Terdaftar dan Biasa per Bulan (2 Tahun)")

# Membuat Plot monthly users
years = [2011, 2012]
colors = ["#FFA126", "#326DA8","#A8A8A8"]
fig, ax = plt.subplots(figsize=(14, 7))

for i, year in enumerate(years):
    data = mnth_data[mnth_data["yr"] == year]
    ax.plot(data["mnth"], data["casual"], label=f"Casual {year}", color=colors[0], linewidth=2, linestyle='--' if i == 0 else '-')
    ax.plot(data["mnth"], data["registered"], label=f"Registered {year}", color=colors[1], linewidth=2, linestyle='--' if i == 0 else '-')
    ax.plot(data["mnth"], data["cnt"], label=f"Total {year}", color=colors[2], linewidth=2, linestyle='--' if i == 0 else '-')

# Menambahkan label, legend, dan Judul
ax.set_title("Pola Peminjaman Sepeda Terdaftar dan Biasa per Bulan (2 Tahun)", fontsize=16)
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Jumlah Pengguna", fontsize=12)
ax.legend(title="Jenis Pengguna", fontsize=10)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(range(1, 13), fontsize=10)
ax.grid(alpha=0.5)
plt.tight_layout()

st.pyplot(fig)


# Membuat kapan sepeda paling banyak dipinjam
st.subheader("Hubungan antara Musim dan Cuaca dengan Jumlah Sewa Sepeda pada Tahun 2011 s.d 2012")
# Buat subplots
fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=False)

# Mendefinisikan labels untuk xticks
season_labels = ["Spring", "Summer", "Fall", "Winter"]
weathersit_labels = ["Clear","Mist", "Light Snow/Rain", "Heavy Rain"]
    
# Mendefinisikan warna
registered_color = "#326DA8"
casual_color = "#FFA126"

# Plot registered dan casual per Musim
sns.barplot(ax=axes[0], data=season_data.melt(id_vars="season", value_vars=["casual", "registered"]),
            x="season", y="value", hue="variable", palette=[registered_color, casual_color])
axes[0].set_title("Jumlah Pengguna Registered dan Casual per Musim")
axes[0].set_xlabel("Musim")
axes[0].set_ylabel("Jumlah Pengguna")
axes[0].set_xticks(range(len(season_labels)))  
axes[0].set_xticklabels(season_labels)         
axes[0].legend(title="Tipe Pengguna")

# Plot registered dan casual users per cuaca
sns.barplot(ax=axes[1], data=weathersit_data.melt(id_vars="weathersit", value_vars=["casual", "registered"]),
            x="weathersit", y="value", hue="variable", palette=[registered_color, casual_color])
axes[1].set_title("Jumlah Pengguna Registered dan Casual per Cuaca")
axes[1].set_xlabel("Cuaca")
axes[1].set_ylabel("Jumlah Pengguna")
axes[1].set_xticks(range(len(weathersit_labels)))  
axes[1].set_xticklabels(weathersit_labels)         
axes[1].legend(title="Tipe Pengguna")
plt.tight_layout()
plt.show()

st.pyplot(fig)

# Membuat kapan sepeda paling banyak dipinjam
st.subheader("Hubungan antara Hari Libur dan Hari Kerja dengan Jumlah Sewa Sepeda pada Tahun 2011 s.d 2012")

# Buat subplots
fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=False)

# Mendefinisikan labels untuk xticks
workingday_labels = ["Libur/Weekend", "Hari Kerja"]
weekday_labels = ["Minggu","Senin", "Selasa", "Rabu", "Kamis", "Jumat","Sabtu"]

# Plot registered dan casual users per status hari
sns.barplot(ax=axes[0], data=workingday_data.melt(id_vars="workingday", value_vars=["casual", "registered"]),
            x="workingday", y="value", hue="variable", palette=[registered_color, casual_color])
axes[0].set_title("Jumlah Pengguna Registered dan Casual per Status Hari")
axes[0].set_xlabel("Status Hari")
axes[0].set_ylabel("Jumlah Pengguna")
axes[0].set_xticks(range(len(workingday_labels)))  
axes[0].set_xticklabels(workingday_labels)         
axes[0].legend(title="Tipe Pengguna")

# Plot registered dan casual users per hari
sns.barplot(ax=axes[1], data=weekday_data.melt(id_vars="weekday", value_vars=["casual", "registered"]),
            x="weekday", y="value", hue="variable", palette=[registered_color, casual_color])
axes[1].set_title("Jumlah Pengguna Registered dan Casual per Hari")
axes[1].set_xlabel("Hari")
axes[1].set_ylabel("Jumlah Pengguna")
axes[1].set_xticks(range(len(weekday_labels))) 
axes[1].set_xticklabels(weekday_labels)         
axes[1].legend(title="Tipe Pengguna")
plt.tight_layout()
plt.show()

st.pyplot(fig)

st.subheader("Korelasi Temperature, Humidity, dan Windspeed dengan jumlah penyewa")

# Buat heatmap
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr_mat, annot=True, cmap="flare", fmt=".2f", ax=ax)

# Menambahkan judul
ax.set_title("Correlation Matrix Heatmap", fontsize=16)

st.pyplot(fig)

st.subheader("Scatterplot Korelasi Temperature dengan Jumlah Sewa")

# Membuat plot korelasi
fig, ax = plt.subplots(figsize=(14, 7))
sns.scatterplot(x="temp", y="cnt", hue="kondisi_suhu", style="jumlah_peminjam", markers={"Sedikit": "^", "Sedang": "X", "Banyak": "s"}, data=temp_df, palette=["#E8C33C", "#E99A2C","#D44437"],s=100)

# menambahkan judul, label, dan legend
ax.set_title("Temperature vs Jumlah Sewa", fontsize=16)
ax.set_xlabel("Temperature (Normalized)", fontsize=12)
ax.set_ylabel("Jumlah Peminjaman", fontsize=12)
ax.legend(title="Keterangan", bbox_to_anchor=(1.18, 1), loc="upper right")
ax.grid(True, linestyle='--', alpha=0.5)

st.pyplot(fig)