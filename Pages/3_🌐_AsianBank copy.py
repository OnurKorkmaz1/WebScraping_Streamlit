import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import base64
import requests

# Veriyi çekmek için fonksiyon
def fetch_data():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(), options=chrome_options)
    driver.get("https://www.aiib.org/en/opportunities/business/project-procurement/list.html")
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    table_section = soup.find('div', {'class': ['table-con', 'col-sm-12']})
    data = []

    if table_section is not None:
        ul_elements = table_section.find_all('ul')
        for ul in ul_elements:
            li_elements = ul.find_all('li')
            if len(li_elements) >= 5:
                row_data = []
                pdf_link = ''
                for li in li_elements:
                    text = li.text.strip()
                    link = li.find('a', href=True)
                    if link and 'DOWNLOAD' in text:
                        pdf_link = 'https://www.aiib.org' + link['href']
                    for header in ['DATE', 'MEMBER', 'PROJECT / NOTICE', 'SECTOR', 'TYPE']:
                        if text.startswith(header):
                            text = text.replace(header, '').strip()
                    row_data.append(text)

                if len(row_data) >= 5:
                    row_data.append(pdf_link)
                    data.append(row_data)

    df = pd.DataFrame(data, columns=['DATE', 'MEMBER', 'PROJECT / NOTICE', 'SECTOR', 'TYPE', 'PDF LINK'])
    return df[df['PDF LINK'] != ''].reset_index(drop=True)

# PDF görüntüleme fonksiyonu
def display_pdf(pdf_url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(pdf_url, headers=headers)
        response.raise_for_status()  # Hata kontrolü
        pdf_data = response.content
        base64_pdf = base64.b64encode(pdf_data).decode("utf-8")
        
        # Toggle (Expander) içinde PDF görüntüleme
        with st.expander("Click to view PDF"):
            pdf_display = (
                f'<embed src="data:application/pdf;base64,{base64_pdf}" '
                'width="100%" height="1000" type="application/pdf"></embed>'
            )
            st.markdown(pdf_display, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading PDF: {e}")

# Streamlit uygulaması
st.title("Project Dashboard")

# Sayfa ilk yüklendiğinde veriyi otomatik olarak çek
if 'df' not in st.session_state:
    st.session_state.df = fetch_data()
    st.session_state.checked_status = [False] * len(st.session_state.df)  # Checkbox durumları
    st.success("Veri başarıyla çekildi!")
elif 'checked_status' not in st.session_state:
    st.session_state.checked_status = [False] * len(st.session_state.df)  # Başlangıçta checkbox durumları

# Kullanıcı düzenlemesi için data editor
if 'Select' not in st.session_state.df.columns:
    st.session_state.df.insert(0, 'Select', False)  # Checkbox kolonu ekle

# Proje kontrol durumu için checkbox kolonu ekleyelim
if 'Checked' not in st.session_state.df.columns:
    st.session_state.df['Checked'] = st.session_state.checked_status  # Proje kontrol durumu için checkbox

# Satır sayısını ayarlamak için input
num_rows = st.number_input("Gösterilecek satır sayısını ayarlayın:", min_value=1, max_value=len(st.session_state.df), value=20)

# Data editor içinde güncel checkbox durumları ile göster
edited_df = st.data_editor(
    st.session_state.df.head(num_rows),  # Sadece ayarlanan satır sayısını göster
    column_config={
        "Select": "Select",
        "DATE": "DATE",
        "MEMBER": "MEMBER",
        "PROJECT / NOTICE": "PROJECT / NOTICE",
        "SECTOR": "SECTOR",
        "TYPE": "TYPE",
        "PDF LINK": "PDF LINK",
        "Checked": st.column_config.CheckboxColumn(
            "Status",
            help="Proje kontrol edildi mi?",
            default=False,
        )
    },
    disabled=["PDF LINK"],  # PDF linkini düzenlenemez yap
    hide_index=True,
)

# Checkbox durumlarını güncelle
for index in range(len(edited_df)):
    st.session_state.checked_status[index] = edited_df['Checked'].iloc[index]

# Seçilen satırların PDF linkini yazdırma
selected_pdf_link = None  # Seçilen PDF linki için değişken
if st.button("Seçilen PDF Linkini Göster"):
    selected_rows = edited_df[edited_df['Select']]  # Seçilen satırları al
    if not selected_rows.empty:  # Boş olup olmadığını kontrol et
        # İlk seçilen satırın PDF linkini al
        first_row = selected_rows.iloc[0]
        selected_pdf_link = first_row.get('PDF LINK')
        if selected_pdf_link:
            st.success("Seçilen PDF Linki gösteriliyor.")  # Başarı mesajı
        else:
            st.warning("Seçilen satırda PDF linki yok.")
    else:
        st.warning("Hiçbir satır seçilmedi.")

# PDF görüntüleme
if selected_pdf_link:
    display_pdf(selected_pdf_link)

# Yenileme butonu
if st.button("Yenile"):
    st.session_state.df = fetch_data()  # Yeniden güncelle
    st.session_state.checked_status = [False] * len(st.session_state.df)  # Yenilendiğinde checkbox durumunu sıfırla
    st.success("Veri yenilendi.")
