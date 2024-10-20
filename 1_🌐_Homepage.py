#--------------------------
#IMPORT LIBRARIES
import pandas as pd  # pip install pandas openpyxl
import streamlit as st  # pip install streamlit
import plotly.express as px
import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

st.set_page_config(layout="wide")


country_coordinates = {
    "Afghanistan": (33.93911, 67.709953),
    "Albania": (41.1533, 20.1683),
    "Algeria": (28.0339, 1.6596),
    "Andorra": (42.5063, 1.5211),
    "Angola": (-11.2027, 17.8739),
    "Antigua and Barbuda": (17.0608, -61.7964),
    "Argentina": (-38.4161, -63.6167),
    "Armenia": (40.0691, 45.0382),
    "Australia": (-25.2744, 133.7751),
    "Austria": (47.5162, 14.5501),
    "Azerbaijan": (40.1431, 47.5769),
    "Bahamas": (25.0343, -77.3963),
    "Bahrain": (25.9304, 50.6372),
    "Bangladesh": (23.685, 90.3563),
    "Barbados": (13.1939, -59.5432),
    "Belarus": (53.9045, 27.559),
    "Belgium": (50.8503, 4.3517),
    "Belize": (17.1899, -88.4976),
    "Benin": (9.3079, 2.3158),
    "Bhutan": (27.5149, 90.4336),
    "Bolivia": (-16.5000, -68.1193),
    "Bosnia and Herzegovina": (43.8486, 18.3564),
    "Botswana": (-22.3285, 24.6849),
    "Brazil": (-14.2350, -51.9253),
    "Brunei": (4.5353, 114.7277),
    "Bulgaria": (42.7339, 25.4858),
    "Burkina Faso": (12.2383, -1.5616),
    "Burundi": (-3.3731, 29.9189),
    "Cabo Verde": (16.0020, -24.0133),
    "Cambodia": (12.5657, 104.9910),
    "Cameroon": (7.3697, 12.3547),
    "Canada": (56.1304, -106.3468),
    "Central African Republic": (6.6111, 20.9394),
    "Chad": (15.4542, 18.7322),
    "Chile": (-35.6751, -71.5430),
    "China": (35.8617, 104.1954),
    "Colombia": (4.5709, -74.2973),
    "Comoros": (-11.6455, 43.3333),
    "Congo": (-0.2280, 15.8277),
    "Congo, Democratic Republic of the": (-4.0383, 21.7587),
    "Costa Rica": (9.7489, -83.7534),
    "Croatia": (45.1, 15.2),
    "Cuba": (21.5218, -77.7812),
    "Cyprus": (35.1264, 33.4299),
    "Czech Republic": (49.8175, 15.4730),
    "Denmark": (56.2639, 9.5018),
    "Djibouti": (11.8251, 42.5903),
    "Dominica": (15.4150, -61.3710),
    "Dominican Republic": (18.7357, -70.1627),
    "Ecuador": (-1.8312, -78.1834),
    "Egypt": (26.8206, 30.8025),
    "El Salvador": (13.7942, -88.8965),
    "Equatorial Guinea": (1.6500, 10.6214),
    "Eritrea": (15.1792, 39.7823),
    "Estonia": (58.5953, 25.0136),
    "Eswatini": (-26.5225, 31.4659),
    "Ethiopia": (9.1450, 40.4897),
    "Fiji": (-17.7134, 178.0650),
    "Finland": (61.9241, 25.7482),
    "France": (46.6034, 1.8883),
    "Gabon": (-0.8031, 11.6094),
    "Gambia": (13.4668, -15.3694),
    "Georgia": (42.3154, 43.3569),
    "Germany": (51.1657, 10.4515),
    "Ghana": (7.3469, -0.3963),
    "Greece": (39.0742, 21.8243),
    "Grenada": (12.2628, -61.6042),
    "Guatemala": (15.7835, -90.2308),
    "Guinea": (9.9456, -9.6966),
    "Guinea-Bissau": (11.8037, -15.1804),
    "Guyana": (4.8600, -58.9300),
    "Haiti": (18.9712, -72.2854),
    "Honduras": (15.1999, -86.2419),
    "Hungary": (47.1625, 19.5033),
    "Iceland": (64.9631, -19.0208),
    "India": (20.5937, 78.9629),
    "Indonesia": (-0.7893, 113.9213),
    "Iran": (32.4279, 53.6880),
    "Iraq": (33.2232, 43.4160),
    "Ireland": (53.4129, -8.2439),
    "Israel": (31.0461, 34.8516),
    "Italy": (41.8719, 12.5674),
    "Jamaica": (18.1096, -77.2975),
    "Japan": (36.2048, 138.2529),
    "Jordan": (30.5852, 36.2384),
    "Kazakhstan": (48.0196, 66.9237),
    "Kenya": (-1.2864, 36.8172),
    "Kiribati": (-3.3704, -168.7340),
    "Korea, North": (40.3399, 127.5101),
    "Korea, South": (35.9078, 127.7669),
    "Kuwait": (29.3759, 47.9774),
    "Kyrgyzstan": (41.2044, 74.7661),
    "Laos": (19.8563, 102.4955),
    "Latvia": (56.8796, 24.6032),
    "Lebanon": (33.8547, 35.8623),
    "Lesotho": (-29.6090, 28.2336),
    "Liberia": (6.4281, -9.4295),
    "Libya": (26.3351, 17.2283),
    "Liechtenstein": (47.1662, 9.5555),
    "Lithuania": (55.1694, 23.8813),
    "Luxembourg": (49.6118, 6.1319),
    "Madagascar": (-18.7669, 46.8691),
    "Malawi": (-13.2543, 34.3015),
    "Malaysia": (4.2105, 101.9758),
    "Maldives": (3.2028, 73.2207),
    "Mali": (17.5700, -3.9962),
    "Malta": (35.9375, 14.3754),
    "Marshall Islands": (7.1315, 171.1845),
    "Mauritania": (20.2540, -10.9408),
    "Mauritius": (-20.348404, 57.552152),
    "Mexico": (23.6345, -102.5528),
    "Micronesia": (7.4256, 150.5508),
    "Moldova": (47.4116, 28.3699),
    "Monaco": (43.7384, 7.4246),
    "Mongolia": (46.8625, 103.8467),
    "Montenegro": (42.7087, 19.3744),
    "Morocco": (31.7917, -7.0926),
    "Mozambique": (-18.6657, 35.5296),
    "Myanmar": (21.9162, 95.9560),
    "Namibia": (-22.9576, 18.4904),
    "Nauru": (-0.5228, 166.9315),
    "Nepal": (28.3949, 84.1240),
    "Netherlands": (52.3792, 4.8994),
    "New Zealand": (-40.9006, 174.886),
    "Nicaragua": (12.8654, -85.2072),
    "Niger": (17.6078, 8.0817),
    "Nigeria": (9.0820, 8.6753),
    "North Macedonia": (41.6086, 21.7453),
    "Norway": (60.4720, 8.4689),
    "Oman": (21.5129, 55.9233),
    "Pakistan": (30.3753, 69.3451),
    "Palau": (7.5149, 134.5825),
    "Palestine": (31.9522, 35.2332),
    "Panama": (8.9824, -79.5199),
    "Papua New Guinea": (-6.31499, 143.95555),
    "Paraguay": (-23.4422, -58.4438),
    "Peru": (-9.1900, -75.0152),
    "Philippines": (12.8797, 121.7740),
    "Poland": (51.9194, 19.1451),
    "Portugal": (39.3999, -8.2245),
    "Qatar": (25.276987, 51.520008),
    "Romania": (45.9432, 24.9668),
    "Russia": (61.5240, 105.3188),
    "Rwanda": (-1.9403, 29.8739),
    "Saint Kitts and Nevis": (17.3578, -62.7834),
    "Saint Lucia": (13.9094, -60.9789),
    "Saint Vincent and the Grenadines": (13.2528, -61.1971),
    "Samoa": (-13.7590, -172.1046),
    "San Marino": (43.9333, 12.4467),
    "Sao Tome and Principe": (0.1864, 6.6131),
    "Saudi Arabia": (23.8859, 45.0792),
    "Senegal": (14.4974, -14.4524),
    "Serbia": (44.0165, 21.0059),
    "Seychelles": (-4.6796, 55.4919),
    "Sierra Leone": (8.4606, -11.7799),
    "Singapore": (1.3521, 103.8198),
    "Slovakia": (48.6690, 19.6990),
    "Slovenia": (46.1512, 14.9955),
    "Solomon Islands": (-9.6457, 160.0000),
    "Somalia": (5.1521, 46.1996),
    "South Africa": (-30.5595, 22.9375),
    "South Sudan": (6.8770, 31.3070),
    "Spain": (40.4637, -3.7492),
    "Sri Lanka": (7.8731, 80.7718),
    "Sudan": (12.8628, 30.2176),
    "Suriname": (3.9193, -56.0273),
    "Sweden": (60.1282, 18.6435),
    "Switzerland": (46.8182, 8.2275),
    "Syria": (34.8021, 38.9968),
    "Tajikistan": (38.8610, 71.2761),
    "Tanzania": (-6.3693, 34.8888),
    "Thailand": (15.8700, 100.9925),
    "Timor-Leste": (-8.8742, 125.7275),
    "Togo": (8.6195, 0.8248),
    "Tonga": (-21.1789, -175.1982),
    "Trinidad and Tobago": (10.6918, -61.2225),
    "Tunisia": (33.8869, 9.5375),
    "Türkiye": (38.9637, 35.2433),
    "Turkmenistan": (40.0622, 59.5566),
    "Tuvalu": (-7.1095, 179.1940),
    "Uganda": (1.3733, 32.2903),
    "Ukraine": (48.3794, 31.1656),
    "United Arab Emirates": (23.4241, 53.8478),
    "United Kingdom": (55.3781, -3.4360),
    "United States": (37.0902, -95.7129),
    "Uruguay": (-32.5228, -55.7658),
    "Uzbekistan": (41.3775, 64.5850),
    "Vanuatu": (-15.3767, 166.9592),
    "Vatican City": (41.9029, 12.4534),
    "Venezuela": (6.4238, -66.5897),
    "Vietnam": (14.0583, 108.2772),
    "Yemen": (15.5524, 48.5164),
    "Zambia": (-13.1339, 27.8493),
    "Zimbabwe": (-19.0138, 29.1549),
}


