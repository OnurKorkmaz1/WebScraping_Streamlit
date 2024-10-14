import base64
import requests
import streamlit as st

# Kullanıcıdan URL girişi al
pdf_url = st.text_input(label="Please enter the URL of a PDF file")
method = st.radio(label="Method", options=["Embed", "Iframe"], horizontal=True)

if not pdf_url:
    st.stop()

# URL'den PDF dosyasını yükle
try:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(pdf_url, headers=headers)
    response.raise_for_status()  # Hata kontrolü
    pdf_data = response.content
except Exception as e:
    st.error(f"Error loading PDF: {e}")
    st.stop()

# PDF dosyasını Base64 formatına çevir
base64_pdf = base64.b64encode(pdf_data).decode("utf-8")

# Toggle (Expander) içinde PDF görüntüleme
with st.expander("Click to view PDF"):
    if method == "Embed":
        pdf_display = (
            f'<embed src="data:application/pdf;base64,{base64_pdf}" '
            'width="100%" height="1000" type="application/pdf"></embed>'
        )
    elif method == "Iframe":
        pdf_display = (
            f'<iframe src="data:application/pdf;base64,{base64_pdf}" '
            'width="100%" height="1000" type="application/pdf"></iframe>'
        )
    else:
        st.error(f"Unknown method: {method}")

    st.markdown(pdf_display, unsafe_allow_html=True)
