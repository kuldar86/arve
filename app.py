import streamlit as st
from jinja2 import Template
from datetime import date
from num2words import num2words

st.set_page_config(page_title="Arve genereerija", layout="centered")

st.title("🧾 Arve genereerimise tööriist")

with st.form("arve_form"):
    col1, col2 = st.columns(2)
    with col1:
        arve_nr = st.text_input("Arve number", "ARV-001")
        kuupäev = st.date_input("Kuupäev", value=date.today())
        tähtaeg = st.date_input("Maksetähtaeg")
    with col2:
        esitaja = st.text_input("Arve esitaja", "OÜ Näidisfirma")
        esitaja_iban = st.text_input("IBAN", "EE123456789012345678")
        esitaja_regnr = st.text_input("Registrikood", "12345678")

    klient = st.text_input("Klient", "OÜ Klient")

    st.markdown("### Arveread")
    arveread = []
    for i in range(1, 6):
        col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
        with col1:
            kirjeldus = st.text_input(f"Kirjeldus {i}", "")
        with col2:
            kogus = st.number_input(f"Kogus {i}", 0.0, step=1.0, key=f"k{i}")
        with col3:
            hind = st.number_input(f"Hind {i}", 0.0, step=1.0, key=f"h{i}")
        with col4:
            km = st.number_input(f"KM% {i}", 20.0, step=0.0, key=f"km{i}")
        if kirjeldus and kogus and hind:
            summa = round(kogus * hind * (1 + km / 100), 2)
            arveread.append({
                "kirjeldus": kirjeldus,
                "kogus": kogus,
                "hind": hind,
                "km": km,
                "summa": summa
            })

    submitted = st.form_submit_button("Näita arvet")

if submitted and arveread:
    kokku = round(sum([r["summa"] for r in arveread]), 2)
    summa_sõnadega = num2words(kokku, lang="et").capitalize()

    with open("arve_mall.html") as f:
        html_template = Template(f.read())

    html_out = html_template.render(
        arve_nr=arve_nr,
        kuupäev=kuupäev.strftime("%d.%m.%Y"),
        tähtaeg=tähtaeg.strftime("%d.%m.%Y"),
        esitaja=esitaja,
        esitaja_iban=esitaja_iban,
        esitaja_regnr=esitaja_regnr,
        klient=klient,
        read=arveread,
        kokku=kokku,
        summa_sõnadega=summa_sõnadega
    )

    st.markdown("### 📄 Arve eelvaade")
    st.components.v1.html(html_out, height=800, scrolling=True)
    st.markdown("👉 **Prindi arve oma brauseri kaudu (Ctrl+P või Cmd+P) ja vali 'Save as PDF'**")
