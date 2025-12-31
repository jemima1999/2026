import streamlit as st
import json
from datetime import date

FICHIER_JOURNAL = "journal_spirituel.json"

# Charger les entrées existantes
def charger_journal():
    try:
        with open(FICHIER_JOURNAL, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def sauvegarder_journal(data):
    with open(FICHIER_JOURNAL, "w") as f:
        json.dump(data, f, indent=4)

st.subheader("📖 Journal spirituel")

today = str(date.today())
journal = charger_journal()

# Entrée quotidienne
st.markdown(f"### Entrée du {today}")
entry = st.text_area("Écris tes pensées, prières, méditations profondes…", 
                     value=journal.get(today, ""), height=250)

if st.button("💾 Enregistrer la journée"):
    journal[today] = entry
    sauvegarder_journal(journal)
    st.success("Entrée enregistrée ✅")

# Historique du journal
st.markdown("### Historique du journal")
for jour, texte in sorted(journal.items(), reverse=True):
    st.markdown(f"**{jour}** : {texte[:150]}{'...' if len(texte)>150 else ''}")
