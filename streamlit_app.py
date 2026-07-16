import streamlit as st
import google.generativeai as genai

# =========================
# NASTAVITVE STRANI
# =========================

st.set_page_config(
    page_title="QAS-99 Ocenjevalnik",
    page_icon="📋",
    layout="wide"
)

st.markdown(
    """
    <h1 style='text-align:center;color:#2E86AB;'>
    QAS-99 Ocenjevalnik vprašanj
    </h1>
    """,
    unsafe_allow_html=True
)

# =========================
# SISTEMSKI PROMPT
# =========================

SYSTEM_PROMPT = """
Ste metodolog anketiranja in strokovnjak za oblikovanje vprašalnikov.

Vaša naloga je oceniti anketna vprašanja in kategorije odgovorov po metodologiji RTI Question Appraisal System (QAS-99).

Za vsako postavko ocenite, ali obstaja problem (DA ali NE).

KORAK 1: BRANJE

Q1a – Težave pri določanju, kateri deli vprašanja so pomembni.
Q1b – Manjkajo informacije za pravilno razumevanje.
Q1c – Besedilo je pretežko za povprečnega respondenta.

KORAK 2: NAVODILA

Q2a – Nejasna ali nasprotujoča navodila.
Q2b – Preveč zapletena navodila.

KORAK 3: JASNOST

Q3a – Predolgo ali nerodno oblikovano vprašanje.
Q3b – Nepojasnjeni strokovni izrazi.
Q3c – Dvoumnost oziroma več možnih interpretacij.
Q3d – Nejasno ali manjkajoče časovno obdobje.

KORAK 4: PREDPOSTAVKE

Q4a – Neustrezne predpostavke o respondentu.
Q4b – Predpostavka o vedenju ali izkušnji.
Q4c – Dvojno vprašanje (double-barrelled).

KORAK 5: ZNANJE IN SPOMIN

Q5a – Respondent odgovora verjetno ne pozna.
Q5b – Respondent nima oblikovanega stališča.
Q5c – Težaven priklic iz spomina.
Q5d – Zahtevni miselni izračuni.

KORAK 6: OBČUTLJIVOST IN PRISTRANSKOST

Q6a – Občutljiva tema.
Q6b – Besedilo povečuje občutljivost.
Q6c – Družbeno zaželen odgovor.

KORAK 7: KATEGORIJE ODGOVOROV

Q7a – Odprto vprašanje ni primerno.
Q7b – Neskladje med vprašanjem in odgovori.
Q7c – Nejasni izrazi v kategorijah.
Q7d – Dvoumne kategorije.
Q7e – Prekrivajoče kategorije.
Q7f – Manjkajoče kategorije.
Q7g – Nelogičen vrstni red.

KORAK 8: DRUGO

Q8a – Druge ugotovljene težave.

Pri vsakem kriteriju:

- Odgovori z DA ali NE.
- Če DA, napiši kratko razlago.
- Če NE, zapiši "Ni zaznane težave".

Na koncu dodaj:

1. Povzetek glavnih ugotovitev.
2. Splošne komentarje.
3. Predlagano izboljšano različico vprašanja, če je potrebna.

Odgovarjaj izključno v slovenščini.
"""

# =========================
# ZAVIHKI
# =========================

tab1, tab2 = st.tabs(
    [
        "Oceni vprašanje",
        "Oceni svoje vprašanje"
    ]
)

# =========================
# PRVI ZAVIHEK
# =========================

with tab1:

    st.header("QAS-99 Ocena vprašanja")

    st.write(
        """
        Vnesite anketno vprašanje in kategorije odgovorov.
        Model bo izvedel presojo po metodologiji QAS-99
        ter predlagal izboljšave.
        """
    )

    question = st.text_area(
        "Besedilo vprašanja",
        height=120
    )

    categories = st.text_area(
        "Kategorije odgovorov (vsaka v svoji vrstici; pustite prazno za odprto vprašanje)",
        height=120
    )

    if st.button("Oceni"):

        if not question.strip():
            st.warning("Vnesite vprašanje.")
            st.stop()

        user_prompt = f"""
VPRAŠANJE

{question}

KATEGORIJE ODGOVOROV

{categories if categories else "Odprto vprašanje"}
"""

        try:

            
            genai.configure(
                api_key=st.secrets["GEMINI_API_KEY"]
            )

            model = genai.GenerativeModel(
                "gemini-2.5-flash"
            )


            
            response = model.generate_content(
                f"""
                {SYSTEM_PROMPT}

                {user_prompt}
                """
            )

            result = response.text


            st.markdown("---")
            st.markdown(result)

        except Exception as e:
            st.error(f"Napaka: {e}")

# =========================
# DRUGI ZAVIHEK
# =========================

with tab2:

    st.header("Hitra analiza vprašanja")

    free_question = st.text_area(
        "Vnesite vprašanje za analizo",
        height=150,
        key="free_question"
    )

    if st.button("Analiziraj vprašanje"):

        if not free_question.strip():
            st.warning("Vnesite vprašanje.")
            st.stop()

        prompt = f"""
Analiziraj naslednje vprašanje po metodologiji QAS-99:

{free_question}

Pripravi strukturirano poročilo.
"""

        try:

            client = OpenAI(
                api_key=st.secrets["OPENAI_API_KEY"]
            )

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            st.markdown(
                response.choices[0].message.content
            )

        except Exception as e:
            st.error(f"Napaka: {e}")
