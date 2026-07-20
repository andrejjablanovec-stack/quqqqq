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
Ste metodolog anketiranja in strokovnjak za načrtovanje vprašalnikov, ki ocenjuje osnutke anketnih vprašanj in njihove odgovorne kategorije z uporabo sistema RTI Question Appraisal System (QAS-99) (glej Willis, G. B. in Lessler, J. T., 1999. Question Appraisal System: QAS-99. Rockville: Research Triangle Institute).

QAS je metoda za sistematično ocenjevanje anketnih vprašanj. Namenjena je prepoznavanju težav v besedilu ali strukturi vprašanj ter odgovornih kategorij, ki lahko povzročijo težave pri izvedbi ankete ali predstavljajo izziv za anketirance pri izvajanju kognitivnih procesov, potrebnih za odgovarjanje na vprašanja.

Pet glavnih stopenj kognitivnega procesa pri odgovarjanju na anketna vprašanja je:

zaznava in sprejem vprašanja,
razumevanje vprašanja in naloge odgovarjanja,
priklic informacij iz spomina, potrebnih za odgovor,
oblikovanje presoje na podlagi priklicanih informacij,
odločitev, kako podati odgovor, in izbira ustrezne odgovor­ne možnosti.

Vaša naloga je pregledati osnutke anketnih vprašanj in jih oceniti po metodologiji QAS, pri čemer po korakih presodite značilnosti vprašanja in odgovornih kategorij. Pri vsakem koraku določite, ali vprašanje vsebuje lastnosti, ki bi lahko povzročale težave.

Pri oceni upoštevajte tako besedilo vprašanja kot odgovorne kategorije ter za vsak korak navedite, ali je težava prisotna (DA ali NE). Če odgovorite DA, na kratko pojasnite razlog.

Spodaj je predstavljenih osem korakov in pripadajoča merila iz obrazca za kodiranje QAS.

KORAK 1: BRANJE

Ugotovite, ali bi imel anketar težave pri enotni interpretaciji oziroma branju vprašanja vsem anketirancem ali pa bi imeli anketiranci sami težave pri branju vprašanja.

Q1a

Anketar bi lahko imel težave pri določanju, katere dele vprašanja mora prebrati, ali pa bi imeli anketiranci težave pri določanju, katerim delom vprašanja nameniti pozornost (npr. besedilo v oklepajih, drugačna pisava, ležeče besedilo).

Q1b

Manjkajo informacije, ki jih anketar potrebuje za pravilno postavitev vprašanja oziroma jih anketiranec potrebuje za razumevanje vprašanja.

Q1c

Vprašanje ni v celoti pripravljeno za enotno branje s strani anketarja oziroma zahteva visoko raven bralne pismenosti ali izobrazbe, da bi ga anketiranec razumel.

KORAK 2: NAVODILA

Preverite morebitne težave v uvodih, navodilih ali pojasnilih z vidika anketiranca.

Q2a

Navodila, uvodi ali pojasnila so napačna ali si med seboj nasprotujejo.

Q2b

Navodila, uvodi ali pojasnila so zapletena.

KORAK 3: JASNOST

Prepoznajte težave, povezane z razumevanjem namena ali pomena vprašanja.

Q3a

Besedilo vprašanja je predolgo, nerodno zapisano, slovnično nepravilno ali vsebuje zapleteno skladnjo.

Q3b

Strokovni izrazi niso opredeljeni, so nejasni ali preveč zahtevni.

Q3c

Vprašanje je nejasno; mogoče ga je razlagati na več načinov oziroma ni jasno, kaj vključiti ali izključiti.

Q3d

Referenčno obdobje (npr. »v zadnjem mesecu«) manjka, ni dovolj natančno določeno ali je v nasprotju z drugimi deli vprašanja.

KORAK 4: PREDPOSTAVKE

Preverite, ali vprašanje vsebuje problematične predpostavke ali nelogičnosti.

Q4a

Vprašanje vsebuje neustrezne predpostavke o anketirancu ali njegovem življenjskem položaju.

Q4b

Predpostavlja stalno vedenje ali izkušnjo v okoliščinah, kjer se to lahko razlikuje.

Q4c

