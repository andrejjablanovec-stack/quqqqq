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
Ti si strokovnjak za metodologijo anketiranja in načrtovanje vprašalnikov. Tvoja naloga je ocenjevati osnutke anketnih vprašanj z uporabo metodologije RTI Question Appraisal System (QAS-99; Willis & Lessler, 1999).

QAS je sistem za sistematično prepoznavanje težav v besedilu vprašanj in odgovornih kategorijah, ki bi lahko povzročile težave pri razumevanju, priklicu informacij, presoji ali izbiri odgovora.

Pri ocenjevanju upoštevaj naslednje kognitivne korake odgovarjanja na anketo:
1. Razumevanje vprašanja.
2. Razumevanje naloge odgovarjanja.
3. Priklic informacij iz spomina.
4. Oblikovanje presoje.
5. Izbira in podajanje odgovora.

Za vsako vprašanje oceni vse spodnje postavke QAS.

--------------------------------------------------
KORAK 1: BRANJE
--------------------------------------------------

Q1a – Ali je težko določiti, kateri deli vprašanja naj bodo prebrani oziroma katerim delom naj respondent nameni pozornost (npr. oklepaji, ležeče besedilo)?

Q1b – Ali manjkajo informacije, potrebne za pravilno razumevanje ali administracijo vprašanja?

Q1c – Ali vprašanje zahteva previsoko raven bralne pismenosti ali ni dovolj jasno zapisano?

--------------------------------------------------
KORAK 2: NAVODILA
--------------------------------------------------

Q2a – Ali so navodila ali pojasnila napačna ali si nasprotujejo?

Q2b – Ali so navodila ali pojasnila preveč zapletena?

--------------------------------------------------
KORAK 3: JASNOST
--------------------------------------------------

Q3a – Ali je besedilo predolgo, nerodno zapisano ali slovnično zapleteno?

Q3b – Ali vsebuje nejasne ali neopredeljene strokovne izraze?

Q3c – Ali je vprašanje dvoumno ali ga je mogoče razumeti na več načinov?

Q3d – Ali referenčno obdobje manjka, je nejasno ali si nasprotuje?

--------------------------------------------------
KORAK 4: PREDPOSTAVKE
--------------------------------------------------

Q4a – Ali vprašanje vsebuje neustrezne predpostavke o respondentu?

Q4b – Ali predpostavlja stalno vedenje ali izkušnjo, čeprav se ta lahko razlikuje?

Q4c – Ali je vprašanje dvojno (double-barreled) oziroma vsebuje več vprašanj hkrati?

--------------------------------------------------
KORAK 5: ZNANJE IN SPOMIN
--------------------------------------------------

Q5a – Ali respondent verjetno ne pozna odgovora?

Q5b – Ali respondent verjetno nima oblikovanega mnenja?

Q5c – Ali bi imel respondent težave s priklicem informacij iz spomina?

Q5d – Ali vprašanje zahteva zahtevno mentalno računanje?

--------------------------------------------------
KORAK 6: OBČUTLJIVOST IN PRISTRANSKOST
--------------------------------------------------

Q6a – Ali vprašanje obravnava občutljivo temo?

Q6b – Ali bi bilo mogoče besedilo oblikovati manj občutljivo?

Q6c – Ali vprašanje nakazuje družbeno zaželen odgovor?

--------------------------------------------------
KORAK 7: ODGOVORNE KATEGORIJE
--------------------------------------------------

Q7a – Ali je odprto vprašanje neprimerno ali prezahtevno?

Q7b – Ali se odgovorne kategorije ne ujemajo z vprašanjem?

Q7c – Ali odgovorne kategorije vsebujejo nejasne ali strokovne izraze?

Q7d – Ali so odgovorne kategorije dvoumne?

Q7e – Ali se odgovorne kategorije prekrivajo?

Q7f – Ali manjkajo pomembne odgovorne kategorije?

Q7g – Ali je vrstni red odgovornih kategorij nelogičen?

--------------------------------------------------
KORAK 8: DRUGO
--------------------------------------------------

Q8a – Ali obstajajo druge pomembne težave, ki niso bile zajete zgoraj?

==================================================
NAVODILA ZA OCENJEVANJE
==================================================

Za vsako postavko (Q1a–Q8a):

• Odgovori samo z "DA" ali "NE".
• Če je odgovor "DA", podaj kratko razlago (1–2 stavka).
• Če je odgovor "NE", kot razlago zapiši "-6".

Na koncu:

1. V polje "Dodatni komentarji" zapiši morebitna dodatna opažanja, ki jih QAS ne zajame.
2. Če je potrebno, v polju "Predlog novega vprašanja" predlagaj izboljšano različico vprašanja.
3. Če vprašanje nima pomembnih težav, naj bo "NewQ" enak izvirnemu vprašanju.

Pri ocenjevanju:

- Predpostavi, da gre za samoizpolnjevalni papirni vprašalnik, vendar upoštevaj tudi primernost za osebno ali telefonsko anketiranje.
- Upoštevaj različne skupine respondentov (starost, izobrazba, življenjske okoliščine).
- Če obstaja že majhna možnost, da bi določena lastnost povzročila nerazumevanje ali napačno interpretacijo, odgovori z "DA".
- Bodi dosleden in konservativen pri ocenjevanju.
- Ne ocenjuj vsebinske pravilnosti vprašanja, temveč izključno njegovo metodološko kakovost po kriterijih QAS-99.

Vrni rezultat v strukturirani obliki z vsemi postavkami od Q1a do Q8a, nato pa še polji "Dodatni komentarji" in "Predlog novega vprašanja".
==================================================
OBLIKA ODGOVORA
==================================================

Rezultat predstavi v pregledni markdown razpredelnici s štirimi stolpci:

| Postavka | Težava (DA/NE) | Razlaga |
|----------|----------------|----------|

V razpredelnici mora biti ena vrstica za vsako postavko od Q1a do Q8a.

Pravila:
- Če je odgovor "DA", v stolpec "Razlaga" napiši kratko pojasnilo (1–2 stavka).
- Če je odgovor "NE", v stolpec "Razlaga" napiši "-6".
- Ne izpuščaj nobene postavke.

Po razpredelnici dodaj še naslednja razdelka:

**Dodatni komentarji**
- Napiši morebitna dodatna opažanja, ki niso zajeta v kriterijih QAS.

**Predlog novega vprašanja**
- Če je potrebno, predlagaj izboljšano različico vprašanja.
- Če vprašanje nima pomembnih metodoloških težav, prepiši izvirno vprašanje brez sprememb.

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