@st.cache_data
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


# Veri güncelleme butonu
if st.sidebar.button("Verileri Güncelle"):
    df = fetch_data()  # Verileri güncelle
    st.success("Veriler başarıyla güncellendi!")
else:
    # İlk kez verileri çek
    df = fetch_data()

df['PROJECT / NOTICE'] = df['PROJECT / NOTICE'].str.replace('DOWNLOAD', '', regex=False).str.strip()

# Ülke isimlerinden koordinatları ekleme
df['Latitude'] = df['MEMBER'].map(lambda country: country_coordinates.get(country, (None, None))[0])
df['Longitude'] = df['MEMBER'].map(lambda country: country_coordinates.get(country, (None, None))[1])


# ------------------- Tarih Ayarlarının Yapılması ------------------------------------------------------------
# 'DATE' sütunundaki 'ISSUE DATE:' kısmını kaldırma
df['DATE'] = df['DATE'].str.replace("ISSUE DATE: ", "", regex=False).str.strip()

# Tarih formatlarını dönüştürmek için bir fonksiyon
def parse_date(date_str):
    date_str = date_str.strip()  # Baş ve sondaki boşlukları kaldır
    # Farklı tarih formatlarını tanımlama
    formats = ['%B %d, %Y', '%b %d, %Y', '%Y-%m-%d']  # Tam ve kısaltılmış ay isimleri
    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt, errors='raise')
        except ValueError:
            continue
    return pd.NaT  # Hiçbir formatla eşleşmezse NaT döndür

