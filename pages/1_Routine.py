import streamlit as st
from datetime import date
import json

st.title("⏰ Routine quotidienne")

FICHIER_ROUTINE = "routine.json"

# -------------------------
# Fonctions pour charger / sauvegarder
# -------------------------
def charger_routine():
    try:
        with open(FICHIER_ROUTINE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def sauvegarder_routine(data):
    with open(FICHIER_ROUTINE, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------
# Interface Streamlit
# -------------------------
today = date.today().isoformat()
routine_data = charger_routine()

st.subheader("Coche ce que tu as accompli aujourd’hui")

priere_matin = st.checkbox("🙏 Prière du matin")
meditation = st.checkbox("📖 Méditation")
preparation = st.checkbox("🧹 Préparation maison")
priere_soir = st.checkbox("🙏 Prière du soir")
coucher = st.checkbox("🛏️ Coucher à l’heure")

# Calcul du score
score = sum([
    priere_matin,
    meditation,
    preparation,
    priere_soir,
    coucher
]) * 20

st.success(f"⭐ Score de discipline : {score}/100")

# Bouton pour enregistrer
if st.button("💾 Enregistrer ma journée"):
    routine_data[today] = {
        "priere_matin": priere_matin,
        "meditation": meditation,
        "preparation": preparation,
        "priere_soir": priere_soir,
        "coucher": coucher,
        "score": score
    }
    sauvegarder_routine(routine_data)
    st.success("Journée enregistrée avec succès ✅")

# Affichage historique
st.subheader("Historique des scores")
for jour, data in sorted(routine_data.items(), reverse=True):
    st.write(f"{jour} : ⭐ {data['score']} / 100")
