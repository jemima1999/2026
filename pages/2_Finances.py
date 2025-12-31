import streamlit as st
import pandas as pd
from datetime import date
import json
import matplotlib.pyplot as plt

st.title("💰 Finances & Budget 2026")

# -------------------------
# CONFIGURATION DES CATEGORIES
# -------------------------
CATEGORIES = [
    "Nourriture",
    "Transport",
    "Loyer",
    "Don",
    "Offrande",
    "Habillement",
    "Tresse",
    "Beauté",
    "Pret",
    "Portable(Forfait, crédit..etc)",
    "Santé",
    "Autre"
]

FICHIER = "depenses.json"

# -------------------------
# FONCTIONS DE SAUVEGARDE
# -------------------------
def charger_donnees():
    try:
        with open(FICHIER, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def sauvegarder_donnees(data):
    with open(FICHIER, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------
# AJOUT D'UNE TRANSACTION
# -------------------------
st.subheader("➕ Ajouter une transaction")

type_ = st.selectbox("Type", ["dépense", "revenu"])
categorie = st.selectbox("Catégorie", CATEGORIES)
montant = st.number_input("Montant (€)", min_value=0.0, step=10.0)
trans_date = st.date_input("Date", value=date.today())
note = st.text_input("Note (optionnel)")

if st.button("💾 Enregistrer la transaction"):
    data = charger_donnees()
    data.append({
        "date": trans_date.isoformat(),
        "type": type_,
        "categorie": categorie,
        "montant": montant,
        "note": note
    })
    sauvegarder_donnees(data)
    st.success(f"{type_.capitalize()} de {montant}€ enregistrée ✅")

st.divider()

# -------------------------
# BUDGET MENSUEL
# -------------------------
st.subheader("📊 Budget mensuel")
budget = st.number_input(
    "Définis ton budget du mois",
    min_value=0,
    step=500
)

st.divider()

# -------------------------
# ANALYSE DU MOIS EN COURS
# -------------------------
st.subheader("📅 Résumé du mois")

data = charger_donnees()
df = pd.DataFrame(data)
if not df.empty:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    today = date.today()
    mois_courant = df[
        (df["date"].dt.month == today.month) &
        (df["date"].dt.year == today.year)
    ]
    
    total_depense = mois_courant[mois_courant["type"]=="dépense"]["montant"].sum()
    total_revenu = mois_courant[mois_courant["type"]=="revenu"]["montant"].sum()
    reste = budget - total_depense

    colA, colB, colC = st.columns(3)
    colA.metric("💸 Total dépensé", f"{total_depense:,.0f}€")
    colB.metric("🎯 Budget", f"{budget:,.0f}€")
    if reste < 0:
        colC.metric("🔴 Dépassement", f"{-reste:,.0f}€")
        st.error("⚠️ Tu es en ROUGE ce mois-ci. Ralentis 🙏")
    else:
        colC.metric("🟢 Reste", f"{reste:,.0f}€")
        st.success("👏 Tu es dans ton budget")
    
    st.divider()

    # -------------------------
    # HISTORIQUE DES DEPENSES
    # -------------------------
    st.subheader("📄 Historique des transactions")
    st.dataframe(
        mois_courant.sort_values("date", ascending=False),
        use_container_width=True
    )

    # -------------------------
    # GRAPHIQUE PAR CATEGORIE
    # -------------------------
    st.subheader("📊 Dépenses par catégorie")
    cat_depenses = mois_courant[mois_courant["type"]=="dépense"].groupby("categorie")["montant"].sum()
    if not cat_depenses.empty:
        fig, ax = plt.subplots()
        cat_depenses.plot(kind="bar", ax=ax, color="tomato")
        ax.set_ylabel("Dépenses (€)")
        ax.set_title("Dépenses par catégorie ce mois")
        plt.xticks(rotation=45)
        st.pyplot(fig)
else:
    st.info("Aucune transaction enregistrée ce mois-ci.")
