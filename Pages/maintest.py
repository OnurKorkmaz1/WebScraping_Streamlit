import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import base64
import requests
import os
from PIL import Image
import pytesseract
from functions import convert_pdf_to_txt_pages, convert_pdf_to_txt_file, images_to_txt
from googletrans import Translator
from io import BytesIO

languages = {
    'English': 'eng',
    'French': 'fra',
    'Arabic': 'ara',
    'Spanish': 'spa',
}



# Translating Code
import streamlit as st
from PIL import Image
import pytesseract

def translate_document(pdf_file, ocr_box, textOutput, languages, translator):
    path = pdf_file.read()
    file_extension = "pdf"

    if pdf_file:
        path = pdf_file.read()

        if file_extension == "pdf":
            if ocr_box:
                option = st.selectbox('Select the document language', list(languages.keys()))

            if textOutput == 'One text file (.txt)':
                if ocr_box:
                    texts, nbPages = images_to_txt(path, languages[option])
                else:
                    text_data_f, nbPages = convert_pdf_to_txt_file(pdf_file)

                if text_data_f.strip():
                    if st.button("Çevir"):
                        try:
                            translated_chunks = []
                            chunks = text_data_f.split('\n\n')

                            for chunk in chunks:
                                if chunk.strip():
                                    translated = translator.translate(chunk, dest='tr')
                                    if translated is not None:
                                        translated_chunks.append(translated.text.replace('\n', ' '))

                            if translated_chunks:
                                translated_text = '\n\n'.join(translated_chunks)
                                st.subheader("Çeviri Sonucu")
                                st.text_area("Çeviri Metni", value=translated_text, height=300)
                            else:
                                st.warning("Çeviri için hiçbir metin bulunamadı.")

                        except Exception as e:
                            st.error(f"Çeviri hatası: {str(e)}")
                else:
                    st.warning("PDF'den alınan metin boş.")

            else:
                if ocr_box:
                    text_data, nbPages = images_to_txt(path, languages[option])
                else:
                    text_data, nbPages = convert_pdf_to_txt_pages(pdf_file)

                for i, page_text in enumerate(text_data):
                    if page_text.strip():
                        if st.button(f"Çevir - Sayfa {i + 1}"):
                            try:
                                translated_chunks = []
                                chunks = page_text.split('\n\n')

                                for chunk in chunks:
                                    if chunk.strip():
                                        translated = translator.translate(chunk, dest='tr')
                                        if translated is not None:
                                            translated_chunks.append(translated.text.replace('\n', ' '))

                                if translated_chunks:
                                    translated_text = '\n\n'.join(translated_chunks)
                                    st.subheader(f"Çeviri Sonucu - Sayfa {i + 1}")
                                    st.text_area(f"Çeviri Metni - Sayfa {i + 1}", value=translated_text, height=300)
                                else:
                                    st.warning(f"Sayfa {i + 1} için çeviri için hiçbir metin bulunamadı.")

                            except Exception as e:
                                st.error(f"Çeviri hatası: {str(e)}")
                    else:
                        st.warning(f"Sayfa {i + 1} için alınan metin boş.")

        else:
            option = st.selectbox("What's the language of the text in the image?", list(languages.keys()))
            pil_image = Image.open(pdf_file)
            text = pytesseract.image_to_string(pil_image, lang=languages[option])
            
            if text.strip():
                if st.button("Çevir"):
                    try:
                        translated = translator.translate(text, dest='tr')
                        if translated is not None:
                            st.subheader("Çeviri Sonucu")
                            st.markdown(f"<div style='font-size: 12px;'>{translated.text}</div>", unsafe_allow_html=True)
                        else:
                            st.error("Çeviri alınamadı.")
                    except Exception as e:
                        st.error(f"Çeviri hatası: {str(e)}")
            else:
                st.warning("Resimden alınan metin boş.")




translator = Translator()