# Tarih formatına dönüştürme
df['ProjectDate'] = df['DATE'].apply(parse_date)
# ---------------------------------------------------------------------------------------------------------

# Gün sayısını seçmek için slider ekle
days = st.sidebar.slider('Filtrele:', 1, 50, 10)  # 1 ile 30 arasında varsayılan 10
end_date = datetime.now()
start_date = end_date - timedelta(days=days)

# Tarih filtresi uygulama
filtered_df = df[(df['ProjectDate'] >= start_date) & (df['ProjectDate'] <= end_date)]

# Folium haritası oluşturma
m = folium.Map(location=[20, 0], zoom_start=3)




def main():
    # Verileri önceden çekip saklama
   
    # Filtrelenmiş proje lokasyonlarını haritaya ekleme
    for i, row in filtered_df.iterrows():
        latitude = row['Latitude']
        longitude = row['Longitude']

        if pd.notna(latitude) and pd.notna(longitude):  # Geçerli lokasyonları kontrol etme
            # Proje tarihini kontrol et
            project_date = row['ProjectDate']
            # Tıklanan MEMBER'a ait projeleri bulma
            member_projects = filtered_df[filtered_df['MEMBER'] == row['MEMBER']]
            
            # Proje tarihlerini kontrol et
            green_found = False  # Yeşil proje var mı kontrolü için bir bayrak
            for _, project_row in member_projects.iterrows():
                project_date = project_row['ProjectDate']
                if pd.notna(project_date):
                    days_diff = (datetime.now() - project_date).days
                    if days_diff <= 10:  # Son 10 gün içerisindeki projeler
                        green_found = True  # En az bir yeşil proje bulundu
                        break

            # Simge rengini ayarlama
            if green_found:
                icon_color = "green"  # Yeşil simge
            else:
                icon_color = "red"  # Kırmızı simge


            icon = folium.Icon(color=icon_color, icon="building", prefix="fa")  


            # Tıklanan MEMBER'a ait projeleri bulma ve listeleme
            member_projects = filtered_df[filtered_df['MEMBER'] == row['MEMBER']]

            # Proje isimlerini liste halinde alıyoruz
            project_list = member_projects['PROJECT / NOTICE'].tolist()

            # Pop-up içeriğini HTML ile oluşturma
            popup_content = f"""
            <div style="font-size: 16px;">
                <strong>Üye:</strong> {row['MEMBER']}<br>
                <strong>Projeler:</strong>
                <ul>
            """
            # Proje isimlerini tek tek listeye ekliyoruz
            for project in project_list:
                popup_content += f"<li>{project}</li>"

            popup_content += "</ul></div>"

            regions = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_regions.geojson"

            folium.Marker(
                location=[latitude, longitude],
                popup=folium.Popup(popup_content, max_width=400, min_width=200),  # Genişlik ayarları
                tooltip=f"Proje sayısı: {len(filtered_df[(filtered_df['Latitude'] == latitude) & (filtered_df['Longitude'] == longitude)])}",  # Tooltip'i güncelle
                color_column="region",
                icon=icon
            ).add_to(m)
        else:
            print(f"Geçersiz lokasyon: {row['MEMBER']} - Latitude: {latitude}, Longitude: {longitude}")

    container1 = st.container(border=True)
    with container1:
        
        # İki kolonu oluştur
        col1, col2 = st.columns([5, 2])  # Sol kolon daha geniş

        with col1:
            container = st.container(border=True)
            with container:
                # Folium haritasını Streamlit'te gösterme
                st_data = st_folium(m, width=1400, height=850)

        with col2:
            container2 = st.container(border=True)
            with container2:
                # Eğer haritada bir tıklama gerçekleşmemişse filtrelenmiş verileri göster
                if st_data["last_object_clicked"] is None:
                    st.write("Projects:")
                    st.dataframe(filtered_df[['ProjectDate', 'PROJECT / NOTICE', 'SECTOR', 'TYPE']])
                else:
                    # Haritanın altına tıklanan yerin bilgilerini yazdırıyoruz
                    clicked_info = st_data["last_object_clicked"]
                    lat = clicked_info["lat"]
                    lon = clicked_info["lng"]

                    # Tıklanan lokasyonu dataframe ile eşleştirme
                    clicked_country = filtered_df[(filtered_df['Latitude'] == lat) & (filtered_df['Longitude'] == lon)]
                    
                    if not clicked_country.empty:
                        # Tıklanan lokasyondaki bilgileri al
                        st.write(f"**{clicked_country.iloc[0]['MEMBER']}** ülkesindeki projeler:")
                        
                        # Tüm projeleri içeren bir DataFrame oluştur
                        projects_df = clicked_country[['ProjectDate', 'PROJECT / NOTICE', 'SECTOR', 'TYPE']].copy()

                        # Tarih formatını düzelt
                        projects_df['ProjectDate'] = projects_df['ProjectDate'].apply(lambda x: x.date())

                        # Tabloyu ekrana yazdır
                        st.dataframe(projects_df)


# streamlit run 1_🌐_Homepage.py


if __name__ == "__main__":
    main()
    
  