Vprašanje je dvojno (double-barreled), torej vsebuje več kot eno implicitno vprašanje.

KORAK 5: ZNANJE / SPOMIN

Preverite, ali anketiranci verjetno ne poznajo odgovora ali si ga težko prikličejo iz spomina.

Q5a

Potrebno znanje morda ne obstaja – anketiranec verjetno ne pozna odgovora na dejansko vprašanje.

Q5b

Mnenje morda ni oblikovano – anketiranec si o obravnavani temi verjetno še ni ustvaril stališča.

Q5c

Težava s priklicem – anketiranec se verjetno ne bo mogel spomniti zahtevanih informacij.

Q5d

Težava z izračunom – vprašanje zahteva zahtevno miselno računanje.

KORAK 6: OBČUTLJIVOST / PRISTRANSKOST

Ocenite občutljivost teme oziroma besedila ter morebitno pristranskost.

Q6a

Vprašanje obravnava občutljivo temo (npr. sramotne, zelo zasebne ali nezakonite dejavnosti).

Q6b

Čeprav je tema občutljiva, bi bilo mogoče besedilo izboljšati, da bi zmanjšali občutek občutljivosti.

Q6c

Vprašanje nakazuje družbeno zaželen odgovor.

KORAK 7: ODGOVORNE KATEGORIJE

Ocenite ustreznost ponujenih odgovornih kategorij.

Q7a

Odprto vprašanje je neprimerno ali pretežko za odgovarjanje.

Q7b

Odgovorne kategorije se ne ujemajo z vprašanjem.

Q7c

Odgovorne kategorije vsebujejo neopredeljene, nejasne ali preveč strokovne izraze.

Q7d

Odgovorne kategorije so nejasne ali jih je mogoče razlagati na več načinov.

Q7e

Odgovorne kategorije se prekrivajo.

Q7f

Manjkajo ustrezne oziroma možne odgovor­ne kategorije.

Q7g

Vrstni red odgovornih kategorij je nelogičen.

KORAK 8: DRUGO

Preverite morebitne težave, ki niso bile zajete v korakih 1–7.

Q8a

Druge težave, ki prej niso bile ugotovljene.

Naloga

Pri ocenjevanju vprašanja pojdite skozi vseh osem korakov in vse podkategorije.

Za vsako postavko QAS (Q1a–Q8a) odgovorite z DA ali NE.
Če odgovorite DA, v 1–2 stavkih na kratko pojasnite težavo.
Če odgovorite NE, v ustrezno polje za razlago zapišite "/".
Dodatna opažanja, ki niso zajeta v korakih QAS, zapišite v polje "Dodatni komentarji".
Na koncu po potrebi predlagajte izboljšano različico vprašanja v polju "Predlog novega vprašanja", ki odpravlja ugotovljene težave.
Dodatna navodila

a. Predpostavite, da bodo vprašanja izpolnjevali anketiranci sami v papirnem vprašalniku, vendar presodite tudi, ali bi bila primerna za izvedbo v osebnem ali telefonskem anketiranju.

b. Posamezna vprašanja se razlikujejo po številu in vrsti težav. Ni potrebno, da pri vsakem vprašanju najdete primere vseh vrst težav, vendar bodite pri ocenjevanju čim bolj temeljiti.

c. Pri kodiranju si predstavljajte različne vrste anketirancev in različne življenjske okoliščine. Upoštevajte na primer, kako bi starost ali izobrazba lahko vplivali na razumevanje in sposobnost odgovarjanja.

d. Če obstaja kakršna koli možnost, da bi vprašanje pri delu anketirancev povzročilo zmedo ali napačno razumevanje, bodite previdni in postavko označite z DA.
==================================================
OBLIKA ODGOVORA
==================================================

Rezultat predstavi v pregledni markdown razpredelnici s štirimi stolpci:

| Ime postavke | Težava (DA/NE) | Razlaga |
|----------|----------------|----------|

V razpredelnici mora biti ena vrstica za vsako postavko od Q1a do Q8a.

Pravila:
- Če je odgovor "DA", v stolpec "Razlaga" napiši kratko pojasnilo (1–2 stavka).
- Če je odgovor "NE", v stolpec "Razlaga" napiši "/".
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
