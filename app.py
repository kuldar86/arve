import streamlit as st
import datetime
from jinja2 import Template

# Load the HTML template
with open("arve_mall.html", "r", encoding="utf-8") as f:
    html_template = f.read()

# Form inputs
st.title("Arve generaator")
esitaja = st.text_input("Arve esitaja (OÜ nimi)", "Näidisfirma OÜ")
saaja = st.text_input("Arve saaja", "Klient AS")
saaja_reg = st.text_input("Arve saaja registrikood", "12345678")
kuupäev = st.date_input("Kuupäev", datetime.date.today())
tähtaeg = st.date_input("Maksetähtaeg", datetime.date.today() + datetime.timedelta(days=7))
kirjeldus = st.text_input("Toote/teenuse kirjeldus", "Teenuse osutamine")
kogus = st.number_input("Kogus", 1, 100, 1)
hind = st.number_input("Ühiku hind (€)", 1.0, 10000.0, 100.0)
kmk = st.selectbox("Kas ettevõte on käibemaksukohustuslane?", ["on", "ei ole"])
aadress = st.text_input("Aadress", "Näidistänav 1, Tallinn")
tel = st.text_input("Telefon", "+372 555 1234")
email = st.text_input("E-post", "info@naidisfirma.ee")
pank = st.text_input("Pank", "SEB")
iban = st.text_input("IBAN", "EE123456789012345678")

# Generate HTML preview
if st.button("Kuva arve"):
    summa = kogus * hind
    kmk_text = "ettevõte on käibemaksukohustuslane" if kmk == "on" else "ettevõte ei ole käibemaksukohustuslane"
    html_filled = Template(html_template).render(
        esitaja=esitaja,
        saaja=saaja,
        saaja_reg=saaja_reg,
        kuupäev=kuupäev.strftime("%d.%m.%Y"),
        tähtaeg=tähtaeg.strftime("%d.%m.%Y"),
        kirjeldus=kirjeldus,
        kogus=kogus,
        hind=hind,
        summa="{:.2f}".format(summa),
        summa_sõnadega=f"{int(summa)} eurot ja {int((summa % 1) * 100)} senti",
        kmk=kmk_text,
        aadress=aadress,
        tel=tel,
        email=email,
        pank=pank,
        iban=iban
    )
    st.components.v1.html(html_filled, height=1300, scrolling=True)
