import streamlit as st
import json
from datetime import date

FICHIER_OBJECTIFS = "objectifs.json"

# -------------------------
# Fonctions pour charger/sauvegarder
# -------------------------
def charger_objectifs():
    try:
        with open(FICHIER_OBJECTIFS, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def sauvegarder_objectifs(data):
    with open(FICHIER_OBJECTIFS, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------
# Interface Streamlit
# -------------------------
st.subheader("Objectifs mensuels et jours spéciaux")

# Sélection du mois
mois = st.selectbox("Choisis le mois", 
                    ["Janvier","Février","Mars","Avril","Mai","Juin",
                     "Juillet","Août","Septembre","Octobre","Novembre","Décembre"])
jour_special = st.date_input("Jour spécial (optionnel)", value=None)

# Saisie d'un nouvel objectif
objectif_text = st.text_area("Écris ton objectif pour ce mois / jour spécial")

if st.button("💾 Enregistrer l'objectif"):
    objectifs = charger_objectifs()
    key = f"{mois}-{jour_special}" if jour_special else mois
    if key not in objectifs:
        objectifs[key] = []
    # Chaque objectif est un dictionnaire avec texte + statut
    objectifs[key].append({"texte": objectif_text, "fait": False})
    sauvegarder_objectifs(objectifs)
    st.success("Objectif enregistré ✅")

# -------------------------
# Affichage et suivi des objectifs
# -------------------------
st.markdown("### Objectifs à suivre")

objectifs = charger_objectifs()
key = f"{mois}-{jour_special}" if jour_special else mois

if key in objectifs:
    total = len(objectifs[key])
    faits = 0
    # Affichage des objectifs avec checkbox
    for i, obj in enumerate(objectifs[key]):
        fait = st.checkbox(obj["texte"], value=obj["fait"], key=f"{key}_{i}")
        objectifs[key][i]["fait"] = fait
        if fait:
            faits += 1
    sauvegarder_objectifs(objectifs)

    # Calcul du pourcentage atteint
    pourcentage = int((faits / total) * 100) if total > 0 else 0
    st.metric("📈 Pourcentage d'objectifs atteints", f"{pourcentage}%")
    st.info(f"{faits} sur {total} objectifs réalisés ce mois")
else:
    st.info("Aucun objectif enregistré pour ce mois / jour spécial")
