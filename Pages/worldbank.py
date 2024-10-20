from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import streamlit as st
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
from googletrans import Translator
import streamlit_shadcn_ui as ui

country_coordinates = {
    "Central Africa": (2.5, 23.5),
    "Kyrgyz Republic": (41.2044, 74.7661),
    "Central Asia": (41.0242, 69.3828),
    "Western and Central Africa": (5.0344, 14.1149), 
    "Cote d'Ivoire": (7.5399, -5.5471),
    "Sierra Leone": (8.4606, -11.7799),
    "Turkiye": (38.9637, 35.2433),
    "Armenia": (40.0691, 45.0382),
    "Jordan": (30.5852, 36.2384),
    "Senegal": (14.4974, -14.4524),
    "Nigeria": (9.0820, 8.6753),
    "Tajikistan": (38.8610, 71.2761),
    "Albania": (41.1533, 20.1683),
    "Central African Republic": (4.3947, 18.5580),
    "Kazakhstan": (48.0196, 66.9237),
    "Morocco": (31.7917, -7.0926),
    "Uzbekistan": (41.3775, 64.5851),
    "Serbia": (44.0165, 21.0059),
    "Chad": (15.8279, 19.1133),
    "Mali": (17.5700, -3.9962),
    "Moldova": (47.4116, 28.3699),
    "Guinea-Bissau": (11.8037, -15.1804),
    "Congo, Republic of": (1.6070, 15.4402),
    "Cabo Verde": (16.0021, -24.0132),
    "Gambia, The": (13.4664, -15.3875),
    "Ghana": (7.0469, -0.5090),
    "Burkina Faso": (12.2383, -1.5616),
    "Egypt, Arab Republic of": (26.8206, 30.8025),
    "Benin": (9.3072, 2.3158),
    "Cameroon": (3.8480, 11.5021),
    "Liberia": (6.4281, -9.4295),
    "Iraq": (33.2232, 43.6793),
    "Tunisia": (33.8869, 9.5375),
    "Guinea": (9.9456, -9.6966),
    "Gambia, The": (13.4664, -16.5780),
    "Kyrgyz Republic": (41.2044, 74.7661),
    "Central Asia": (40.0, 69.0),
    "Western and Central Africa": (7.5, -5.0),
    "West Bank and Gaza": (31.9522, 35.2332),
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
    "Afghanistan": (33.93911, 67.709953),
    "Albanie": (41.1533, 20.1683),
    "Algérie": (28.0339, 1.6596),
    "Andorre": (42.5063, 1.5211),
    "Angola": (-11.2027, 17.8739),
    "Antigua-et-Barbuda": (17.0608, -61.7964),
    "Argentine": (-38.4161, -63.6167),
    "Arménie": (40.0691, 45.0382),
    "Australie": (-25.2744, 133.7751),
    "Autriche": (47.5162, 14.5501),
    "Azerbaïdjan": (40.1431, 47.5769),
    "Bahamas": (25.0343, -77.3963),
    "Bahreïn": (25.9304, 50.6372),
    "Bangladesh": (23.685, 90.3563),
    "Barbade": (13.1939, -59.5432),
    "Biélorussie": (53.9045, 27.559),
    "Belgique": (50.8503, 4.3517),
    "Belize": (17.1899, -88.4976),
    "Bénin": (9.3079, 2.3158),
    "Bhoutan": (27.5149, 90.4336),
    "Bolivie": (-16.5000, -68.1193),
    "Bosnie-Herzégovine": (43.8486, 18.3564),
    "Botswana": (-22.3285, 24.6849),
    "Brésil": (-14.2350, -51.9253),
    "Brunei": (4.5353, 114.7277),
    "Bulgarie": (42.7339, 25.4858),
    "Burkina Faso": (12.2383, -1.5616),
    "Burundi": (-3.3731, 29.9189),
    "Cabo Verde": (16.0020, -24.0133),
    "Cambodge": (12.5657, 104.9910),
    "Cameroun": (7.3697, 12.3547),
    "Canada": (56.1304, -106.3468),
    "République Centrafricaine": (6.6111, 20.9394),
    "Tchad": (15.4542, 18.7322),
    "Chili": (-35.6751, -71.5430),
    "Chine": (35.8617, 104.1954),
    "Colombie": (4.5709, -74.2973),
    "Comores": (-11.6455, 43.3333),
    "Congo": (-0.2280, 15.8277),
    "Congo, République démocratique du": (-4.0383, 21.7587),
    "Costa Rica": (9.7489, -83.7534),
    "Croatie": (45.1, 15.2),
    "Cuba": (21.5218, -77.7812),
    "Chypre": (35.1264, 33.4299),
    "République tchèque": (49.8175, 15.4730),
    "Danemark": (56.2639, 9.5018),
    "Djibouti": (11.8251, 42.5903),
    "Dominique": (15.4150, -61.3710),
    "République dominicaine": (18.7357, -70.1627),
    "Équateur": (-1.8312, -78.1834),
    "Égypte": (26.8206, 30.8025),
    "El Salvador": (13.7942, -88.8965),
    "Guinée équatoriale": (1.6500, 10.6214),
    "Érythrée": (15.1792, 39.7823),
    "Estonie": (58.5953, 25.0136),
    "Eswatini": (-26.5225, 31.4659),
    "Éthiopie": (9.1450, 40.4897),
    "Fidji": (-17.7134, 178.0650),
    "Finlande": (61.9241, 25.7482),
    "France": (46.6034, 1.8883),
    "Gabon": (-0.8031, 11.6094),
    "Gambie": (13.4668, -15.3694),
    "Géorgie": (42.3154, 43.3569),
    "Allemagne": (51.1657, 10.4515),
    "Ghana": (7.3469, -0.3963),
    "Grèce": (39.0742, 21.8243),
    "Grenade": (12.2628, -61.6042),
    "Guatemala": (15.7835, -90.2308),
    "Guinée": (9.9456, -9.6966),
    "Guinée-Bissau": (11.8037, -15.1804),
    "Guyana": (4.8600, -58.9300),
    "Haïti": (18.9712, -72.2854),
    "Honduras": (15.1999, -86.2419),
    "Hongrie": (47.1625, 19.5033),
    "Islande": (64.9631, -19.0208),
    "Inde": (20.5937, 78.9629),
    "Indonésie": (-0.7893, 113.9213),
    "Iran": (32.4279, 53.6880),
    "Irak": (33.2232, 43.4160),
    "Irlande": (53.4129, -8.2439),
    "Israël": (31.0461, 34.8516),
    "Italie": (41.8719, 12.5674),
    "Jamaïque": (18.1096, -77.2975),
    "Japon": (36.2048, 138.2529),
    "Jordanie": (30.5852, 36.2384),
    "Kazakhstan": (48.0196, 66.9237),
    "Kenya": (-1.2864, 36.8172),
    "Kiribati": (-3.3704, -168.7340),
    "Corée du Nord": (40.3399, 127.5101),
    "Corée du Sud": (35.9078, 127.7669),
    "Kuwait": (29.3759, 47.9774),
    "Kyrgyzstan": (41.2044, 74.7661),
    "Laos": (19.8563, 102.4955),
    "Lettonie": (56.8796, 24.6032),
    "Liban": (33.8547, 35.8623),
    "Lesotho": (-29.6090, 28.2336),
    "Libéria": (6.4281, -9.4295),
    "Libye": (26.3351, 17.2283),
    "Liechtenstein": (47.1662, 9.5555),
    "Lituanie": (55.1694, 23.8813),
    "Luxembourg": (49.6118, 6.1319),
    "Madagascar": (-18.7669, 46.8691),
    "Malawi": (-13.2543, 34.3015),
    "Malaisie": (4.2105, 101.9758),
    "Maldives": (3.2028, 73.2207),
    "Mali": (17.5700, -3.9962),
    "Malte": (35.9375, 14.3754),
    "Îles Marshall": (7.1315, 171.1845),
    "Mauritanie": (20.2540, -10.9408),
    "Maurice": (-20.348404, 57.552152),
    "Mexique": (23.6345, -102.5528),
    "Micronésie": (7.4256, 150.5508),
    "Moldavie": (47.4116, 28.3699),
    "Monaco": (43.7384, 7.4246),
    "Mongolie": (46.8625, 105.0000),
    "Mozambique": (-18.6657, 35.5296),
    "Namibie": (-22.9576, 18.4904),
    "Nauru": (-0.5228, 166.9315),
    "Népal": (28.3949, 84.1240),
    "Nicaragua": (12.8654, -85.2072),
    "Niger": (17.6078, 8.0817),
    "Nigeria": (9.0820, 8.6753),
    "Norvège": (60.4720, 8.4689),
    "Nouvelle-Zélande": (-40.9006, 174.886),
    "Oman": (21.5129, 55.9233),
    "Pakistan": (30.3753, 69.3451),
    "Palaos": (7.5149, 134.5825),
    "Panama": (8.9824, -79.5205),
    "Papouasie-Nouvelle-Guinée": (-6.314993, 143.95555),
    "Paraguay": (-23.4422, -58.4438),
    "Pays-Bas": (52.1326, 5.2913),
    "Pérou": (-9.1900, -75.0152),
    "Philippines": (12.8797, 121.7740),
    "Pologne": (51.9194, 19.1451),
    "Portugal": (39.3999, -8.2245),
    "Qatar": (25.276987, 51.520008),
    "République de Corée": (35.9078, 127.7669),
    "République démocratique du Congo": (-4.0383, 21.7587),
    "République du Congo": (-0.2280, 15.8277),
    "République tchèque": (49.8175, 15.4730),
    "Roumanie": (45.9432, 24.9668),
    "Royaume-Uni": (55.3781, -3.4360),
    "Russie": (61.5240, 105.3188),
    "Rwanda": (-1.9403, 29.8739),
    "Saint-Kitts-et-Nevis": (17.3578, -62.7820),
    "Saint-Vincent-et-les-Grenadines": (12.9833, -61.2872),
    "Samoa": (-13.7590, -172.1046),
    "Sao Tomé-et-Principe": (0.1860, 6.6131),
    "Arabie Saoudite": (23.8859, 45.0792),
    "Sénégal": (14.4974, -14.4524),
    "Serbie": (44.0165, 21.0059),
    "Seychelles": (-4.6796, 55.4919),
    "Sierra Leone": (8.4606, -11.7799),
    "Singapour": (1.3521, 103.8198),
    "Slovaquie": (48.6690, 19.6990),
    "Slovénie": (46.1512, 14.9955),
    "Somalie": (5.1521, 46.1996),
    "Soudan": (12.8628, 30.2176),
    "Soudan du Sud": (4.8594, 29.6197),
    "Sri Lanka": (7.8731, 80.7718),
    "Suède": (60.1282, 18.6435),
    "Suisse": (46.8182, 8.2275),
    "Syrie": (34.8021, 38.9968),
    "Tadjikistan": (38.8610, 71.2761),
    "Tanzanie": (-6.3690, 34.8888),
    "Tchad": (15.4542, 18.7322),
    "Thaïlande": (15.8700, 100.9925),
    "Timor oriental": (-8.8742, 125.7275),
    "Togo": (8.6195, 0.8248),
    "Trinité-et-Tobago": (10.6918, -61.2225),
    "Tunisie": (33.8869, 9.5375),
    "Turkménistan": (40.6260, 59.3007),
    "Turquie": (38.9637, 35.2433),
    "Tuvalu": (-7.1095, 179.1945),
    "Ukraine": (48.3794, 31.1656),
    "Uruguay": (-32.5228, -55.7658),
    "Vanuatu": (-15.3767, 166.9592),
    "Vatican": (41.9029, 12.4534),
    "Venezuela": (6.4238, -66.5897),
    "Viêt Nam": (14.0583, 108.2772),
    "Yémen": (15.5527, 48.5164),
    "Zambie": (-13.1339, 27.8493),
    "Zimbabwe": (-19.0154, 29.1549),
    "Afganistán": (33.9391, 67.7099),
    "Albania": (41.1533, 20.1683),
    "Argelia": (28.0339, 1.6596),
    "Andorra": (42.5063, 1.5211),
    "Angola": (-11.2027, 17.8739),
    "Antigua y Barbuda": (17.0608, -61.7964),
    "Arabia Saudita": (23.8859, 45.0792),
    "Argentina": (-38.4161, -63.6167),
    "Armenia": (40.0691, 45.0382),
    "Australia": (-25.2744, 133.7751),
    "Austria": (47.5162, 14.5501),
    "Azerbaiyán": (40.1431, 47.5769),
    "Bahamas": (25.0343, -77.3963),
    "Barbados": (13.1939, -59.5432),
    "Bélgica": (50.8503, 4.3517),
    "Belice": (17.1899, -88.4976),
    "Benín": (9.3079, 2.3158),
    "Bielorrusia": (53.9045, 27.5590),
    "Birmania": (21.9139, 95.9560),
    "Bolivia": (-16.2902, -63.5887),
    "Bosnia y Herzegovina": (43.9159, 17.6791),
    "Botsuana": (-22.3285, 24.6849),
    "Brasil": (-14.2350, -51.9253),
    "Brunéi": (4.5353, 114.7277),
    "Bulgaria": (42.7339, 25.4858),
    "Burkina Faso": (12.2383, -1.5616),
    "Burundi": (-3.3731, 29.9189),
    "Cabo Verde": (16.0020, -24.0132),
    "Camerún": (7.3697, 12.3547),
    "Canadá": (56.1304, -106.3468),
    "República Centroafricana": (4.3947, 18.5582),
    "Chad": (15.4542, 18.7322),
    "Chile": (-35.6751, -71.5430),
    "China": (35.8617, 104.1954),
    "Colombia": (4.5709, -74.2973),
    "Comoras": (-11.8750, 43.8722),
    "Congo": (-0.2280, 15.8277),
    "República Democrática del Congo": (-4.0383, 21.7587),
    "Costa Rica": (9.7489, -83.7534),
    "Croacia": (45.1000, 15.2000),
    "Cuba": (21.5216, -77.7812),
    "Chipre": (35.1264, 33.4299),
    "República Checa": (49.8175, 15.4730),
    "Dinamarca": (56.2639, 9.5018),
    "Dominica": (15.4150, -61.3710),
    "República Dominicana": (18.7357, -70.1627),
    "Ecuador": (-1.8312, -78.1834),
    "Egipto": (26.8206, 30.8025),
    "El Salvador": (13.7942, -88.8965),
    "Emiratos Árabes Unidos": (23.4241, 53.8478),
    "Eslovaquia": (48.6690, 19.6990),
    "Eslovenia": (46.1512, 14.9955),
    "España": (40.4637, -3.7492),
    "Estados Unidos": (37.0902, -95.7129),
    "Estonia": (58.5953, 25.0136),
    "Eswatini": (-26.5225, 31.4659),
    "Etiopía": (9.1450, 40.489673),
    "Filipinas": (12.8797, 121.7740),
    "Finlandia": (61.9241, 25.7482),
    "Francia": (46.6034, 1.8883),
    "Gabón": (-0.8031, 11.6094),
    "Gambia": (13.4432, -16.5760),
    "Georgia": (42.3154, 43.3569),
    "Ghana": (7.1736, -0.0966),
    "Grecia": (39.0742, 21.8243),
    "Granada": (12.2628, -61.6042),
    "Guatemala": (15.7835, -90.2308),
    "Guinea": (9.9456, -9.6966),
    "Guinea-Bisáu": (11.8037, -15.1804),
    "Guyana": (4.8600, -58.9302),
    "Haití": (18.9712, -72.2852),
    "Honduras": (13.9637, -85.7285),
    "Hungría": (47.1625, 19.5033),
    "India": (20.5937, 78.9629),
    "Indonesia": (-0.7893, 113.9213),
    "Irak": (33.2232, 43.6793),
    "Irán": (32.4279, 53.6880),
    "Irlanda": (53.4129, -8.2439),
    "Islandia": (64.9631, -19.0208),
    "Islas Marshall": (7.1095, 171.1850),
    "Islas Salomón": (-9.4280, 160.0000),
    "Islas Seychelles": (-4.6796, 55.4919),
    "Italia": (41.8719, 12.5674),
    "Jamaica": (18.1096, -77.2975),
    "Japón": (36.2048, 138.2529),
    "Jordania": (30.5852, 36.2384),
    "Kazajistán": (48.0196, 66.9237),
    "Kenia": (-0.0236, 37.9062),
    "Kirguistán": (41.2044, 74.7661),
    "Kiribati": (-3.3704, -168.7340),
    "Kuwait": (29.3117, 47.4818),
    "Laos": (19.8563, 102.4955),
    "Lesoto": (-29.6099, 28.2336),
    "Letonia": (56.8796, 24.6032),
    "Líbano": (33.8547, 35.8623),
    "Liberia": (6.4281, -9.4295),
    "Libia": (26.3351, 17.2283),
    "Liechtenstein": (47.1662, 9.5555),
    "Lituania": (55.1694, 23.8813),
    "Luxemburgo": (49.6118, 6.1319),
    "Madagascar": (-18.7669, 46.8691),
    "Malasia": (4.2105, 101.9758),
    "Malawi": (-13.2543, 34.3015),
    "Maldivas": (3.2028, 73.2207),
    "Mali": (17.5700, -3.9962),
    "Malta": (35.9375, 14.3754),
    "Marruecos": (31.7917, -7.0926),
    "Mauricio": (-20.348404, 57.552152),
    "Mauritania": (20.2540, -10.9408),
    "México": (23.6345, -102.5528),
    "Micronesia": (7.4256, 150.5508),
    "Moldavia": (47.4116, 28.3699),
    "Mónaco": (43.7384, 7.4246),
    "Mongolia": (46.8625, 103.8467),
    "Montenegro": (42.7087, 19.3744),
    "Mozambique": (-18.6657, 35.5296),
    "Namibia": (-22.9576, 18.4904),
    "Nepal": (28.1667, 84.1250),
    "Nicaragua": (12.8654, -85.2072),
    "Níger": (17.6078, 8.0817),
    "Nigeria": (9.0820, 8.6753),
    "Noruega": (60.4720, 8.4689),
    "Nueva Zelanda": (-40.9006, 174.8860),
    "Omán": (21.5129, 55.9233),
    "Países Bajos": (52.3792, 4.8994),
    "Pakistán": (30.3753, 69.3451),
    "Panamá": (8.5379, -80.7821),
    "Papúa Nueva Guinea": (-6.314993, 143.9555),
    "Paraguay": (-23.4420, -58.4438),
    "Perú": (-9.1900, -75.0152),
    "Polonia": (51.9194, 19.1451),
    "Portugal": (39.3999, -8.2245),
    "Reino Unido": (55.3781, -3.4360),
    "República de Corea": (35.9078, 127.7669),
    "República del Congo": (-0.2280, 15.8277),
    "República Dominicana": (18.7357, -70.1627),
    "Rumania": (45.9432, 24.9668),
    "Rusia": (61.5240, 105.3188),
    "Rwanda": (-1.9403, 29.8739),
    "San Cristóbal y Nieves": (17.3578, -62.7820),
    "San Marino": (43.9333, 12.4468),
    "San Vicente y las Granadinas": (13.2528, -61.1971),
    "Santo Tomé y Príncipe": (0.1860, 6.6131),
    "Senegal": (14.4974, -14.4524),
    "Serbia": (44.0165, 21.0059),
    "Seychelles": (-4.6796, 55.4919),
    "Sierra Leona": (8.4606, -11.7799),
    "Singapur": (1.3521, 103.8198),
    "Siria": (34.8021, 38.9968),
    "Suecia": (60.1282, 18.6435),
    "Suiza": (46.8182, 8.2275),
    "Tailandia": (15.8700, 100.9925),
    "Tanzania": (-6.3690, 34.8888),
    "Timor Oriental": (-8.8742, 125.7275),
    "Togo": (8.6195, 0.8248),
    "Tonga": (-21.1789, -175.1982),
    "Trinidad y Tobago": (10.6918, -61.2225),
    "Túnez": (33.8869, 9.5375),
    "Turkmenistán": (40.0622, 59.5564),
    "Turquía": (38.9637, 35.2433),
    "Tuvalu": (-7.1095, 179.1940),
    "Uganda": (-1.3733, 32.2903),
    "Ucrania": (48.3794, 31.1656),
    "Uruguay": (-32.5228, -55.7659),
    "Uzbekistán": (41.3775, 64.5853),
    "Vanuatu": (-15.3763, 166.9592),
    "Vaticano": (41.9029, 12.4534),
    "Venezuela": (6.4238, -66.5897),
    "Vietnam": (14.0583, 108.2772),
    "Yemen": (15.5522, 48.5164),
    "Zambia": (-13.1339, 27.8493),
    "Zimbabue": (-19.0154, 29.1549)
}


