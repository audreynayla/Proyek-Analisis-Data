import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Menginput / Membaca Data CSV
customers_df = pd.read_csv("customers.csv")
payments_df = pd.read_csv("payments.csv")
reviews_df = pd.read_csv("reviews.csv")

# Mengolah data
datetime_columns = ["review_creation_date"]
reviews_df.sort_values(by="review_creation_date", inplace=True)
reviews_df.reset_index(inplace=True)
for column in datetime_columns:
    reviews_df[column] = pd.to_datetime(reviews_df[column])

min_date = reviews_df["review_creation_date"].min()
max_date = reviews_df["review_creation_date"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = reviews_df[(reviews_df["review_creation_date"] >= str(start_date)) & 
                (reviews_df["review_creation_date"] <= str(end_date))]

st.header('E-Commerce Public Dashboard :sparkles:')


# Jumlah pelanggan berdasarkan negara bagian
bystate_df = customers_df.groupby(by="customer_state")["customer_id"].nunique().reset_index()
bystate_df.rename(columns={"customer_id": "customer_count"}, inplace=True)
st.title("Jumlah Pelanggan Berdasarkan Negara Bagian / States")
plt.figure(figsize=(10, 5))
sns.barplot(
    x="customer_count",
    y="customer_state",
    data=bystate_df.sort_values(by="customer_count", ascending=False),
)
plt.title("Jumlah Pelanggan Berdasarkan Negara Bagian / States", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=12)
st.pyplot(plt)

# Tabel Jumlah Transaksi Berdasarkan Metode Pembayaran
sum_payment_type_df = payments_df.groupby("payment_type")['order_id'].count().sort_values(ascending=False).reset_index()
sum_payment_type_df.columns = ['payment_type', 'transaction_count']
sum_payment_type_df.head(15)

# Jumlah Transaksi Berdasarkan Metode Pembayaran
st.title("Jumlah Transaksi Berdasarkan Metode Pembayaran")
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(sum_payment_type_df['payment_type'], sum_payment_type_df['transaction_count'],
              color=["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"])
ax.set_title('Jumlah Transaksi Berdasarkan Metode Pembayaran', fontsize=16)
ax.set_xlabel('Jumlah Transaksi', fontsize=12)
ax.set_ylabel('Metode Pembayaran', fontsize=12)
ax.tick_params(axis='both', which='both', labelsize=10)
for bar in bars:
    yval = bar.get_height()
    plt.text(yval, bar.get_y() + bar.get_height()/2, round(yval, 2), ha='center', va='center', fontsize=10)
st.pyplot(fig)

# Persentase Metode Pembayaran yang Digunakan Oleh Pelanggan
payment_type_counts = payments_df['payment_type'].value_counts()
colors = ('#FF9999', '#66B2FF', '#99FF99', '#FFCC99')
st.title('Persentase Metode Pembayaran yang Digunakan Oleh Pelanggan')
fig, ax = plt.subplots()
ax.pie(
    x=payment_type_counts,
    labels=payment_type_counts.index,
    autopct='%1.1f%%',
    colors=colors,
)
ax.axis('equal')  # Pastikan pie chart berbentuk lingkaran
st.pyplot(fig)