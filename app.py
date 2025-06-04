import streamlit as st
from jinja2 import Template
from datetime import date

st.set_page_config(page_title="Arve genereerimise tööriist", layout="centered")

st.title("🧾 Arve genereerimise tööriist")

def num_to_estonian_words_full(number):
    def num_to_estonian_words(n):
        ones = ["", "üks", "kaks", "kolm", "neli", "viis", "kuus", "seitse", "kaheksa", "üheksa"]
        teens = ["kümme", "üksteist", "kaksteist", "kolmteist", "neliteist", "viisteist",
                 "kuusteist", "seitseteist", "kaheksateist", "üheksateist"]
        tens = ["", "", "kakskümmend", "kolmkümmend", "nelikümmend", "viiskümmend",
                "kuuskümmend", "seitsekümmend", "kaheksakümmend", "üheksakümmend"]
        hundreds = ["", "sada", "kakssada", "kolmsada", "nelisada", "viissada",
                    "kuussada", "seitsesada", "kaheksasada", "üheksasada"]
        if n == 0: return "null"
        words = []
        if n >= 1000:
            words.append(ones[n // 1000] + " tuhat")
            n %= 1000
        if n >= 100:
            words.append(hundreds[n // 100])
            n %= 100
        if 10 <= n < 20:
            words.append(teens[n - 10])
        else:
            if n >= 20:
                words.append(tens[n // 10])
            if n % 10 > 0:
                words.append(ones[n % 10])
        return " ".join(words)

    eurod = int(number)
    sendid = round((number - eurod) * 100)
    if sendid > 0:
        return f"{num_to_estonian_words(eurod)} eurot ja {num_to_estonian_words(sendid)} senti"
    else:
        return f"{num_to_estonian_words(eurod)} eurot"

with st.form("arve_form"):
    col1, col2 = st.columns(2)
    with col1:
        arve_nr = st.text_input("Arve number", "ARV-001")
        kuupäev = st.date_input("Kuupäev", value=date.today())
        tähtaeg = st.date_input("Maksetähtaeg")
    with col2:
        esitaja = st.text_input("Arve esitaja", "OÜ Näidisfirma")
        esitaja_regnr = st.text_input("Registrikood", "12345678")
        esitaja_iban = st.text_input("IBAN", "EE123456789012345678")
        esitaja_aadress = st.text_input("Registreeritud aadress", "Näidistänav 1, Tallinn")
        esitaja_kmk = st.selectbox("Käibemaksukohustuslane", ["on", "ei ole"])
        esitaja_tel = st.text_input("Telefon", "+372 555 1234")
        esitaja_email = st.text_input("E-post", "info@naidisfirma.ee")
        esitaja_pank = st.text_input("Panga nimi", "SEB")
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
            km = st.selectbox(f"KM% {i}", [0, 9, 20], key=f"km{i}")
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
    summa_sõnadega = num_to_estonian_words_full(kokku).capitalize()

    with open("arve_mall.html") as f:
        html_template = Template(f.read())

    html_out = html_template.render(
        arve_nr=arve_nr,
        kuupäev=kuupäev.strftime("%d.%m.%Y"),
        tähtaeg=tähtaeg.strftime("%d.%m.%Y"),
        esitaja=esitaja,
        esitaja_iban=esitaja_iban,
        esitaja_regnr=esitaja_regnr,
        esitaja_aadress=esitaja_aadress,
        esitaja_kmk=esitaja_kmk,
        esitaja_tel=esitaja_tel,
        esitaja_email=esitaja_email,
        esitaja_pank=esitaja_pank,
        klient=klient,
        read=arveread,
        kokku="{:,.2f}".format(kokku).replace('.', ','),
        summa_sõnadega=summa_sõnadega
    )

    st.markdown("### 📄 Arve eelvaade")
    st.components.v1.html(html_out, height=850, scrolling=True)
    st.markdown("👉 **Prindi arve oma brauseri kaudu või kasuta allolevat nuppu**")