@st.cache_data
def FetchData():
    # Chrome WebDriver'ı başlat
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)  # Chrome sekmesinin kapanmaması için
    options.add_argument("--start-maximized")  # Tarayıcıyı başlatırken tam ekran aç
    driver = webdriver.Chrome(options=options)

    # Web sayfasını aç
    driver.get("https://projects.worldbank.org/en/projects-operations/procurement?showrecent=true&srce=notices")

    # 'Region' toggle'ını açmak için önce bu bölümü tıklıyoruz
    try:
        region_toggle = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Region')]"))
        )
        region_toggle.click()  # 'Region' toggle'ını aç

        #time.sleep(1)  # Toggle'ın açılmasını bekle
        
    except Exception as e:
        print(f"Region toggle açma sırasında hata oluştu: {e}")

    # 'See More +' butonuna tıklayın
    try:
        see_more_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'expand-link')]//a[contains(text(), 'See More +')]"))
        )
        see_more_button.click()  # 'See More +' butonuna tıklayın

        #time.sleep(1)  # Butonun açılmasını bekle
        
    except Exception as e:
        print(f"See More + butonuna tıklama sırasında hata oluştu: {e}")

    # 'hideContent' sınıfını kaldır
    try:
        driver.execute_script("var elements = document.getElementsByClassName('hideContent');"
                            "while(elements.length > 0){ elements[0].classList.remove('hideContent'); }")
        
        #time.sleep(2)  # Değişikliklerin uygulanmasını bekle
        
    except Exception as e:
        print(f"hideContent sınıfını kaldırma sırasında hata oluştu: {e}")
    
    #region Seçilen checkboxların filtrelenmesi

    # -----------------------------------------------------
    # Seçilen checkboxların filtrelenmesi
    # -----------------------------------------------------

    # 'Western And Central Africa' checkbox'ını bul ve tıkla
    checkbox1 = driver.find_element(By.XPATH, "//span[contains(text(), 'Western And Central Africa')]/ancestor::li//input[@type='checkbox']")
    checkbox1.click()  

    # 'Middle East And North Africa' checkbox'ını bul ve tıkla
    checkbox2 = driver.find_element(By.XPATH, "//span[contains(text(), 'Middle East And North Africa')]/ancestor::li//input[@type='checkbox']")
    checkbox2.click() 

    # 'Europe And Central Asia' checkbox'ını bul ve tıkla
    checkbox3 = driver.find_element(By.XPATH, "//span[contains(text(), 'Europe And Central Asia')]/ancestor::li//input[@type='checkbox']")
    checkbox3.click() 
    #endregion
    # Tarayıcıyı kapatmayın, işlemi sonlandırmak için elle kapatabilirsiniz
    

    # --------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------------------


    # 'Notice Type' toggle'ını açmak için önce bu bölümü tıklıyoruz
    try:
        Notice_toggle = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Notice Type')]"))
        )
        Notice_toggle.click()  # 'Region' toggle'ını aç

        time.sleep(1)  # Toggle'ın açılmasını bekle
        
    except Exception as e:
        print(f"Region toggle açma sırasında hata oluştu: {e}")


    # 'Request for Expression of Interest' checkbox'ını bul ve tıkla
    checkbox4 = driver.find_element(By.XPATH, "//span[contains(text(), 'Request for Expression of Interest')]/ancestor::li//input[@type='checkbox']")
    checkbox4.click()  
    

    # 'Invitation for Bids' checkbox'ını bul ve tıkla
    checkbox5 = driver.find_element(By.XPATH, "//span[contains(text(), 'Invitation for Bids')]/ancestor::li//input[@type='checkbox']")
    checkbox5.click() 

    # 'General Procurement Notice'ını bul ve tıkla
    checkbox6 = driver.find_element(By.XPATH, "//span[contains(text(), 'General Procurement Notice')]/ancestor::li//input[@type='checkbox']")
    checkbox6.click() 

    # 'Invitation for Prequalification' checkbox'ını bul ve tıkla
    checkbox7 = driver.find_element(By.XPATH, "//span[contains(text(), 'Invitation for Prequalification')]/ancestor::li//input[@type='checkbox']")
    checkbox7.click() 

    # --------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------------------


    # 'Procurement Group' toggle'ını açmak için önce bu bölümü tıklıyoruz
    try:
        Procurement_toggle = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Procurement Group')]"))
        )
        Procurement_toggle.click()  # 'Region' toggle'ını aç

        time.sleep(1)  # Toggle'ın açılmasını bekle
        
    except Exception as e:
        print(f"Region toggle açma sırasında hata oluştu: {e}")


    # 'Consultant Services' checkbox'ını bul ve tıkla
    checkbox8 = driver.find_element(By.XPATH, "//span[contains(text(), 'Consultant Services')]/ancestor::li//input[@type='checkbox']")
    checkbox8.click()  
    

    # 'Works' checkbox'ını bul ve tıkla (ilk 'Works' checkbox'ı)
    checkbox9 = driver.find_elements(By.XPATH, "//span[contains(text(), 'Works')]/ancestor::li//input[@type='checkbox']")
    if checkbox9:
        checkbox9[1].click()  # İndeks sıfırdan başlar, ilk öğeyi seçiyoruz.

    data = []

    # --------------------------------------------------------------------------------------------------------------------------------------
    wait = WebDriverWait(driver, 10)

    # İlk 5 sayfa için döngü
    for page in range(1, 15):  # 1'den 5'e kadar sayfalar
        # Tablonun tbody elemanını bekleyin
        tbody = wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'project-operation-tab-table')]//tbody")))

        # Tbody içeriğini al
        tbody_content = tbody.get_attribute('innerHTML')  

        # BeautifulSoup ile tbody içeriğini parse et
        soup = BeautifulSoup(tbody_content, 'html.parser')

        # Tablodaki tüm satırları al
        rows = soup.find_all('tr')

        # Her satırdaki hücreleri al ve data listesine ekle
        for row in rows:
            cols = row.find_all('td')
            if cols:  # Eğer satır boş değilse
                # Verileri eklemeden önce tekrar eden verileri kontrol et
                row_data = [col.get_text(strip=True) for col in cols]
                if row_data not in data:  # Eğer bu satır zaten yoksa ekle
                    data.append(row_data)

        # Eğer daha fazla sayfa varsa, bir sonraki sayfaya git
        if page < 10:  # Son sayfaya gitmeden önce sayfa geçişi
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[contains(@class, 'pagination')]//a[text()='{}']".format(page + 1))))
            next_button.click()

            # Sayfa geçişinden sonra tabloyu yeniden yükle
            wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'project-operation-tab-table')]//tbody")))  

    # DataFrame oluştur ve başlıkları ayarla
    headers = ["Description", "Country", "Project Title", "Notice Type", "Language", "Published Date"]
    df = pd.DataFrame(data, columns=headers)

    return df
    # DataFrame'i Streamlit'te göster
    