with st.sidebar:
    st.title(":outbox_tray: PDF to Text")
    textOutput = st.selectbox(
        "How do you want your output text?",
        ('One text file (.txt)', 'Text file per page (ZIP)'))
    ocr_box = st.checkbox('Enable OCR (scanned document)')

# CSS for hiding Streamlit footer and menu
hide = """
<style>
footer {
    visibility: hidden;
    position: relative;
}
.viewerBadge_container__1QSob {
    visibility: hidden;
}
#MainMenu {
    visibility: hidden;
}
</style>
"""
st.markdown(hide, unsafe_allow_html=True)

# Initialize pdf_file in session state
if 'pdf_file' not in st.session_state:
    st.session_state.pdf_file = None

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
        response.raise_for_status()  
        pdf_data = response.content
        base64_pdf = base64.b64encode(pdf_data).decode("utf-8")
        
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
    st.session_state.checked_status = [False] * len(st.session_state.df)  
    st.success("Veri başarıyla çekildi!")
elif 'checked_status' not in st.session_state:
    st.session_state.checked_status = [False] * len(st.session_state.df)  

# Kullanıcı düzenlemesi için data editor
if 'Select' not in st.session_state.df.columns:
    st.session_state.df.insert(0, 'Select', False)  

# Proje kontrol durumu için checkbox kolonu ekleyelim
if 'Checked' not in st.session_state.df.columns:
    st.session_state.df['Checked'] = st.session_state.checked_status  

# Satır sayısını ayarlamak için input
num_rows = st.number_input("Gösterilecek satır sayısını ayarlayın:", min_value=1, max_value=len(st.session_state.df), value=20)

# Data editor içinde güncel checkbox durumları ile göster
edited_df = st.data_editor(
    st.session_state.df.head(num_rows),  
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
    disabled=["PDF LINK"],  
    hide_index=True,
)

# Checkbox durumlarını güncelle
for index in range(len(edited_df)):
    st.session_state.checked_status[index] = edited_df['Checked'].iloc[index]

# Seçilen satırların PDF linkini yazdırma
selected_pdf_link = None  
if st.button("Seçilen PDF Linkini Göster"):
    selected_rows = edited_df[edited_df['Select']]  
    if not selected_rows.empty:  
        first_row = selected_rows.iloc[0]
        selected_pdf_link = first_row.get('PDF LINK')
        if selected_pdf_link:
            st.success("Seçilen PDF Linki gösteriliyor.")  
            
            # PDF'yi göster
            display_pdf(selected_pdf_link)  

            # PDF'yi indir
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            response = requests.get(selected_pdf_link, headers=headers)

            if response.status_code == 200:
                project_name = first_row.get('PROJECT / NOTICE').replace('/', '-')  
                downloads_dir = os.path.join(os.getcwd(), "downloads")  

                if not os.path.exists(downloads_dir):
                    os.makedirs(downloads_dir)

                pdf_file_path = os.path.join(downloads_dir, f"{project_name}.pdf")  
                with open(pdf_file_path, 'wb') as f:
                    f.write(response.content)
                st.write(pdf_file_path)

                # PDF dosyasını oku
                if os.path.exists(pdf_file_path):
                    with open(pdf_file_path, 'rb') as f:
                        filePDF = BytesIO(f.read())  # PDF dosyasını BytesIO nesnesine çevir
                        pdf_file = filePDF


                if os.path.exists(pdf_file_path):
                    with open(pdf_file_path, 'rb') as f:
                        st.session_state.pdf_file = BytesIO(f.read())  # Store in session state

                #translate_document(st.session_state.pdf_file, ocr_box, textOutput, languages, translator)

                

            else:
                st.error(f"PDF indirilirken bir hata oluştu: {response.status_code} - {response.reason}")

        else:
            st.warning("Seçilen satırda PDF linki yok.")
    else:
        st.warning("Hiçbir satır seçilmedi.")










# Yenileme butonu
if st.button("Yenile"):
    st.session_state.df = fetch_data()  
    st.session_state.checked_status = [False] * len(st.session_state.df)  
    st.success("Veri yenilendi.")
