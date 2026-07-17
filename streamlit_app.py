import streamlit as st
from openai import OpenAI

# ====================================================
# NASTAVITVE
# ====================================================

st.set_page_config(
    page_title="QAS-99 Ocenjevalnik",
    page_icon="📋",
    layout="wide"
)

# ====================================================
# GROQ
# ====================================================

client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

# ====================================================
# SISTEMSKI PROMPT
# ====================================================

SYSTEM_PROMPT = """
Ste metodolog anketiranja in strokovnjak za oblikovanje vprašalnikov.

Vaša naloga je oceniti anketna vprašanja in kategorije odgovorov po metodologiji RTI Question Appraisal System (QAS-99).

Za vsako postavko ocenite obstoj potencialne težave.

KORAK 1: BRANJE

Q1a – Težave pri razumevanju pomembnih delov vprašanja.
Q1b – Manjkajoče informacije.
Q1c – Zahtevna raven bralne pismenosti.

KORAK 2: NAVODILA

Q2a – Nejasna navodila.
Q2b – Zapletena navodila.

KORAK 3: JASNOST

Q3a – Predolgo ali nerodno vprašanje.
Q3b – Nepojasnjeni strokovni izrazi.
Q3c – Dvoumnost.
Q3d – Nejasno referenčno obdobje.

KORAK 4: PREDPOSTAVKE

Q4a – Neustrezne predpostavke.
Q4b – Predpostavke o vedenju ali izkušnjah.
Q4c – Dvojno vprašanje.

KORAK 5: ZNANJE IN SPOMIN

Q5a – Respondent odgovora ne pozna.
Q5b – Respondent nima oblikovanega stališča.
Q5c – Težaven priklic informacij.
Q5d – Zahtevni miselni izračuni.

KORAK 6: OBČUTLJIVOST

Q6a – Občutljiva tema.
Q6b – Povečana občutljivost zaradi formulacije.
Q6c – Socialno zaželen odgovor.

KORAK 7: KATEGORIJE ODGOVOROV

Q7a – Neprimerna odprta oblika.
Q7b – Neskladje vprašanja in odgovorov.
Q7c – Nejasni izrazi.
Q7d – Dvoumne kategorije.
Q7e – Prekrivanje kategorij.
Q7f – Manjkajoče kategorije.
Q7g – Nelogičen vrstni red.

KORAK 8: DRUGO

Q8a – Druge težave.

Za vsak kriterij odgovori:

DA ali NE

Če DA:
kratka razlaga.

Če NE:
"Nobena težava ni zaznana."

Na koncu dodaj:

1. Povzetek.
2. Splošne komentarje.
3. Predlagano izboljšano vprašanje.

Odgovarjaj v slovenščini.
"""

# ====================================================
# NASLOV
# ====================================================

st.title("📋 QAS-99 Ocenjevalnik vprašanj")

st.markdown("""
Orodje za avtomatsko evalvacijo vprašanj po metodologiji **QAS-99**.
""")

# ====================================================
# ZAVIHKI
# ====================================================

tab1, tab2 = st.tabs(
    [
        "Oceni vprašanje",
        "O aplikaciji"
    ]
)

# ====================================================
# TAB 1
# ====================================================

with tab1:

    st.subheader("Vnesite vprašanje")

    question = st.text_area(
        "Besedilo vprašanja",
        height=120
    )

    categories = st.text_area(
        "Kategorije odgovorov (vsaka v svoji vrstici)",
        height=120
    )

    if st.button("Oceni vprašanje"):

        if not question.strip():
            st.warning("Vnesite vprašanje.")
            st.stop()

        user_prompt = f"""
VPRAŠANJE

{question}

KATEGORIJE ODGOVOROV

{categories if categories.strip() else "Odprto vprašanje"}
"""

        with st.spinner("Izvajam analizo ..."):

            try:

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    temperature=0.2,
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        },
                        {
                            "role": "user",
                            "content": user_prompt
                        }
                    ]
                )

                result = response.choices[0].message.content

                st.markdown("---")
                st.markdown(result)

            except Exception as e:
                st.error(f"Napaka: {e}")

# ====================================================
# TAB 2
# ====================================================

with tab2:

    st.markdown("""
### Namen

Orodje demonstrira uporabo velikih jezikovnih modelov
za evalvacijo anketnih vprašanj po metodologiji QAS-99.

### Kaj preverja?

- razumljivost vprašanja,
- jasnost in dvoumnost,
- predpostavke,
- kognitivno obremenitev,
- občutljivost teme,
- kakovost kategorij odgovorov.

### Tehnologija

- Streamlit
- Groq API
- Llama 3.3 70B
""")