# Veri güncelleme butonu
if st.sidebar.button("Verileri Güncelle"):
    df = FetchData()  # Verileri güncelle
    st.success("Veriler başarıyla güncellendi!")
else:
    # İlk kez verileri çek
    df = FetchData()


# Ülke isimlerinden koordinatları ekleme
df['Latitude'] = df['Country'].map(lambda country: country_coordinates.get(country, (None, None))[0])
df['Longitude'] = df['Country'].map(lambda country: country_coordinates.get(country, (None, None))[1])



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
df['Date'] = df['Published Date'].apply(parse_date)


# Gün sayısını seçmek için slider ekle
days = st.sidebar.slider('Filtrele:', 1, 50, 10)  # 1 ile 30 arasında varsayılan 10
end_date = datetime.now()
start_date = end_date - timedelta(days=days)


# Tarih filtresi uygulama
filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]






# Folium haritası oluşturma
m = folium.Map(location=[20, 0], zoom_start=3)



def main():
    
    # Filtrelenmiş proje lokasyonlarını haritaya ekleme
    for i, row in filtered_df.iterrows():
        latitude = row['Latitude']
        longitude = row['Longitude']

        if pd.notna(latitude) and pd.notna(longitude):  # Geçerli lokasyonları kontrol etme
            # Proje tarihini kontrol et
            project_date = row['Date']
            # Tıklanan MEMBER'a ait projeleri bulma
            member_projects = filtered_df[filtered_df['Country'] == row['Country']]
            
            # Proje tarihlerini kontrol et
            green_found = False  # Yeşil proje var mı kontrolü için bir bayrak
            for _, project_row in member_projects.iterrows():
                project_date = project_row['Date']
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
            member_projects = filtered_df[filtered_df['Country'] == row['Country']]

            # Proje isimlerini liste halinde alıyoruz
            project_list = member_projects['Project Title'].tolist()

            # Pop-up içeriğini HTML ile oluşturma
            popup_content = f"""
            <div style="font-size: 16px;">
                <strong>Üye:</strong> {row['Country']}<br>
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
            print(f"Geçersiz lokasyon: {row['Country']} - Latitude: {latitude}, Longitude: {longitude}")

    container1 = st.container(border=True)
    with container1:
        cols1, cols2= st.columns([5, 2])  # Sol kolon daha geniş


        with cols1:

            container8 = st.container(border=True)
            with container8:
            
                cols = st.columns(3)
                with cols[0]:
                        ui.metric_card(
                            title = "New Project",
                            content = "$ 45 000",
                            description = "las month",
                            key = "card1"
                        )
                with cols[1]:
                        ui.metric_card(
                            title = "Total Revenue",
                            content = "$ 45 000",
                            description = "las month",
                            key = "card2"
                        )

                with cols[2]:
                        ui.metric_card(
                            title = "Total Revenue",
                            content = "$ 45 000",
                            description = "las month",
                            key = "card3"
                        ) 
        
        with cols2:

            container_1 = st.container(border=True)
            with container_1:
                st.write("test")
        
     
        
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

                    # 'Select' sütunu ekleniyor
                    if 'Select' not in filtered_df.columns:
                        filtered_df.insert(0, 'Select', False)  
                    
                    filtered_df['Date'] = filtered_df['Date'].apply(lambda x: x.date())

                    # Etkileşimli tablo oluştur
                    edited_df = st.data_editor(
                        filtered_df[['Select', 'Date', 'Project Title', 'Notice Type', 'Language']],
                        column_config={
                            "Select": st.column_config.CheckboxColumn("Select", default=False),
                            "Date": "Date",
                            "Project Title": "Project Title",
                            "Notice Type": "Notice Type",
                            "Language": "Language"
                        },
                        disabled=["Date", "Project Title", "Notice Type", "Language"],  # Diğer sütunlar düzenlenemez
                        hide_index=True
                    )

                    # Seçilen satırları bul
                    selected_rows = edited_df[edited_df['Select']]
                                # Eğer herhangi bir satır seçilmişse bilgileri yazdır
                    if not selected_rows.empty:
                        st.write("Selected Projects:")
                        st.dataframe(selected_rows)
                    else:
                        st.write("No projects selected.")
                            
                else:
                    # Haritanın altına tıklanan yerin bilgilerini yazdırıyoruz
                    clicked_info = st_data["last_object_clicked"]
                    lat = clicked_info["lat"]
                    lon = clicked_info["lng"]

                    # Tıklanan lokasyonu dataframe ile eşleştirme
                    clicked_country = filtered_df[(filtered_df['Latitude'] == lat) & (filtered_df['Longitude'] == lon)]
                    
                    if not clicked_country.empty:
                        # Tıklanan lokasyondaki bilgileri al
                        st.write(f"**{clicked_country.iloc[0]['Country']}** ülkesindeki projeler:")
                        
                        # Tüm projeleri içeren bir DataFrame oluştur
                        projects_df = clicked_country[['Date', 'Project Title', 'Notice Type', 'Language']].copy()
                        # Tarih formatını düzelt
                        projects_df['Date'] = projects_df['Date'].apply(lambda x: x.date())


                        # 'Select' sütunu ekleniyor
                        if 'Select' not in projects_df.columns:
                            projects_df.insert(0, 'Select', False)  

                        # Etkileşimli tablo oluştur
                        edited_df = st.data_editor(
                            projects_df[['Select', 'Date', 'Project Title', 'Notice Type', 'Language']],
                            column_config={
                                "Select": st.column_config.CheckboxColumn("Select", default=False),
                                "Date": "Date",
                                "Project Title": "Project Title",
                                "Notice Type": "Notice Type",
                                "Language": "Language"
                            },
                            disabled=["Date", "Project Title", "Notice Type", "Language"],  # Diğer sütunlar düzenlenemez
                            hide_index=True
                        )

                        # Seçilen satırları bul
                        selected_rows = edited_df[edited_df['Select']]
                        # Eğer herhangi bir satır seçilmişse bilgileri yazdır



    container4 = st.container(border=True)


    # pdf viewer gelecek >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    with container4:
        if not selected_rows.empty:
            st.write("Selected Projects:")
            st.dataframe(selected_rows)
        else:
            st.write("No projects selected.")

if __name__ == "__main__":
    main()
