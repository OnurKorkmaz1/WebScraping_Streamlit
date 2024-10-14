import streamlit as st
import pdf2image
from PIL import Image
import pytesseract
from functions import convert_pdf_to_txt_pages, convert_pdf_to_txt_file, save_pages, displayPDF, images_to_txt
from googletrans import Translator

st.set_page_config(page_title="PDF to Text")

st.markdown("""
    ## Text data extractor: PDF to Text
""")

languages = {
    'English': 'eng',
    'French': 'fra',
    'Arabic': 'ara',
    'Spanish': 'spa',
}

translator = Translator()

with st.sidebar:
    st.title(":outbox_tray: PDF to Text")
    textOutput = st.selectbox(
        "How do you want your output text?",
        ('One text file (.txt)', 'Text file per page (ZIP)'))
    ocr_box = st.checkbox('Enable OCR (scanned document)')

pdf_file = st.file_uploader("Load your PDF", type=['pdf', 'png', 'jpg'])
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




if pdf_file:
    path = pdf_file.read()
    file_extension = pdf_file.name.split(".")[-1]

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
                            if chunk.strip():  # Boş chunk'ları atla
                                translated = translator.translate(chunk, dest='tr')
                                if translated is not None:
                                    translated_chunks.append(translated.text.replace('\n', ' '))  # Satır sonlarını kaldır

                        if translated_chunks:  # Eğer en az bir çeviri varsa
                            translated_text = '\n\n'.join(translated_chunks)  # Paragraflar arasında iki boşluk bırak
                            st.subheader("Çeviri Sonucu")
                            st.text_area("Çeviri Metni", value=translated_text, height=300)  # Kullanıcı düzenleyebilir
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
                                if chunk.strip():  # Boş chunk'ları atla
                                    translated = translator.translate(chunk, dest='tr')
                                    if translated is not None:
                                        translated_chunks.append(translated.text.replace('\n', ' '))  # Satır sonlarını kaldır

                            if translated_chunks:  # Eğer en az bir çeviri varsa
                                translated_text = '\n\n'.join(translated_chunks)  # Paragraflar arasında iki boşluk bırak
                                st.subheader(f"Çeviri Sonucu - Sayfa {i + 1}")
                                st.text_area(f"Çeviri Metni - Sayfa {i + 1}", value=translated_text, height=300)  # Kullanıcı düzenleyebilir
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
